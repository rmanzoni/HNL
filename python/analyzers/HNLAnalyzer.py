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

from CMGTools.HNL.physicsobjects.DiMuon import DiMuon
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
        # FIXME! understand exactly to which extent it is reasonable to assign the PV to *all* leptons
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
        # event.maxptsMu=sorted(event.sMu,key=lambda x: x.pt(),reverse = True)[0] 

        event.n_dSAMu = len(event.dSAMu)
        # event.maxptdSAMu=sorted(event.dSAMu,key=lambda x: x.pt(),reverse=True)[0]
        
        ##############
        # for now ONLY work with sMu
        ##############

        # select only events with >= 3 muons
        if event.n_sMu < 3:
            return False

        self.counters.counter('HNL').inc('>= 3 muons')
       
        # select only events with OS muon pairs and collect the pairs
        event.os_pairs = [pair for pair in combinations(event.sMu,2) if pair[0].charge() != pair[1].charge()] 

        if not len(event.os_pairs):
            return False

        self.counters.counter('HNL').inc('os_pairs')

        # only selecting dimuon pairs with mutual vertices (surviving the kinematic vertex fitter) 
        dimuon = []
        for pair in event.os_pairs:
            self.tofit.clear()
            for il in pair:
                myp4 = ROOT.Math.LorentzVector('<ROOT::Math::PxPyPzE4D<double> >')(il.px(), il.py(), il.pz(), sqrt(il.mass()**2 + il.px()**2 + il.py()**2 + il.pz()**2))
                ic = ROOT.reco.RecoChargedCandidate() # instantiate a dummy RecoChargedCandidate
                ic.setCharge(il.charge())           # assign the correct charge
                ic.setP4(myp4)                      # assign the correct p4
                ic.setTrack(il.track())             # set the correct TrackRef
                if ic.track().isNonnull():          # check that the track is valid, there are photons around too!
                    self.tofit.push_back(ic)
            # further sanity check: two *distinct* tracks
            if self.tofit.size() == 2 and self.tofit[0].track() != self.tofit[1].track:
                svtree = self.vtxfit.Fit(self.tofit) # the actual vertex fitting!
                if not svtree.get().isEmpty() and svtree.get().isValid(): # check that the vertex is good
                    svtree.movePointerToTheTop()
                    sv = svtree.currentDecayVertex().get()
                    # if sv.event.recoSv.Chi2() 
                    # event.recoSv = makeRecoVertex(sv, kinVtxTrkSize=2)
                    dimuon.append(DiMuon(pair, makeRecoVertex(sv, kinVtxTrkSize=2)))

        if not len(dimuon):
            return False
        
        self.counters.counter('HNL').inc('dimuons')
        
        # # only selecting those pairs with a vertex fit chi2 < 1. 
        # for dm in dimuon:
            # if dm.vtx.chi2() > 1.: 
                # dimuon.remove(dm)
        
        event.n_dimuon = len(dimuon)
         
        # select the dimuon with lowest vertex fit chi2 as the HNL dimuon candidate
        hnldimuon = sorted(dimuon, key = lambda x: x.chi2(), reverse = False)[0] 


        # TODO: Gather all relevant observables of the hnldimuon
        event.hnldimuon_displacement2D = hnldimuon.displacement2D()


        return True

        # event.maxptsMu=sorted(event.sMu,key=lambda x: x.pt(),reverse = True)[0] 
        # event.muons = self.handles ['muons'].product()
        # event.positivemuons = [mu for mu in event.muons if mu.charge()==1]
        # event.run = event.input.eventAuxiliary().run() 
        # event.lumi = event.input.eventAuxiliary().luminosityBlock() 
