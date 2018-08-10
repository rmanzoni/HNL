'''
This is the main analyzer going through data and trying to identify HNL->3L events.
'''

import ROOT
from itertools import product, combinations
from math import sqrt, pow

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.utils.deltar             import deltaR, deltaPhi
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
from CMGTools.HNL.physicsobjects.DiLepton            import DiLepton
from CMGTools.HNL.physicsobjects.DisplacedMuon       import DisplacedMuon

from pdb import set_trace

# load custom library to ROOT. This contains the kinematic vertex fitter class
ROOT.gSystem.Load('libCMGToolsHNL')
from ROOT import HNLKinematicVertexFitter as VertexFitter

class HNLAnalyzer(Analyzer):
    '''
    '''

    def declareHandles(self):
        super(HNLAnalyzer, self).declareHandles()

        self.handles['electrons'] = AutoHandle(('slimmedElectrons'             ,'','PAT' ), 'std::vector<pat::Electron>'                    )
        self.handles['muons'    ] = AutoHandle(('slimmedMuons'                 ,'','PAT' ), 'std::vector<pat::Muon>'                        )
        self.handles['dsamuons' ] = AutoHandle(('displacedStandAloneMuons'     ,'','RECO'), 'std::vector<reco::Track>'                      )
        self.handles['dgmuons'  ] = AutoHandle(('displacedGlobalMuons'         ,'','RECO'), 'std::vector<reco::Track>'                      )
        self.handles['photons'  ] = AutoHandle(('slimmedPhotons'               ,'','PAT' ), 'std::vector<pat::Photon>'                      )
        self.handles['taus'     ] = AutoHandle(('slimmedTaus'                  ,'','PAT' ), 'std::vector<pat::Tau>'                         )
        self.handles['jets'     ] = AutoHandle( 'slimmedJets'                             , 'std::vector<pat::Jet>'                         )
        self.handles['pvs'      ] = AutoHandle(('offlineSlimmedPrimaryVertices','','PAT' ), 'std::vector<reco::Vertex>'                     )
        self.handles['svs'      ] = AutoHandle(('slimmedSecondaryVertices'     ,'','PAT' ), 'std::vector<reco::VertexCompositePtrCandidate>')
        self.handles['beamspot' ] = AutoHandle(('offlineBeamSpot'              ,'','RECO'), 'reco::BeamSpot'                                )
        self.handles['pfmet'    ] = AutoHandle(('slimmedMETs'                  ,'','PAT' ), 'std::vector<pat::MET>'                         )
        self.handles['puppimet' ] = AutoHandle('slimmedMETsPuppi'                         , 'std::vector<pat::MET>'                         )

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
        count.register('> 0 di-muon')
        count.register('> 0 di-muon + vtx')
        count.register('pairs')
        count.register('dimuons')
        # initiate the VertexFitter
        self.vtxfit = VertexFitter()

        # create a std::vector<RecoChargedCandidate> to be passed to the fitter
        self.tofit = ROOT.std.vector('reco::RecoChargedCandidate')()

    def buildDisplacedMuons(self, collection):
        muons = [DisplacedMuon(mm, collection) for mm in collection]
        return muons

    def testLepKin(self, lep, pt, eta):
        # kinematics
        if abs(lep.eta())>eta: return False
        if lep.pt()      <pt : return False
        # passed
        return True        

    def testLepVtx(self, lep, dxy, dz):
        # vertex
        if abs(ele.dz()) >dz : return False
        if abs(ele.dxy())>dxy: return False
        # passed
        return True
    
    def preselectPromptElectrons(self, ele, pt=30, eta=2.5, dxy=0.045, dz=0.2):
        # kinematics
        if not self.testLepKin(ele, pt, eta): return False
        # id
        if not ele.mvaIDRun2('NonTrigSpring15MiniAOD', 'POG90'): return False
        # vertex
        if not self.testLepVtx(ele, dxy, dz): return False
        # passed
        return True

    def preselectPromptMuons(self, mu, pt=25, eta=2.4, dxy=0.045, dz=0.2):
        # kinematics
        if not self.testLepKin(mu, pt, eta): return False
        # id
        if not mu.looseId(): return False
        # vertex
        if not self.testLepVtx(mu, dxy, dz): return False
        # passed
        return True

    def process(self, event):
        self.readCollections(event.input)
        self.counters.counter('HNL').inc('all events')

        #####################################################################################
        # produce collections and map our objects to convenient Heppy objects
        #####################################################################################

        # make muon collections
        event.muons       = map(Muon, self.handles['muons'].product())
        event.dsamuons    = self.buildDisplacedMuons(self.handles['dsamuons'].product())
        event.dgmuons     = self.buildDisplacedMuons(self.handles['dgmuons' ].product())

        for imu in event.muons   : imu.type = 13
        for imu in event.dsamuons: imu.type = 26
        for imu in event.dgmuons : imu.type = 39

        event.electrons   = map(Electron, self.handles['electrons'].product())
        event.photons     = map(Photon  , self.handles['photons'  ].product())
        event.taus        = map(Tau     , self.handles['taus'     ].product())

        # make vertex objects 
        event.pvs         = self.handles['pvs'     ].product()
        event.svs         = self.handles['svs'     ].product()
        event.beamspot    = self.handles['beamspot'].product()

        # make met object
        event.pfmet       = self.handles['pfmet'   ].product().at(0)
        event.puppimet    = self.handles['puppimet'].product().at(0)

        # make jet object
        jets = self.handles['jets'].product()        

        # assign to the leptons the primary vertex, will be needed to compute a few quantities
        myvtx = event.pvs[0] if len(event.pvs) else event.beamspot
        
        self.assignVtx(event.muons    , myvtx)
        self.assignVtx(event.electrons, myvtx)

