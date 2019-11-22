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
v2s = np.linspace(1,9,9)
order_of_magnitudes = np.linspace(-10,-1,10)

new_v2s = []
for ioom, iv2 in product(order_of_magnitudes, v2s):
    # print 'value', iv2,'\texpo', ioom, '\t\t\t\t',
    new_v2 = iv2 * np.power(10., ioom)
    new_v2s.append(new_v2)
    # print new_v2

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

        # save the gen W
        the_ws = sorted([ip for ip in event.genp_pruned if ip.isLastCopy() and ip.statusFlags().isPrompt() and abs(ip.pdgId())==24], key = lambda x : x.pt(), reverse=True)
        event.the_gen_w = the_ws[0] if len(the_ws) else None

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
    
