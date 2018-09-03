import os
import pickle

import ROOT
from ROOT import gSystem, gROOT

from pdb import set_trace

from CMGTools.HNL.plotter.PlotConfigs import SampleCfg, HistogramCfg
#from CMGTools.HNL.samples.spring16.sms_xsec import get_xsec

from CMGTools.HNL.samples.samples_mc_2017 import hnl_bkg
from CMGTools.HNL.samples.samples_data_2017_noskim import Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F
from CMGTools.HNL.samples.samples_data_2017_noskim import Single_mu_2017B,  Single_mu_2017C,  Single_mu_2017D,  Single_mu_2017E,  Single_mu_2017F
from CMGTools.HNL.samples.samples_mc_2017 import TTJets_amcat, TTJets_mdgrph, DYJetsToLL_M50, DYJetsToLL_M50_ext, WJetsToLNu, W3JetsToLNu, W4JetsToLNu, WLLJJ_WToLNu_EWK, WW_DoubleScattering, WZTo3LNu, ZZTo4L, ZZTo4L_ext
from CMGTools.HNL.samples.signal import HN3L_M_3_V_0p00316227766017_e_onshell  as HN3L_M3_e #.ctau = 14.6 cm
from CMGTools.HNL.samples.signal import HN3L_M_3_V_0p00316227766017_mu_onshell as HN3L_M3_m #.ctau = 14.6 cm
from CMGTools.HNL.samples.signal import HN3L_M_2_V_0p01_e_onshell              as HN3L_M2_e #.ctau = 11.1 cm
from CMGTools.HNL.samples.samples_mc_2017_noskim import DYJetsToLL_M5to50, DYJetsToLL_M50, DY1JetsToLL_M50, DY2JetsToLL_M50, DY2JetsToLL_M50_ext, DY3JetsToLL_M50, DY3JetsToLL_M50_ext
from CMGTools.HNL.samples.samples_mc_2017_noskim import ZZZ, WZZ, WWZ, WWW, WWTo2L2Nu, WGGJets, TTWJetsToLNu, TTZToLLNuNu_M10, TTZToLL_M1To10
from CMGTools.HNL.samples.samples_mc_2017_noskim import ST_s_channel_4f_leptonDecays as ST_sc_4f_lD 
from CMGTools.HNL.samples.samples_mc_2017_noskim import ST_t_channel_antitop_4f_inclusiveDecays as ST_tc_at_4f_incD 
from CMGTools.HNL.samples.samples_mc_2017_noskim import ST_t_channel_top_4f_inclusiveDecays as ST_tc_t_4f_incD
from CMGTools.HNL.samples.samples_mc_2017_noskim import ST_tW_antitop_5f_inclusiveDecays as ST_tW_at_5f_incD
from CMGTools.HNL.samples.samples_mc_2017_noskim import ST_tW_top_5f_inclusiveDecays as ST_tW_t_5f_incD

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


