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
from CMGTools.HNL.utils.utils                     import isAncestor, displacement2D, displacement3D, makeRecoVertex
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi

from CMGTools.HNL.physicsobjects.DiMuon import DiMuon
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
        count.register('>= 3 muons')
        count.register('os_pairs')
        count.register('dimuons')

        # initiate the VertexFitter
        self.vtxfit = VertexFitter()

        # create a std::vector<RecoChargedCandidate> to be passed to the fitter
        self.tofit = ROOT.std.vector('reco::RecoChargedCandidate')()

    def process(self, event):
        self.readCollections(event.input)
        self.counters.counter('HNL').inc('all events')

        # produce collections and map our objects to convenient Heppy objects
        event.sMu         = map(Muon         , self.handles  ['sMu'        ].product())
        event.dSAMu       = map(PhysicsObject, self.handles  ['dSAMu'      ].product())

        # make vertex objects 
        event.pvs         = self.handles['pvs'     ].product()
        event.svs         = self.handles['svs'     ].product()
        event.beamspot    = self.handles['beamspot'].product()

        # make met object
        event.met         = self.handles['met'].product().at(0)

        # assign to the leptons the primary vertex, will be needed to compute a few quantities
        # TODO! understand exactly to which extent it is reasonable to assign the PV to *all* leptons
        #        regardless whether they're displaced or not
        if len(event.pvs):
            myvtx = event.pvs[0]
        else:
            myvtx = event.beamspot
        
        self.assignVtx(event.sMu,myvtx)
        
        # impose the muon PDG ID and TrackRef to the displaced objects, that otherwise carry none
        for mm in event.dSAMu:
            mm.mass   = lambda : 0.10565837
            mm.pdgId  = lambda : -(mm.charge()*13)
        
        for jj, mm in enumerate(event.dSAMu):
            mm.track = lambda : ROOT.reco.TrackRef(self.handles['dSAMu'].product(),jj)
            
        
        # store the number of sMu and dSAMu per event
        event.n_sMu = len(event.sMu)
        event.n_dSAMu = len(event.dSAMu)
       
        # Merge Reco Muons
        # Create an array of DisplacedMuon objects, summarizing all sMu and dSAMus into a single array, while avoiding redundancies through dR<0.2
        dMus = []
        dxy_cut = 1000 # cut selection for sMu / dSAMu in mm
        event.n_sMuOnly = 0
        event.n_dSAMuOnly = 0
        event.n_sMuRedundant = 0
        event.n_dSAMuRedundant = 0
        for smu in event.sMu:
            matches = [dsa for dsa in event.dSAMu if deltaR(smu,dsa)<0.2] 
            if not len(matches):
                dmu = DisplacedMuon(smu,event.sMu)
                dmu.reco = 'sMu'
                dMus.append(dmu)
                event.n_sMuOnly += 1
            if len(matches) > 0:
                bestmatch = sorted(matches, key = lambda dsa: deltaR(smu,dsa), reverse = True)[0] 
                if smu.dxy() < dxy_cut:
                    dmu = DisplacedMuon(smu,event.sMu)
                    dmu.reco = 'sMu'
                    dMus.append(dmu)
                    event.n_sMuRedundant += 1
                if smu.dxy() > dxy_cut:
                    dmu = DisplacedMuon(dsa,event.dSAMu)
                    dmu.reco = 'dSAMu'
                    dMus.append(dmu)
                    event.n_dSAMuRedundant += 1
                    
        for dsa in event.dSAMu:
            matches = [smu for smu in event.sMu if deltaR(dsa,smu)<0.2]
            if not len(matches):
                dmu = DisplacedMuon(dsa,event.dSAMu)
                dmu.reco = 'dSAMu'
                dMus.append(dmu)
                event.n_dSAMuOnly += 1
       
        event.n_dMu = len(dMus) # important to understand how well the "Merge Reco Muons" process went. 

        # select only events with >= 3 muons
        if event.n_dMu < 3:
            return False

        self.counters.counter('HNL').inc('>= 3 muons')
       
        # select only events with OS muon pairs and collect the pairs
        event.os_pairs = [pair for pair in combinations(dMus,2) if pair[0].charge() != pair[1].charge()] 
        event.n_os_pairs = len(event.os_pairs)

        if not len(event.os_pairs):
            return False

        self.counters.counter('HNL').inc('os_pairs')

        # select only dimuon pairs with mutual vertices (surviving the kinematic vertex fitter)
        # TODO: can the kinematic vertex fitter further summarized into one function?  
        dimuons = []
        for pair in event.os_pairs:
            self.tofit.clear()
            for il in pair:
                # if the reco particle is a displaced thing, it does not have the p4() method, so let's build it 
                myp4 = ROOT.Math.LorentzVector('<ROOT::Math::PxPyPzE4D<double> >')(il.px(), il.py(), il.pz(), sqrt(il.mass()**2 + il.px()**2 + il.py()**2 + il.pz()**2))
                ic = ROOT.reco.RecoChargedCandidate() # instantiate a dummy RecoChargedCandidate
                ic.setCharge(il.charge())           # assign the correct charge
                ic.setP4(myp4)                      # assign the correct p4
                if il.reco == 'sMu':
                    ic.setTrack(il.outerTrack())             # set the correct TrackRef
                if il.reco == 'dSAMu':
                    ic.setTrack(il.GetPhysObj().track())             # set the correct TrackRef
                if ic.track().isNonnull():          # check that the track is valid, there are photons around too!
                    self.tofit.push_back(ic)
            # further sanity check: two *distinct* tracks
            if self.tofit.size() == 2 and self.tofit[0].track() != self.tofit[1].track():
                svtree = self.vtxfit.Fit(self.tofit) # the actual vertex fitting!
                if not svtree.get().isEmpty() and svtree.get().isValid(): # check that the vertex is good
                    svtree.movePointerToTheTop()
                    sv = svtree.currentDecayVertex().get()
                    dimuons.append(DiMuon(pair, makeRecoVertex(sv, kinVtxTrkSize=2)))

        if not len(dimuons):
            return False
        
        self.counters.counter('HNL').inc('dimuons')
        
        event.n_dimuon = len(dimuons)
         
        # select the dimuon with lowest vertex fit chi2 as the HNL dimuon candidate
        dimuonChi2 = sorted(dimuons, key = lambda x: x.chi2(), reverse = False)[0] 
        event.dimuonChi2 = dimuonChi2
        event.dMu1Chi2 = sorted(dimuonChi2.pair, key = lambda x: x.pt(), reverse = False)[0]
        event.dMu2Chi2 = sorted(dimuonChi2.pair, key = lambda x: x.pt(), reverse = True)[0] 
        
        # select the dimuon with largest displacement
        dimuonDxy = sorted(dimuons, key = lambda x: x.displacement2D(), reverse = False)[0] 
        event.dimuonDxy = dimuonDxy
        event.dMu1Dxy = sorted(dimuonDxy.pair, key = lambda x: x.pt(), reverse = False)[0]
        event.dMu2Dxy = sorted(dimuonDxy.pair, key = lambda x: x.pt(), reverse = True)[0] 

        



        return True
