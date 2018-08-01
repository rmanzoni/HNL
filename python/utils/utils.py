import ROOT
from math import sqrt
from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from pdb import set_trace
# load custom library to ROOT. This contains the kinematic vertex fitter class
ROOT.gSystem.Load('libCMGToolsHNL')
from ROOT import HNLKinematicVertexFitter as VertexFitter

# initiate the VertexFitter
vtxfit = VertexFitter()

# create a std::vector<RecoChargedCandidate> to be passed to the fitter
tofit = ROOT.std.vector('reco::RecoChargedCandidate')()

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

def fitVertex(pair):
    vtx = None
    tofit.clear()
    for il in pair:

        ic = ROOT.reco.RecoChargedCandidate() # instantiate a dummy RecoChargedCandidate
        ic.setCharge(il.charge())           # assign the correct charge

        if il.pdgId()%13==0:
            if il.muonBestTrack().isNull(): # check that the track is valid. e.g. photons... 
            # if il.standAloneMuon().isNull(): # check that the track is valid. e.g. photons... 
            # if il.globalTrack().isNull(): # check that the track is valid. e.g. photons... 
                continue
            ic.setTrack(il.muonBestTrack())
            # ic.setTrack(il.standAloneMuon())
            # ic.setTrack(il.globalTrack())
        else:
            if il.track().isNull():
                continue
            ic.setTrack(il.track())

        # if the reco particle is a displaced thing, it does not have the p4() method, so let's build it 
        myp4 = ROOT.Math.LorentzVector('<ROOT::Math::PxPyPzE4D<double> >')(il.px(), il.py(), il.pz(), sqrt(il.mass()**2 + il.px()**2 + il.py()**2 + il.pz()**2))
        ic.setP4(myp4)                      # assign the correct p4
        if ic.track().isNonnull():          # check that the track is valid, there are photons around too!
            tofit.push_back(ic)

    # further sanity check: two *distinct* tracks
    if tofit.size() == 2 and tofit[0].track() != tofit[1].track():
        svtree = vtxfit.Fit(tofit) # the actual vertex fitting!
        if not svtree.get().isEmpty() and svtree.get().isValid(): # check that the vertex is good
            svtree.movePointerToTheTop()
            vtx = makeRecoVertex(svtree.currentDecayVertex().get(),kinVtxTrkSize=2)
            # set_trace()
    # set_trace()
    return vtx