#         #####################################################################################
#         # select only events with good gen events
#         #####################################################################################
#         if not( abs(event.the_hnl.l1().pdgId())==13   and \
#                 abs(event.the_hnl.l2().pdgId())==13   and \
#                 abs(event.the_hnl.l1().eta())   < 2.4 and \
#                 abs(event.the_hnl.l2().eta())   < 2.4 and \
#                 abs(event.the_hnl.l0().eta())   < 2.4): 
#             return False
# 
#         # FIXME! just for testing
#         if displacement2D(event.the_hn.lep1, event.the_hn) > 40:
#             return False
#         # if displacement2D(event.the_hn.lep1, event.the_hn) > 100:
#         #    return False
#         # import pdb ; pdb.set_trace()
#         if (not hasattr(event.the_hnl.l1(), 'bestmatch')) or (event.the_hnl.l1().bestmatch is None):
#             return False
#         if (not hasattr(event.the_hnl.l2(), 'bestmatch')) or (event.the_hnl.l2().bestmatch is None):
#             return False
# 
#         self.counters.counter('HNL').inc('good gen')
# 
        #####################################################################################
        # Find the prompt lepton
        #####################################################################################
        
        prompt_ele_cands = sorted([ele for ele in event.electrons if self.preselectPromptElectrons(ele)], key = lambda x : x.pt(), reverse = True)
        prompt_mu_cands  = sorted([mu  for mu  in event.muons     if self.preselectPromptElectrons(mu)] , key = lambda x : x.pt(), reverse = True)

        # PROMPT CANDIDATE
        if self.cfg_ana.promptLepton=='mu':
            if not len(prompt_mu_cands):
                return False
            prompt_cand = prompt_mu_cands[0]
            # remove from the leptons that will be later used to find the displaced di-lepton
            event.filtered_muons = [mu for mu in event.muons if mu.physObj != prompt_cand.physObj]

        if self.cfg_ana.promptLepton=='ele':
            if not len(prompt_ele_cands):
                return False
            prompt_cand = prompt_ele_cands[0]
            # remove from the leptons that will be later used to find the displaced di-lepton
            event.filtered_electrons = [ele for ele in event.electrons if ele.physObj != prompt_cand.physObj]

        # RM: FIXME! check this!
        #####################################################################################
        # Backmatching with HLT # TODO TEST THIS AND SEE IF IT WORKS PROPERLY
        #####################################################################################
        
        # match only if the trigger fired
        event.fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]

        # trigger matching
        if hasattr(self.cfg_ana, 'trigger_match') and len(self.cfg_ana.trigger_match.keys())>0:
                                   
            for lep in the_prompt_cand:
                
                lep.hltmatched = [] # initialise to no match
                
                lep.trig_objs = OrderedDict()
                lep.trig_objs[1] = [] # initialise to no trigger objct matches
    
                lep.trig_matched = OrderedDict()
                lep.trig_matched[1] = False # initialise to no match

                lep.best_trig_match = OrderedDict()
                lep.best_trig_match[1] = OrderedDict()

                # add all matched objects to each muon
                for info in event.trigger_infos:
                                    
                    mykey = '_'.join(info.name.split('_')[:-1])

                    # start with simple matching
                    these_objects = sorted([obj for obj in info.objects if deltaR(lep, obj)<0.15], key = lambda x : deltaR(x, lep))

                    lep.trig_objs[1] += these_objects

                    # get the set of trigger types from the cfg 
                    trigger_types_to_match = self.cfg_ana.trigger_match[mykey][1]
                    
                    # list of tuples of matched objects
                    good_matches = []

                    # initialise the matching to None
                    lep.best_trig_match[1][mykey] = None

                    # investigate all the possible matches (leps, pairs or singlets)
                    for t_o in these_objects:

                        # intersect found trigger types to desired trigger types
                        itypes = Counter()
                        for ikey in trigger_types_to_match.keys():
                            itypes[ikey] = sum([1 for iobj in t_o if iobj.triggerObjectTypes()[0]==ikey])
                                            
                        # all the types to match are matched then assign the 
                        # corresponding trigger object to each lep
                        if itypes & trigger_types_to_match == trigger_types_to_match:
                            good_matches.append(t_o)
                    
                    
                    if len(good_matches):
                        good_matches.sort(key = lambda x : deltaR(x, lep))        

                # iterate over the path:filters dictionary
                #     the filters MUST be sorted correctly: i.e. first filter in the dictionary 
                #     goes with the first muons and so on
                for k, vv in self.cfg_ana.trigger_match.iteritems():

                    if not any(k in name for name in event.fired_triggers):
                         continue
                    
                    v = vv[0]
                                                                 
                    for ii, filters in enumerate(v):
                        if not lep.best_trig_match[ii+1][k]:
                            continue
                        if set([filters]) & set(lep.best_trig_match[ii+1][k].filterLabels()):
                            lep.trig_matched[ii+1] = True                 
                    
                    ismatched = sum(lep.trig_matched.values())            
                                
                    if len(v) == ismatched:
                        lep.hltmatched.append(k)

            the_prompt_cand = [lep for lep in the_prompt_cand if len(lep.hltmatched)>0] 
            
            if the_prompt_cand == None:
                return False 

        event.the_prompt_cand = the_prompt_cand


        # What is this?
        if cfg.DataSignalMode == 'signal': event.prompt_ana_success = -99 # NO RECO FOUND


        # RM: a bit convoluted, will unerstand it later
        # REMOVING PROMPT LEPTON FROM MATCHES
        # AND EVALUATING ANALYZER 
        if the_prompt_cand in ele_cand:
            if cfg.DataSignalMode == 'signal':
                if hasattr(event.the_hnl.l0().bestmatch, 'physObj'):
                    if  the_prompt_cand.physObj == event.the_hnl.l0().bestmatch.physObj:
                        event.prompt_ana_success = 1
                    else: event.prompt_ana_success = -11 # FAKE ELECTRONS
        if the_prompt_cand in mu_cand:
            if cfg.DataSignalMode == 'signal':
                if hasattr(event.the_hnl.l0().bestmatch, 'physObj'):
                    if  the_prompt_cand.physObj == event.the_hnl.l0().bestmatch.physObj:
                        event.prompt_ana_success = 1
                else: event.prompt_ana_success = -13 # FAKE MUONS

        event.the_prompt_cand = the_prompt_cand 
  
      
