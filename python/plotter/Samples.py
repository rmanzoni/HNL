import os
import pickle

import ROOT
from ROOT import gSystem, gROOT
from collections import OrderedDict

from pdb import set_trace

from CMGTools.HNL.plotter.PlotConfigs import SampleCfg, HistogramCfg

from CMGTools.HNL.samples.samples_mc_2017          import hnl_bkg
from CMGTools.HNL.samples.samples_mc_2017          import TTJets_amcat, TTJets_mdgrph, DYJetsToLL_M50, DYJetsToLL_M50_ext, WJetsToLNu, W3JetsToLNu, W4JetsToLNu, WLLJJ_WToLNu_EWK, WW_DoubleScattering, WZTo3LNu, ZZTo4L, ZZTo4L_ext
from CMGTools.HNL.samples.samples_mc_2017_noskim   import DYBB, DYJetsToLL_M10to50,DYJetsToLL_M50, DY1JetsToLL_M50, DY2JetsToLL_M50, DY2JetsToLL_M50_ext, DY3JetsToLL_M50, DY3JetsToLL_M50_ext
# from CMGTools.HNL.samples.samples_mc_2017_noskim   import DYBB, DYJetsToLL_M50, DY1JetsToLL_M50, DY2JetsToLL_M50, DY2JetsToLL_M50_ext, DY3JetsToLL_M50, DY3JetsToLL_M50_ext
from CMGTools.HNL.samples.samples_mc_2017_noskim   import ZZZ, WZZ, WWZ, WWW, WWTo2L2Nu, WGGJets, TTWJetsToLNu, TTZToLL_M10, TTZToLL_M1to10, ST_sch_lep, STbar_tch_inc, ST_tch_inc, STbar_tW_inc, ST_tW_inc
from CMGTools.HNL.samples.samples_data_2017_noskim import Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F
from CMGTools.HNL.samples.samples_data_2017_noskim import Single_mu_2017B,  Single_mu_2017C,  Single_mu_2017D,  Single_mu_2017E,  Single_mu_2017F
from CMGTools.HNL.samples.samples_mc_2017_noskim   import QCD_pt_15to20_em, QCD_pt_20to30_em, QCD_pt_30to50_em, QCD_pt_50to80_em, QCD_pt_120to170_em, QCD_pt_300toInf_em    
from CMGTools.HNL.samples.samples_mc_2017_noskim   import QCD_pt_15to20_mu,  QCD_pt_20to30_mu, QCD_pt_30to50_mu, QCD_pt_50to80_mu, QCD_pt_80to120_mu 
from CMGTools.HNL.samples.samples_mc_2017_noskim   import QCD_pt_20to30_bcToE, QCD_pt_30to80_bcToE, QCD_pt_80to170_bcToE, QCD_pt_170to250_bcToE, QCD_pt_250toInf_bcToE 
from CMGTools.HNL.samples.signal_old               import HN3L_M_3_V_0p00316227766017_e_onshell  as HN3L_M3_e #.ctau = 14.6 cm
#from CMGTools.HNL.samples.signal                   import HN3L_M_3_V_0p00316227766017_mu_onshell as HN3L_M3_m #.ctau = 14.6 cm
#from CMGTools.HNL.samples.signal                   import HN3L_M_2_V_0p01_e_onshell              as HN3L_M2_e #.ctau = 11.1 cm
from CMGTools.HNL.samples.signal import all_signals_e

#FIXME UPDATE SAMPLES TO NEW VERSION
from CMGTools.HNL.samples.samples_mc_2017_noskim   import W1JetsToLNu, W2JetsToLNu


def createSampleLists(analysis_dir='/eos/user/v/vstampf/ntuples/', 
                      server='t3',
                      channel='emm',
                      signal_scale=0.09,#27.0,#200.0,#0.09,
                      no_data=True,
                      tree_prod_name='HNLTreeProducer', 
                      add_data_cut=None,
                      add_mc_cut=None):
    
    if channel == 'emm':
