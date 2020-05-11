import ROOT
import numpy as np
from copy import deepcopy as dc
from collections import OrderedDict

ROOT.gROOT.SetBatch(True)

global deepflavour_wp
deepflavour_wp = OrderedDict()

deepflavour_wp[2018] = OrderedDict()
deepflavour_wp[2018]['loose' ] = 0.0494
deepflavour_wp[2018]['medium'] = 0.2770
deepflavour_wp[2018]['tight' ] = 0.7264

deepflavour_wp[2017] = OrderedDict()
deepflavour_wp[2017]['loose' ] = 0.0521
deepflavour_wp[2017]['medium'] = 0.3033
deepflavour_wp[2017]['tight' ] = 0.7489

deepflavour_wp[2016] = OrderedDict()
deepflavour_wp[2016]['loose' ] = 0.0614
deepflavour_wp[2016]['medium'] = 0.3093
deepflavour_wp[2016]['tight' ] = 0.7221

years = OrderedDict()
years[2018] = '/afs/cern.ch/work/m/manzoni/HNL/cmg/CMSSW_10_4_0_patch1/src/CMGTools/HNL/cfg/2018/ttbar_for_btag_eff_v3/TTJets_ext/'
# years[2017] = 'FIXME!'
# years[2016] = 'FIXME!'

bins = np.array([20., 30., 50., 70., 100., 150., 200., 400., 1000.])
num = ROOT.TH1F('num', '', len(bins)-1, bins)
den = ROOT.TH1F('den', '', len(bins)-1, bins)

for iyear, idir in years.iteritems():

    files = OrderedDict()
    files['mmm'] = ROOT.TFile.Open('/'.join([idir, 'HNLTreeProducer_mmm', 'tree.root']))
    files['mem'] = ROOT.TFile.Open('/'.join([idir, 'HNLTreeProducer_mem', 'tree.root']))
    files['eee'] = ROOT.TFile.Open('/'.join([idir, 'HNLTreeProducer_eee', 'tree.root']))
    files['eem'] = ROOT.TFile.Open('/'.join([idir, 'HNLTreeProducer_eem', 'tree.root']))

    trees = OrderedDict()

    for k, v in files.iteritems():
        v.cd()
        trees[k] = v.Get('tree')

    flavours = OrderedDict()
    flavours['b'   ] = 'abs(jX_flavour_parton)==5'
    flavours['c'   ] = 'abs(jX_flavour_parton)==4'
    flavours['udsg'] = 'abs(jX_flavour_parton)!=5 & abs(jX_flavour_parton)!=4'

    eta_bins = OrderedDict()
    eta_bins['barrel'] = 'abs(jX_eta)<=1.5'
    eta_bins['endcap'] = 'abs(jX_eta)>1.5 & abs(jX_eta)<2.4'

    all_hists = []

    for ifs, itree in trees.iteritems():
        for iflav, iflavcut in flavours.iteritems():
            for ieta, ietacut in eta_bins.iteritems():
                inum = num.Clone()
                iden = den.Clone()
            
                inum_name = 'num_%s_%s_%s' %(ifs, iflav, ieta)
                iden_name = 'den_%s_%s_%s' %(ifs, iflav, ieta)
            
                print '======> ', inum_name
            
                inum.SetName(inum_name)
                iden.SetName(iden_name)
                        
                itree.Draw('j1_pt >> %s' %iden_name, 'abs(j1_eta)<2.4 & j1_genjet_pt>8 & %s & %s           ' %(ietacut.replace('X', '1'),  iflavcut.replace('X', '1')                                ))
                itree.Draw('j1_pt >> %s' %inum_name, 'abs(j1_eta)<2.4 & j1_genjet_pt>8 & %s & %s & j1_df>%f' %(ietacut.replace('X', '1'),  iflavcut.replace('X', '1'), deepflavour_wp[iyear]['medium']))

                # set the histos obtained for j1 aside
                tmp_num = inum.Clone()
                tmp_den = iden.Clone()

                # get histos for j2
                itree.Draw('j2_pt >> %s' %iden_name, 'abs(j2_eta)<2.4 & j2_genjet_pt>8 & %s & %s           ' %(ietacut.replace('X', '2'),  iflavcut.replace('X', '2')                                ))
                itree.Draw('j2_pt >> %s' %inum_name, 'abs(j2_eta)<2.4 & j2_genjet_pt>8 & %s & %s & j2_df>%f' %(ietacut.replace('X', '2'),  iflavcut.replace('X', '2'), deepflavour_wp[iyear]['medium']))
            
                # add all up
                inum.Add(tmp_num)
                iden.Add(tmp_den)
            
                iratio = inum.Clone()
                iratio.SetName(inum_name.replace('num', 'eff'))
                iratio.Divide(iden)
                iratio.SetMinimum(0.)
                iratio.SetMaximum(1.)
            
                all_hists.append(inum)
                all_hists.append(iden)
                all_hists.append(iratio)

    # OUTPUT
    output_file = ROOT.TFile.Open('btag_deepflavour_wp_medium_efficiencies_%d.root' %iyear, 'recreate')
    output_file.cd()
    for ihist in all_hists:
        ihist.Write()
    output_file.Close()



