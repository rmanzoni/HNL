import ROOT
import numpy as np
from DataFormats.FWLite import Events, Handle
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
from PhysicsTools.Heppy.physicsutils.PileUpSummaryInfo import PileUpSummaryInfo
from pdb import set_trace

ROOT.gROOT.SetBatch()        # don't pop up canvases

creator = ComponentCreator()

TTJets_18 = creator.makeMCComponent(
    name    = 'TTJets_18', 
    dataset = '/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 831.76, 
    useAAA  = True
)

handle = Handle('std::vector<PileupSummaryInfo>')
label  = ("slimmedAddPileupInfo")

for sample in [TTJets_18]:
    print '#######################################'
    print '#### computing pileup for %s'%(sample.name)
    print '#######################################'
    # outfile = ROOT.TFile.Open('pileup_TEST.root', 'recreate')
    outfile = ROOT.TFile.Open('pileup_%s.root'%(sample.name), 'recreate')

    # fill with true interactions
    h_ti = ROOT.TH1F('pileup', 'pileup', 200, 0, 200)

    totevents = 0
    nfiles = len(sample.files)
    # nfiles = 1
    batch = 5
    maxend = (nfiles - nfiles%batch) / batch + 1

    for i in range(maxend):
    # for i in range(1):
        
        begin  = batch * (i)
        end    = batch * (i+1)
        
        print 'running of %d-th batch of %d files out of %d total batches' %(i+1, batch, maxend)
        
        # need to cast to strings, otherwise file names are returned as unicode objects
        # and ROOT doesn't like them 
        files_in_batch = map(str, sample.files[begin:end])

        events = Events(files_in_batch)

        for j, event in enumerate(events):
            if j%100000==0:
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
