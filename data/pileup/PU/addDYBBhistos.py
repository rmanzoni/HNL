import ROOT 
import os
from pdb import set_trace

f_out = ROOT.TFile('pileup_DYBB_total.root', 'recreate')

h_out = ROOT.TH1F('pileup_total', 'pileup_total', 200, 0, 200)

for i in range(10):
    if not os.path.isfile('./DYBB_batches/pileup_DYBB_batch_%i.root'%i):
        continue
    file_path = 'DYBB_batches/pileup_DYBB_batch_%i.root'%i
    f_in = ROOT.TFile(file_path)
    print 'merging %s'%(file_path)
    h_in = f_in.Get('pileup')
    h_out.Add(h_in)
    f_in.Close()
    if i%10 == 0: print(i)

f_out.cd()
h_out.Write()
f_out.Close()
   
