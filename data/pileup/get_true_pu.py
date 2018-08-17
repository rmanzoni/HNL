import ROOT
import numpy as np
from DataFormats.FWLite import Events, Handle
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
from PhysicsTools.Heppy.physicsutils.PileUpSummaryInfo import PileUpSummaryInfo

ROOT.gROOT.SetBatch()        # don't pop up canvases

creator = ComponentCreator()

TTJets_amcat = creator.makeMCComponent(
    name    = 'TTJets_amcat', 
    dataset = '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 831.76, 
    useAAA  = True
)

outfile = ROOT.TFile.Open('pileup_TTJets_amcat_TEST.root', 'recreate')

# fill with true interactions
h_ti = ROOT.TH1F('pileup', 'pileup', 200, 0, 200)

handle  = Handle ('std::vector<PileupSummaryInfo>')
label = ("slimmedAddPileupInfo")

totevents = 0
nfiles = len(TTJets_amcat.files)
batch = 20
maxend = (nfiles - nfiles%batch) / batch + 1

# for i in range(maxend):
for i in range(3):
    
    begin  = batch * (i)
    end    = batch * (i+1)
    
    print 'running of %d-th batch of %d files out of %d total batches' %(i+1, batch, maxend)

    events = Events(TTJets_amcat.files[begin:end])

    for j, event in enumerate(events):
        if j%1000==0:
            print '\t\tprocessing the %d-th event of the %d-th batch' %(j, i+1)
        event.getByLabel(label, handle)
        puinfos = map(PileUpSummaryInfo, handle.product())
        for pu in puinfos:
            if pu.getBunchCrossing()==0:
                h_ti.Fill(pu.nTrueInteractions())
                break

    totevents += events.size()
    print '\tprocessed %d events so far' %(totevents)

outfile.cd()
h_ti.Write()
outfile.Close()
