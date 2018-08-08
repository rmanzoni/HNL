'''
This is the main analyzer going through data and trying to identify HNL->3L events.
'''

import ROOT
from itertools import product, combinations
from math import sqrt, pow

import PhysicsTools.HeppyCore.framework.config       as cfg
from PhysicsTools.Heppy.analyzers.core.Analyzer      import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle    import AutoHandle
from PhysicsTools.Heppy.physicsobjects.GenParticle   import GenParticle
from PhysicsTools.Heppy.physicsobjects.Photon        import Photon
from PhysicsTools.Heppy.physicsobjects.Tau           import Tau
from PhysicsTools.Heppy.physicsobjects.Muon          import Muon
from PhysicsTools.Heppy.physicsobjects.Electron      import Electron
from PhysicsTools.Heppy.physicsobjects.Jet           import Jet
from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from CMGTools.HNL.utils.utils                        import isAncestor, displacement2D, displacement3D, makeRecoVertex, fitVertex
from PhysicsTools.HeppyCore.utils.deltar             import deltaR, deltaPhi

from CMGTools.HNL.physicsobjects.DiLepton import DiLepton
from CMGTools.HNL.physicsobjects.DisplacedMuon import DisplacedMuon
from pdb import set_trace

# load custom library to ROOT. This contains the kinematic vertex fitter class
ROOT.gSystem.Load('libCMGToolsHNL')
from ROOT import HNLKinematicVertexFitter as VertexFitter