#        #####################################################################################
#        # Merge Reco Muons
#        # Create an array of DisplacedMuon objects, summarizing all sMu, dSAMu and dGMu into a single array
#        # Comment those out which are not needed for the current run
#        #####################################################################################
#        dMus = []
#
#        for smu in event.sMu:
#           dmu = smu
#           dmu.reco = 1 # sMu = 1, dSAMu = 2, dGMu = 3
#           dMus.append(dmu)
#
#        # for dsa in event.dSAMu:
#            # dmu = dsa
#            # dmu.reco = 2 # sMu = 1, dSAMu = 2, dGMu = 3
#            # dMus.append(dmu)
#
#        # for dg in event.dGMu:
#            # dmu = dg
#            # dmu.reco = 3 # sMu = 1, dSAMu = 2, dGMu = 3
#            # dMus.append(dmu)
#
#       
#        event.n_dMu = len(dMus) # important to understand how well the "Merge Reco Muons" process went. 

       
        ########################################################################################
        # Preselection for the reco muons before pairing them
        ########################################################################################
        # some simple preselection
        event.muons    = [imu for imu in event.filtered_muons if imu.pt()>3. and abs(imu.eta())<2.4]
        event.dsamuons = [imu for imu in event.dsamuons       if imu.pt()>3. and abs(imu.eta())>2.4]
        event.dgmuons  = [imu for imu in event.dgmuons        if imu.pt()>3. and abs(imu.eta())>2.4]

        # create all the possible di-muon pairs out of the three different collections
        dimuons = combinations(event.muons + event.dsamuons + event.dgmuons, 2)
        
        dimuons = [(mu1, mu2) for mu1, mu2 in dimuons if deltaR(mu1, mu2)>0.01]
        
        if not len(dimuons):
            # return False
            pass
        self.counters.counter('HNL').inc('> 0 di-muon + vtx')

        event.flag_IsThereTHEDimuon = False

        ########################################################################################
        # Vertex Fit: Select only dimuon pairs with mutual vertices
        ########################################################################################
        dimuonsvtx = []
        for index, pair in enumerate(dimuons):
            if pair[0]==pair[1]: continue
            sv = fitVertex(pair)
            if not sv: continue
            dimuonsvtx.append(DiLepton(pair, makeRecoVertex(sv, kinVtxTrkSize=2), myvtx, event.beamspot))

        event.dimuonsvtx = dimuonsvtx
        
        if len(event.dimuonsvtx):
            return False 
        
        self.counters.counter('HNL').inc('> 0 di-muon + vtx')

        ########################################################################################
        # candidate choice by different criteria
        ########################################################################################
        
        which_candidate = getattr(self.cfg_ana, 'candidate_selection', 'maxpt')
        
        if which_candidate == 'minmass'    : event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(),  x.mass()                        ), reverse=False)[0]
        if which_candidate == 'minchi2'    : event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(),  x.chi2()                        ), reverse=False)[0]
        if which_candidate == 'mindr'      : event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(),  x.dr()                          ), reverse=False)[0]
        if which_candidate == 'maxdphi'    : event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.dphi()                        ), reverse=False)[0]
        if which_candidate == 'mindeta'    : event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(),  x.deta()                        ), reverse=False)[0]
        if which_candidate == 'maxdisp2dbs': event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp2DFromBS()                ), reverse=False)[0]
        if which_candidate == 'maxdisp2dpv': event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp2DFromPV()                ), reverse=False)[0]
        if which_candidate == 'maxdisp3dpv': event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp3DFromPV()                ), reverse=False)[0]
        if which_candidate == 'maxdls2dbs' : event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp2DFromBSSignificance()    ), reverse=False)[0]
        if which_candidate == 'maxdls2dpv' : event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp2DFromPVSignificance()    ), reverse=False)[0]
        if which_candidate == 'maxdls3dpv' : event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp3DFromPVSignificance()    ), reverse=False)[0]
        if which_candidate == 'maxcos'     : event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.cosTransversePointingAngleBS()), reverse=False)[0]
        if which_candidate == 'maxpt'      : event.hnl_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.pt()                          ), reverse=False)[0]

        # RM: FIXME! at this point one should instantiate a 3L object


        # print 'hnl_minmass    ', event.hnl_minchi2    
        # print 'hnl_minchi2    ', event.hnl_minchi2    
        # print 'hnl_maxpt      ', event.hnl_maxpt      
        # print 'hnl_mindr      ', event.hnl_mindr      
        # print 'hnl_maxdphi    ', event.hnl_maxdphi    
        # print 'hnl_mindeta    ', event.hnl_mindeta    
        # print 'hnl_maxdisp2dbs', event.hnl_maxdisp2dbs
        # print 'hnl_maxdisp2dpv', event.hnl_maxdisp2dpv
        # print 'hnl_maxdisp3dpv', event.hnl_maxdisp3dpv
        # print 'hnl_maxdls2dbs ', event.hnl_maxdls2dbs 
        # print 'hnl_maxdls2dpv ', event.hnl_maxdls2dpv 
        # print 'hnl_maxdls3dpv ', event.hnl_maxdls3dpv 
        # print 'hnl_maxcos     ', event.hnl_maxcos     

        # import pdb ; pdb.set_trace()        

        # if not len(dimuonsvtx):
        #     import pdb ; pdb.set_trace()        

        #####################################################################################
        # Check whether the correct dimuon is part of the collection dimuons
        #####################################################################################
        # RM: a bit convoluted, will unerstand it later
        if cfg.DataSignalMode == 'signal':
            if len(dimuons) > 0:
                for dimu in dimuons:
                    dMu1 = dimu.lep1()
                    dMu2 = dimu.lep2() 
                    if (dMu1.physObj == event.the_hnl.l1().bestmatch.physObj or dMu1.physObj == event.the_hnl.l2().bestmatch.physObj) and (dMu2.physObj == event.the_hnl.l1().bestmatch.physObj or dMu2.physObj == event.the_hnl.l2().bestmatch.physObj):
                        event.flag_IsThereTHEDimuon = True

        return True
        
        