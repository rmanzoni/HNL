import ROOT
import numpy as np
from DataFormats.FWLite import Events, Handle
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
from PhysicsTools.Heppy.physicsutils.PileUpSummaryInfo import PileUpSummaryInfo
import os
from multiprocessing import Process
from pdb import set_trace


ROOT.gROOT.SetBatch()        # don't pop up canvases

creator = ComponentCreator()

DYJetsToLL_M5To50 = creator.makeMCComponent(
    name    = 'DYJetsToLL_M5To50', 
    dataset = '/DYJetsToLL_M-5to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',
    user    = 'CMS', 
    pattern = '.*root', 
    xSec    = 1, 
    useAAA  = True
)

# fill with true interactions

handle  = Handle ('std::vector<PileupSummaryInfo>')
label = ("slimmedAddPileupInfo")

nfiles = len(DYJetsToLL_M5To50.files)
batch = 10
maxend = (nfiles - nfiles%batch) / batch + 1

print('\nnumber of batches: %d' % maxend)

def makehistos(batch, i, maxend):
    totevents = 0
    h_ti = ROOT.TH1F('pileup', 'pileup', 200, 0, 200)
    outfile = ROOT.TFile.Open('pileup_DYJetsToLL_M5To50_batch_%i.root'%i, 'recreate')
    begin  = batch * (i)
    end    = batch * (i+1)

    print 'running of %d-th batch of %d files' %(i+1, batch)

    events = Events(DYJetsToLL_M5To50.files[begin:end])
    for j, event in enumerate(events):
        if j%200000==0:
            print '\t\tprocessing the %d-th event of the %d-th batch' %(j, i+1)
        event.getByLabel(label, handle)
        puinfos = map(PileUpSummaryInfo, handle.product())
        for pu in puinfos:
            if pu.getBunchCrossing()==0:
                try:
                    h_ti.Fill(pu.nTrueInteractions())
                except:
                    print('batch %i failed at event %i'%(i+1,event)); break
                break
    totevents += j
    print '\tprocessed %d events so far' %(events.size())
    proc = os.getpid()
    outfile.cd()
    h_ti.Write()
    outfile.Close()

if __name__ == '__main__':
    procs = []
 
    print('\nenter start batch and end batch\n')
    START = input('start batch: ')
    END = input('end batch: ')

    print('start = %i, end = %i'%(START,END))
    print('press c to continue')
    set_trace()

    for i in range(START,END):
        proc = Process(target=makehistos, args=(batch, i, maxend))
        procs.append(proc)
        proc.start()
 
    for proc in procs:
        proc.join()
