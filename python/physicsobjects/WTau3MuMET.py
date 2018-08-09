import math

from itertools import combinations, product
# from copy import deepcopy as dc

from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Muon
from CMGTools.WTau3Mu.analyzers.resonances import resonances, sigmas_to_exclude
from ROOT import TVector3, Math

class Tau3MuMET(object):

    ''' 
    '''

    def __init__(self, muons, met, useMVAmet=False):
        muons = sorted(muons, key=lambda mu : mu.pt(), reverse=True)
        self.mu1_ = muons[0]
        self.mu2_ = muons[1]
        self.mu3_ = muons[2]
        if useMVAmet:
            self.met_ = self.findMVAmet(met)
        else: 
            self.met_ = met        
        self.checkResonances()
        
    def findMVAmet(self, met):
        '''
        For each triplet there's a corresponding MVA MET object.
        This method finds the correct correspondence.
        '''
        muons = [self.mu1_.physObj , self.mu2_.physObj , self.mu3_.physObj]

        for imet in met:        
            metmuons = [imet.userCand(iname).get() for iname in imet.userCandNames()]
            matched = 0
            already_matched = []
            for i, j in product(metmuons, muons):
                if i==j and j not in already_matched:
                    already_matched.append(j)
                    matched += 1
            if matched == 3:
                # get rid of eta component and mass being != 0
                newp4 = Math.LorentzVector('<ROOT::Math::PtEtaPhiM4D<double>')(imet.pt(), 0., imet.phi(), 0.)
                imet.setP4(newp4)
                return imet
        
        import pdb ; pdb.set_trace()
        raise Exception('no good MVA met found!')
        
    def checkResonances(self):
        '''
        Save info about di-muon resonances, including whether the two muons are OS or SS.
        Negative is SS.
        '''
        self.vetoResonance3sigma = 0
        self.vetoResonance2sigma = 0
        
        masses = [
            (self.mass12(), self.charge12(),  0), 
            (self.mass13(), self.charge13(), 10), 
            (self.mass23(), self.charge23(), 20),
        ]
        
        for mm in masses:
            distance = lambda rr : abs(mm[0]-rr[0]) / rr[1]
            resonance = sorted(resonances, key=distance)[0]
            id = (mm[2] + resonance[2]) * ((mm[1]==0) - (mm[1]!=0))
            if distance(resonance) < 3. :
                self.vetoResonance3sigma = id
            if distance(resonance) < 2. :
                self.vetoResonance2sigma = id

    def _me(self):
        '''
        Longitudinal momentum component of the neutrino, assuming W mass = 80.385 GeV and
        mw^2 = (E_tau + E_inv)^2 - (pz_tau + pz_inv)^2 - (px_tau - px_inv)^2  - (py_tau - py_inv)^2
        
        The quadratic equation gives two solutions, both are returned.
        '''
        mw = 80.385

        constant = (self.met().px()*self.p4Muons().px() + self.met().py()*self.p4Muons().py()) + 0.5*(mw**2 - self.p4Muons().mass()**2)
        
        A = self.p4Muons().energy()**2 - self.p4Muons().pz()**2
        B = -2.*constant*self.p4Muons().pz()
        C = self.p4Muons().energy()**2*self.met().pt()**2 - constant**2
        
        radical = B**2 - 4.*A*C
        
        if radical>=0.:
            mez_plus  = 0.5 * ( -B + math.sqrt(radical) ) / A
            mez_minus = 0.5 * ( -B - math.sqrt(radical) ) / A
        else: 
            mez_plus  = 0.
            mez_minus = 0.
            # non physical solutions might simply be resolution effects. 
            # Should think of how to treat them, e.g. set the square root argument to 0
            return Math.LorentzVector('<ROOT::Math::PxPyPzE4D<double>')(0., 0., 0., 0.), Math.LorentzVector('<ROOT::Math::PxPyPzE4D<double>')(0., 0., 0., 0.)

        if abs(mez_plus) > abs(mez_minus):
            mez_min = mez_minus
            mez_max = mez_plus
        else:
            mez_min = mez_plus
            mez_max = mez_minus

        energy_min = math.sqrt(self.met().pt()**2 + mez_min**2)
        energy_max = math.sqrt(self.met().pt()**2 + mez_max**2)
        
        missing_energy_p4_mez_min = Math.LorentzVector('<ROOT::Math::PxPyPzE4D<double>')(self.met().px(), self.met().py(), mez_min, energy_min) 
        missing_energy_p4_mez_max = Math.LorentzVector('<ROOT::Math::PxPyPzE4D<double>')(self.met().px(), self.met().py(), mez_max, energy_max) 
                
        return missing_energy_p4_mez_min, missing_energy_p4_mez_max

    def me(self):
        return self._me()[0]

    def me_mez_min(self):
        return self._me()[0]

    def me_mez_max(self):
        return self._me()[1]

    def reco_w(self):
        wp4_min = Math.LorentzVector('<ROOT::Math::PxPyPzE4D<double>')(0., 0., 0., 0.) 
        wp4_max = Math.LorentzVector('<ROOT::Math::PxPyPzE4D<double>')(0., 0., 0., 0.)
        if self.me_mez_min().energy()>0.:
            wp4_min = self.me_mez_min() + self.p4Muons()            
        if self.me_mez_max().energy()>0.:
            wp4_max = self.me_mez_max() + self.p4Muons()
                    
        return wp4_min, wp4_max
        
    def sumPt(self):
        return self.p4().pt()

    def sumPtMuons(self):
        return self.p4Muons().pt()
        
    def mass(self):
        return self.p4().mass()

    def massMuons(self):
        return self.p4Muons().mass()

    def mass12(self):
        return (self.mu1().p4() + self.mu2().p4()).mass()

    def mass13(self):
        return (self.mu1().p4() + self.mu3().p4()).mass()

    def mass23(self):
        return (self.mu2().p4() + self.mu3().p4()).mass()

    def charge12(self):
        return self.mu1().charge() + self.mu2().charge()

    def charge13(self):
        return self.mu1().charge() + self.mu3().charge()

    def charge23(self):
        return self.mu2().charge() + self.mu3().charge()

    def dR12(self):
        return deltaR(self.mu1().p4(), self.mu2().p4())

    def dR13(self):
        return deltaR(self.mu1().p4(), self.mu3().p4())

    def dR23(self):
        return deltaR(self.mu2().p4(), self.mu3().p4())

    def pt12(self):
        return (self.mu1().p4() + self.mu2().p4()).pt()

    def pt13(self):
        return (self.mu1().p4() + self.mu3().p4()).pt()

    def pt23(self):
        return (self.mu2().p4() + self.mu3().p4()).pt()

    def dRtauMET(self):
        return deltaR(self.p4Muons(), self.met())

    def dRtauMuonMax(self):
        return max([deltaR(self.p4Muons(), mu) for mu in [self.mu1(), self.mu2(), self.mu3()]])

    def dPhitauMET(self):
        return deltaPhi(self.p4Muons().phi(), self.met().phi())

    def p4(self):
        return self.mu1().p4() + self.mu2().p4() + self.mu3().p4() + self.met().p4()
        
    def p4Muons(self):
        return self.mu1().p4() + self.mu2().p4() + self.mu3().p4()

    def mu1(self):
        return self.mu1_

    def mu2(self):
        return self.mu2_

    def mu3(self):
        return self.mu3_

    def charge(self):
        return self.mu1().charge() + self.mu2().charge() + self.mu3().charge()
        
    def met(self):
        return self.met_

    def calcPZeta(self):
        mu1PT = TVector3(self.mu1().p4().x(), self.mu1().p4().y(), 0.)
        mu2PT = TVector3(self.mu2().p4().x(), self.mu2().p4().y(), 0.)
        mu3PT = TVector3(self.mu3().p4().x(), self.mu3().p4().y(), 0.)
        metPT = TVector3(self.met().p4().x(), self.met().p4().y(), 0.)
        zetaAxis = (mu1PT.Unit() + mu2PT.Unit() + mu3PT.Unit()).Unit()
        self.pZetaVis_ = mu1PT*zetaAxis + mu2PT*zetaAxis + mu3PT*zetaAxis
        self.pZetaMET_ = metPT*zetaAxis

    def mt1(self):
        mt1 = self.calcMT(self.mu1().p4(), self.met())
        return mt1

    def mt2(self):
        mt2 = self.calcMT(self.mu2().p4(), self.met())
        return mt2

    def mt3(self):
        mt3 = self.calcMT(self.mu3().p4(), self.met())
        return mt3

    def mttau(self):
        mttau = self.calcMT(self.p4Muons(), self.met())
        return mttau

    def mtTotal12(self):
        mtTotal12 = self.mt1()**2 + \
                    self.mt2()**2 + \
                    self.calcMT(self.mu1(), self.mu2())**2
        return math.sqrt(mtTotal12)

    def mtTotal13(self):
        mtTotal13 = self.mt1()**2 + \
                    self.mt3()**2 + \
                    self.calcMT(self.mu1(), self.mu3())**2
        return math.sqrt(mtTotal13)

    def mtTotal23(self):
        mtTotal23 = self.mt2()**2 + \
                    self.mt3()**2 + \
                    self.calcMT(self.mu2(), self.mu3())**2
        return math.sqrt(mtTotal23)

    def mtSumMuons(self):
        return self.mt1() + self.mt2() + self.mt3()

    def mtSqSumMuons(self):
        return math.sqrt(self.mt1()**2 + self.mt2()**2 + self.mt3()**2)

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

#     @staticmethod
#     def calcMtTotal(cands):
#         return math.sqrt(sum(DiObject.calcMT(c1, c2)**2 for c1, c2 in combinations(cands, 2)))

    def __getattr__(self, name):
        '''Redefine getattr to original version.'''
        raise AttributeError

#     def __str__(self):
#         header = '{cls}: mvis={mvis}, sumpT={sumpt}'.format(
#             cls=self.__class__.__name__,
#             mvis=self.mass(),
#             sumpt=self.sumPt())
#         return '\n'.join([header,
#                           '\t'+str(self.leg1()),
#                           '\t'+str(self.leg2())])
)
]
