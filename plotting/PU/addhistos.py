import ROOT as rt
from pdb import set_trace

f_out = rt.TFile('pileup_TTJets_total.root', 'recreate')

h_out = rt.TH1F()
col = []

for i in range(116):
   f_in = rt.TFile('pileup_TTJets_amcat_batch_%i.root'%i)
   h_in = f_in.Get('pileup')
   col.append(h_in)
   f_in.Close()

h_out.Merge(col)

f_out.cd()
h_out.Write()
f_out.Close()
   
