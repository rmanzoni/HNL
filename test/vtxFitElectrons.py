from pdb import set_trace
import ROOT
ROOT.gSystem.Load('libCMGToolsHNL')
from ROOT import HNLKinematicVertexFitter as VertexFitter
import sys
from DataFormats.FWLite import Events, Handle
from itertools import product, combinations

# Make VarParsing object
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options = VarParsing ('analysis')
options.parseArguments()

def makeRecoVertex(kinVtx, kinVtxChi2=0., kinVtxNdof=0, kinVtxTrkSize=0): point = ROOT.reco.Vertex.Point(
        kinVtx.vertexState().position().x(),
        kinVtx.vertexState().position().y(),
        kinVtx.vertexState().position().z(),
    )
    error = kinVtx.vertexState().error().matrix()
    chi2  = kinVtxChi2 if kinVtxChi2 else kinVtx.chiSquared()
    ndof  = kinVtxNdof if kinVtxNdof else kinVtx.degreesOfFreedom()
    recoVtx = ROOT.reco.Vertex(point, error, chi2, ndof, kinVtxTrkSize)
    return recoVtx

# use Varparsing object
events = Events ('/afs/cern.ch/work/d/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/test/testfile.root')

# create handle outside of loop
handle_ele  = Handle ("std::vector<pat::Electron>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label_ele = ("slimmedElectrons")

# initiate the VertexFitter and create a std::vector<RecoChargedCandidate> to be passed to the fitter 
vtxfit = VertexFitter()
tofit = ROOT.std.vector('reco::Track')()

print 'start looping...'

# loop over events
for ii, event in enumerate(events):
    print '#############################################################'
    print 'event %d'%(ii)

    # use getByLabel, just like in cmsRun
    event.getByLabel (label_ele, handle_ele)

    # get the product; eles is a <ROOT.pat::Electron object>    
    eles = handle_ele.product()
    neles = len(eles)
    print 'neles = %d'%(neles)
    
    pairs = []
    eles_tracks = []

    if neles >1:
        for i in xrange(neles):
            print '%d. pt(e_pat) = %.2f; pt(e_gsf) = %.2f;'%(i,eles[i].pt(),eles[i].gsfTrack().pt())    
            #make a reco::Track object out of this electron
            eles_tracks.append(ROOT.reco.Track(eles[i].gsfTrack().get()))
        
        #prepare the track pairs
        pairs = combinations(eles_tracks,2)
        pairs = [(e1,e2) for e1,e2 in pairs]
        print 'we have %d pair(s)!'%(len(pairs)) 
        
        vtx = None
        tofit.clear()

        #now loop through the pairs and fit Vertices with them
        for index, pair in enumerate(pairs):
            e1_track = pair[0]
            e2_track = pair[1]
            tofit.push_back(e1_track)
            tofit.push_back(e2_track)
            if e1_track!=e2_track:
        
                #call the vertix fit function from framework
                sv = vtxfit.Fit(tofit)

                if not sv.get().isEmpty() and sv.get().isValid():
                    sv.movePointerToTheTop()
                    vtx = makeRecoVertex(sv.currentDecayVertex().get(),kinVtxTrkSize=tofit.size())
                    print 'vtx %d: x/xerr = %.2f/%.2f'%(index,vtx.x(),vtx.xError())
            
            

            
        

    else:
        continue


    set_trace()
