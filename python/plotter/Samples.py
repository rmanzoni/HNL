import os
import pickle

import ROOT
from ROOT import gSystem, gROOT
from collections import OrderedDict

from pdb import set_trace

from CMGTools.HNL.plotter.PlotConfigs import SampleCfg, HistogramCfg

from CMGTools.HNL.samples.samples_mc_2017          import hnl_bkg
from CMGTools.HNL.samples.samples_mc_2017          import TTJets_amcat, TTJets_mdgrph, DYJetsToLL_M50, DYJetsToLL_M50_ext, WJetsToLNu, W3JetsToLNu, W4JetsToLNu, WLLJJ_WToLNu_EWK, WW_DoubleScattering, WZTo3LNu, ZZTo4L, ZZTo4L_ext
from CMGTools.HNL.samples.samples_mc_2017_noskim   import DYJetsToLL_M5to50, DYJetsToLL_M50, DY1JetsToLL_M50, DY2JetsToLL_M50, DY2JetsToLL_M50_ext, DY3JetsToLL_M50, DY3JetsToLL_M50_ext
from CMGTools.HNL.samples.samples_mc_2017_noskim   import ZZZ, WZZ, WWZ, WWW, WWTo2L2Nu, WGGJets, TTWJetsToLNu, TTZToLL_M10, TTZToLL_M1to10, ST_sch_lep, STbar_tch_inc, ST_tch_inc, STbar_tW_inc, ST_tW_inc
from CMGTools.HNL.samples.samples_data_2017_noskim import Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F
from CMGTools.HNL.samples.samples_data_2017_noskim import Single_mu_2017B,  Single_mu_2017C,  Single_mu_2017D,  Single_mu_2017E,  Single_mu_2017F
from CMGTools.HNL.samples.samples_mc_2017_noskim   import QCD_pt_15to20_em, QCD_pt_20to30_em, QCD_pt_30to50_em, QCD_pt_50to80_em, QCD_pt_120to170_em, QCD_pt_300toInf_em    
from CMGTools.HNL.samples.samples_mc_2017_noskim   import QCD_pt_15to20_mu,  QCD_pt_20to30_mu, QCD_pt_30to50_mu, QCD_pt_50to80_mu, QCD_pt_80to120_mu 
from CMGTools.HNL.samples.samples_mc_2017_noskim   import QCD_pt_20to30_bcToE, QCD_pt_30to80_bcToE, QCD_pt_80to170_bcToE, QCD_pt_170to250_bcToE, QCD_pt_250toInf_bcToE 
#from CMGTools.HNL.samples.signal                   import HN3L_M_3_V_0p00316227766017_e_onshell  as HN3L_M3_e #.ctau = 14.6 cm
#from CMGTools.HNL.samples.signal                   import HN3L_M_3_V_0p00316227766017_mu_onshell as HN3L_M3_m #.ctau = 14.6 cm
#from CMGTools.HNL.samples.signal                   import HN3L_M_2_V_0p01_e_onshell              as HN3L_M2_e #.ctau = 11.1 cm
#FIXME UPDATE SAMPLES TO NEW VERSION

if "/sDYReweighting_cc.so" not in gSystem.GetLibraries(): 
    gROOT.ProcessLine(".L %s/src/CMGTools/HNL/python/plotter/DYReweighting.cc+" % os.environ['CMSSW_BASE']);
    from ROOT import getDYWeight

splitDY = False
useDYWeight = False

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
                      signal_scale=200,
                      no_data=False,
                      tree_prod_name='HNLTreeProducer', 
                      add_data_cut=None,
                      add_mc_cut=None): 
    
    if channel == 'e':