#        data_dir = '/eos/user/m/manzoni/HNL/singleele_e_23_08_2018/'              # first version
        # data_dir = '/eos/user/v/vstampf/ntuples/data_2017_e_noskim/partial_hadd/'  # 9/13 production including met filters and masses between vetoing leps and 3l
        if server == 'lxplus':
            data_dir = '/eos/user/v/vstampf/ntuples/data_2017_e_noskim/'
            bkg_dir = 'bkg_mc_e/'
            sig_dir = 'sig_mc_e/ntuples/'
            DY_dir  = '/eos/user/v/vstampf/ntuples/DDE_v0/prompt_e/'
        if server == 't3':
            data_dir = analysis_dir + 'data/'
            bkg_dir = 'background'
            sig_dir = 'signal'
            # DY_dir  = '/eos/user/v/vstampf/ntuples/DDE_v0/prompt_e/'
        dataB = Single_ele_2017B; dataC = Single_ele_2017C; dataD = Single_ele_2017D; dataE = Single_ele_2017E; dataF = Single_ele_2017F; 

    if channel == 'mmm':
        if server == 'lxplus':
            data_dir = '/eos/user/v/vstampf/ntuples/data_2017_m_noskim/'
            bkg_dir = 'bkg_mc_m/'
            sig_dir = 'sig_mc_m/ntuples/'
            DY_dir = analysis_dir + bkg_dir
        if server == 't3':
            # data_dir = analysis_dir + 'data/'
            data_dir = 'root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/data/'
            bkg_dir = 'background'
            sig_dir = 'signal/ntuples'
            DY_dir = analysis_dir + bkg_dir

        dataB = Single_mu_2017B; dataC = Single_mu_2017C; dataD = Single_mu_2017D; dataE = Single_mu_2017E; dataF = Single_mu_2017F; 

    samples_essential = [
        SampleCfg(name='DYJetsToLL_M10to50', dir_name=DYJetsToLL_M10to50 .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M10to50 .xSection, sumweights=DYJetsToLL_M10to50 .nGenEvents, is_MC=True),
        # SampleCfg(name='DYJetsToLL_M10to50_ext', dir_name=DYJetsToLL_M10to50_ext .name, ana_dir=DY_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M10to50_ext .xSection, sumweights=DYJetsToLL_M10to50_ext .nGenEvents, is_MC=True),
        SampleCfg(name='DYJets_ext'       , dir_name=DYJetsToLL_M50_ext.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50_ext.xSection, sumweights=DYJetsToLL_M50_ext.nGenEvents, is_MC=True),
        SampleCfg(name='TTJets_amc'       , dir_name=TTJets_amcat      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTJets_amcat      .xSection, sumweights=TTJets_amcat      .nGenEvents, is_MC=True),
        SampleCfg(name='ZZTo4L'           , dir_name=ZZTo4L            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ZZTo4L            .xSection, sumweights=ZZTo4L            .nGenEvents, is_MC=True),
        SampleCfg(name='WZTo3LNu'         , dir_name=WZTo3LNu          .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WZTo3LNu          .xSection, sumweights=WZTo3LNu          .nGenEvents, is_MC=True),
    ]

    

    if channel == 'mmm': 
        samples_essential += [
            SampleCfg(name='WJetsToLNu'       , dir_name=WJetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WJetsToLNu        .xSection, sumweights=WJetsToLNu        .nGenEvents, is_MC=True),
            SampleCfg(name='W1JetsToLNu'       , dir_name=W1JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W1JetsToLNu        .xSection, sumweights=W1JetsToLNu        .nGenEvents, is_MC=True),
            SampleCfg(name='W2JetsToLNu'       , dir_name=W2JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W2JetsToLNu        .xSection, sumweights=W2JetsToLNu        .nGenEvents, is_MC=True),
            SampleCfg(name='W3JetsToLNu'       , dir_name=W3JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W3JetsToLNu        .xSection, sumweights=W3JetsToLNu        .nGenEvents, is_MC=True),
            SampleCfg(name='W4JetsToLNu'       , dir_name=W4JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W4JetsToLNu        .xSection, sumweights=W4JetsToLNu        .nGenEvents, is_MC=True)]

    if channel == 'emm': 
        samples_essential += [
            SampleCfg(name='W1JetsToLNu'       , dir_name=W1JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W1JetsToLNu        .xSection, sumweights=W1JetsToLNu        .nGenEvents, is_MC=True),
            SampleCfg(name='W2JetsToLNu'       , dir_name=W2JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W2JetsToLNu        .xSection, sumweights=W2JetsToLNu        .nGenEvents, is_MC=True),
            SampleCfg(name='W3JetsToLNu'       , dir_name=W3JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W3JetsToLNu        .xSection, sumweights=W3JetsToLNu        .nGenEvents, is_MC=True),
            SampleCfg(name='W4JetsToLNu'       , dir_name=W4JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W4JetsToLNu        .xSection, sumweights=W4JetsToLNu        .nGenEvents, is_MC=True)
        ]

    samples_signal_emm = [
        SampleCfg(name='HN3L_M3' , dir_name=HN3L_M3_e.name, ana_dir=analysis_dir+sig_dir, tree_prod_name=tree_prod_name, xsec=signal_scale, sumweights=HN3L_M3_e.nGenEvents, is_signal=True)
        # SampleCfg(name='HN3L' , dir_name=HN3L_M3_e.name, ana_dir=analysis_dir+sig_dir, tree_prod_name=tree_prod_name, xsec=signal_scale, sumweights=HN3L_M3_e.nGenEvents, is_signal=True)
    ]
    samples_signal_mmm = [
       # SampleCfg(name='HN3L_M3'              , dir_name=HN3L_M3_m           .name, ana_dir=analysis_dir+sig_dir, tree_prod_name=tree_prod_name, xsec=200.0                       , sumweights=HN3L_M3_m          .nGenEvents, is_signal=True)

    ]
    if channel == 'emm': samples_signal = samples_signal_emm
    if channel == 'mmm': samples_signal = samples_signal_mmm

    samples_essential += samples_signal

    # samples_data = [
        # SampleCfg(name='data_2017B', dir_name=dataB.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents =  5265969 
        # SampleCfg(name='data_2017C', dir_name=dataC.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 10522062 
        # SampleCfg(name='data_2017D', dir_name=dataD.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                           #nevents =  3829353
        # SampleCfg(name='data_2017E', dir_name=dataE.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 10926946 
        # SampleCfg(name='data_2017F', dir_name=dataF.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 19122658 ; SUM of BCDEF = 49'666'988
    # ]

    samples_additional = [
#        SampleCfg(name='DY1Jets_M50'        , dir_name=DY1JetsToLL_M50      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY1JetsToLL_M50     .xSection, sumweights=DY1JetsToLL_M50     .nGenEvents, is_MC=True),
#        SampleCfg(name='DY2Jets_M50'        , dir_name=DY2JetsToLL_M50      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY2JetsToLL_M50     .xSection, sumweights=DY2JetsToLL_M50     .nGenEvents, is_MC=True),
#        SampleCfg(name='DY2Jets_M50_ext'    , dir_name=DY2JetsToLL_M50_ext  .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY2JetsToLL_M50_ext .xSection, sumweights=DY2JetsToLL_M50_ext .nGenEvents, is_MC=True),
#        SampleCfg(name='DY3Jets_M50'        , dir_name=DY3JetsToLL_M50      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY3JetsToLL_M50     .xSection, sumweights=DY3JetsToLL_M50     .nGenEvents, is_MC=True),
#        SampleCfg(name='DY3Jets_M50_ext'    , dir_name=DY3JetsToLL_M50_ext  .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DY3JetsToLL_M50_ext .xSection, sumweights=DY3JetsToLL_M50_ext .nGenEvents, is_MC=True),
  
#         SampleCfg(name='ZZTo4L_ext'         , dir_name=ZZTo4L_ext         .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ZZTo4L_ext         .xSection, sumweights=ZZTo4L_ext         .nGenEvents, is_MC=True),
#         SampleCfg(name='WW_DoubleScattering', dir_name=WW_DoubleScattering.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WW_DoubleScattering.xSection, sumweights=WW_DoubleScattering.nGenEvents, is_MC=True),
#         SampleCfg(name='W3JetsToLNu'        , dir_name=W3JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W3JetsToLNu        .xSection, sumweights=W3JetsToLNu        .nGenEvents, is_MC=True),        
#         SampleCfg(name='W4JetsToLNu'        , dir_name=W4JetsToLNu        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=W4JetsToLNu        .xSection, sumweights=W4JetsToLNu        .nGenEvents, is_MC=True),        
#         SampleCfg(name='WLLJJ_WToLNu_EWK'   , dir_name=WLLJJ_WToLNu_EWK   .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WLLJJ_WToLNu_EWK   .xSection, sumweights=WLLJJ_WToLNu_EWK   .nGenEvents, is_MC=True),        
    ]

    if channel == 'mmm':
        samples_additional += [
            SampleCfg(name='DYBB'               , dir_name=DYBB               .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYBB               .xSection, sumweights=DYBB               .nGenEvents, is_MC=True),
            SampleCfg(name='DYJetsToLL_M10to50'               , dir_name=DYJetsToLL_M10to50               .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M10to50               .xSection, sumweights=DYJetsToLL_M10to50               .nGenEvents, is_MC=True),
            # SampleCfg(name='Conversion_DYBB', 
                # dir_name=DYBB.name, 
                # ana_dir=analysis_dir+bkg_dir, 
                # tree_prod_name=tree_prod_name, 
                # xsec=DYBB.xSection, 
                # sumweights=DYBB.nGenEvents, is_MC=True),
            # SampleCfg(name='Conversion_DYJetsToLL_M10to50',
                # dir_name=DYJetsToLL_M10to50.name, 
                # ana_dir=analysis_dir+bkg_dir, 
                # tree_prod_name=tree_prod_name, 
                # xsec=DYJetsToLL_M10to50.xSection, 
                # sumweights=DYJetsToLL_M10to50.nGenEvents, is_MC=True),
            # SampleCfg(name='Conversion_WJetsToLNu',
                # dir_name=WJetsToLNu.name, 
                # ana_dir=analysis_dir+bkg_dir, 
                # tree_prod_name=tree_prod_name, 
                # xsec=WJetsToLNu.xSection, 
                # sumweights=WJetsToLNu.nGenEvents, is_MC=True),
            # # SampleCfg(name='WJetsToLNu'               , dir_name=WJetsToLNu               .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WJetsToLNu               .xSection, sumweights=WJetsToLNu               .nGenEvents, is_MC=True),
        ]

    if channel == 'emm':
        samples_additional += [
            SampleCfg(name='ZZZ'                , dir_name=ZZZ                .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ZZZ                .xSection, sumweights=ZZZ                .nGenEvents, is_MC=True),
            SampleCfg(name='DYJets'             , dir_name=DYJetsToLL_M50     .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50     .xSection, sumweights=DYJetsToLL_M50     .nGenEvents, is_MC=True),
            SampleCfg(name='WZZ'                , dir_name=WZZ                .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WZZ                .xSection, sumweights=WZZ                .nGenEvents, is_MC=True),
            SampleCfg(name='WWZ'                , dir_name=WWZ                .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WWZ                .xSection, sumweights=WWZ                .nGenEvents, is_MC=True),
            SampleCfg(name='WWW'                , dir_name=WWW                .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WWW                .xSection, sumweights=WWW                .nGenEvents, is_MC=True),
            SampleCfg(name='WGGJets'            , dir_name=WGGJets            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WGGJets            .xSection, sumweights=WGGJets            .nGenEvents, is_MC=True),
            SampleCfg(name='TTWJetsToLNu'       , dir_name=TTWJetsToLNu       .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTWJetsToLNu       .xSection, sumweights=TTWJetsToLNu       .nGenEvents, is_MC=True),
            SampleCfg(name='TTZToLL_M10'        , dir_name=TTZToLL_M10        .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTZToLL_M10        .xSection, sumweights=TTZToLL_M10        .nGenEvents, is_MC=True),
            SampleCfg(name='TTZToLL_M1to10'     , dir_name=TTZToLL_M1to10     .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTZToLL_M1to10     .xSection, sumweights=TTZToLL_M1to10     .nGenEvents, is_MC=True),
            SampleCfg(name='ST_sch_lep'         , dir_name=ST_sch_lep         .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ST_sch_lep         .xSection, sumweights=ST_sch_lep         .nGenEvents, is_MC=True),
            SampleCfg(name='STbar_tch_inc'      , dir_name=STbar_tch_inc      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=STbar_tch_inc      .xSection, sumweights=STbar_tch_inc      .nGenEvents, is_MC=True),
            SampleCfg(name='ST_tch_inc'         , dir_name=ST_tch_inc         .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ST_tch_inc         .xSection, sumweights=ST_tch_inc         .nGenEvents, is_MC=True),
            SampleCfg(name='STbar_tW_inc'       , dir_name=STbar_tW_inc       .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=STbar_tW_inc       .xSection, sumweights=STbar_tW_inc       .nGenEvents, is_MC=True),
            SampleCfg(name='ST_tW_inc'          , dir_name=ST_tW_inc          .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ST_tW_inc          .xSection, sumweights=ST_tW_inc          .nGenEvents, is_MC=True),
            SampleCfg(name='WWTo2L2Nu'        , dir_name=WWTo2L2Nu         .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WWTo2L2Nu         .xSection, sumweights=WWTo2L2Nu         .nGenEvents, is_MC=True),
        ]
   
   

    samples_qcd_e = [
        SampleCfg(name='QCD_pt_20to30_bcToE', dir_name=QCD_pt_20to30_bcToE.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_20to30_bcToE.xSection, sumweights=QCD_pt_20to30_bcToE.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_30to80_bcToE', dir_name=QCD_pt_30to80_bcToE.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_30to80_bcToE.xSection, sumweights=QCD_pt_30to80_bcToE.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_80to170_bcToE', dir_name=QCD_pt_80to170_bcToE.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_80to170_bcToE.xSection, sumweights=QCD_pt_80to170_bcToE.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_170to250_bcToE', dir_name=QCD_pt_170to250_bcToE.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_170to250_bcToE.xSection, sumweights=QCD_pt_170to250_bcToE.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_250toInf_bcToE', dir_name=QCD_pt_250toInf_bcToE.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_250toInf_bcToE.xSection, sumweights=QCD_pt_250toInf_bcToE.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_15to20_em', dir_name=QCD_pt_15to20_em.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_15to20_em.xSection, sumweights=QCD_pt_15to20_em.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_20to30_em', dir_name=QCD_pt_20to30_em.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_20to30_em.xSection, sumweights=QCD_pt_20to30_em.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_30to50_em', dir_name=QCD_pt_30to50_em.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_30to50_em.xSection, sumweights=QCD_pt_30to50_em.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_50to80_em', dir_name=QCD_pt_50to80_em.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_50to80_em.xSection, sumweights=QCD_pt_50to80_em.nGenEvents, is_MC=True),
#        SampleCfg(name='QCD_pt_80to120_em', dir_name=QCD_pt_80to120_em.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_80to120_em.xSection, sumweights=QCD_pt_80to120_em.nGenEvents, is_MC=True),  #NOT IN DAS
        SampleCfg(name='QCD_pt_120to170_em', dir_name=QCD_pt_120to170_em.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_120to170_em.xSection, sumweights=QCD_pt_120to170_em.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_300toInf_em', dir_name=QCD_pt_300toInf_em.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_300toInf_em.xSection, sumweights=QCD_pt_300toInf_em.nGenEvents, is_MC=True),
    ]


    samples_qcd_mu = [
        SampleCfg(name='QCD_pt_15to20_mu', dir_name=QCD_pt_15to20_mu.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_15to20_mu.xSection, sumweights=QCD_pt_15to20_mu.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_20to30_mu', dir_name=QCD_pt_20to30_mu.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_20to30_mu.xSection, sumweights=QCD_pt_20to30_mu.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_30to50_mu', dir_name=QCD_pt_30to50_mu.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_30to50_mu.xSection, sumweights=QCD_pt_30to50_mu.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_50to80_mu', dir_name=QCD_pt_50to80_mu.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_50to80_mu.xSection, sumweights=QCD_pt_50to80_mu.nGenEvents, is_MC=True),
        SampleCfg(name='QCD_pt_80to120_mu', dir_name=QCD_pt_80to120_mu.name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=QCD_pt_80to120_mu.xSection, sumweights=QCD_pt_80to120_mu.nGenEvents, is_MC=True),
    ]

    samples_DDE_mmm_doublefake = [
        SampleCfg(name='DDE_mmm_doublefake',
            dir_name='DDE', 
            ana_dir=analysis_dir+bkg_dir, 
            tree_prod_name='added_trees', 
            is_dde=True,
            is_singlefake=False,
            is_doublefake=True), 
    ]
    samples_DDE_mmm_singlefake = [
        SampleCfg(name='DDE_mmm_singlefake',
            dir_name='DDE', 
            ana_dir=analysis_dir+bkg_dir, 
            tree_prod_name='added_trees', 
            is_dde=True,
            is_singlefake=True,
            is_doublefake=False), 
    ]

    SampleCfg(name='DYBB'               , dir_name=DYBB               .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYBB               .xSection, sumweights=DYBB               .nGenEvents, is_MC=True),
    # SampleCfg(name='DYJetsToLL_M10to50'               , dir_name=DYJetsToLL_M10to50               .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M10to50               .xSection, sumweights=DYJetsToLL_M10to50               .nGenEvents, is_MC=True),

    samples_conversion = [
        # SampleCfg(name='Conversion_DYBB', 
            # dir_name=DYBB.name, 
            # ana_dir=analysis_dir+bkg_dir, 
            # tree_prod_name=tree_prod_name, 
            # xsec=DYBB.xSection, 
            # sumweights=DYBB.nGenEvents, is_MC=True),
        SampleCfg(name='Conversion_DYJetsToLL_M10to50',
            dir_name=DYJetsToLL_M10to50.name, 
            ana_dir=analysis_dir+bkg_dir, 
            tree_prod_name=tree_prod_name, 
            xsec=DYJetsToLL_M10to50.xSection, 
            sumweights=DYJetsToLL_M10to50.nGenEvents, is_MC=True),
        # SampleCfg(name='Conversion_WJetsToLNu',
            # dir_name=WJetsToLNu.name, 
            # ana_dir=analysis_dir+bkg_dir, 
            # tree_prod_name=tree_prod_name, 
            # xsec=WJetsToLNu.xSection, 
            # sumweights=WJetsToLNu.nGenEvents, is_MC=True),
    ]
  

    # samples_data_dde = [
        # SampleCfg(name='data_2017', dir_name=dataB.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                          
    # ]

    samples_data_dde = [
        SampleCfg(name='data_2017', 
            dir_name='DDE', 
            ana_dir=analysis_dir+bkg_dir, 
            tree_prod_name='added_trees', 
            is_data=True),                                          
    ]


    #Temporal data 
    samples_data = [
        SampleCfg(name='data_2017B', dir_name=dataB.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents =  5265969 
        SampleCfg(name='data_2017C', dir_name=dataC.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 10522062 
        SampleCfg(name='data_2017D', dir_name=dataD.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                           #nevents =  3829353
        SampleCfg(name='data_2017E', dir_name=dataE.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 10926946 
        SampleCfg(name='data_2017F', dir_name=dataF.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 19122658 ; SUM of BCDEF = 49'666'988
    ]

    # # define all sample configurations
    # samples_mc  = samples_essential + samples_additional 
    samples     = samples_essential + samples_additional # + samples_data

    if channel == 'emm':
        samples_mc = samples_essential + samples_additional + samples_qcd_e
        samples_dde = samples_DDE_mmm_doublefake + samples_DDE_mmm_singlefake #warning: this is just a placeholder, it's mmm

    if channel == 'mmm':
        # samples_mc = samples_essential + samples_qcd_mu + [samples_additional[1]] # DYBB
        # samples_mc = samples_essential + samples_qcd_mu + samples_additional # DYBB
        # samples_mc = samples_essential + samples_additional 
        samples_mc = samples_essential + samples_additional + samples_conversion
        samples_dde = samples_DDE_mmm_doublefake + samples_DDE_mmm_singlefake
        # samples_dde = samples_DDE_mmm_doublefake 
    samples_bkg = samples_dde + samples_mc
    samples_essential_data = samples_essential + samples_data
    samples_dde_data = samples_dde + samples_data_dde
    samples_signal_mc = samples_mc + samples_signal
     
    all_samples_mc = samples_mc  + samples_data
    # all_samples = samples_bkg + samples_data
    all_samples_dde = samples_bkg + samples_data_dde



    sampleDict = {}
    for s in all_samples_dde:
        sampleDict[s.name] = s
    for s in all_samples_mc:
        sampleDict[s.name] = s

    for sample in all_samples_dde:
        if sample.is_signal:
            sample.scale = sample.scale * signal_scale
    for sample in all_samples_mc:
        if sample.is_signal:
            sample.scale = sample.scale * signal_scale

    samples_DY = [
            SampleCfg(name='DYJetsToLL_M10to50',dir_name=DYJetsToLL_M10to50.name, ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M10to50.xSection, sumweights=DYJetsToLL_M10to50.nGenEvents, is_DY=True),
            SampleCfg(name='DYJets_ext'       , dir_name=DYJetsToLL_M50_ext.name, ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50_ext.xSection, sumweights=DYJetsToLL_M50_ext.nGenEvents, is_DY=True),
            # SampleCfg(name='TTJets_amc'       , dir_name=TTJets_amcat      .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=TTJets_amcat      .xSection, sumweights=TTJets_amcat      .nGenEvents, is_MC=True),
            # SampleCfg(name='ZZTo4L'           , dir_name=ZZTo4L            .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=ZZTo4L            .xSection, sumweights=ZZTo4L            .nGenEvents, is_MC=True),
            # SampleCfg(name='WZTo3LNu'         , dir_name=WZTo3LNu          .name, ana_dir=analysis_dir+bkg_dir, tree_prod_name=tree_prod_name, xsec=WZTo3LNu          .xSection, sumweights=WZTo3LNu          .nGenEvents, is_MC=True),
            ]
    samples_conversion = [
        # SampleCfg(name='Conversion_DYBB', 
            # dir_name=DYBB.name, 
            # ana_dir=analysis_dir+bkg_dir, 
            # tree_prod_name=tree_prod_name, 
            # xsec=DYBB.xSection, 
            # sumweights=DYBB.nGenEvents, is_MC=True),
        SampleCfg(name='Conversion_DYJetsToLL_M10to50',
            dir_name=DYJetsToLL_M10to50.name, 
            ana_dir=analysis_dir+bkg_dir, 
            tree_prod_name=tree_prod_name, 
            xsec=DYJetsToLL_M10to50.xSection, 
            sumweights=DYJetsToLL_M10to50.nGenEvents, is_MC_Conversions=True),
        SampleCfg(name='Conversion_DYJets_ext',
            dir_name=DYJetsToLL_M50_ext.name, 
            ana_dir=analysis_dir+bkg_dir, 
            tree_prod_name=tree_prod_name, 
            xsec=DYJetsToLL_M50_ext.xSection, 
            sumweights=DYJetsToLL_M50_ext.nGenEvents, is_MC_Conversions=True),
        # SampleCfg(name='Conversion_WJetsToLNu',
            # dir_name=WJetsToLNu.name, 
            # ana_dir=analysis_dir+bkg_dir, 
            # tree_prod_name=tree_prod_name, 
            # xsec=WJetsToLNu.xSection, 
            # sumweights=WJetsToLNu.nGenEvents, is_MC=True),
        ]

    # samples_DY_data = samples_DY + samples_conversion + samples_data 
    samples_DY_data = samples_DY + samples_data 
    # samples_DY_data = samples_DY + samples_conversion 
    # samples_DY_data = samples_conversion 
    # samples_DY_data = samples_DY

    return samples_mc, samples_signal_mc, samples_data, samples, all_samples_dde, all_samples_mc, sampleDict, samples_essential, samples_essential_data, samples_dde, samples_data_dde, samples_dde_data, samples_bkg, samples_DY_data




def setSumWeights(samples, weight_dir='SkimAnalyzerCount', norm=True):
    print '###########################################################'
    print '# setting sum weights for the samples...'
    print '###########################################################'

    
    # RM: this is needed to retrieve the sum of weights *before* any selection
    # FIXME! on hold now until SkimAnalyzerCount is fixed. Otherwise the code runs.
    # to activate it, simply comment out the sample names in weighted_list

    weighted_list = [
       'HN3L_M3'            ,
       'DYJets'             ,
       # 'DYJets_ext'         ,
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
#       'W3JetsToLNu'        ,
#       'W4JetsToLNu'        ,
       'WLLJJ_WToLNu_EWK'   ,
    ]

    # RM hand made patch!
    initial_weights = OrderedDict()
    initial_weights['HN3L_M3'            ] = 1.
    initial_weights['DYJets'             ] = 0.6777
    # initial_weights['DYJets_ext'         ] = 0.6777
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
    
    for sample in samples:
        try:
            if isinstance(sample, HistogramCfg) or sample.is_data:
                continue
        except:
            set_trace()

#         print 'A: Set sum weights for sample', sample.name, 'to', sample.sumweights        
        if sample.name in weighted_list:
            # sample.sumweights *= initial_weights[sample.name]
            print 'Set sum weights for sample', sample.name, 'to', sample.sumweights
            # print 'Sum weights from sample', sample.name, 'in weighted_list: ', sample.sumweights

        if sample.name not in weighted_list:
#            pass # turn this off later, for NLO or higher order samples
            # print 'Set sum weights for sample', sample.name, 'to', sample.sumweights
            # setSumWeights(sample, 'SkimAnalyzerCount', False)

            if sample.is_dde == False:
                pckfile = '/'.join([sample.ana_dir, sample.dir_name, weight_dir, 'SkimReport.pck'])
                try:
                    pckobj = pickle.load(open(pckfile, 'r'))
                    counters = dict(pckobj)
                    # set_trace()
                    if norm:
                        if 'Sum Norm Weights' in counters:
                            sample.sumweights = counters['Sum Norm Weights']
                    else:
                        if 'Sum Weights' in counters:
                            sample.sumweights = counters['Sum Weights']
                except IOError:
                    print 'Warning: could not find sum weights information for sample', sample.name
                    pass

            # if sample.is_dde == True:
                # set_trace()
                # sample.sumweights *=50000 
                # print 'sample ' + sample.dir_name + 'has been set to ', sample.sumweights

            print 'Sum weights from sample',sample.name, 'not in weighted_list. Setting it to', sample.sumweights

    return samples
