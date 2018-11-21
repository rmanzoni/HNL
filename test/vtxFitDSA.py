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

# use Varparsing object
events = Events ('/afs/cern.ch/work/d/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/test/testfile.root')

# create handle outside of loop
handle_dsa  = Handle ("std::vector<reco::Track>")
handle_gen_pruned  = Handle ("std::vector<reco::GenParticle>")
handle_gen_packed  = Handle ("std::vector<pat::PackedGenParticle>")

# create the labels
label_dsa = ("displacedStandAloneMuons","","RECO")
label_gen_pruned = ("prunedGenParticles","","PAT")
label_gen_packed = ("packedGenParticles","","PAT")

# initiate the VertexFitter and create a std::vector<RecoChargedCandidate> to be passed to the fitter 
vtxfit = VertexFitter()
tofit = ROOT.std.vector('reco::Track')()


print 'start looping...'

# loop over events
for ii, event in enumerate(events):
    print '#############################################################'
    print 'event %d'%(ii)

    pairs = []
    leps  = []

    # use getByLabel, just like in cmsRun
    event.getByLabel (label_dsa,  handle_dsa)
    event.getByLabel (label_gen_packed, handle_gen_packed)
    event.getByLabel (label_gen_pruned, handle_gen_pruned)

    # find and print out the gen vtx position:
    genp = [ip for ip in handle_gen_packed.product()] + [ip for ip in handle_gen_pruned.product()]
    hnl = [ip for ip in genp if abs(ip.pdgId())==9900012 and ip.isLastCopy()][0]
    hnl.initialdaus = [hnl.daughter(jj) for jj in range(hnl.numberOfDaughters())]
    hnl.lepdaus = [dd for dd in hnl.initialdaus if abs(dd.pdgId()) in [11,13]]
    if len(hnl.lepdaus) < 2: 
        print 'only %d leptonic daughters from the HNL on the gen level (at least 2 required), jumping to net event...'%(len(hnl.lepdaus))
        continue
    hnl.lep1 = max([ii for ii in hnl.initialdaus if abs(ii.pdgId()) in [11, 13]], key = lambda x : x.pt())
    hnl.lep2 = min([ii for ii in hnl.initialdaus if abs(ii.pdgId()) in [11, 13]], key = lambda x : x.pt())
    print 'the gen vertex consists of a pair with pdgId = (%d/%d) and pt = (%.3f/%.3f)'%(hnl.lep1.pdgId(),hnl.lep2.pdgId(),hnl.lep1.pt(),hnl.lep2.pt())
    print 'the gen vertex position is x = %.6f'%(hnl.lep1.vertex().x())  


    # get the leptons    
    mus = handle_dsa.product()
    nmus = len(mus)
    
    for m in mus:  leps.append(m)
    nleps = len(leps)

    #Get the gen vertex
    gens_packed = handle_gen_packed.product()
    gens_pruned = handle_gen_pruned.product()

    print '%d leptons: %d electrons and %d muons'%(len(leps),0,nmus)
    

    if nleps >1:
        for i in xrange(nleps):
            print '%d. pdgId = %d * 13;\tpt = %.2f;'%(i,leps[i].charge(),leps[i].pt())    
        
        #prepare the track pairs
        pairs = combinations(leps,2)
        pairs = [(l1,l2) for l1,l2 in pairs]
        print ''
        print 'we have %d pair(s)! Now fitting the vertices...'%(len(pairs)) 
        

        #now loop through the pairs and fit Vertices with them
        for index, pair in enumerate(pairs):
            vtx = None
            tofit.clear()
            if pair[0] != pair [1]:
                for il in pair:
                    if il:
                        tofit.push_back(il)
                        if not il.numberOfValidHits()>0:
                            print 'vtx %d: there are no valid tracker hits in this muon track'%(index)
                    else: print 'vtx %d: could not load dsa Track from the muon'%(index)
            
                if tofit.size() == 2 and tofit[0]!=tofit[1]:
                    #call the vertix fit function from framework
                    sv = vtxfit.Fit(tofit)
                        

                    if not sv.get().isEmpty() and sv.get().isValid():
                        sv.movePointerToTheTop()
                        vtx = makeRecoVertex(sv.currentDecayVertex().get(),kinVtxTrkSize=tofit.size())
                        print 'vtx %d:\tcharge(l1/l2) = %d/%d;\t\tpt(l1/l2) = %.3f/%.3f\t\tx= %.6f\txErr = %.6f\t Chi2 = %.6f'%(index,pair[0].charge(),pair[1].charge(),pair[0].pt(),pair[1].pt(),vtx.x(),vtx.xError(),vtx.chi2())
                        continue
                    else: 
                        print 'vtx %d: vertex either is empty or not valid...'%(index)
            print 'vtx %d: fit failed!'%(index) 
            

            
        

    else:
        continue


    set_trace()
