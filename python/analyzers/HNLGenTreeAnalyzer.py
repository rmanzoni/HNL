'''
Analyses a HNL -> 3L signal event, identifying the prompt and displaced leptons.
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
from PhysicsTools.Heppy.physicsobjects.GenParticle   import GenParticle
from PhysicsTools.Heppy.physicsobjects.Photon        import Photon
from PhysicsTools.Heppy.physicsobjects.Tau           import Tau
from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from PhysicsTools.HeppyCore.utils.deltar             import deltaR, deltaR2

from CMGTools.HNL.utils.utils         import isAncestor, displacement2D, displacement3D, makeRecoVertex # utility functions
from CMGTools.HNL.physicsobjects.HN3L import HN3L

from pdb import set_trace

class HNLGenTreeAnalyzer(Analyzer):
    '''
    '''

    def declareHandles(self):
        super(HNLGenTreeAnalyzer, self).declareHandles()

        self.handles  ['muons'      ] = AutoHandle(('slimmedMuons'                 , '', 'PAT' ), 'std::vector<pat::Muon>'                        )
        self.handles  ['electrons'  ] = AutoHandle(('slimmedElectrons'             , '', 'PAT' ), 'std::vector<pat::Electron>'                    )
        self.handles  ['photons'    ] = AutoHandle(('slimmedPhotons'               , '', 'PAT' ), 'std::vector<pat::Photon>'                      )
        self.handles  ['taus'       ] = AutoHandle(('slimmedTaus'                  , '', 'PAT' ), 'std::vector<pat::Tau>'                         )
        self.handles  ['jets'       ] = AutoHandle(('slimmedJets'                  , '', 'PAT' ), 'std::vector<pat::Jet>'                         )
        self.handles  ['pvs'        ] = AutoHandle(('offlineSlimmedPrimaryVertices', '', 'PAT' ), 'std::vector<reco::Vertex>'                     )
        self.handles  ['svs'        ] = AutoHandle(('slimmedSecondaryVertices'     , '', 'PAT' ), 'std::vector<reco::VertexCompositePtrCandidate>')
        self.handles  ['dsmuons'    ] = AutoHandle(('displacedStandAloneMuons'     , '', 'RECO'), 'std::vector<reco::Track>'                      )
        self.handles  ['dgmuons'    ] = AutoHandle(('displacedGlobalMuons'         , '', 'RECO'), 'std::vector<reco::Track>'                      )
        self.handles  ['beamspot'   ] = AutoHandle(('offlineBeamSpot'              , '', 'RECO'), 'reco::BeamSpot'                                )
        self.mchandles['genp_pruned'] = AutoHandle(('prunedGenParticles'           , '', 'PAT' ), 'std::vector<reco::GenParticle>'                )
        self.mchandles['genp_packed'] = AutoHandle(('packedGenParticles'           , '', 'PAT' ), 'std::vector<pat::PackedGenParticle>'           )

    def beginLoop(self, setup):
        super(HNLGenTreeAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('HNLGenTree')
        count = self.counters.counter('HNLGenTree')
        count.register('all events')
        
    def process(self, event):
        self.readCollections(event.input)

        self.counters.counter('HNLGenTree').inc('all events')

        # produce collections
        event.muons       = self.handles  ['muons'      ].product()
        event.electrons   = self.handles  ['electrons'  ].product()
        event.photons     = self.handles  ['photons'    ].product()
        event.taus        = self.handles  ['taus'       ].product()
        event.jets        = self.handles  ['jets'       ].product()
        event.pvs         = self.handles  ['pvs'        ].product()
        event.svs         = self.handles  ['svs'        ].product()
        event.dsmuons     = self.handles  ['dsmuons'    ].product()
        event.dgmuons     = self.handles  ['dgmuons'    ].product()
        event.beamspot    = self.handles  ['beamspot'   ].product()
        event.genp_pruned = self.mchandles['genp_pruned'].product()
        event.genp_packed = self.mchandles['genp_packed'].product()

        # all gen particles
        event.genp = [ip for ip in event.genp_pruned] + [ip for ip in event.genp_packed]

        # get the heavy neutrino
        the_hns = [ip for ip in event.genp_pruned if abs(ip.pdgId())==9900012 and ip.isLastCopy()]
        event.the_hn = the_hns[0] # one per event

        # prompt lepton
        event.the_pl = map(GenParticle, [ip for ip in event.genp_pruned if abs(ip.pdgId()) in [11,13] and ip.isPromptFinalState() and not isAncestor(event.the_hn, ip)])[0]      

        # get the immediate daughters of the heavy neutrino decay
        event.the_hn.initialdaus = [event.the_hn.daughter(jj) for jj in range(event.the_hn.numberOfDaughters())]

        event.the_hn.lep1 = max([ii for ii in event.the_hn.initialdaus if abs(ii.pdgId()) in [11, 13]], key = lambda x : x.pt())
        event.the_hn.lep2 = min([ii for ii in event.the_hn.initialdaus if abs(ii.pdgId()) in [11, 13]], key = lambda x : x.pt())
        event.the_hn.neu  =     [ii for ii in event.the_hn.initialdaus if abs(ii.pdgId()) in [12, 14]][0] # there can be only one

        # identify the secondary vertex
        event.the_hn.the_sv = event.the_hn.lep1.vertex()
    
        # need to analyse the lepton after they radiated / converted
        for ip in [event.the_hn.lep1, event.the_hn.lep2, event.the_pl]:
            finaldaus  = []
            for ipp in event.genp_packed:
                mother = ipp.mother(0)
                if mother and isAncestor(ip, mother):
                    finaldaus.append(ipp)
            ip.finaldaughters = sorted(finaldaus , key = lambda x : x.pt(), reverse = True)
            ip.hasConvOrRad = (len(ip.finaldaughters)>1)
            if len(ip.finaldaughters)>1:
                try:
                    ip.finallep = max([ii for ii in ip.finaldaughters if ii.pdgId()==ip.pdgId()], key = lambda x : x.pt())
                except:
                    ip.finallep = max([ii for ii in ip.finaldaughters if abs(ii.pdgId()) in [11, 13]], key = lambda x : x.pt())                
            else:
                ip.finallep = ip

        # 4-momentum of the visible part of the HN
        event.the_hn.vishn = event.the_hn.lep1.finallep.p4() + event.the_hn.lep2.finallep.p4()

        # make it into a handy class
        # import pdb ; pdb.set_trace()
        event.the_hnl = HN3L(event.the_pl.finallep, event.the_hn.lep1.finallep, event.the_hn.lep2.finallep, event.the_hn.neu)
        # import pdb ; pdb.set_trace()

        return True
    