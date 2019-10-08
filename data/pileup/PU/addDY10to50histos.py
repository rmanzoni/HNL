import ROOT as rt
from pdb import set_trace

f_out = rt.TFile('pileup_DYJets_M10to50_total.root', 'recreate')

h_out = rt.TH1F('pileup_total', 'pileup_total', 200, 0, 200)

for i in range(47):
   f_in = rt.TFile('pileup_DYJetsToLL_M10to50_batch_%i.root'%i)
   h_in = f_in.Get('pileup')
   h_out.Add(h_in)
   f_in.Close()
   if i%10 == 0: print(i)

f_out.cd()
h_out.Write()
f_out.Close()
   
