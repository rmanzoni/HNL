#! /usr/bin/env python
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


# Events takes either
# - single file name
# - list of file names
# - VarParsing options

# use Varparsing object
events = Events ('/eos/user/d/dezhu/HNL/projects/20181119_ElectronTracks/outputElectronTracks.root')
# events = Events ('/eos/user/d/dezhu/HNL/projects/20181119_ElectronTracks/outputBKstLL.root')
# events = Events ('outputElectronTracks.root')

# create handle outside of loop
handle_ele  = Handle ("std::vector<pat::Electron>")
handle_map  = Handle ("vector<pair<edm::Ptr<pat::Electron>,reco::Track>>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label_ele = ("slimmedElectrons")
# label_ele = ("selectedElectrons","","TTK")
label_map = ("ttk", "eleTtkMap", "MakeElectronTracks")
# label_map = ("ttk", "eleTtkMap", "TTK")

# Create histograms, etc.
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.gROOT.SetStyle('Plain') # white background


# initiate the VertexFitter and create a std::vector<RecoChargedCandidate> to be passed to the fitter 
vtxfit = VertexFitter()
tofit = ROOT.std.vector('reco::RecoChargedCandidate')()

print 'start looping...'

# loop over events
for ii, event in enumerate(events):
    pte  = 0
    pte2 = 0
    ptm1 = 0
    ptm2 = 0
    # if event.eventAuxiliary().run() != 316060:
         # continue
    # if event.eventAuxiliary().luminosityBlock() != 306:
         # continue
    # if event.eventAuxiliary().event() != 291325724:
         # continue
    # if ii > 2: continue
    print '#############################################################'
    print 'event %d'%(ii)

    # use getByLabel, just like in cmsRun
    event.getByLabel (label_ele, handle_ele)
    event.getByLabel (label_map, handle_map)

    # get the product; eles is a <ROOT.pat::Electron object>, while maps is a <ROOT.pair<edm::Ptr<pat::Electron>,reco::Track> object>
    eles = handle_ele.product()
    maps = handle_map.product()
    neles = len(eles)
    nmaps = len(maps)
    print 'neles = %d; nmaps = %d'%(neles,nmaps)

    #prepare the pair that need to be fit later for the vertex
    pairs = []
    
    # set_trace()
    if neles == 0 and nmaps == 0:
        print '----------no electrons and no electron tracks'
        continue
    elif neles!=nmaps:
        print '!!!!!!!!!!different numbers of electrons and tracks'    
        continue
    else: #the case where we would expect good pairs
        for i in xrange(neles):
            try:
                pte  = eles[i].pt()
                pte2 = eles[i].gsfTrack().pt()
                ptm1 = maps[i].first.pt()
                ptm2 = maps[i].second.pt()
                print '%d. pt(e_pat) = %.2f; pt(e_gsf) = %.2f; pt(m1_pat) = %.2f; pt (m2_track) = %.2f'%(i,pte,pte2,ptm1,ptm2)    
            except:
                set_trace()
                continue
         
        pairs = combinations(maps,2)  
        pairs = [(e1,e2) for e1,e2 in pairs]
        print 'we have %d pair(s)!'%(len(pairs))
        for index, pair in enumerate(pairs):
            if pair[0]==pair[1]: continue
            vtx = None
            tofit.clear()
            break
                
   

