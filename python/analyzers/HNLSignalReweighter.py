'''
Analyses a HNL -> 3L signal event, compute weights
'''

import ROOT
from itertools import product, combinations
from collections import OrderedDict
import numpy as np

from PhysicsTools.Heppy.analyzers.core.Analyzer      import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle    import AutoHandle
from PhysicsTools.Heppy.physicsobjects.GenParticle   import GenParticle
from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from PhysicsTools.HeppyCore.utils.deltar             import deltaR, deltaR2

from CMGTools.HNL.utils.utils         import isAncestor, displacement2D, displacement3D, makeRecoVertex # utility functions
from CMGTools.HNL.physicsobjects.HN3L import HN3L

from pdb import set_trace

global new_v2s

# couplings to compute weights for
new_v2s = [
    1e-10, 
    5e-10, 
    1e-9, 
    5e-9, 
    1e-8, 
    5e-8, 
    1e-7, 
    5e-7, 
    1e-6, 
    5e-6, 
    6e-06, 
    8e-06, 
    1e-5, 
    2e-5, 
    3e-5, 
    4e-5, 
    5e-5, 
    7e-05, 
    0.0001, 
    0.0002, 
    0.00025, 
    0.0003, 
    0.0005, 
    0.0012,
]



class HNLSignalReweighter(Analyzer):
    '''
    '''




    def declareHandles(self):
        super(HNLSignalReweighter, self).declareHandles()
        self.mchandles['genp_pruned'] = AutoHandle(('prunedGenParticles', '', 'PAT' ), 'std::vector<reco::GenParticle>'     )
        self.mchandles['lhe'        ] = AutoHandle('externalLHEProducer'             , 'LHEEventProduct'                    )

    def beginLoop(self, setup):
        super(HNLSignalReweighter, self).beginLoop(setup)
        self.counters.addCounter('HNLSigRew')
        count = self.counters.counter('HNLSigRew')
        count.register('all events')

    def weight_to_new_ctau(self, old_ctau, old_v2, new_v2, ct):
        '''
        Returns an event weight based on the ratio of the normalised lifetime distributions.
        old_ctau: reference ctau
        old_v2  : reference coupling squared
        new_v2  : target coupling squared
        ct      : heavy neutrino lifetime in the specific event
        '''
        new_ctau = old_ctau * old_v2 / new_v2
        weight = old_ctau/new_ctau * np.exp( (1./old_ctau - 1./new_ctau) * ct )
        return weight, new_ctau
        
    def process(self, event):
        '''
        FIXME! save W pt for NLO reweighing
        '''
        self.readCollections(event.input)
        
        self.counters.counter('HNLSigRew').inc('all events')

        # no point to run this if it's not a HNL signal
        if 'HN3L' not in self.cfg_comp.name:
            return True

        # produce collections
        event.genp_pruned = self.mchandles['genp_pruned'].product()
        event.lhe         = self.mchandles['lhe'].product()

        hepup = event.lhe.hepeup()
    
        # for each particle at LHE level, its lifetime is saved. If the particle decays immediately, it is set to 0.
        # http://home.thep.lu.se/~torbjorn/talks/fnal04lha.pdf
        ctaus = [hepup.VTIMUP.at(ictau) for ictau in xrange(hepup.VTIMUP.size()) if hepup.VTIMUP.at(ictau)>0.]
    
        # there should be only one particle at LHE level with lifetime > 0, that is the HNL
        event.hnl_ct_lhe = ctaus[0]

        ctau_weights = OrderedDict()
        
        for iv2 in new_v2s:
            mysample = self.cfg_comp
            ctau_weights[iv2] = OrderedDict()
            ctau_weights[iv2]['new_ctau'   ] = self.weight_to_new_ctau(mysample.ctau, mysample.v2, iv2, event.hnl_ct_lhe)[1]
            ctau_weights[iv2]['ctau_weight'] = self.weight_to_new_ctau(mysample.ctau, mysample.v2, iv2, event.hnl_ct_lhe)[0]
            ctau_weights[iv2]['xs_weight'  ] = iv2 / mysample.v2
        
        event.ctau_weights = ctau_weights
        
        return True
    
