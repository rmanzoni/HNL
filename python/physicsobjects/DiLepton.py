from math import sqrt

from itertools import combinations, product
# from copy import deepcopy as dc

from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from ROOT import TVector3, Math
import ROOT
from pdb import set_trace


class DiLepton(object):
    '''
    '''
    def __init__(self, pair, sv, pv, bs, prompt):
        self._prompt = prompt
        self._leptons = sorted(pair, key = lambda x : x.pt(), reverse = True)
        self._vtx = sv
        self._pv  = pv
        self._bs  = bs
        # create an 'ideal' vertex out of the BS
        point = ROOT.reco.Vertex.Point(
            bs.position().x(),
            bs.position().y(),
            bs.position().z(),
        )
        error = bs.covariance3D()
        chi2 = 0.
        ndof = 0.
        bsvtx = ROOT.reco.Vertex(point, error, chi2, ndof, 2) # size? say 2? does it matter?
        self._bsvtx  = bsvtx

    def leptons(self):
        return self._leptons

    def lep0(self):
        return self._prompt

    def lep1(self):
        return self.leptons()[0]

    def lep2(self):
        return self.leptons()[1]

    def p4_01(self):
        try:
            return self.lep0().p4() + self.lep1().p4()
        except:
            set_trace()
    
    def p4_02(self):
        return self.lep0().p4() + self.lep2().p4()
    
    def p4_12(self):
        return self.lep1().p4() + self.lep2().p4()
    
    def pt_01(self):
        return self.p4_01().pt()

    def pt_02(self):
        return self.p4_02().pt()

    def pt_12(self):
        return self.p4_12().pt()

    def p_01(self):
        return self.p4_01().P()

    def p_02(self):
        return self.p4_02().P()

    def p_12(self):
        return self.p4_12().P()

    def deta_01(self):
        return abs(self.lep0().eta() - self.lep1().p4().eta())

    def deta_02(self):
        return abs(self.lep0().eta() - self.lep2().p4().eta())

    def deta_12(self):
        return abs(self.lep1().eta() - self.lep2().p4().eta())

    def eta_12(self):
        return self.p4_12().eta()

    def deta_hn0_vis(self):
        return abs(self.p4_12().eta() - self.lep0().p4().eta())


    def dphi_01(self):
        return abs(self.lep0().phi() - self.lep1().p4().phi())

    def dphi_02(self):
        return abs(self.lep0().phi() - self.lep2().p4().phi())

    def dphi_12(self):
        return abs(self.lep1().phi() - self.lep2().p4().phi())

    def phi_12(self):
        return self.p4_12().phi()

    def dphi_hn0_vis(self):
        return abs(self.p4_12().phi() - self.lep0().p4().phi())

    def dr_01(self):
        return deltaR(self.lep0(), self.lep1()) 

    def dr_02(self):
        return deltaR(self.lep0(), self.lep2()) 

    def dr_12(self):
        return deltaR(self.lep1(), self.lep2()) 

    def dr_hn0_vis(self):
        return sqrt(pow((self.eta_12()-self.lep0().eta()),2) + pow((self.phi_12()-self.lep0().phi()),2) ) 

    def mass_01(self):
        return self.p4_01().mass()

    def mass_02(self):
        return self.p4_02().mass()

    def mass_12(self):
        return self.p4_12().mass()

    def q_01(self):
        return (self.lep0().charge() + self.lep1().charge())

    def q_02(self):
        return (self.lep0().charge() + self.lep2().charge())

    def q_12(self):
        return (self.lep1().charge() + self.lep2().charge())

    def q_012(self):
        return (self.lep0().charge() + self.lep1().charge() + self.lep2().charge())

    def p_12_x(self):
        return self.p4_12().px()

    def p_12_y(self):
        return self.p4_12().py()

    def p_12_z(self):
        return self.p4_12().pz()

    def vtx(self):
        return self.vtx

    def vtx(self):
        return self._vtx

    def chi2(self):
        return self.vtx().chi2()

    def isSS(self):
        return int(self.lep1().charge()==self.lep2().charge())

    def isOS(self):
        return int(self.lep1().charge()!=self.lep2().charge())

    def _disp3DFromPV(self):
        return ROOT.VertexDistance3D().distance(self.vtx(), self._pv)

    def disp3DFromPV(self):
        return self._disp3DFromPV().value()

    def disp3DFromPVSignificance(self):
        return self._disp3DFromPV().significance()

    def _disp2DFromBS(self):
        return ROOT.VertexDistanceXY().distance(self.vtx(), self._bsvtx)

    def disp2DFromBS(self):
        return self._disp2DFromBS().value()

    def disp2DFromBSSignificance(self):
        return self._disp2DFromBS().significance()

    def _disp2DFromPV(self):
        return ROOT.VertexDistanceXY().distance(self.vtx(), self._pv)

    def disp2DFromPV(self):
        return self._disp2DFromPV().value()

    def disp2DFromPVSignificance(self):
        return self._disp2DFromPV().significance()

    def cosTransversePointingAngleBS(self):
        
        if not hasattr(self, '_cos'):

            perp = ROOT.math.XYZVector(self.p_12_x(),
                                       self.p_12_y(),
                                       0.)
        
            dxybs = ROOT.GlobalPoint(-1*((self._bs.x0() - self.vtx().x()) + (self.vtx().z() - self._bs.z0()) * self._bs.dxdz()), 
                                     -1*((self._bs.y0() - self.vtx().y()) + (self.vtx().z() - self._bs.z0()) * self._bs.dydz()),
                                      0)
        
            vperp = ROOT.math.XYZVector(dxybs.x(), dxybs.y(), 0.)
        
            cos = vperp.Dot(perp)/(vperp.R()*perp.R())
            
            self._cos = cos

        return self._cos

    def __str__(self):
        try:
            return '\n'.join(['',
                              self.lep1().__str__(),
                              self.lep2().__str__(),
                              '\t pt_12       %.2f' %self.pt_12(),
                              '\t eta_12      %.2f' %self.eta_12(),
                              '\t phi_12      %.2f' %self.phi_12(),
                              '\t mass_12     %.3f' %self.mass_12(),
                              '\t deltaR_12   %.5f' %self.dr_12(),
                              '\t deltaPhi_12 %.5f' %self.dphi_12(),
                              '\t deltaEta_12 %.5f' %self.deta_12(),
                              '\t vertex x=%.2f y=%.2f z=%.2f' %(self.vtx().x(), self.vtx().y(), self.vtx().z()),
                              '\t vertex chi2 %.5f' %self.chi2(),
                              '\t 2d displacement from BS %.3f with L/sigma %.3f' %(self.disp2DFromBS(), self.disp2DFromBSSignificance()),
                              '\t 2d displacement from PV %.3f with L/sigma %.3f' %(self.disp2DFromPV(), self.disp2DFromPVSignificance()),
                              '\t 3d displacement from PV %.3f with L/sigma %.3f' %(self.disp3DFromPV(), self.disp3DFromPVSignificance()),
                              '\t pointing angle cosine %.7f' %self.cosTransversePointingAngleBS(),
                              '',
                            ]) 
        except:
            set_trace()

