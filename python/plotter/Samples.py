import os
import pickle

import ROOT
from ROOT import gSystem, gROOT

from CMGTools.HNL.plotter.PlotConfigs import SampleCfg, HistogramCfg
#from CMGTools.HNL.samples.spring16.sms_xsec import get_xsec

from CMGTools.HNL.samples.samples_mc_2017 import hnl_bkg
from CMGTools.HNL.samples.samples_mc_2017 import TTJets_amcat, TTJets_mdgrph, DYJetsToLL_M50, DYJetsToLL_M50_ext, WJetsToLNu, W3JetsToLNu, W4JetsToLNu, WLLJJ_WToLNu_EWK, WW_DoubleScattering, WZTo3LNu, ZZTo4L, ZZTo4L_ext

if "/sDYReweighting_cc.so" not in gSystem.GetLibraries(): 
    gROOT.ProcessLine(".L %s/src/CMGTools/HNL/python/plotter/DYReweighting.cc+" % os.environ['CMSSW_BASE']);
    from ROOT import getDYWeight

splitDY = False
useDYWeight = False
# data2016G = True

if useDYWeight or splitDY:
    dy_exps = []
    if splitDY:
        for njet in xrange(0, 5):
            weight = dy_weight_dict[njet]
            dy_exps.append('(geninfo_nup == {njet})*{weight}'.format(njet=njet, weight=weight))
            # dy_exps.append('(geninfo_nup == {njet} && (geninfo_invmass<150. || !(l2_gen_match==5 || l1_gen_lepfromtau)))*{weight}'.format(njet=njet, weight=weight))
            # weight = dy_weight_dict[(njet, 150)]
            # dy_exps.append('(geninfo_nup == {njet} && (geninfo_invmass>=150. && (l2_gen_match==5 || l1_gen_lepfromtau)))*{weight}'.format(njet=njet, weight=weight))
    # if useDYWeight:
    #     dy_exps.append('')
    dy_exp = '*({})'.format(' + '.join(dy_exps))
    if useDYWeight:
        dy_exp += '*getDYWeight(genboson_mass, genboson_pt)'
    print 'Using DY expression', dy_exp

w_exps = []
# for njet in xrange(0, 5):
#     weight = w_weight_dict[njet]
#     w_exps.append('(geninfo_nup == {njet})*{weight}'.format(njet=njet, weight=weight))
# 
# w_exp = '({w})'.format(w=' + '.join(w_exps))


def createSampleLists(analysis_dir='/eos/user/v/vstampf/ntuples/bkg_mc_prompt_e/', #'/afs/cern.ch/user/v/vstampf/work/public/prod',
                      channel='e',
                      mode='sm',
                      ztt_cut='', zl_cut='',
                      zj_cut='',
                      data2016G=False,
                      signal_scale=1.,
                      no_data=False):
    if channel == 'e':
        tree_prod_name = 'HNLTreeProducerPromptEle' 
    if channel == 'mu':
        tree_prod_name = 'HNLTreeProducerPromptMu' 

    samples_essential = [
        SampleCfg(name='DYJets'              , dir_name=DYJetsToLL_M50      .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=DYJetsToLL_M50     .xSection, sumweights=DYJetsToLL_M50     .nGenEvents),

        SampleCfg(name='DYJets_ext'          , dir_name=DYJetsToLL_M50_ext  .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=DYJetsToLL_M50_ext .xSection, sumweights=DYJetsToLL_M50_ext .nGenEvents),

        SampleCfg(name='TTJets_amc'          , dir_name=TTJets_amcat        .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=TTJets_amcat       .xSection, sumweights=TTJets_amcat       .nGenEvents),

        SampleCfg(name='TTJets_mdg'          , dir_name=TTJets_mdgrph       .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=TTJets_mdgrph      .xSection, sumweights=TTJets_mdgrph      .nGenEvents),

#        SampleCfg(name='WJetsToLNu'          , dir_name=WJetsToLNu          .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
#                  xsec=WJetsToLNu         .xSection, sumweights=WJetsToLNu         .nGenEvents),        
        ]

    # FIXME
    samples_data = [
        SampleCfg(name='Data'                , dir_name=DYJetsToLL_M50_ext  .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=DYJetsToLL_M50_ext .xSection, sumweights=DYJetsToLL_M50_ext .nGenEvents, is_data=True),
    ]
    
    samples_additional = [
        SampleCfg(name='ZZTo4L'              , dir_name=ZZTo4L              .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=ZZTo4L             .xSection, sumweights=ZZTo4L             .nGenEvents),

        SampleCfg(name='ZZTo4L_ext'          , dir_name=ZZTo4L_ext          .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=ZZTo4L_ext         .xSection, sumweights=ZZTo4L_ext         .nGenEvents),

        SampleCfg(name='WZTo3Lnu'            , dir_name=WZTo3LNu            .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=WZTo3LNu           .xSection, sumweights=WZTo3LNu           .nGenEvents),

        SampleCfg(name='WW_DoubleScattering' , dir_name=WW_DoubleScattering .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=WW_DoubleScattering.xSection, sumweights=WW_DoubleScattering.nGenEvents),

        SampleCfg(name='W3JetsToLNu'         , dir_name=W3JetsToLNu         .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=W3JetsToLNu        .xSection, sumweights=W3JetsToLNu        .nGenEvents),        

        SampleCfg(name='W4JetsToLNu'         , dir_name=W4JetsToLNu         .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=W4JetsToLNu        .xSection        , sumweights=W4JetsToLNu.nGenEvents),        

        SampleCfg(name='WLLJJ_WToLNu_EWK'    , dir_name=WLLJJ_WToLNu_EWK    .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=WLLJJ_WToLNu_EWK   .xSection, sumweights=WLLJJ_WToLNu_EWK   .nGenEvents),        
 ]

    samples_mc = samples_essential + samples_additional 
    samples = samples_essential + samples_additional + samples_data
    all_samples = samples_mc + samples_data

    weighted_list = []

    for sample in samples_mc:
        if sample.name not in weighted_list:
            setSumWeights(sample, 'MCWeighter' if channel not in ['tau_fr'] else 'SkimAnalyzerCount')
            print 'Set sum weights for sample', sample.name, 'to', sample.sumweights

    # sampleDict = {s.name: s for s in all_samples}
    sampleDict = {}
    for s in all_samples:
        sampleDict[s.name] = s

    for sample in all_samples:
        if sample.is_signal:
            sample.scale = sample.scale * signal_scale

    return samples_mc, samples_data, samples, all_samples, sampleDict

def setSumWeights(sample, weight_dir='MCWeighter'):
    if isinstance(sample, HistogramCfg) or sample.is_data:
        return

    pckfile = '/'.join([sample.ana_dir, sample.dir_name, weight_dir, 'SkimReport.pck'])
    try:
        pckobj = pickle.load(open(pckfile, 'r'))
        counters = dict(pckobj)
        if 'Sum Weights' in counters:
            sample.sumweights = counters['Sum Weights']
    except IOError:
        # print 'Warning: could not find sum weights information for sample', sample.name
        pass
