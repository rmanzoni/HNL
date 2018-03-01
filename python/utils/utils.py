import ROOT
from math import sqrt

def isAncestor(a, p):
    if a == p :
        return True
    for i in xrange(0,p.numberOfMothers()):
        if isAncestor(a,p.mother(i)):
            return True
    return False

def displacement2D(p1, p2):    
    dx = p1.vx() - p2.vx()    
    dy = p1.vy() - p2.vy()    
    return sqrt(dx**2 + dy**2)    

def displacement3D(p1, p2):    
    dx = p1.vx() - p2.vx()    
    dy = p1.vy() - p2.vy()    
    dz = p1.vz() - p2.vz()    
    return sqrt(dx**2 + dy**2 + dz**2)    

def makeRecoVertex(kinVtx, kinVtxChi2=0., kinVtxNdof=0, kinVtxTrkSize=0):
    point = ROOT.reco.Vertex.Point(
        kinVtx.vertexState().position().x(),
        kinVtx.vertexState().position().y(),
        kinVtx.vertexState().position().z(),
    )
    error = kinVtx.vertexState().error().matrix()
    chi2  = kinVtxChi2 if kinVtxChi2 else kinVtx.chiSquared()
    ndof  = kinVtxNdof if kinVtxNdof else kinVtx.degreesOfFreedom()
    recoVtx = ROOT.reco.Vertex(point, error, chi2, ndof, kinVtxTrkSize)
    return recoVtx
