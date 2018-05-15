from math import sqrt

from itertools import combinations, product
# from copy import deepcopy as dc

from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from ROOT import TVector3, Math


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

    # how should displacement 2D really defined as distance A=>B? B could be the HNL decay vertex, A could be (0,0,0), beam spot or primary vertex...
    def displacement2D(self):
        return sqrt(pow(self.vtx.x(),2)+pow(self.vtx.y(),2))

    def chi2(self):
        return self.vtx.chi2()
