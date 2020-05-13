import os
from collections import OrderedDict

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Jet, GenJet

from PhysicsTools.HeppyCore.utils.deltar import cleanObjectCollection, matchObjectCollection

from CMGTools.HNL.utils.BTagSF import BTagSF
from PhysicsTools.Heppy.physicsutils.JetReCalibrator import JetReCalibrator

# BTAG recommendations
# general: https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation
# 2016: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation2016Legacy
# 2017: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
# 2018: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
global deepflavour_wp
deepflavour_wp = OrderedDict()

deepflavour_wp[2018] = OrderedDict()
deepflavour_wp[2018]['loose' ] = 0.0494
deepflavour_wp[2018]['medium'] = 0.2770
deepflavour_wp[2018]['tight' ] = 0.7264

deepflavour_wp[2017] = OrderedDict()
deepflavour_wp[2017]['loose' ] = 0.0521
deepflavour_wp[2017]['medium'] = 0.3033
deepflavour_wp[2017]['tight' ] = 0.7489

deepflavour_wp[2016] = OrderedDict()
deepflavour_wp[2016]['loose' ] = 0.0614
deepflavour_wp[2016]['medium'] = 0.3093
deepflavour_wp[2016]['tight' ] = 0.7221

class JetAnalyzer(Analyzer):

    """Analyze jets.

    Copied from heppy examples and edit to not rely on heppy examples.

    This analyzer filters the jets that do not correspond to the leptons
    stored in event.selectedLeptons, and puts in the event:
    - jets: all jets passing the pt and eta cuts
    - cleanJets: the collection of jets away from the leptons
    - cleanBJets: the jets passing testBJet, and away from the leptons

    Example configuration:

    jetAna = cfg.Analyzer(
      'JetAnalyzer',
      jetCol = 'slimmedJets'
      # cmg jet input collection
      # pt threshold
      jetPt = 30,
      # eta range definition
      jetEta = 5.0,
      # seed for the btag scale factor
      btagSFseed = 0xdeadbeef,
      # if True, the PF and PU jet ID are not applied, and the jets get flagged
      relaxJetId = False,
      relaxPuJetId = False,
    )
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(JetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.btagSF = BTagSF(seed=getattr(self.cfg_ana, 'btagSFseed', 0), 
                             mc_eff_file=getattr(self.cfg_ana, 'mc_eff_file'),
                             sf_file=getattr(self.cfg_ana, 'sf_file'),
                             wp=getattr(self.cfg_ana, 'btag_wp', 'medium'),
                             )
        self.recalibrateJets = getattr(cfg_ana, 'recalibrateJets', False)

        mcGT = getattr(cfg_ana, 'mcGT', 'Spring16_25nsV6_MC')
        dataGT = getattr(cfg_ana, 'dataGT', 'Spring16_25nsV6_DATA')

        if self.recalibrateJets:
            doResidual = getattr(cfg_ana, 'applyL2L3Residual', 'Data')
            if doResidual == "MC":
                doResidual = self.cfg_comp.isMC
            elif doResidual == "Data":
                doResidual = not self.cfg_comp.isMC
            elif doResidual not in [True, False]:
                raise RuntimeError, "If specified, applyL2L3Residual must be any of { True, False, 'MC', 'Data'(default)}"
            GT = getattr(cfg_comp, 'jecGT', mcGT if self.cfg_comp.isMC else dataGT)

            # instantiate the jet re-calibrator
            self.jetReCalibrator = JetReCalibrator(GT, 'AK4PFchs', doResidual, jecPath="%s/src/CMGTools/RootTools/data/jec" % os.environ['CMSSW_BASE'])

    def declareHandles(self):
        super(JetAnalyzer, self).declareHandles()

        # self.handles['jets'] = AutoHandle(self.cfg_ana.jetCol, 'std::vector<pat::Jet>')
        # try to use recomputed jets, but if it fails, resort to normal slimmedJets in miniAODs
        self.handles['jets'] = AutoHandle(self.cfg_ana.jetCol, 'std::vector<pat::Jet>', mayFail=True, fallbackLabel='slimmedJets', lazy=False)

        if self.cfg_comp.isMC:
            self.mchandles['genParticles'] = AutoHandle('packedGenParticles', 'std::vector<pat::PackedGenParticle>')
            self.mchandles['genJets'     ] = AutoHandle('slimmedGenJets'    , 'std::vector<reco::GenJet>'          )

    def beginLoop(self, setup):
        super(JetAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('jets')
        count = self.counters.counter('jets')
        count.register('all events')

    def process(self, event):

        self.readCollections(event.input)
        
        # create Heppy Jet objects
        allJets = map(Jet, self.handles['jets'].product())

        # create intially empty jet collections
        event.jets  = []
        event.bJets = []
        event.cleanJets   = OrderedDict()
        event.cleanJets30 = OrderedDict()
        event.cleanBJets  = OrderedDict()
        
        # selected leptons as defined in the analyzer prior to this
        leptons = getattr(event, 'selectedLeptons', [])

        genJets = None
        if self.cfg_comp.isMC:
            genJets = map(GenJet, self.mchandles['genJets'].product())
            
        # recalibrate jets
        if self.recalibrateJets:
            self.jetReCalibrator.correctAll(allJets, event.rho, delta=0., metShift=[0.,0.], addCorr=True, addShifts=True)

        # fill the various jet collections and
        # possibly correct jets (if configured to do so)
        for jet in allJets:
            if genJets:
                # Use DeltaR = 0.25 matching like JetMET
                pairs = matchObjectCollection([jet], genJets, 0.25 * 0.25)
                if pairs[jet] is None:
                    pass
                else:
                    jet.matchedGenJet = pairs[jet]
                    
            # Add JER/JES correction for MC jets. Requires gen-jet matching.
            # Add JES correction for MC jets.
            if self.cfg_comp.isMC and hasattr(self.cfg_ana, 'jerCorr') and self.cfg_ana.jerCorr: self.jerCorrection(jet)
            if self.cfg_comp.isMC and hasattr(self.cfg_ana, 'jesCorr')                         : self.jesCorrection(jet, self.cfg_ana.jesCorr)
            
            # preselect jets
            if self.testJet(jet) : event.jets.append(jet)
            
            # compute deepjet scores only once
            self._prepareDeepJet(jet, year=self.cfg_ana.year, wp=getattr(self.cfg_ana, 'btag_wp', 'medium'))

            # create collection of bjets
            if self.testBJet(jet, 
                             year=self.cfg_ana.year, 
                             wp=getattr(self.cfg_ana, 'btag_wp', 'medium'), 
                             final_state='tot'): 
                event.bJets.append(jet)

        self.counters.counter('jets').inc('all events')

        for final_state in ['mmm', 'mem', 'eee', 'eem']:
            
            if final_state not in leptons.keys():
                continue

            # RM: found out that there's not a lot of final state dependency,
            #     so we'll use the inclusive measurement that has better stats
            # preselect jets, with the appropriate btag SF correction **final state dependent**!
            # event.bJets = []
            # for jet in event.jets:
            #     if self.testBJet(jet, 
            #                      year=self.cfg_ana.year, 
            #                      wp=getattr(self.cfg_ana, 'btag_wp', 'medium'), 
            #                      final_state=final_state): 
            #         event.bJets.append(jet)
                        
            # clean jets from selected leptons (per final state!)
            event.cleanJets [final_state], dummy = cleanObjectCollection(event.jets , masks=leptons[final_state], deltaRMin=0.5)
            event.cleanBJets[final_state], dummy = cleanObjectCollection(event.bJets, masks=leptons[final_state], deltaRMin=0.5)

            pairs = matchObjectCollection(leptons[final_state], allJets, 0.5 * 0.5)
            # associating a jet to each lepton
            for lepton in leptons[final_state]:
                jet = pairs[lepton]
                if jet is None:
                    lepton.jet = lepton
                else:
                    lepton.jet = jet

            # associating to each (clean) jet the lepton that's closest to it
            invpairs = matchObjectCollection(event.cleanJets[final_state], leptons[final_state], 99999.)
            for jet in event.cleanJets[final_state]:
                leg = invpairs[jet]
                jet.leg = leg

            for jet in event.cleanJets[final_state]:
                jet.matchGenParton = 999.0

            event.jets30                   = [jet for jet in event.jets                   if jet.pt() > 30]
            event.cleanJets30[final_state] = [jet for jet in event.cleanJets[final_state] if jet.pt() > 30]
                                    
        return True

    def jerCorrection(self, jet):
        ''' Adds JER correction according to first method at
        https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution

        Requires some attention when genJet matching fails.
        '''
        if not hasattr(jet, 'matchedGenJet'):
            return
        #import pdb; pdb.set_trace()
        corrections = [0.052, 0.057, 0.096, 0.134, 0.288]
        maxEtas = [0.5, 1.1, 1.7, 2.3, 5.0]
        eta = abs(jet.eta())
        for i, maxEta in enumerate(maxEtas):
            if eta < maxEta:
                pt = jet.pt()
                deltaPt = (pt - jet.matchedGenJet.pt()) * corrections[i]
                totalScale = (pt + deltaPt) / pt

                if totalScale < 0.:
                    totalScale = 0.
                jet.scaleEnergy(totalScale)
                break

    def jesCorrection(self, jet, scale=0.):
        ''' Adds JES correction in number of sigmas (scale)
        '''
        # Do nothing if nothing to change
        if scale == 0.:
            return
        unc = jet.uncOnFourVectorScale()
        totalScale = 1. + scale * unc
        if totalScale < 0.:
            totalScale = 0.
        jet.scaleEnergy(totalScale)

    def testJetID(self, jet):
        jet.puJetIdPassed = jet.puJetId()
        jet.pfJetIdPassed = jet.jetID("POG_PFID_Tight")
        puJetId = self.cfg_ana.relaxPuJetId or jet.puJetIdPassed 
        pfJetId = self.cfg_ana.relaxJetId or jet.pfJetIdPassed 
        return puJetId and pfJetId

    def testJet(self, jet):
        pt = jet.pt()
        if hasattr(self.cfg_ana, 'ptUncTolerance') and self.cfg_ana.ptUncTolerance:
            pt = max(pt, pt * jet.corrJECUp/jet.corr, pt * jet.corrJECDown/jet.corr)
        return pt > self.cfg_ana.jetPt and \
            abs( jet.eta() ) < self.cfg_ana.jetEta and \
            self.testJetID(jet)

    def _prepareDeepJet(self, jet, year, wp):
        jet.deepflavour_prob_b    = jet.btag('pfDeepFlavourJetTags:probb')
        jet.deepflavour_prob_bb   = jet.btag('pfDeepFlavourJetTags:probbb')
        jet.deepflavour_prob_lepb = jet.btag('pfDeepFlavourJetTags:problepb')
        jet.deepflavour_score = jet.deepflavour_prob_b   + \
                                jet.deepflavour_prob_bb  + \
                                jet.deepflavour_prob_lepb

        jet.pass_deepflavour = jet.deepflavour_score >= deepflavour_wp[year][wp]

    def testBJet(self, jet, year, wp, final_state):    
        '''
        Test DeepFlavour
        including scale factors
        '''
        # Use the following once we start applying data-MC scale factors:
        jet.btagFlag = self.btagSF.isBTagged(
            pt          = jet.pt(),
            eta         = jet.eta(),
            deepjet     = jet.deepflavour_score,
            jetflavor   = abs(jet.partonFlavour()),
            is_data     = not self.cfg_comp.isMC,
            deepjet_cut = deepflavour_wp[year][wp],
            final_state = final_state,
        )

        return self.testJet(jet) and \
            abs(jet.eta()) < 2.4 and \
            jet.btagFlag and \
            self.testJetID(jet)
