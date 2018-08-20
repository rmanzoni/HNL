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
from CMGTools.HNL.physicsobjects.HN3L                import HN3L
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
#        self.handles['dsamuons' ] = AutoHandle(('displacedStandAloneMuons'     ,'','RECO'), 'std::vector<reco::Track>'                      )
#        self.handles['dgmuons'  ] = AutoHandle(('displacedGlobalMuons'         ,'','RECO'), 'std::vector<reco::Track>'                      )
        self.handles['photons'  ] = AutoHandle(('slimmedPhotons'               ,'','PAT' ), 'std::vector<pat::Photon>'                      )
        self.handles['taus'     ] = AutoHandle(('slimmedTaus'                  ,'','PAT' ), 'std::vector<pat::Tau>'                         )
        self.handles['jets'     ] = AutoHandle( 'slimmedJets'                             , 'std::vector<pat::Jet>'                         )
        self.handles['pvs'      ] = AutoHandle(('offlineSlimmedPrimaryVertices','','PAT' ), 'std::vector<reco::Vertex>'                     )
        self.handles['svs'      ] = AutoHandle(('slimmedSecondaryVertices'     ,'','PAT' ), 'std::vector<reco::VertexCompositePtrCandidate>')
        self.handles['beamspot' ] = AutoHandle(('offlineBeamSpot'              ,'','RECO'), 'reco::BeamSpot'                                )
        self.handles['pfmet'    ] = AutoHandle(('slimmedMETs'                  ,'','PAT' ), 'std::vector<pat::MET>'                         )
        self.handles['puppimet' ] = AutoHandle('slimmedMETsPuppi'                         , 'std::vector<pat::MET>'                         )
        self.handles['pfcand'   ] = AutoHandle('packedPFCandidates'                       , 'std::vector<pat::PackedCandidate> '            )

    def assignVtx(self, particles, vtx):    
        for ip in particles:
            ip.associatedVertex = vtx

    def beginLoop(self, setup):
        super(HNLAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('HNL')
        count = self.counters.counter('HNL')
        count.register('all events')
        count.register('>0 good vtx')
        count.register('>0 prompt lep')
        count.register('>0 trig match prompt lep')
        count.register('> 0 di-muon')
        count.register('> 0 di-muon + vtx')

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
        if abs(lep.dz()) >dz : return False
        if abs(lep.dxy())>dxy: return False
        # passed
        return True
    
    def preselectPromptElectrons(self, ele, pt=30, eta=2.5, dxy=0.045, dz=0.2):
        # kinematics
        if not self.testLepKin(ele, pt, eta): return False
        # id
        if not ele.electronID("MVA_ID_nonIso_Fall17_Loose"): return False
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

    def isOotMuon(self, muon):
        '''
        returns True if the muon fires the out-of-time selection proposed by Piotr
        https://indico.cern.ch/event/695762/contributions/2853865/attachments/1599433/2535174/ptraczyk_201802_oot_fakes.pdf
        
        For in-time muons you want this to return False.
        '''
        cmb = muon.time()
        rpc = muon.rpcTime()
        
        # I guess one needs to understand which type of time is needed
        # there is an enum to do that
        # http://cmslxr.fnal.gov/source/DataFormats/MuonReco/interface/MuonTime.h#0007
        
        if rpc.direction == -1:
            rpc.time    = rpc.timeAtIpOutIn()
            rpc.timeerr = rpc.timeAtIpOutInErr()
        elif rpc.direction == 1:
            rpc.time = rpc.timeAtIpInOut()
            rpc.timeerr = rpc.timeAtIpInOutErr()
        else:
            # print 'WARNING: undefined muon direction, cannot understand RPC time'
            return False

        if cmb.direction == -1:
            cmb.time    = cmb.timeAtIpOutIn()
            cmb.timeerr = cmb.timeAtIpOutInErr()
        elif cmb.direction == 1:
            cmb.time = cmb.timeAtIpInOut()
            cmb.timeerr = cmb.timeAtIpInOutErr()
        else:
            # print 'WARNING: undefined muon direction, cannot understand CMB time'
            return False
        
        cmbok = (cmb.nDof>7)
        rpcok = (rpc.nDof>1 and rpc.timeerr==0)
        
        if rpcok:
            if abs(rpc.time)>10 and not (cmbok and abs(cmb.time)<10):
                return True
        else:
            if cmbok and (cmb.time>20 or cmb.time<-45):
                return True
        
        return False


    def process(self, event):
        self.readCollections(event.input)
        self.counters.counter('HNL').inc('all events')

        #####################################################################################
        # primary vertex
        #####################################################################################
        if not len(event.goodVertices):
            return False

        self.counters.counter('HNL').inc('>0 good vtx')

        #####################################################################################
        # produce collections and map our objects to convenient Heppy objects
        #####################################################################################

        # make muon collections
        event.muons       = map(Muon, self.handles['muons'].product())
#        event.dsamuons    = self.buildDisplacedMuons(self.handles['dsamuons'].product())
#        event.dgmuons     = self.buildDisplacedMuons(self.handles['dgmuons' ].product())

        for imu in event.muons   : imu.type = 13
#        for imu in event.dsamuons: imu.type = 26
#        for imu in event.dgmuons : imu.type = 39

        # save a flag to know whether the muons is likely OOT
        # FIXME! for displaced too?
        for imu in event.muons:
            imu.isoot = self.isOotMuon(imu)

        event.electrons   = map(Electron, self.handles['electrons'].product())
        
        # prepare the electrons for ID mangling
        for ele in event.electrons:
            ele.event = event.input.object() # RM: this is needed god knows why to get the eleID
            ele.rho = event.rho

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
        jets = map(Jet, self.handles['jets'].product())        

        # make PF candidates
#        try:
        pfs = map(PhysicsObject, self.handles['pfcand'].product())
#            set_trace()
#            return False
#        except: set_trace()

        # assign to the leptons the primary vertex, will be needed to compute a few quantities
        pv = event.goodVertices[0]
        
        self.assignVtx(event.muons    , pv)
        self.assignVtx(event.electrons, pv)

        #####################################################################################
        # Preselect the prompt leptons
        #####################################################################################
        
        prompt_mu_cands  = sorted([mu  for mu  in event.muons     if self.preselectPromptMuons    (mu) ], key = lambda x : x.pt(), reverse = True)
        prompt_ele_cands = sorted([ele for ele in event.electrons if self.preselectPromptElectrons(ele)], key = lambda x : x.pt(), reverse = True)

        if   self.cfg_ana.promptLepton=='mu':
            prompt_leps = prompt_mu_cands       
        elif self.cfg_ana.promptLepton=='ele':
            prompt_leps = prompt_ele_cands
        else:
            print 'ERROR: HNLAnalyzer not supported lepton flavour', self.cfg_ana.promptLepton
            exit(0) 

        if not len(prompt_leps):
            return False

        self.counters.counter('HNL').inc('>0 prompt lep')

        #####################################################################################
        # HLT matching
        #####################################################################################
        
        # match only if the trigger fired and if it is among those we care about
        fired_triggers = [info for info in getattr(event, 'trigger_infos', []) if info.fired and '_'.join(info.name.split('_')[:-1]) in self.cfg_ana.triggersAndFilters.keys()]
    
        drmax=0.15
        
        # loop over the selected prompt leptons
        for ilep in prompt_leps:
        
            # prepare the HLT obj container, empty
            ilep.matched_hlt_obj = []
            
            # loop over the final HLT objects of each path
            for info in fired_triggers:
            
                # get the HLT name w/o version
                hltname     = '_'.join(info.name.split('_')[:-1])          
                # get the filter name you want to match the offline lepton to
                lastfilter  = self.cfg_ana.triggersAndFilters[hltname]
                # get the corresponding HLT objects
                lastobjects = [iobj for iobj in info.objects if lastfilter in [ilab for ilab in iobj.filterLabels()]]
                # match HLT objects and leptons
                matchedobjs = [iobj for iobj in lastobjects if deltaR(iobj, ilep)<drmax]
                # extend the list of matched objects
                ilep.matched_hlt_obj.extend(matchedobjs)
            
            # remove duplicates through 'set'
            ilep.matched_hlt_obj = [iobj for iobj in set(ilep.matched_hlt_obj)]
        
        # now filter out non matched leptons
        prompt_leps = [ilep for ilep in prompt_leps if len(ilep.matched_hlt_obj)>0]
        
        if len(prompt_leps)==0:
            return False
        
        self.counters.counter('HNL').inc('>0 trig match prompt lep')
        
        #####################################################################################
        # Select the prompt lepton candidate and remove it from the collection of leptons
        #####################################################################################

        # the collection is already sorted by pt, just take the first
        prompt_lep = prompt_leps[0]

        # remove the prompt lepton from the corresponding lepton collection that will be later used to find the displaced di-lepton
        event.filtered_muons     = [mu  for mu  in event.muons     if mu.physObj  != prompt_lep.physObj]
        event.filtered_electrons = [ele for ele in event.electrons if ele.physObj != prompt_lep.physObj]
         
        ########################################################################################
        # Preselection for the reco muons before pairing them
        ########################################################################################
        # some simple preselection
        event.muons    = [imu for imu in event.filtered_muons if imu.pt()>3. and abs(imu.eta())<2.4]
#        event.dsamuons = [imu for imu in event.dsamuons       if imu.pt()>3. and abs(imu.eta())>2.4]
#        event.dgmuons  = [imu for imu in event.dgmuons        if imu.pt()>3. and abs(imu.eta())>2.4]

        # create all the possible di-muon pairs out of the three different collections
        
        # FIXME! configure which collections to use
        # dimuons = combinations(event.muons + event.dsamuons + event.dgmuons, 2)
        dimuons = combinations(event.muons, 2)
        
        dimuons = [(mu1, mu2) for mu1, mu2 in dimuons if deltaR(mu1, mu2)>0.01]
        
        if not len(dimuons):
            return False
        self.counters.counter('HNL').inc('> 0 di-muon')

        ########################################################################################
        # Vertex Fit: Select only dimuon pairs with mutual vertices
        ########################################################################################
        dimuonsvtx = []
        for index, pair in enumerate(dimuons):
            if pair[0]==pair[1]: continue
            sv = fitVertex(pair)
            if not sv: continue
            dimuonsvtx.append(DiLepton(pair, sv, pv, event.beamspot))

        event.dimuonsvtx = dimuonsvtx
        
        if not len(event.dimuonsvtx):
            return False 
        
        self.counters.counter('HNL').inc('> 0 di-muon + vtx')

        ########################################################################################
        # candidate choice by different criteria
        ########################################################################################
        
        which_candidate = getattr(self.cfg_ana, 'candidate_selection', 'maxpt')
        
        if which_candidate == 'minmass'    : event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(),  x.mass()                        ), reverse=False)[0]
        if which_candidate == 'minchi2'    : event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(),  x.chi2()                        ), reverse=False)[0]
        if which_candidate == 'mindr'      : event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(),  x.dr()                          ), reverse=False)[0]
        if which_candidate == 'maxdphi'    : event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.dphi()                        ), reverse=False)[0]
        if which_candidate == 'mindeta'    : event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(),  x.deta()                        ), reverse=False)[0]
        if which_candidate == 'maxdisp2dbs': event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp2DFromBS()                ), reverse=False)[0]
        if which_candidate == 'maxdisp2dpv': event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp2DFromPV()                ), reverse=False)[0]
        if which_candidate == 'maxdisp3dpv': event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp3DFromPV()                ), reverse=False)[0]
        if which_candidate == 'maxdls2dbs' : event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp2DFromBSSignificance()    ), reverse=False)[0]
        if which_candidate == 'maxdls2dpv' : event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp2DFromPVSignificance()    ), reverse=False)[0]
        if which_candidate == 'maxdls3dpv' : event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.disp3DFromPVSignificance()    ), reverse=False)[0]
        if which_candidate == 'maxcos'     : event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.cosTransversePointingAngleBS()), reverse=False)[0]
        if which_candidate == 'maxpt'      : event.displaced_dilepton_reco_cand = None if not len(dimuonsvtx) else sorted(dimuonsvtx, key = lambda x : (x.isSS(), -x.pt()                          ), reverse=False)[0]

        ########################################################################################
        # Create a reco HNL3L object
        ########################################################################################
        event.the_3lep_cand = HN3L(prompt_lep, 
                                   event.displaced_dilepton_reco_cand.lep1(), 
                                   event.displaced_dilepton_reco_cand.lep2(), 
                                   event.pfmet)
        
        # save reco secondary vertex
        event.recoSv = event.displaced_dilepton_reco_cand.vtx()

        event.recoSv.disp3DFromBS      = ROOT.VertexDistance3D().distance(event.recoSv, pv)
        event.recoSv.disp3DFromBS_sig  = event.recoSv.disp3DFromBS.significance()
        
        # create an 'ideal' vertex out of the BS
        point = ROOT.reco.Vertex.Point(
            event.beamspot.position().x(),
            event.beamspot.position().y(),
            event.beamspot.position().z(),
        )
        error = event.beamspot.covariance3D()
        chi2 = 0.
        ndof = 0.
        bsvtx = ROOT.reco.Vertex(point, error, chi2, ndof, 2) # size? say 3? does it matter?
                                        
        event.recoSv.disp2DFromBS      = ROOT.VertexDistanceXY().distance(event.recoSv, bsvtx)
        event.recoSv.disp2DFromBS_sig  = event.recoSv.disp2DFromBS.significance()
        event.recoSv.prob              = ROOT.TMath.Prob(event.recoSv.chi2(), int(event.recoSv.ndof()))
        
        dilep_p4 = event.displaced_dilepton_reco_cand.lep1().p4() + event.displaced_dilepton_reco_cand.lep2().p4()

        perp = ROOT.math.XYZVector(dilep_p4.px(),
                                   dilep_p4.py(),
                                   0.)
        
        dxybs = ROOT.GlobalPoint(-1*((event.beamspot.x0() - event.recoSv.x()) + (event.recoSv.z() - event.beamspot.z0()) * event.beamspot.dxdz()), 
                                 -1*((event.beamspot.y0() - event.recoSv.y()) + (event.recoSv.z() - event.beamspot.z0()) * event.beamspot.dydz()),
                                  0)
        
        vperp = ROOT.math.XYZVector(dxybs.x(), dxybs.y(), 0.)
        
        cos = vperp.Dot(perp)/(vperp.R()*perp.R())
        
        event.recoSv.disp2DFromBS_cos = cos

        ########################################################################################
        # Define event.selectedLeptons, will be used by JetAnalyzer.py
        ########################################################################################

        # the selected 3 leptons must be leptons and not jets
        event.selectedLeptons = [event.the_3lep_cand.l0(),
                                 event.the_3lep_cand.l1(),
                                 event.the_3lep_cand.l2()]

        # plus any isolated electron or muon is also a good lepton rather than a jet
        event.selMuons     = [mu  for mu  in event.muons     if self.preselectPromptMuons    (mu , pt=10) and mu .relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0)<0.15]
        event.selElectrons = [ele for ele in event.electrons if self.preselectPromptElectrons(ele, pt=10) and ele.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0)<0.15]
        # RM: what about taus?

        event.selectedLeptons += event.selMuons
        event.selectedLeptons += event.selElectrons

        ########################################################################################
        # Extra prompt and isolated lepton veto
        ########################################################################################        
        event.veto_eles = [ele for ele in event.selMuons     if ele.physObj not in [event.the_3lep_cand.l0().physObj, event.the_3lep_cand.l1().physObj, event.the_3lep_cand.l2().physObj] ]
        event.veto_mus  = [mu  for mu  in event.selElectrons if mu .physObj not in [event.the_3lep_cand.l0().physObj, event.the_3lep_cand.l1().physObj, event.the_3lep_cand.l2().physObj] ]

        ########################################################################################
        # charged PF isolation
        ########################################################################################        
        chargedpfs = [ipf for ipf in pfs if ipf.charge()!=0 and abs(ipf.pdgId())!=11 and abs(ipf.pdgId())!=13]
        chargedpfs = [ipf for ipf in chargedpfs if ipf.pt()>0.6 and abs(ipf.eta())<2.5]
        chargedpfs = [ipf for ipf in chargedpfs if abs(ipf.dxy(event.recoSv.position()))<0.1 and abs(ipf.dz(event.recoSv.position()))<0.5]

        chisopfs = [ipf for ipf in chargedpfs if deltaR(ipf, event.the_3lep_cand.hnP4())<0.5]

        event.the_3lep_cand.abs_ch_iso = sum([ipf.pt() for ipf in chisopfs])
        event.the_3lep_cand.rel_ch_iso = event.the_3lep_cand.abs_ch_iso/event.the_3lep_cand.hnP4().pt()

        return True
        
        
    
