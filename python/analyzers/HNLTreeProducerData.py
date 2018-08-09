import ROOT
from CMGTools.HNL.analyzers.TreeProducerBase import TreeProducerBase
from PhysicsTools.HeppyCore.utils.deltar import deltaR
from CMGTools.HNL.utils.utils import isAncestor, displacement2D, displacement3D, makeRecoVertex # utility functions
from pdb import set_trace

class HNLTreeProducerData(TreeProducerBase):
    '''
    '''
    def declareVariables(self, setup):
        '''
        '''
        # output for reco analysis
        self.bookEvent(self.tree)
        self.bookHNLReco(self.tree)
        self.bookDiMuon(self.tree, 'dimuonMaxCosBPA')
        self.bookDisplacedMuon (self.tree,'dMu1MaxCosBPA')
        self.bookDisplacedMuon (self.tree,'dMu2MaxCosBPA')
        self.bookEle(self.tree, 'prompt_ele') 


    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

        # output of reco analysis
        self.fillEvent(self.tree, event)
        self.fillHNLReco(self.tree, event)
        if hasattr(event, 'dimuonMaxCosBPA'):
            self.fillDiMuon(self.tree, 'dimuonMaxCosBPA', event.dimuonMaxCosBPA)
            self.fillDisplacedMuon (self.tree,'dMu1MaxCosBPA', event.dMu1MaxCosBPA)
            self.fillDisplacedMuon (self.tree,'dMu2MaxCosBPA', event.dMu2MaxCosBPA)

        if event.the_prompt_cand != None: # hasattr(event, 'the_prompt_cand'):
            if abs(event.the_prompt_cand.pdgId()) == 11:
                self.fillEle(self.tree, 'prompt_ele', event.the_prompt_cand)


        self.fillTree(event)