class HNLAnalyzer(Analyzer):
    '''
    '''

    def declareHandles(self):
        super(HNLAnalyzer, self).declareHandles()

        self.handles['ele']      = AutoHandle(('slimmedElectrons', '','PAT'), 'std::vector<pat::Electron>')
        self.handles['sMu']      = AutoHandle(('slimmedMuons','','PAT'),'std::vector<pat::Muon>')
        self.handles['dSAMu']    = AutoHandle(('displacedStandAloneMuons','','RECO'),'std::vector<reco::Track>')
        self.handles['dGMu']     = AutoHandle(('displacedGlobalMuons','','RECO'),'std::vector<reco::Track>')
        self.handles['pvs']      = AutoHandle(('offlineSlimmedPrimaryVertices','','PAT'),'std::vector<reco::Vertex>')
        self.handles['svs']      = AutoHandle(('slimmedSecondaryVertices','','PAT'),'std::vector<reco::VertexCompositePtrCandidate>')
        self.handles['beamspot'] = AutoHandle(('offlineBeamSpot','','RECO'),'reco::BeamSpot')
        self.handles['pfmet']      = AutoHandle(('slimmedMETs','','PAT'),'std::vector<pat::MET>')
        self.handles['puppimet']      = AutoHandle('slimmedMETsPuppi','std::vector<pat::MET>')
        self.handles['jets']      = AutoHandle('slimmedJets','std::vector<pat::Jet>')
        self.handles['photons'] = AutoHandle(('slimmedPhotons','','PAT'),'std::vector<pat::Photon>')
        self.handles['taus'] = AutoHandle(('slimmedTaus', '','PAT'), 'std::vector<pat::Tau>')

    def assignVtx(self, particles, vtx):    
        for ip in particles:
            ip.associatedVertex = vtx

    def beginLoop(self, setup):
        super(HNLAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('HNL')
        count = self.counters.counter('HNL')
        count.register('all events')
        count.register('trigger matched, prompt candidate found')
        count.register('good gen')
        count.register('pairs')
        count.register('dimuons')
        # initiate the VertexFitter
        self.vtxfit = VertexFitter()

        # create a std::vector<RecoChargedCandidate> to be passed to the fitter
        self.tofit = ROOT.std.vector('reco::RecoChargedCandidate')()

    def buildDisplacedMuons(self, collection):
        muons = [DisplacedMuon(mm, collection) for mm in collection]
        return muons

    def process(self, event):
        self.readCollections(event.input)
        self.counters.counter('HNL').inc('all events')

        #####################################################################################
        # produce collections and map our objects to convenient Heppy objects
        #####################################################################################

        # make lepton objects
        event.ele         = map(Electron,self.handles['ele'].product())
        event.sMu         = map(Muon,self.handles['sMu'].product())
        event.dSAMu       = self.buildDisplacedMuons(self.handles['dSAMu'].product())
        event.dGMu        = self.buildDisplacedMuons(self.handles['dGMu' ].product())
        event.photons     = map(Photon       , self.handles  ['photons'    ].product())
        event.taus        = map(Tau          , self.handles  ['taus'       ].product())

        # make vertex objects 
        event.pvs         = self.handles['pvs'     ].product()
        event.svs         = self.handles['svs'     ].product()
        event.beamspot    = self.handles['beamspot'].product()

        # make met object
        event.pfmet         = self.handles['pfmet'].product().at(0)
        event.puppimet         = self.handles['puppimet'].product().at(0)

        # make jet object
        jets = self.handles['jets'].product()        


        # assign to the leptons the primary vertex, will be needed to compute a few quantities
        if len(event.pvs):
            myvtx = event.pvs[0]
        else:
            myvtx = event.beamspot
        
        self.assignVtx(event.sMu,myvtx)
        self.assignVtx(event.ele,myvtx)

        # store the number of sMu and dSAMu per event
        event.n_sMu   = len(event.sMu)
        event.n_dSAMu = len(event.dSAMu)
        event.n_dGMu  = len(event.dGMu)

        #####################################################################################
        # Find the prompt lepton
        #####################################################################################
        
        # ELECTRONS
        ele_cand = []
        if cfg.PromptLeptonMode == 'ele':
            matchable_ele = [ele for ele in event.ele]
            # selection
            ele_sel_eta = 2.5; ele_sel_pt = 30; ele_sel_vtx = 0.2 
            # match collections
            matchable_ele_sel_pt = [ele for ele in matchable_ele if (ele.pt() > ele_sel_pt)] 
            matchable_ele_sel_eta = [ele for ele in matchable_ele if (abs(ele.eta()) < ele_sel_eta)] 
            matchable_ele_sel_id = [ele for ele in matchable_ele if (ele.mvaIDRun2('NonTrigSpring15MiniAOD', 'POG90') == True)] 
            # https://github.com/rmanzoni/cmgtools-lite/blob/825_HTT/H2TauTau/python/proto/analyzers/TauEleAnalyzer.py#L193
#            print(ele.gsfTrack())
            matchable_ele_sel_vtx = [ele for ele in matchable_ele if abs(ele.dz()) < ele_sel_vtx] # TODO what about dxy component ?
            # https://github.com/rmanzoni/cmgtools-lite/blob/825_HTT/H2TauTau/python/proto/analyzers/TauEleAnalyzer.py#L104
            ele_cand = [ele for ele in matchable_ele if (ele in matchable_ele_sel_pt and ele in matchable_ele_sel_eta and ele in matchable_ele_sel_id and ele in matchable_ele_sel_vtx)]
            

        # MUONS
        mu_cand = []
        if cfg.PromptLeptonMode == 'mu':
            matchable_mu = [mu for mu in event.sMu] 
            # selection
            mu_sel_eta = 2.4; mu_sel_pt = 3; mu_sel_vtx = 0.2 
            # match collections
            matchable_mu_sel_pt = [mu for mu in matchable_mu if (mu.pt() > mu_sel_pt)] 
            matchable_mu_sel_eta = [mu for mu in matchable_mu if (abs(mu.eta()) < mu_sel_eta)] 
            matchable_mu_sel_id = [mu for mu in matchable_mu if (mu.looseId() == True)] 
            matchable_mu_sel_vtx = [mu for mu in matchable_mu if abs(mu.dz()) < mu_sel_vtx] # TODO what about dxy component ?
            mu_cand = [mu for mu in matchable_mu if (mu in matchable_mu_sel_pt and mu in matchable_mu_sel_eta and mu in matchable_mu_sel_id and mu in matchable_mu_sel_vtx)]

        # PROMPT CANDIDATE
        prompt_cand = ele_cand + mu_cand # ONE IS ALWAYS EMPTY; check this:
        if cfg.PromptLeptonMode == 'mu' and not len(ele_cand) == 0: print('ERROR: cfg.PromptLeptonMode = mu but len(ele_can) != 0')
        if cfg.PromptLeptonMode == 'ele' and not len(mu_cand) == 0: print('ERROR: cfg.PromptLeptonMode = ele but len(mu_can) != 0')
        the_prompt_cand = None

        if cfg.DataSignalMode == 'signal': event.prompt_ana_success = -99 # NO RECO FOUND
        if not len(prompt_cand): return False # TODO TURN THIS ON FOR DATA
        if len(prompt_cand): 
        # selection: pick candidate with highest pt 
        # there must be something better; maybe if both are matched check some additional stuff
            the_prompt_cand = sorted(prompt_cand, key = lambda lep: lep.pt(), reverse = True)[0]
#           # REMOVING PROMPT LEPTON FROM MATCHES
#           # AND EVALUATING ANALYZER 
            if the_prompt_cand in ele_cand:
                for i in event.ele:
                    if i.physObj == the_prompt_cand.physObj: event.ele.remove(i)
                if cfg.DataSignalMode == 'signal':
                    if hasattr(event.the_hnl.l0().bestmatch, 'physObj'):
                        if  the_prompt_cand.physObj == event.the_hnl.l0().bestmatch.physObj:
                            event.prompt_ana_success = 1
                        else: event.prompt_ana_success = -11 # FAKE ELECTRONS
            if the_prompt_cand in mu_cand:
                for i in event.muons:
                    if i.physObj == the_prompt_cand.physObj: event.muons.remove(i)
                if cfg.DataSignalMode == 'signal':
                    if hasattr(event.the_hnl.l0().bestmatch, 'physObj'):
                        if  the_prompt_cand.physObj == event.the_hnl.l0().bestmatch.physObj:
                            event.prompt_ana_success = 1
                    else: event.prompt_ana_success = -13 # FAKE MUONS
            if the_prompt_cand == None:
                return False #TODO TURN ON FOR DATA

        event.the_prompt_cand = the_prompt_cand 
       
        #####################################################################################
        # Merge Reco Muons
        # Create an array of DisplacedMuon objects, summarizing all sMu, dSAMu and dGMu into a single array
        # Comment those out which are not needed for the current run
        #####################################################################################
        dMus = []

        for smu in event.sMu:
           dmu = smu
           dmu.reco = 1 # sMu = 1, dSAMu = 2, dGMu = 3
           dMus.append(dmu)

        # for dsa in event.dSAMu:
            # dmu = dsa
            # dmu.reco = 2 # sMu = 1, dSAMu = 2, dGMu = 3
            # dMus.append(dmu)

        # for dg in event.dGMu:
            # dmu = dg
            # dmu.reco = 3 # sMu = 1, dSAMu = 2, dGMu = 3
            # dMus.append(dmu)

       
        event.n_dMu = len(dMus) # important to understand how well the "Merge Reco Muons" process went. 
       
        #####################################################################################
        # select only events with good gen events
        #####################################################################################
        if cfg.DataSignalMode == 'signal':
            if not( abs(event.the_hnl.l1().pdgId())==13   and \
                    abs(event.the_hnl.l2().pdgId())==13   and \
                    # abs(event.the_hnl.l0().pdgId())==11   and \
                    abs(event.the_hnl.l0().pdgId())==13   and \
                    abs(event.the_hnl.l1().eta())   < 2.4 and \
                    abs(event.the_hnl.l2().eta())   < 2.4 and \
                    # abs(event.the_hnl.l0().eta())   < 2.5): 
                    abs(event.the_hnl.l0().eta())   < 2.4): 
                return False

            if (not hasattr(event.the_hnl.l1(), 'bestmatch')) or (event.the_hnl.l1().bestmatch is None):
                return False
            if (not hasattr(event.the_hnl.l2(), 'bestmatch')) or (event.the_hnl.l2().bestmatch is None):
                return False

            self.counters.counter('HNL').inc('good gen')

        # #####################################################################################
        # Preselection for the reco muons before pairing them
        # #####################################################################################
        # some simple preselection based on pt
        event.sMu   = [imu for imu in event.sMu   if (imu.pt()>3. and abs(imu.eta())<2.4)]
        event.dSAMu = [imu for imu in event.dSAMu if (imu.pt()>3. and abs(imu.eta())>2.4)]
        event.dGMu  = [imu for imu in event.dGMu  if (imu.pt()>3. and abs(imu.eta())>2.4)]


        #####################################################################################
        # collect all muon pairs
        #####################################################################################
        pairs = [pair for pair in combinations(dMus,2)] 
        pairs = [(mu1,mu2) for mu1, mu2 in pairs if deltaR(mu1,mu2)>0.01] 
        event.n_pairs = len(pairs)
        event.flag_IsThereTHEDimuon = False

        event.n_dimuon = 0
        if len(pairs) == 0:
            pass

        self.counters.counter('HNL').inc('pairs')

        ########################################################################################
        # Vertex Fit: Select only dimuon pairs with mutual vertices
        ########################################################################################
        dimuons = []
        for pair in pairs:
            sv = None
            # print pair[0]
            # print pair[1]
            if not pair[0]==pair[1]:
                sv = fitVertex(pair)
                if sv != None:
                    dimuons.append(DiLepton(pair,sv,myvtx,event.beamspot,event.the_prompt_cand))

        #####################################################################################
        # Check whether the correct dimuon is part of the collection dimuons
        #####################################################################################
        if cfg.DataSignalMode == 'signal':
            if len(dimuons) > 0:
                for dimu in dimuons:
                    dMu1 = dimu.lep1()
                    dMu2 = dimu.lep2() 
                    if (dMu1.physObj == event.the_hnl.l1().bestmatch.physObj or dMu1.physObj == event.the_hnl.l2().bestmatch.physObj) and (dMu2.physObj == event.the_hnl.l1().bestmatch.physObj or dMu2.physObj == event.the_hnl.l2().bestmatch.physObj):
                        event.flag_IsThereTHEDimuon = True


        #####################################################################################
        # select the best dimuon pairs 
        #####################################################################################
        event.n_dimuon = len(dimuons)
        if len(dimuons) > 0:
            self.counters.counter('HNL').inc('dimuons')
             
            # select the dimuon with lowest vertex fit chi2 as the HNL dimuon candidate
            dimuonChi2 = sorted(dimuons, key = lambda x: (x.isSS(),x.chi2()), reverse = False)[0] 
            event.dimuonChi2 = dimuonChi2
            event.dMu1Chi2 = dimuonChi2.lep1()
            event.dMu2Chi2 = dimuonChi2.lep2()
            
            # select the dimuon with largest displacement
            dimuonDxy = sorted(dimuons, key = lambda x: (x.isOS(),x.disp2DFromBS()), reverse = True)[0] 
            event.dimuonDxy = dimuonDxy
            event.dMu1Dxy = dimuonDxy.lep1()
            event.dMu2Dxy = dimuonDxy.lep2()

            # select leptons ito added momenta's pt
            dimuonMaxPt = sorted(dimuons, key = lambda x: (x.isOS(),x.pt_12()), reverse = True)[0] 
            event.dimuonMaxPt = dimuonMaxPt
            event.dMu1MaxPt = dimuonMaxPt.lep1()
            event.dMu2MaxPt = dimuonMaxPt.lep2()

            # select closest leptons ito dr
            dimuonMinDr12 = sorted(dimuons, key = lambda x: (x.isSS(),x.dr_12()), reverse = False)[0]
            event.dimuonMinDr12 = dimuonMinDr12
            event.dMu1MinDr12 = dimuonMinDr12.lep1()
            event.dMu2MinDr12 = dimuonMinDr12.lep2()

            # select smallest backpointing angle in the transverse plane
            dimuonMaxCosBPA = sorted(dimuons, key = lambda x : (x.isSS(), -x.cosTransversePointingAngleBS()), reverse=False)[0]
            event.dimuonMaxCosBPA = dimuonMaxCosBPA
            event.dMu1MaxCosBPA = dimuonMaxCosBPA.lep1()
            event.dMu2MaxCosBPA = dimuonMaxCosBPA.lep2()


        #####################################################################################
        # TODO: Final Qualification and 'ok' to nominate the selection dimuon as HNL candidate
        #####################################################################################
        # event.flag_HNLRecoSuccess = False
        # if event.dMu1MaxCosBPA.charge() != event.dMu2MaxCosBPA.charge():
            # event.flag_HNLRecoSuccess = True 
#       #####################################################################################
#       ###            JET ANALYZER
#       #####################################################################################
#
#       allJets = []
#       event.jets = []
#       event.bJets = []
#       event.cleanJets = []
#       event.cleanBJets = []
#
#       leptons = []
#       if hasattr(event, 'selectedLeptons'):
#           leptons = event.selectedLeptons
#       if hasattr(self.cfg_ana, 'toClean'):
#           leptons = getattr(event, self.cfg_ana.toClean)
#           
#       if hasattr(self.cfg_ana, 'leptonCollections'):
#           for coll in self.cfg_ana.leptonCollections:
#               leptons += self.handles[coll].product()
#
#       allJets = [Jet(jet) for jet in miniaodjets]
#
#       ###   CONFIG   ###
#       self.recalibrateJets = False
#
#       if self.recalibrateJets:
#           self.jetReCalibrator.correctAll(allJets, event.rho, delta=0., 
#                                               addCorr=True, addShifts=True)
#
#       for jet in allJets:
#           if self.testJet(jet):
#               event.jets.append(jet)
#           if self.testBJet(jet):
#               event.bJets.append(jet)
#
#       self.counters.counter('jets').inc('all events')
#
#       event.cleanJets, dummy = cleanObjectCollection(event.jets,
#                                                      masks=leptons,
#                                                      deltaRMin=0.5)
#       event.cleanBJets, dummy = cleanObjectCollection(event.bJets,
#                                                       masks=leptons,
#                                                       deltaRMin=0.5)
#
#       event.allLeptons = event.sMu + event.dSAmu + event.dGmu + event.ele #+event.tau
#       # Attach matched jets to selected + other leptons
#       if hasattr(event, 'allLeptons'):
#           leptons = event.allLeptons
#           
#       pairs = matchObjectCollection(leptons, allJets, 0.5 * 0.5)
#       # associating a jet to each lepton
#       for lepton in leptons:
#           jet = pairs[lepton]
#           if jet is None:
#               lepton.jet = lepton
#           else:
#               lepton.jet = jet
#
#       # associating a leg to each clean jet
#       invpairs = matchObjectCollection(event.cleanJets, leptons, 99999.)
#       for jet in event.cleanJets:
#           leg = invpairs[jet]
#           jet.leg = leg
#
#       for jet in event.cleanJets:
#           jet.matchGenParton = 999.0
#
#       event.jets30 = [jet for jet in event.jets if jet.pt() > 30]
#       event.cleanJets30 = [jet for jet in event.cleanJets if jet.pt() > 30]
#       if len(event.jets30) >= 2:
#           self.counters.counter('jets').inc('at least 2 good jets')
#       if len(event.cleanJets30) >= 2:
#           self.counters.counter('jets').inc('at least 2 clean jets')
#       if len(event.cleanBJets) > 0:
#           self.counters.counter('jets').inc('at least 1 b jet')
#           if len(event.cleanBJets) > 1:
#               self.counters.counter('jets').inc('at least 2 b jets')
#               
#       # save HTs
#       event.HT_allJets     = sum([jet.pt() for jet in allJets          ])
#       event.HT_jets        = sum([jet.pt() for jet in event.jets       ])
#       event.HT_bJets       = sum([jet.pt() for jet in event.bJets      ])
#       event.HT_cleanJets   = sum([jet.pt() for jet in event.cleanJets  ])
#       event.HT_jets30      = sum([jet.pt() for jet in event.jets30     ])
#       event.HT_cleanJets30 = sum([jet.pt() for jet in event.cleanJets30])
#       #####################################################################################
#       # TODO: Final Qualification and 'ok' to nominate the selection dimuon as HNL candidate
#       #####################################################################################
#       # event.flag_HNLRecoSuccess = False
#       # if event.dMu1MaxCosBPA.charge() != event.dMu2MaxCosBPA.charge():
#           # event.flag_HNLRecoSuccess = True 
#   
        # return True
#
#### from jet analyzer https://github.com/rmanzoni/cmgtools-lite/blob/825_HTT/H2TauTau/python/proto/analyzers/JetAnalyzer.py#L238
#
#   def testJetID(self, jet):
#       jet.puJetIdPassed = jet.puJetId()
#       jet.pfJetIdPassed = jet.jetID("POG_PFID_Loose")
#       puJetId = self.cfg_ana.relaxPuJetId or jet.puJetIdPassed 
#       pfJetId = self.cfg_ana.relaxJetId or jet.pfJetIdPassed 
#       return puJetId and pfJetId
#
#   def testJet(self, jet):
#       pt = jet.pt()
#       if hasattr(self.cfg_ana, 'ptUncTolerance') and self.cfg_ana.ptUncTolerance:
#           pt = max(pt, pt * jet.corrJECUp/jet.corr, pt * jet.corrJECDown/jet.corr)
#       return pt > self.cfg_ana.jetPt and \
#           abs( jet.eta() ) < self.cfg_ana.jetEta and \
#           self.testJetID(jet)
#
#   def testBJet(self, jet, csv_cut=0.8484):
#       # medium csv working point
#       # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation74X
#       jet.btagMVA = jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags')
#       # jet.btagFlag = jet.btagMVA > csv_cut
#
#       # Use the following once we start applying data-MC scale factors:
#       jet.btagFlag = self.btagSF.isBTagged(
#           pt=jet.pt(),
#           eta=jet.eta(),
#           csv=jet.btag("pfCombinedInclusiveSecondaryVertexV2BJetTags"),
#           jetflavor=abs(jet.partonFlavour()),
#           is_data=not self.cfg_comp.isMC,
#           csv_cut=csv_cut
#       )
#
#       return self.testJet(jet) and \
#           abs(jet.eta()) < 2.4 and \
#           jet.btagFlag and \
#           self.testJetID(jet)

# ) 
        return True
