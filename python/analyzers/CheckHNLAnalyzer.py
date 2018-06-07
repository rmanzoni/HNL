'''
Check the HNLAnalyzer how efficient it can identify HNL by comparing it to Gen HNLs.
'''

import ROOT
from itertools import product, combinations
import math
import numpy as np

from PhysicsTools.Heppy.analyzers.core.Analyzer      import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle    import AutoHandle
from PhysicsTools.Heppy.physicsobjects.GenParticle   import GenParticle
from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from PhysicsTools.HeppyCore.utils.deltar             import deltaR, deltaR2
from PhysicsTools.Heppy.physicsobjects.Muon          import Muon
from PhysicsTools.Heppy.physicsobjects.Electron      import Electron
from PhysicsTools.Heppy.physicsobjects.Tau           import Tau
from PhysicsTools.Heppy.physicsobjects.Photon        import Photon
from PhysicsTools.Heppy.physicsobjects.Tau           import Tau
from PhysicsTools.Heppy.physicsobjects.Jet           import Jet
from PhysicsTools.HeppyCore.utils.deltar             import deltaR, deltaPhi, inConeCollection, bestMatch

from CMGTools.HNL.utils.utils         import isAncestor, displacement2D, displacement3D, makeRecoVertex # utility functions
from CMGTools.HNL.physicsobjects.HN3L import HN3L

from pdb import set_trace

##########################################################################################
# load custom library to ROOT. This contains the kinematic vertex fitter class
ROOT.gSystem.Load('libCMGToolsHNL')
from ROOT import HNLKinematicVertexFitter as VertexFitter

class CheckHNLAnalyzer(Analyzer):
    '''
    '''

    def declareHandles(self):
        super(CheckHNLAnalyzer, self).declareHandles()

    def beginLoop(self, setup):
        super(CheckHNLAnalyzer, self).beginLoop(setup)

    def process(self, event):
        event.matchedL1Chi2 = False
        event.matchedL2Chi2 = False
        event.matchedL1Dxy  = False
        event.matchedL2Dxy  = False

        # confirm HNL reconstruction success if both gen leptons l1 and l2 are matched.
        if (deltaR(event.dMu1Chi2,event.the_hnl.l1()) < 0.2) or (deltaR(event.dMu2Chi2,event.the_hnl.l1()) < 0.2): 
            event.matchedL1Chi2 = True

        if (deltaR(event.dMu1Chi2,event.the_hnl.l2()) < 0.2) or (deltaR(event.dMu2Chi2,event.the_hnl.l2()) < 0.2):    
            event.matchedL2Chi2 = True

        if (deltaR(event.dMu1Dxy,event.the_hnl.l1()) < 0.2) or (deltaR(event.dMu2Dxy,event.the_hnl.l1()) < 0.2): 
            event.matchedL1Dxy = True

        if (deltaR(event.dMu1Dxy,event.the_hnl.l2()) < 0.2) or (deltaR(event.dMu2Dxy,event.the_hnl.l2()) < 0.2): 
            event.matchedL2Dxy = True

        event.matchedHNLChi2 = False
        event.matchedHNLDxy  = False
        set_trace()
        event.matchedHNLChi2 = event.matchedL1Chi2 and matchedL2Chi2
        event.matchedHNLDxy  = event.matchedL1Dxy  and matchedL2Dxy    


        return True
    
