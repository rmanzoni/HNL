'''
This is the main analyzer going through data and trying to identify HNL->3L events.
'''

import ROOT
from itertools import product, combinations
from math import sqrt, pow

from PhysicsTools.Heppy.analyzers.core.Analyzer      import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle    import AutoHandle
from PhysicsTools.Heppy.physicsobjects.GenParticle   import GenParticle
from PhysicsTools.Heppy.physicsobjects.Muon          import Muon
from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from CMGTools.HNL.utils.utils                     import isAncestor, displacement2D, displacement3D, makeRecoVertex, fitVertex
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi

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

        self.handles['sMu']      = AutoHandle(('slimmedMuons','','PAT'),'std::vector<pat::Muon>')
        self.handles['dSAMu']    = AutoHandle(('displacedStandAloneMuons','','RECO'),'std::vector<reco::Track>')
        self.handles['dGMu']     = AutoHandle(('displacedGlobalMuons','','RECO'),'std::vector<reco::Track>')
        self.handles['pvs']      = AutoHandle(('offlineSlimmedPrimaryVertices','','PAT'),'std::vector<reco::Vertex>')
        self.handles['svs']      = AutoHandle(('slimmedSecondaryVertices','','PAT'),'std::vector<reco::VertexCompositePtrCandidate>')
        self.handles['beamspot'] = AutoHandle(('offlineBeamSpot','','RECO'),'reco::BeamSpot')
        self.handles['met']      = AutoHandle(('slimmedMETs','','PAT'),'std::vector<pat::MET>')

    def assignVtx(self, particles, vtx):    
        for ip in particles:
            ip.associatedVertex = vtx

    def beginLoop(self, setup):
        super(HNLAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('HNL')
        count = self.counters.counter('HNL')
        count.register('all events')
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

        event.sMu         = map(Muon,self.handles['sMu'].product())
        event.dSAMu       = self.buildDisplacedMuons(self.handles['dSAMu'].product())
        event.dGMu        = self.buildDisplacedMuons(self.handles['dGMu' ].product())

        # make vertex objects 
        event.pvs         = self.handles['pvs'     ].product()
        event.svs         = self.handles['svs'     ].product()
        event.beamspot    = self.handles['beamspot'].product()

        # make met object
        event.met         = self.handles['met'].product().at(0)

        # assign to the leptons the primary vertex, will be needed to compute a few quantities
        if len(event.pvs):
            myvtx = event.pvs[0]
        else:
            myvtx = event.beamspot
        
        self.assignVtx(event.sMu,myvtx)

        # store the number of sMu and dSAMu per event
        event.n_sMu   = len(event.sMu)
        event.n_dSAMu = len(event.dSAMu)
        event.n_dGMu  = len(event.dGMu)
       
        #####################################################################################
        # MUCO, the MUon COncatenator
        # Concatenate all Muon Reconstructions:
        # Create an array of DisplacedMuon objects, 
        # summarizing all sMu and dSAMus into a single array, 
        # avoid redundancies with dR < dr_cut
        #####################################################################################
        # Merge Reco Muons
        # Create an array of DisplacedMuon objects, summarizing all sMu and dSAMus into a single array, while avoiding redundancies through dR < dr_cut
        dr_cut = 0.1
        dMus = []
        event.n_sMuOnly = 0
        event.n_dSAMuOnly = 0
        event.n_dGMuOnly = 0
        event.n_sMuRedundant = 0
        event.n_dSAMuRedundant = 0

        # for smu in event.sMu:
            # matches = []
            # # matches = [dsa for dsa in event.dSAMu if (deltaR(smu,dsa) < dr_cut)] #this is commented out to turn off the MUCO 
            # if len(matches) == 0:
                # dmu = smu
                # dmu.reco = 1 # sMu = 1, dSAMu = 2
                # dmu.redundancy = 0
                # dMus.append(dmu)
                # event.n_sMuOnly += 1
            # else:
                # bestmatch = sorted(matches, key = lambda dsa: deltaR(smu,dsa), reverse = False)[0] 
                # # if smu.dxy() < dxy_cut:
                # if hasattr(smu.globalTrack(),'p'):
                    # dmu = smu
                    # dmu.reco = 1 # sMu = 1, dSAMu = 2 
                    # dmu.redundancy = len(matches)
                    # dMus.append(dmu)
                    # event.n_sMuRedundant += 1
                # else:
                    # dmu = bestmatch
                    # dmu.reco = 2 # sMu = 1, dSAMu = 2
                    # dmu.redundancy = len(matches)
                    # dMus.append(dmu)
                    # event.n_dSAMuRedundant += 1

                # event.dSAMu.remove(bestmatch)    

        for smu in event.sMu:
            dmu = smu
            dmu.reco = 1 # sMu = 1, dSAMu = 2
            dmu.redundancy = 0 
            dMus.append(dmu)
            event.n_sMuOnly += 1

        # for dsa in event.dSAMu:
            # dmu = dsa
            # dmu.reco = 2 # sMu = 1, dSAMu = 2
            # dmu.redundancy = 0 
            # dMus.append(dmu)
            # event.n_dSAMuOnly += 1

        # for dg in event.dGMu:
            # dmu = dg
            # dmu.reco = 3 # sMu = 1, dSAMu = 2, dGMu = 3
            # dmu.redundancy = 0
            # dMus.append(dmu)
            # event.n_dGMuOnly += 1

       
        event.n_dMu = len(dMus) # important to understand how well the "Merge Reco Muons" process went. 
       
        #####################################################################################
        # Qualify the performance of the MUCO
        #####################################################################################
        event.flag_MUCOsuccess = False    
        l1matched=False
        l2matched=False
        if len(dMus) > 1 and hasattr(event.the_hnl.l1().bestmatch, 'physObj') and hasattr(event.the_hnl.l2().bestmatch,'physObj'):
            for dmu in dMus:
                if dmu.physObj == event.the_hnl.l1().bestmatch.physObj:
                    l1matched = True
                if dmu.physObj == event.the_hnl.l2().bestmatch.physObj:
                    l2matched = True
        if l1matched and l2matched:
            event.flag_MUCOsuccess = True


        #####################################################################################
        # select only events with good gen events
        #####################################################################################
        if not( abs(event.the_hnl.l1().pdgId())==13   and \
                abs(event.the_hnl.l2().pdgId())==13   and \
                abs(event.the_hnl.l1().eta())   < 2.4 and \
                abs(event.the_hnl.l2().eta())   < 2.4 and \
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
        event.sMu   = [imu for imu in event.sMu   if imu.pt()>3.]
        event.dSAMu = [imu for imu in event.dSAMu if imu.pt()>3.]
        event.dGMu  = [imu for imu in event.dGMu  if imu.pt()>3.]


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
                    dimuons.append(DiLepton(pair,sv,myvtx,event.beamspot))

        #####################################################################################
        # Check whether the correct dimuon is part of the collection dimuons
        #####################################################################################
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
            dimuonDxy = sorted(dimuons, key = lambda x: (x.isSS(),x.disp2DFromBS()), reverse = True)[0] 
            event.dimuonDxy = dimuonDxy
            event.dMu1Dxy = dimuonDxy.lep1()
            event.dMu2Dxy = dimuonDxy.lep2()

            # select leptons ito added momenta's pt
            dimuonMaxPt = sorted(dimuons, key = lambda x: (x.isSS(),x.pt()), reverse = True)[0] 
            event.dimuonMaxPt = dimuonMaxPt
            event.dMu1MaxPt = dimuonMaxPt.lep1()
            event.dMu2MaxPt = dimuonMaxPt.lep2()

            # select closest leptons ito dr
            dimuonMinDr12 = sorted(dimuons, key = lambda x: (x.isSS(),x.dr()), reverse = False)[0]
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



        return True