def createSampleLists(analysis_dir='/eos/user/v/vstampf/ntuples/', 
                      channel='e',
                      mode='sm',
                      ztt_cut='', zl_cut='',
                      zj_cut='',
                      data2016G=False,
                      signal_scale=1.,
                      no_data=False):
    tree_prod_name = 'HNLTreeProducer' 
    if channel == 'e':
        data_dir = '/eos/user/m/manzoni/HNL/singleele_e_23_08_2018/'
        bkg_dir = 'bkg_mc_e/'
        sig_dir = 'sig_mc_e/ntuples/'
        dataB = Single_ele_2017B; dataC = Single_ele_2017C; dataD = Single_ele_2017D; dataE = Single_ele_2017E; dataF = Single_ele_2017F; 
    if channel == 'm':
        data_dir = '/eos/user/v/vstampf/ntuples/data_2017_m_noskim/'
        bkg_dir = 'bkg_mc_m/'
        sig_dir = 'sig_mc_m/ntuples/'
        dataB = Single_mu_2017B; dataC = Single_mu_2017C; dataD = Single_mu_2017D; dataE = Single_mu_2017E; dataF = Single_mu_2017F; 

    samples_essential = [
#        SampleCfg(name='DYJets_M50_%s'%channel  , dir_name=DYJetsToLL_M50      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50     .xSection, sumweights=DYJetsToLL_M50     .nGenEvents),
#        SampleCfg(name='DYJets_M50_x_%s'%channel, dir_name=DYJetsToLL_M50_ext  .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50_ext .xSection, sumweights=DYJetsToLL_M50_ext .nGenEvents),
        SampleCfg(name='DYJets_M5T50_%s'%channel, dir_name=DYJetsToLL_M5to50   .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M5to50  .xSection, sumweights=DYJetsToLL_M5to50  .nGenEvents),
        SampleCfg(name='TTJets_amc_%s'%channel  , dir_name=TTJets_amcat        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTJets_amcat       .xSection, sumweights=TTJets_amcat       .nGenEvents),
        SampleCfg(name='WJetsToLNu_%s'%channel  , dir_name=WJetsToLNu          .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WJetsToLNu         .xSection, sumweights=WJetsToLNu         .nGenEvents),        
        SampleCfg(name='ZZTo4L_%s'%channel      , dir_name=ZZTo4L              .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ZZTo4L             .xSection, sumweights=ZZTo4L             .nGenEvents),
        SampleCfg(name='WZTo3LNu_%s'%channel    , dir_name=WZTo3LNu            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WZTo3LNu           .xSection, sumweights=WZTo3LNu           .nGenEvents),
#        SampleCfg(name='TTJets_mdg'          , dir_name=TTJets_mdgrph       .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
#                  xsec=TTJets_mdgrph      .xSection, sumweights=TTJets_mdgrph      .nGenEvents),
        ]


    samples_signal_e = [
        SampleCfg(name='HN3L_M3_e'              , dir_name=HN3L_M3_e           .name, ana_dir=analysis_dir+sig_dir, tree_prod_name=tree_prod_name, xsec=200.0                       , sumweights=HN3L_M3_e          .nGenEvents, is_signal=True)
        ]
    samples_signal_m = [
        SampleCfg(name='HN3L_M3_m'              , dir_name=HN3L_M3_m           .name, ana_dir=analysis_dir+sig_dir, tree_prod_name=tree_prod_name, xsec=200.0                       , sumweights=HN3L_M3_m          .nGenEvents, is_signal=True)
        ]
    
    if channel == 'e': samples_signal = samples_signal_e
    if channel == 'm': samples_signal = samples_signal_m

    samples_essential += samples_signal

    samples_data = [
        SampleCfg(name='data_2017B_%s'%channel          , dir_name=dataB               .name, ana_dir=data_dir           , tree_prod_name=tree_prod_name, is_data=True),    
        SampleCfg(name='data_2017C_%s'%channel          , dir_name=dataC               .name, ana_dir=data_dir           , tree_prod_name=tree_prod_name, is_data=True),  
        SampleCfg(name='data_2017D_%s'%channel          , dir_name=dataD               .name, ana_dir=data_dir           , tree_prod_name=tree_prod_name, is_data=True),                       
        SampleCfg(name='data_2017E_%s'%channel          , dir_name=dataE               .name, ana_dir=data_dir           , tree_prod_name=tree_prod_name, is_data=True),   
        SampleCfg(name='data_2017F_%s'%channel          , dir_name=dataF               .name, ana_dir=data_dir           , tree_prod_name=tree_prod_name, is_data=True),
    ]

    samples_additional = [
        SampleCfg(name='DY1Jets_M50_%s'%channel  , dir_name=DY1JetsToLL_M50      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY1JetsToLL_M50     .xSection, sumweights=DY1JetsToLL_M50     .nGenEvents),
        SampleCfg(name='DY2Jets_M50_%s'%channel  , dir_name=DY2JetsToLL_M50      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY2JetsToLL_M50     .xSection, sumweights=DY2JetsToLL_M50     .nGenEvents),
        SampleCfg(name='DY2Jets_M50_x_%s'%channel, dir_name=DY2JetsToLL_M50_ext  .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY2JetsToLL_M50_ext .xSection, sumweights=DY2JetsToLL_M50_ext .nGenEvents),
        SampleCfg(name='DY3Jets_M50_%s'%channel  , dir_name=DY3JetsToLL_M50      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY3JetsToLL_M50     .xSection, sumweights=DY3JetsToLL_M50     .nGenEvents),
        SampleCfg(name='DY3Jets_M50_x_%s'%channel, dir_name=DY3JetsToLL_M50_ext  .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY3JetsToLL_M50_ext .xSection, sumweights=DY3JetsToLL_M50_ext .nGenEvents),
#        SampleCfg(name='ZZTo4L_ext'          , dir_name=ZZTo4L_ext          .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
#                  xsec=ZZTo4L_ext         .xSection, sumweights=ZZTo4L_ext         .nGenEvents),

#        SampleCfg(name='WZTo3Lnu'            , dir_name=WZTo3LNu            .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
#                  xsec=WZTo3LNu           .xSection, sumweights=WZTo3LNu           .nGenEvents),

#        SampleCfg(name='WW_DoubleScattering' , dir_name=WW_DoubleScattering .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
#                  xsec=WW_DoubleScattering.xSection, sumweights=WW_DoubleScattering.nGenEvents),

#        SampleCfg(name='W3JetsToLNu'         , dir_name=W3JetsToLNu         .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
#                  xsec=W3JetsToLNu        .xSection, sumweights=W3JetsToLNu        .nGenEvents),        

#        SampleCfg(name='W4JetsToLNu'         , dir_name=W4JetsToLNu         .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
#                  xsec=W4JetsToLNu        .xSection        , sumweights=W4JetsToLNu.nGenEvents),        

#        SampleCfg(name='WLLJJ_WToLNu_EWK'    , dir_name=WLLJJ_WToLNu_EWK    .name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
#                  xsec=WLLJJ_WToLNu_EWK   .xSection, sumweights=WLLJJ_WToLNu_EWK   .nGenEvents),        
 ]

    samples_rare = [
        SampleCfg(name='ZZZ_%s'%channel    , dir_name=ZZZ            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ZZZ           .xSection, sumweights=ZZZ           .nGenEvents),
        SampleCfg(name='WZZ_%s'%channel    , dir_name=WZZ            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WZZ           .xSection, sumweights=WZZ           .nGenEvents),
        SampleCfg(name='WWZ_%s'%channel    , dir_name=WWZ            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WWZ           .xSection, sumweights=WWZ           .nGenEvents),
        SampleCfg(name='WWW_%s'%channel    , dir_name=WWW            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WWW           .xSection, sumweights=WWW           .nGenEvents),
        SampleCfg(name='WWTo2L2Nu_%s'%channel    , dir_name=WWTo2L2Nu            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WWTo2L2Nu           .xSection, sumweights=WWTo2L2Nu           .nGenEvents),
        SampleCfg(name='WGGJets_%s'%channel    , dir_name=WGGJets            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WGGJets           .xSection, sumweights=WGGJets           .nGenEvents),
        SampleCfg(name='TTWJetsToLNu_%s'%channel    , dir_name=TTWJetsToLNu            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTWJetsToLNu           .xSection, sumweights=TTWJetsToLNu           .nGenEvents),
        SampleCfg(name='TTZToLLNuNu_M10_%s'%channel  , dir_name=TTZToLLNuNu_M10            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTZToLLNuNu_M10           .xSection, sumweights=TTZToLLNuNu_M10           .nGenEvents),
        SampleCfg(name='TTZToLL_M1To10_%s'%channel    , dir_name=TTZToLL_M1To10            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTZToLL_M1To10           .xSection, sumweights=TTZToLL_M1To10           .nGenEvents),
        SampleCfg(name='ST_sc_4f_lD_%s'%channel       , dir_name=ST_sc_4f_lD            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ST_sc_4f_lD           .xSection, sumweights=ST_sc_4f_lD           .nGenEvents),
        SampleCfg(name='ST_tc_at_4f_incD_%s'%channel    , dir_name=ST_tc_at_4f_incD            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ST_tc_at_4f_incD           .xSection, sumweights=ST_tc_at_4f_incD           .nGenEvents),
        SampleCfg(name='ST_tc_t_4f_incD_%s'%channel    , dir_name=ST_tc_t_4f_incD            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ST_tc_t_4f_incD           .xSection, sumweights=ST_tc_t_4f_incD           .nGenEvents),
        SampleCfg(name='ST_tW_at_5f_incD_%s'%channel    , dir_name=ST_tW_at_5f_incD            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ST_tW_at_5f_incD           .xSection, sumweights=ST_tW_at_5f_incD           .nGenEvents),
        SampleCfg(name='ST_tW_t_5f_incD_%s'%channel    , dir_name=ST_tW_t_5f_incD            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ST_tW_t_5f_incD           .xSection, sumweights=ST_tW_t_5f_incD           .nGenEvents),
    ]  

    samples_additional += samples_rare

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
