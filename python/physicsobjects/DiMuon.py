from math import sqrt

from itertools import combinations, product
# from copy import deepcopy as dc

from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from ROOT import TVector3, Math
from pdb import set_trace


class DiMuon(object):
    '''
    '''
    def __init__(self, pair, vtx):
        self.pair = pair
        self.vtx = vtx

    def pair(self):
        return self.pair

    def vtx(self):
        return self.vtx

    def chi2(self):
        return self.vtx.chi2()

    def isSS(self):
        if self.pair[0].charge()==self.pair[1].charge():
            return 1
        else:
            return 0    

    # TODO: function to compute the sum of the 4-vectors

    # how should displacement 2D really defined as distance A=>B? B could be the HNL decay vertex, A could be (0,0,0), beam spot or primary vertex...
    # I'm not event sure what the current vertex is.... TODO: Divide and conquer!
    def dxy(self):
        return sqrt(pow(self.vtx.x(),2)+pow(self.vtx.y(),2))

