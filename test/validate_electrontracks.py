#! /usr/bin/env python
from pdb import set_trace
import ROOT
ROOT.gSystem.Load('libCMGToolsHNL')

import sys
from DataFormats.FWLite import Events, Handle

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
events = Events ('outputElectronTracks.root')

# create handle outside of loop
handle_ele  = Handle ("std::vector<pat::Electron>")
handle_map  = Handle ("vector<pair<edm::Ptr<pat::Electron>,reco::Track>>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label_ele = ("slimmedElectrons")
label_map = ("ttk", "eleTtkMap", "MakeElectronTracks")

# Create histograms, etc.
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.gROOT.SetStyle('Plain') # white background

print 'start looping...'

# loop over events
for ii, event in enumerate(events):
    pte  = 0
    ptm1 = 0
    ptm2 = 0
    # if event.eventAuxiliary().run() != 316060:
         # continue
    # if event.eventAuxiliary().luminosityBlock() != 306:
         # continue
    # if event.eventAuxiliary().event() != 291325724:
         # continue
    print '#############################################################'
    print 'event %d'%(ii)

    # use getByLabel, just like in cmsRun
    event.getByLabel (label_ele, handle_ele)
    event.getByLabel (label_map, handle_map)
    # get the product
    eles = handle_ele.product()
    maps = handle_map.product()

    neles = len(eles)
    nmaps = len(maps)

    print 'neles = %d; nmaps = %d'%(neles,nmaps)
    #eles is the <ROOT.pat::Electron object at 0x16ef9f60>, while maps is the <ROOT.pair<edm::Ptr<pat::Electron>,reco::Track> object at 0x16fae6d0>
    if ii == 19: set_trace()
    if neles == 0 and nmaps == 0:
        print '----------no electrons and no electron tracks'
    elif neles!=nmaps:
        print '!!!!!!!!!!different numbers of electrons and tracks'    
    else:
        for i in xrange(neles):
            try:
                pte  = eles[i].pt()
                ptm1 = maps[i].first.pt()
                ptm2 = maps[i].second.pt()
                print '%d. pt(e_pat) = %.2f; pt(m1_pat) = %.2f; pt (m2_track) = %.2f'%(i,pte,ptm1,ptm2)    
            except:
                set_trace()



