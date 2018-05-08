import math

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

    # def chi2(self):
        # return self.vtx.chi2