#        data_dir = '/eos/user/m/manzoni/HNL/singleele_e_23_08_2018/'              # first version
        data_dir = '/eos/user/v/vstampf/ntuples/data_2017_e_noskim/partial_hadd/'  # 9/13 production including met filters and masses between vetoing leps and 3l
        qcd_dir = 'bkg_mc_e/qcd/'
        bkg_dir = 'bkg_mc_e/'
        sig_dir = 'sig_mc_e/ntuples/'
        dataB = Single_ele_2017B; dataC = Single_ele_2017C; dataD = Single_ele_2017D; dataE = Single_ele_2017E; dataF = Single_ele_2017F; 
    if channel == 'm':
        data_dir = '/eos/user/v/vstampf/ntuples/data_2017_m_noskim/'
        qcd_dir = 'bkg_mc_m/qcd/'
        bkg_dir = 'bkg_mc_m/'
        sig_dir = 'sig_mc_m/ntuples/'
        dataB = Single_mu_2017B; dataC = Single_mu_2017C; dataD = Single_mu_2017D; dataE = Single_mu_2017E; dataF = Single_mu_2017F; 

    samples_essential = [
        SampleCfg(name='DYJetsToLL_M5to50', dir_name=DYJetsToLL_M5to50 .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M5to50 .xSection, sumweights=DYJetsToLL_M5to50 .nGenEvents),
        SampleCfg(name='DYJets_ext'       , dir_name=DYJetsToLL_M50_ext.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50_ext.xSection, sumweights=DYJetsToLL_M50_ext.nGenEvents),
        SampleCfg(name='TTJets_amc'       , dir_name=TTJets_amcat      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTJets_amcat      .xSection, sumweights=TTJets_amcat      .nGenEvents),
        SampleCfg(name='WJetsToLNu'       , dir_name=WJetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WJetsToLNu        .xSection, sumweights=WJetsToLNu        .nGenEvents),        
        SampleCfg(name='ZZTo4L'           , dir_name=ZZTo4L            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ZZTo4L            .xSection, sumweights=ZZTo4L            .nGenEvents),
        SampleCfg(name='WZTo3LNu'         , dir_name=WZTo3LNu          .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WZTo3LNu          .xSection, sumweights=WZTo3LNu          .nGenEvents),
    ]

    samples_signal_e = [
#        SampleCfg(name='HN3L_M3' , dir_name=HN3L_M3_e.name, ana_dir=analysis_dir+sig_dir, tree_prod_name=tree_prod_name, xsec=signal_scale, sumweights=HN3L_M3_e.nGenEvents, is_signal=True)
    ]
    samples_signal_m = [
#        SampleCfg(name='HN3L_M3'              , dir_name=HN3L_M3_m           .name, ana_dir=analysis_dir+sig_dir, tree_prod_name=tree_prod_name, xsec=200.0                       , sumweights=HN3L_M3_m          .nGenEvents, is_signal=True)

    ]
    if channel == 'e': samples_signal = samples_signal_e
    if channel == 'm': samples_signal = samples_signal_m

    samples_essential += samples_signal

    samples_data = [
        SampleCfg(name='data_2017B', dir_name=dataB.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                          
        SampleCfg(name='data_2017C', dir_name=dataC.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                          
        SampleCfg(name='data_2017D', dir_name=dataD.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                          
        SampleCfg(name='data_2017E', dir_name=dataE.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                          
        SampleCfg(name='data_2017F', dir_name=dataF.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),
    ]

    samples_additional = [
        SampleCfg(name='DYJets'           , dir_name=DYJetsToLL_M50    .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50    .xSection, sumweights=DYJetsToLL_M50    .nGenEvents),
#        SampleCfg(name='DY1Jets_M50'        , dir_name=DY1JetsToLL_M50      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY1JetsToLL_M50     .xSection, sumweights=DY1JetsToLL_M50     .nGenEvents),
#        SampleCfg(name='DY2Jets_M50'        , dir_name=DY2JetsToLL_M50      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY2JetsToLL_M50     .xSection, sumweights=DY2JetsToLL_M50     .nGenEvents),
#        SampleCfg(name='DY2Jets_M50_ext'    , dir_name=DY2JetsToLL_M50_ext  .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY2JetsToLL_M50_ext .xSection, sumweights=DY2JetsToLL_M50_ext .nGenEvents),
#        SampleCfg(name='DY3Jets_M50'        , dir_name=DY3JetsToLL_M50      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY3JetsToLL_M50     .xSection, sumweights=DY3JetsToLL_M50     .nGenEvents),
#        SampleCfg(name='DY3Jets_M50_ext'    , dir_name=DY3JetsToLL_M50_ext  .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY3JetsToLL_M50_ext .xSection, sumweights=DY3JetsToLL_M50_ext .nGenEvents),
        SampleCfg(name='ZZZ'                , dir_name=ZZZ                .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ZZZ                .xSection, sumweights=ZZZ                .nGenEvents),
        SampleCfg(name='WZZ'                , dir_name=WZZ                .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WZZ                .xSection, sumweights=WZZ                .nGenEvents),
        SampleCfg(name='WWZ'                , dir_name=WWZ                .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WWZ                .xSection, sumweights=WWZ                .nGenEvents),
        SampleCfg(name='WWW'                , dir_name=WWW                .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WWW                .xSection, sumweights=WWW                .nGenEvents),
        SampleCfg(name='WGGJets'            , dir_name=WGGJets            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WGGJets            .xSection, sumweights=WGGJets            .nGenEvents),
        SampleCfg(name='TTWJetsToLNu'       , dir_name=TTWJetsToLNu       .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTWJetsToLNu       .xSection, sumweights=TTWJetsToLNu       .nGenEvents),
        SampleCfg(name='TTZToLL_M10'        , dir_name=TTZToLL_M10        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTZToLL_M10        .xSection, sumweights=TTZToLL_M10        .nGenEvents),
        SampleCfg(name='TTZToLL_M1to10'     , dir_name=TTZToLL_M1to10     .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTZToLL_M1to10     .xSection, sumweights=TTZToLL_M1to10     .nGenEvents),
        SampleCfg(name='ST_sch_lep'         , dir_name=ST_sch_lep         .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ST_sch_lep         .xSection, sumweights=ST_sch_lep         .nGenEvents),
        SampleCfg(name='STbar_tch_inc'      , dir_name=STbar_tch_inc      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=STbar_tch_inc      .xSection, sumweights=STbar_tch_inc      .nGenEvents),
        SampleCfg(name='ST_tch_inc'         , dir_name=ST_tch_inc         .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ST_tch_inc         .xSection, sumweights=ST_tch_inc         .nGenEvents),
        SampleCfg(name='STbar_tW_inc'       , dir_name=STbar_tW_inc       .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=STbar_tW_inc       .xSection, sumweights=STbar_tW_inc       .nGenEvents),
        SampleCfg(name='ST_tW_inc'          , dir_name=ST_tW_inc          .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ST_tW_inc          .xSection, sumweights=ST_tW_inc          .nGenEvents),
#         SampleCfg(name='ZZTo4L_ext'         , dir_name=ZZTo4L_ext         .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ZZTo4L_ext         .xSection, sumweights=ZZTo4L_ext         .nGenEvents),
        SampleCfg(name='WWTo2L2Nu'        , dir_name=WWTo2L2Nu         .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WWTo2L2Nu         .xSection, sumweights=WWTo2L2Nu         .nGenEvents),
#         SampleCfg(name='WW_DoubleScattering', dir_name=WW_DoubleScattering.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WW_DoubleScattering.xSection, sumweights=WW_DoubleScattering.nGenEvents),
#         SampleCfg(name='W3JetsToLNu'        , dir_name=W3JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W3JetsToLNu        .xSection, sumweights=W3JetsToLNu        .nGenEvents),        
#         SampleCfg(name='W4JetsToLNu'        , dir_name=W4JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W4JetsToLNu        .xSection, sumweights=W4JetsToLNu        .nGenEvents),        
#         SampleCfg(name='WLLJJ_WToLNu_EWK'   , dir_name=WLLJJ_WToLNu_EWK   .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WLLJJ_WToLNu_EWK   .xSection, sumweights=WLLJJ_WToLNu_EWK   .nGenEvents),        
    ]

    samples_qcd_e = [
        SampleCfg(name='QCD_pt_20to30_bcToE', dir_name=QCD_pt_20to30_bcToE.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_20to30_bcToE.xSection, sumweights=QCD_pt_20to30_bcToE.nGenEvents),
        SampleCfg(name='QCD_pt_30to80_bcToE', dir_name=QCD_pt_30to80_bcToE.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_30to80_bcToE.xSection, sumweights=QCD_pt_30to80_bcToE.nGenEvents),
        SampleCfg(name='QCD_pt_80to170_bcToE', dir_name=QCD_pt_80to170_bcToE.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_80to170_bcToE.xSection, sumweights=QCD_pt_80to170_bcToE.nGenEvents),
        SampleCfg(name='QCD_pt_170to250_bcToE', dir_name=QCD_pt_170to250_bcToE.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_170to250_bcToE.xSection, sumweights=QCD_pt_170to250_bcToE.nGenEvents),
        SampleCfg(name='QCD_pt_250toInf_bcToE', dir_name=QCD_pt_250toInf_bcToE.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_250toInf_bcToE.xSection, sumweights=QCD_pt_250toInf_bcToE.nGenEvents),
        SampleCfg(name='QCD_pt_15to20_em', dir_name=QCD_pt_15to20_em.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_15to20_em.xSection, sumweights=QCD_pt_15to20_em.nGenEvents),
        SampleCfg(name='QCD_pt_20to30_em', dir_name=QCD_pt_20to30_em.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_20to30_em.xSection, sumweights=QCD_pt_20to30_em.nGenEvents),
        SampleCfg(name='QCD_pt_30to50_em', dir_name=QCD_pt_30to50_em.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_30to50_em.xSection, sumweights=QCD_pt_30to50_em.nGenEvents),
        SampleCfg(name='QCD_pt_50to80_em', dir_name=QCD_pt_50to80_em.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_50to80_em.xSection, sumweights=QCD_pt_50to80_em.nGenEvents),
#        SampleCfg(name='QCD_pt_80to120_em', dir_name=QCD_pt_80to120_em.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_80to120_em.xSection, sumweights=QCD_pt_80to120_em.nGenEvents),  #NOT IN DAS
        SampleCfg(name='QCD_pt_120to170_em', dir_name=QCD_pt_120to170_em.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_120to170_em.xSection, sumweights=QCD_pt_120to170_em.nGenEvents),
        SampleCfg(name='QCD_pt_300toInf_em', dir_name=QCD_pt_300toInf_em.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_300toInf_em.xSection, sumweights=QCD_pt_300toInf_em.nGenEvents),
    ]


    samples_qcd_mu = [
        SampleCfg(name='QCD_pt_15to20_mu', dir_name=QCD_pt_15to20_mu.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_15to20_mu.xSection, sumweights=QCD_pt_15to20_mu.nGenEvents),
        SampleCfg(name='QCD_pt_20to30_mu', dir_name=QCD_pt_20to30_mu.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_20to30_mu.xSection, sumweights=QCD_pt_20to30_mu.nGenEvents),
        SampleCfg(name='QCD_pt_30to50_mu', dir_name=QCD_pt_30to50_mu.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_30to50_mu.xSection, sumweights=QCD_pt_30to50_mu.nGenEvents),
        SampleCfg(name='QCD_pt_50to80_mu', dir_name=QCD_pt_50to80_mu.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_50to80_mu.xSection, sumweights=QCD_pt_50to80_mu.nGenEvents),
        SampleCfg(name='QCD_pt_80to120_mu', dir_name=QCD_pt_80to120_mu.name, ana_dir=analysis_dir+qcd_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_80to120_mu.xSection, sumweights=QCD_pt_80to120_mu.nGenEvents),
    ]
  
    samples_additional += samples_qcd_e

    samples_mc  = samples_essential + samples_additional 
    samples     = samples_essential + samples_additional + samples_data
    if channel == 'm':
        samples_mc = samples_essential + samples_qcd_mu
    all_samples = samples_mc + samples_data

    # RM: this is needed to retrieve the sum of weights *before* any selection
    # FIXME! on hold now until SkimAnalyzerCount is fixed. Otherwise the code runs.
    # to activate it, simply comment out the sample names in weighted_list

    weighted_list = [
       'HN3L_M3'            ,
       'DYJetsToLL_M5to50'  ,
       'DYJets'             ,
       'DYJets_ext'         ,
       'DY1Jets_M50'        ,
       'DY2Jets_M50'        ,
       'DY2Jets_M50_ext'    ,
       'DY3Jets_M50'        ,
       'DY3Jets_M50_ext'    ,
       'TTJets_amc'         ,
       'WJetsToLNu'         ,
       'ZZTo4L'             ,
       'WZTo3LNu'           ,
       'WWTo2L2Nu'          ,
       'ZZZ'                ,
       'WZZ'                ,
       'WWZ'                ,
       'WWW'                ,
       'WGGJets'            ,
       'TTWJetsToLNu'       ,
       'TTZToLL_M10'        ,
       'TTZToLL_M1to10'     ,
       'ST_sch_lep'         ,
       'STbar_tch_inc'      ,
       'ST_tch_inc'         ,
       'STbar_tW_inc'       ,
       'ST_tW_inc'          ,
       'ZZTo4L_ext'         ,
       'WW_DoubleScattering',
       'W3JetsToLNu'        ,
       'W4JetsToLNu'        ,
       'WLLJJ_WToLNu_EWK'   ,
    ]

    # RM hand made patch!
    initial_weights = OrderedDict()
    initial_weights['HN3L_M3'            ] = 1.
    initial_weights['DYJetsToLL_M5to50'  ] = 0.9992
    initial_weights['DYJets'             ] = 0.6777
    initial_weights['DYJets_ext'         ] = 0.6777
    initial_weights['DY1Jets_M50'        ] = 0.9992
    initial_weights['DY2Jets_M50'        ] = 0.9989
    initial_weights['DY2Jets_M50_ext'    ] = 0.9990
    initial_weights['DY3Jets_M50'        ] = 0.9986
    initial_weights['DY3Jets_M50_ext'    ] = 0.9985
    initial_weights['TTJets_amc'         ] = 0.3733
    initial_weights['WJetsToLNu'         ] = 0.9992
    initial_weights['ZZTo4L'             ] = 0.9899
    initial_weights['WZTo3LNu'           ] = 0.6268
    initial_weights['WWTo2L2Nu'          ] = 0.9959
    initial_weights['ZZZ'                ] = 0.8541
    initial_weights['WZZ'                ] = 0.8786
    initial_weights['WWZ'                ] = 0.8865
    initial_weights['WWW'                ] = 0.8770
    initial_weights['WGGJets'            ] = 0.9988
    initial_weights['TTWJetsToLNu'       ] = 0.5438
    initial_weights['TTZToLL_M10'        ] = 0.4721 
    initial_weights['TTZToLL_M1to10'     ] = 0.5248
    initial_weights['ST_sch_lep'         ] = 0.6240
    initial_weights['STbar_tch_inc'      ] = 1.
    initial_weights['ST_tch_inc'         ] = 1.
    initial_weights['STbar_tW_inc'       ] = 0.9924
    initial_weights['ST_tW_inc'          ] = 0.9923
    initial_weights['ZZTo4L_ext'         ] = 0.9899
    initial_weights['WW_DoubleScattering'] = 1.0000
    initial_weights['W3JetsToLNu'        ] = 0.9984
    initial_weights['W4JetsToLNu'        ] = 0.9973
    initial_weights['WLLJJ_WToLNu_EWK'   ] = 0.9928

    for sample in samples_mc:
#         print 'A: Set sum weights for sample', sample.name, 'to', sample.sumweights        
        if sample.name in weighted_list:
            sample.sumweights *= initial_weights[sample.name]
#         print 'B: Set sum weights for sample', sample.name, 'to', sample.sumweights

    for sample in samples_mc:
        if sample.name not in weighted_list:
#            pass # turn this off later, for NLO or higher order samples
            # print 'Set sum weights for sample', sample.name, 'to', sample.sumweights
            setSumWeights(sample, 'SkimAnalyzerCount', False)
            print 'Set sum weights for sample', sample.name, 'to', sample.sumweights

    # sampleDict = {s.name: s for s in all_samples}
    sampleDict = {}
    for s in all_samples:
        sampleDict[s.name] = s

#    for sample in all_samples:
#        if sample.is_signal:
#            sample.scale = sample.scale * signal_scale

    return samples_mc, samples_data, samples, all_samples, sampleDict

def setSumWeights(sample, weight_dir='SkimAnalyzerCount', norm=True):
    if isinstance(sample, HistogramCfg) or sample.is_data:
        return
    
    pckfile = '/'.join([sample.ana_dir, sample.dir_name, weight_dir, 'SkimReport.pck'])
    try:
        pckobj = pickle.load(open(pckfile, 'r'))
        counters = dict(pckobj)
        if norm:
            if 'Sum Norm Weights' in counters:
                sample.sumweights = counters['Sum Weights']
        else:
            if 'Sum Weights' in counters:
                sample.sumweights = counters['Sum Weights']
    except IOError:
        print 'Warning: could not find sum weights information for sample', sample.name
        pass
