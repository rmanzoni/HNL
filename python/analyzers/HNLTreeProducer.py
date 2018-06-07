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
        self.bookDiMuon(self.tree, 'dimuon')
        self.bookParticle (self.tree,'dMu1')
        self.bookParticle (self.tree,'dMu2')

     
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
        self.fillDiMuon(self.tree, 'dimuon', event.dimuon)
        self.fillParticle(self.tree,'dMu1', event.dMu1)
        self.fillParticle(self.tree,'dMu2', event.dMu2)
        # if hasattr(event,'maxptsMu'):self.fillMuon(self.tree,'sMu', event.maxptsMu)
        # if hasattr(event,'maxptdSAMu'):self.fillParticle(self.tree,'dSAMu', event.maxptdSAMu)

        self.fillTree(event)


