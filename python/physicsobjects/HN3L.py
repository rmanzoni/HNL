import math

from itertools import combinations, product
# from copy import deepcopy as dc

from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from ROOT import TVector3, Math


class HN3L(object):

    ''' 
    '''

    def __init__(self, pl, dl1, dl2, met=None):
        self.pl_  = pl
        self.dl1_ = dl1
        self.dl2_ = dl2
        self.met_ = met

    # objects
    def pl(self):
        return self.pl_

    def dl1(self):
        return self.dl1_

    def dl2(self):
        return self.dl2_

    def met(self):
        return self.met_

    def charge(self):
        return self.pl().charge() + self.dl1().charge() + self.dl2().charge()

    def hnCharge(self):
        return self.dl1().charge() + self.dl2().charge()
        
    # W kinematics w/ met
    def p4(self):
        return self.pl().p4() + self.dl1().p4() + self.dl2().p4() + self.met().p4() if self.met() else None

    def pt(self):
        return self.p4().pt() if self.met() else None

    def eta(self):
        return self.p4().eta() if self.met() else None

    def phi(self):
        return self.p4().phi() if self.met() else None

    def mass(self):
        return self.p4().mass() if self.met() else None

    def sumPt(self):
        return self.pl().pt() + self.dl1().pt() + self.dl2().pt() + self.met().pt() if self.met() else None

    # W kinematics w/o met
    def visP4(self):
        return self.pl().p4() + self.dl1().p4() + self.dl2().p4()

    def visPt(self):
        return self.visP4().pt()

    def visEta(self):
        return self.visP4().eta()

    def visPhi(self):
        return self.visP4().phi()

    def visMass(self):
        return self.visP4().mass()

    def visSumPt(self):
        return self.pl().pt() + self.dl1().pt() + self.dl2().pt()

    # heavy neutrino kinematics w/ met
    def hnP4(self):
        return self.dl1().p4() + self.dl2().p4() + self.met().p4() if self.met() else None

    def hnPt(self):
        return self.hnP4().pt() if self.met() else None

    def hnEta(self):
        return self.hnP4().eta() if self.met() else None

    def hnPhi(self):
        return self.hnP4().phi() if self.met() else None

    def hnMass(self):
        return self.hnP4().mass() if self.met() else None

    def hnSumPt(self):
        return self.dl1().pt() + self.dl2().pt() + self.met().pt() if self.met() else None

    # heavy neutrino kinematics w/o met
    def hnVisP4(self):
        return self.dl1().p4() + self.dl2().p4()

    def hnVisPt(self):
        return self.hnVisP4().pt()

    def hnVisEta(self):
        return self.hnVisP4().eta()

    def hnVisPhi(self):
        return self.hnVisP4().phi()

    def hnVisMass(self):
        return self.hnVisP4().mass()

    def hnVisSumPt(self):
        return self.dl1().pt() + self.dl2().pt()
        
    # pair masses
    def mass01(self):
        return (self.pl().p4() + self.dl1().p4()).mass() 

    def mass02(self):
        return (self.pl().p4() + self.dl2().p4()).mass() 

    def mass12(self):
        return (self.dl1().p4() + self.dl2().p4()).mass() 

    # lepton charges
    def charge01(self):
        return self.pl().charge() + self.dl1().charge()

    def charge02(self):
        return self.pl().charge() + self.dl2().charge()

    def charge12(self):
        return self.dl1().charge() + self.dl2().charge()

    # delta R & delta phi
    def dR01(self):
        return deltaR(self.pl().p4(), self.dl1().p4())

    def dR02(self):
        return deltaR(self.pl().p4(), self.dl2().p4())

    def dR12(self):
        return deltaR(self.dl1().p4(), self.dl2().p4())

    def dR0MET(self):
        return deltaR(self.pl().p4(), self.met().p4()) if self.met() else None

    def dR1MET(self):
        return deltaR(self.dl1().p4(), self.met().p4()) if self.met() else None

    def dR2MET(self):
        return deltaR(self.dl2().p4(), self.met().p4()) if self.met() else None

    def dPhi01(self):
        return deltaPhi(self.pl().phi(), self.dl1().phi())

    def dPhi02(self):
        return deltaPhi(self.pl().phi(), self.dl2().phi())

    def dPhi12(self):
        return deltaPhi(self.dl1().phi(), self.dl2().phi())

    def dPhi0MET(self):
        return deltaPhi(self.pl().phi(), self.met().phi()) if self.met() else None

    def dPhi1MET(self):
        return deltaPhi(self.dl1().phi(), self.met().phi()) if self.met() else None

    def dPhi2MET(self):
        return deltaPhi(self.dl2().phi(), self.met().phi()) if self.met() else None

    def dRvisHnMET(self):
        return deltaR(self.hnVisP4(), self.met()) if self.met() else None

    def dRvisHnPl(self):
        return deltaR(self.hnVisP4(), self.pl())

    def dRHnMET(self):
        return deltaR(self.hnP4(), self.met()) if self.met() else None

    def dRHnPl(self):
        return deltaR(self.hnP4(), self.pl()) if self.met() else None

    def dPhiVisHnMET(self):
        return deltaPhi(self.hnVisP4().phi(), self.met().phi()) if self.met() else None

    def dPhiVisHnPl(self):
        return deltaPhi(self.hnVisP4().phi(), self.pl().phi())

    def dPhiHnMET(self):
        return deltaPhi(self.hnP4().phi(), self.met().phi()) if self.met() else None

    def dPhiHnPl(self):
        return deltaPhi(self.hnP4().phi(), self.pl().phi()) if self.met() else None

    # pt of two-body pairs
    def pt01(self):
        return (self.pl().p4() + self.dl1().p4()).pt()

    def pt02(self):
        return (self.pl().p4() + self.dl2().p4()).pt()

    def pt12(self):
        return (self.dl1().p4() + self.dl2().p4()).pt()

    def pt0MET(self):
        return (self.pl().p4() + self.met().p4()).pt() if self.met() else None

    def pt1MET(self):
        return (self.dl1().p4() + self.met().p4()).pt() if self.met() else None

    def pt2MET(self):
        return (self.dl2().p4() + self.met().p4()).pt() if self.met() else None

    # transverse masses
    def mt0(self):
        mt0 = self.calcMT(self.pl().p4(), self.met()) if self.met() else None
        return mt0

    def mt1(self):
        mt1 = self.calcMT(self.dl1().p4(), self.met()) if self.met() else None
        return mt1

    def mt2(self):
        mt2 = self.calcMT(self.dl2().p4(), self.met()) if self.met() else None
        return mt2

    def mtVisHnMET(self):
        mtHnMET = self.calcMT(self.hnVisP4(), self.met()) if self.met() else None
        return mtHnMET
    
    # more stuff
    def calcPZeta(self):
        plPT  = TVector3(self.pl() .p4().x(), self.pl() .p4().y(), 0.)
        dl1PT = TVector3(self.dl1().p4().x(), self.dl1().p4().y(), 0.)
        dl2PT = TVector3(self.dl2().p4().x(), self.dl2().p4().y(), 0.)
        metPT = TVector3(self.met().p4().x(), self.met().p4().y(), 0.)
        zetaAxis = (plPT.Unit() + dl1PT.Unit() + dl2PT.Unit()).Unit()
        self.pZetaVis_ = plPT*zetaAxis + dl1PT*zetaAxis + dl2PT*zetaAxis
        self.pZetaMET_ = metPT*zetaAxis

    # Calculate the transverse mass with the same algorithm
    # as previously in the C++ DiObject class
    @staticmethod
    def calcMT(cand1, cand2):
        pt = cand1.pt() + cand2.pt()
        px = cand1.px() + cand2.px()
        py = cand1.py() + cand2.py()
        try:
            return math.sqrt(pt*pt - px*px - py*py)
        except ValueError:
            print 'Funny rounding issue', pt, px, py
            print cand1.px(), cand1.py(), cand1.pt()
            print cand2.px(), cand2.py(), cand2.pt()
            return 0.

    def __getattr__(self, name):
        '''Redefine getattr to original version.'''
        raise AttributeError