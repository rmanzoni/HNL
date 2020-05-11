import os
from collections import OrderedDict

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Jet, GenJet

from PhysicsTools.HeppyCore.utils.deltar import cleanObjectCollection, matchObjectCollection

# from PhysicsTools.Heppy.physicsutils.BTagSF import BTagSF
from CMGTools.HNL.utils.BTagSF import BTagSF
from PhysicsTools.Heppy.physicsutils.JetReCalibrator import JetReCalibrator

# JAN: Kept this version of the jet analyzer in the tau-tau sequence
# for now since it has all the agreed-upon features used in the tau-tau group,
# in particular the SF seeding for b-tagging.
# In the long run, it might be a good idea to switch to the generic jet analyzer
# in heppy and possibly add b-tagging in another step or add it to the generic
# jet analyzer


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
        self.btagSF = BTagSF(0, wp=getattr(self.cfg_ana, 'btag_wp', 'medium'))
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

        self.handles['jets'] = AutoHandle(self.cfg_ana.jetCol, 'std::vector<pat::Jet>')

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
            if self.testJet(jet) : event.jets .append(jet)
            if self.testBJet(jet, year=self.cfg_ana.year, wp=getattr(self.cfg_ana, 'btag_wp', 'medium')): event.bJets.append(jet)

        self.counters.counter('jets').inc('all events')

        for final_state in ['mmm', 'mem', 'eee', 'eem']:
            
            if final_state not in leptons.keys():
                continue
            
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

            # save HTs
#             event.HT_allJets     = sum([jet.pt() for jet in allJets          ])
#             event.HT_jets        = sum([jet.pt() for jet in event.jets       ])
#             event.HT_jets30      = sum([jet.pt() for jet in event.jets30     ])
#             event.HT_bJets       = sum([jet.pt() for jet in event.bJets      ])
#             event.HT_cleanJets[final_state]   = sum([jet.pt() for jet in event.cleanJets  ])
#             event.HT_cleanJets30 [final_state]= sum([jet.pt() for jet in event.cleanJets30])
                                    
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

    def testBJet(self, jet, year, wp):    
        '''
        Test DeepFlavour
        '''
        
        # RM remove me!
        jet.btagMVA = jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags')

        # recommendations
        # general: https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation
        # 2016: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation2016Legacy
        # 2017: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
        # 2018: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
        jet.deepflavour_prob_b    = jet.btag('pfDeepFlavourJetTags:probb')
        jet.deepflavour_prob_bb   = jet.btag('pfDeepFlavourJetTags:probbb')
        jet.deepflavour_prob_lepb = jet.btag('pfDeepFlavourJetTags:problepb')
        jet.deepflavour_score = jet.deepflavour_prob_b   + \
                                jet.deepflavour_prob_bb  + \
                                jet.deepflavour_prob_lepb

        jet.pass_deepflavour = jet.deepflavour_score >= deepflavour_wp[year][wp]

        # Use the following once we start applying data-MC scale factors:
        jet.btagFlag = self.btagSF.isBTagged(
            pt=jet.pt(),
            eta=jet.eta(),
            deepjet=jet.deepflavour_score,
            jetflavor=abs(jet.partonFlavour()),
            is_data=not self.cfg_comp.isMC,
            deepjet_cut=deepflavour_wp[year][wp]
        )

        return self.testJet(jet) and \
            abs(jet.eta()) < 2.4 and \
            jet.btagFlag and \
            self.testJetID(jet)
