import ROOT
from CMGTools.HNL.analyzers.TreeProducerBase import TreeProducerBase
from PhysicsTools.HeppyCore.utils.deltar import deltaR
from CMGTools.HNL.utils.utils import isAncestor, displacement2D, displacement3D, makeRecoVertex # utility functions
from pdb import set_trace

class HNLTreeProducer(TreeProducerBase):
    '''
    '''
    def declareVariables(self, setup):
        '''
        '''
        #event quantities
        self.bookEvent(self.tree)
        self.bookHNLReco(self.tree)

     
        # # the slimmedMuons
        # self.bookMuon    (self.tree, 'sMu'    )
        # self.bookParticle  (self.tree, 'dSAMu'  )

    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

    
        self.fillEvent(self.tree, event)
        self.fillHNLReco(self.tree, event)
        # if hasattr(event,'maxptsMu'):self.fillMuon(self.tree,'sMu', event.maxptsMu)
        # if hasattr(event,'maxptdSAMu'):self.fillParticle(self.tree,'dSAMu', event.maxptdSAMu)

        self.fillTree(event)


