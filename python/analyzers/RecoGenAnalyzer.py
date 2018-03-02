'''
Matching bewteen gen and reco quantities.
'''

import ROOT
from itertools import product, combinations
import math

from PhysicsTools.Heppy.analyzers.core.Analyzer      import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle    import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon          import Muon
from PhysicsTools.Heppy.physicsobjects.Electron      import Electron
from PhysicsTools.Heppy.physicsobjects.Tau           import Tau
from PhysicsTools.Heppy.physicsobjects.Photon        import Photon
from PhysicsTools.Heppy.physicsobjects.Tau           import Tau
from PhysicsTools.Heppy.physicsobjects.Jet           import Jet
from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from PhysicsTools.HeppyCore.utils.deltar             import deltaR, deltaPhi, inConeCollection, bestMatch

from CMGTools.HNL.utils.utils         import isAncestor, displacement2D, displacement3D, makeRecoVertex # utility functions
from CMGTools.HNL.physicsobjects.HN3L import HN3L

from pdb import set_trace

##########################################################################################
# load custom library to ROOT. This contains the kinematic vertex fitter class
ROOT.gSystem.Load('libCMGToolsHNL')
from ROOT import HNLKinematicVertexFitter as VertexFitter

class RecoGenAnalyzer(Analyzer):
    '''
    '''
    def declareHandles(self):
        super(RecoGenAnalyzer, self).declareHandles()

        self.handles  ['muons'      ] = AutoHandle(('slimmedMuons'                 , '', 'PAT' ), 'std::vector<pat::Muon>'                        )
        self.handles  ['electrons'  ] = AutoHandle(('slimmedElectrons'             , '', 'PAT' ), 'std::vector<pat::Electron>'                    )
        self.handles  ['photons'    ] = AutoHandle(('slimmedPhotons'               , '', 'PAT' ), 'std::vector<pat::Photon>'                      )
        self.handles  ['taus'       ] = AutoHandle(('slimmedTaus'                  , '', 'PAT' ), 'std::vector<pat::Tau>'                         )
        self.handles  ['jets'       ] = AutoHandle(('slimmedJets'                  , '', 'PAT' ), 'std::vector<pat::Jet>'                         )
        self.handles  ['dsmuons'    ] = AutoHandle(('displacedStandAloneMuons'     , '', 'RECO'), 'std::vector<reco::Track>'                      )
        self.handles  ['dgmuons'    ] = AutoHandle(('displacedGlobalMuons'         , '', 'RECO'), 'std::vector<reco::Track>'                      )
        self.handles  ['pvs'        ] = AutoHandle(('offlineSlimmedPrimaryVertices', '', 'PAT' ), 'std::vector<reco::Vertex>'                     )
        self.handles  ['svs'        ] = AutoHandle(('slimmedSecondaryVertices'     , '', 'PAT' ), 'std::vector<reco::VertexCompositePtrCandidate>')
        self.handles  ['beamspot'   ] = AutoHandle(('offlineBeamSpot'              , '', 'RECO'), 'reco::BeamSpot'                                )
        self.handles  ['met'        ] = AutoHandle(('slimmedMETs'                  , '', 'PAT' ), 'std::vector<pat::MET>'                         )

    def beginLoop(self, setup):
        super(RecoGenAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('RecoGenTreeAnalyzer')
        count = self.counters.counter('RecoGenTreeAnalyzer')
        count.register('all events')
 
        # stuff I need to instantiate only once
        self.vtxfit = VertexFitter()
        # create a std::vector<RecoChargedCandidate> to be passed to the fitter 
        self.tofit = ROOT.std.vector('reco::RecoChargedCandidate')()
       
    def process(self, event):
        self.readCollections(event.input)

        self.counters.counter('RecoGenTreeAnalyzer').inc('all events')

        # produce collections and map our objects to convenient Heppy objects
        event.muons       = map(Muon         , self.handles  ['muons'      ].product())
        event.electrons   = map(Electron     , self.handles  ['electrons'  ].product())
        event.photons     = map(Photon       , self.handles  ['photons'    ].product())
        event.taus        = map(Tau          , self.handles  ['taus'       ].product())
        event.jets        = map(Jet          , self.handles  ['jets'       ].product())
        event.dsmuons     = map(PhysicsObject, self.handles  ['dsmuons'    ].product())
        event.dgmuons     = map(PhysicsObject, self.handles  ['dgmuons'    ].product())

        # vertex stuff
        event.pvs         = self.handles['pvs'     ].product()
        event.svs         = self.handles['svs'     ].product()
        event.beamspot    = self.handles['beamspot'].product()

        # met
        event.met         = self.handles['met'].product().at(0)
        
        # impose the muon PDG ID to the displaced objects, that otherwise carry none
        for mm in event.dsmuons + event.dgmuons:
            mm.mass   = lambda : 0.10565837
            mm.pdgId  = lambda : -(mm.charge()*13)

        # also append a TrackRef, this will be needed for the refitting 
        for jj, mm in enumerate(event.dsmuons):
            mm.track = lambda : ROOT.reco.TrackRef(self.handles['dsmuons'].product(), jj)

        for jj, mm in enumerate(event.dgmuons):
            mm.track = lambda : ROOT.reco.TrackRef(self.handles['dgmuons'].product(), jj)
    
        # all matchable objects
        matchable = event.electrons + event.photons + event.muons + event.taus + event.dsmuons + event.dgmuons 

        # match gen to reco
        for ip in [event.the_hnl.l0(), 
                   event.the_hnl.l1(), 
                   event.the_hnl.l2()]:
            ip.bestmatch     = None
            ip.bestmatchtype = None
            ip.matches = inConeCollection(ip, matchable, getattr(self.cfg_ana, 'drmax', 0.2), 0.)

            # matches the corresponding "slimmed electron" to the gen particle
            if len(event.electrons):
                match, dr = bestMatch(ip,event.electrons)
                if dr < 0.2: 
                    ip.bestelectron = match

            # matches the corresponding "slimmed photon" to the gen particle
            if len(event.photons):
                match, dr = bestMatch(ip,event.photons)
                if dr < 0.2: 
                    ip.bestphoton = match

            # matches the corresponding "slimmed muon" to the gen particle
            if len(event.muons):
                match, dr = bestMatch(ip,event.muons)
                if dr < 0.2: 
                    ip.bestmuon = match
            
            # matches the corresponding "slimmed tau" to the gen particle
            if len(event.taus):
                match, dr = bestMatch(ip,event.taus)
                if dr < 0.2: 
                    ip.besttau = match
            
            # matches the corresponding "displaced stand alone muon" to the gen particle
            if len(event.dsmuons):
                match, dr = bestMatch(ip,event.dsmuons)
                if dr < 0.2: 
                    ip.bestdsmuon = match
                    
            # matches the corresponding "displaced global muon" to the gen particle
            if len(event.dgmuons):
                match, dr = bestMatch(ip,event.dgmuons)
                if dr < 0.2: 
                    ip.bestdgmuon = match
            
            
            
            
            # to find the best match, give precedence to any matched 
            # piarticle in the matching cone with the correct PDG ID
            # then to the one which is closest
            ip.matches.sort(key = lambda x : (x.pdgId()==ip.pdgId(), -deltaR(x, ip)), reverse = True )
            if len(ip.matches):
                ip.bestmatch = ip.matches[0]
                # remove already matched particles, avoid multiple matches to the same candidate
                matchable.remove(ip.bestmatch)
                # record which is which
                if ip.bestmatch in event.electrons: ip.bestmatchtype = 0
                if ip.bestmatch in event.photons  : ip.bestmatchtype = 1
                if ip.bestmatch in event.muons    : ip.bestmatchtype = 2
                if ip.bestmatch in event.taus     : ip.bestmatchtype = 3
                if ip.bestmatch in event.dsmuons  : ip.bestmatchtype = 4
                if ip.bestmatch in event.dgmuons  : ip.bestmatchtype = 5
    
        # clear it before doing it again
        event.recoSv = None

        # let's refit the secondary vertex, IF both leptons match to some reco particle
        if not(event.the_hnl.l1().bestmatch is None or \
               event.the_hnl.l2().bestmatch is None):
            # clear the vector
            self.tofit.clear()
            # create a RecoChargedCandidate for each reconstructed lepton and flush it into the vector
            for il in [event.the_hnl.l1().bestmatch, 
                       event.the_hnl.l2().bestmatch]:
                # if the reco particle is a displaced thing, it does not have the p4() method, so let's build it 
                myp4 = ROOT.Math.LorentzVector('<ROOT::Math::PxPyPzE4D<double> >')(il.px(), il.py(), il.pz(), math.sqrt(il.mass()**2 + il.px()**2 + il.py()**2 + il.pz()**2))
                ic = ROOT.reco.RecoChargedCandidate() # instantiate a dummy RecoChargedCandidate
                ic.setCharge(il.charge())             # assign the correct charge
                ic.setP4(myp4)                        # assign the correct p4
                ic.setTrack(il.track())               # set the correct TrackRef
                if ic.track().isNonnull():            # check that the track is valid, there are photons around too!
                    self.tofit.push_back(ic)

            # further sanity check: two *distinct* tracks
            if self.tofit.size()==2 and self.tofit[0].track() != self.tofit[1].track():
                # fit it!
                svtree = self.vtxfit.Fit(self.tofit) # actual vertex fitting
                # check that the vertex is good
                if not svtree.get().isEmpty() and svtree.get().isValid():
                    svtree.movePointerToTheTop()
                    sv = svtree.currentDecayVertex().get()
                    event.recoSv = makeRecoVertex(sv, kinVtxTrkSize=2) # need to do some gymastics
        
        return True
    
