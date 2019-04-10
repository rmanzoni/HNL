import ROOT
import plotfactory as pf
import numpy as np
import sys
from pdb import set_trace

pf.setpfstyle()

t = ROOT.TChain('tree')
# t.Add('root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv1.0/mmm/background/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root')
t.Add('/work/dezhu/4_production/production_20190402_BkgMC/mmm/ntuples/DYJetsToLL_M50_ext//HNLTreeProducer/tree.root')

binsx = np.arange(0.,200.,5.)

c = ROOT.TCanvas('c','c')

h = ROOT.TH1F('h','h',len(binsx)-1,binsx)

# L_data = 41000
L_data = 4790
xsec = 2075.14*3 
# N_events = 158048935. #v1.0
# SumWeights = 5939397. #v2.0, using the SumNormWeights from SkimAnalyzercount/SkimReport.txt
# SumWeights = 123584524. #v2.0, higher stats
SumWeights = 116914789. #v2.0, 20190402
L_MC   = SumWeights /xsec

L_ratio = L_data/L_MC # L_ratio = 4.106083204928521

selection = ('(l0_pt>25 & abs(l0_eta)<2.4 & (l0_q != l1_q) '
    '& l1_pt > 15 & abs(l1_eta) < 2.4 '
    '& abs(l0_dxy) < 0.05 & abs(l0_dz) < 0.2 '
    '& abs(l1_dxy) < 0.05 & abs(l1_dz) < 0.2 '
    '& nbj == 0 & '
    # 'abs(hnl_m_01 - 91) < 5 '
    '& l0_id_t & l1_id_t & l2_id_m '
    '& l0_reliso_rho_03 < 0.20 '
    '& l1_reliso_rho_03 < 0.20 '
    '& l2_reliso_rho_03 < 0.20 '
    # '& abs(l2_gen_match_pdgid) != 22'
    ')'
    )

weight = 'weight * lhe_weight'
lumi_correction = L_ratio


# final_selection = '(%s)'%(selection) 
# final_selection = '(%s)*(%s)'%(selection,weight) 
final_selection = '(%s)*(%s)*(%f)'%(selection,weight,lumi_correction) 

# weight2 = '(l0_pt>25 & abs(l0_eta)<2.4 & (l0_q != l1_q) & l1_pt > 15 & abs(l1_eta) < 2.4 & abs(l0_dxy) < 0.05 & abs(l0_dz) < 0.2 & abs(l1_dxy) < 0.05 & abs(l1_dz) < 0.2 & nbj == 0 & & l0_id_t & l1_id_t& l2_id_m & l0_reliso05_03 < 0.15& l1_reliso05_03 < 0.15& l2_reliso05_03 < 0.15& abs(l2_gen_match_pdgid) != 22 ) * weight * lhe_weight'

# t.Draw("hnl_m_01 >> h",'(%s)*(%s)'%(selection,weight))
# t.Draw("hnl_m_01 >> h",weight2)
t.Draw("hnl_m_01 >> h",final_selection)
# t.Draw("hnl_m_01 >> h",selection + '* weight * lhe_weight * %d'%(lumi_correction))
c.Update()

cn = ROOT.TCanvas('cn','cn')
t.Draw("1 >> HISTO(1, 0, 2)", final_selection)
integral = ROOT.gDirectory.Get('HISTO').Integral()
print 'The integral of the histogram is %d'%(integral)
cn.Update()

