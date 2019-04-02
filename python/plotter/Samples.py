import os
import pickle

import ROOT
from ROOT import gSystem, gROOT
from collections import OrderedDict

from pdb import set_trace

from CMGTools.HNL.plotter.PlotConfigs import SampleCfg, HistogramCfg

from CMGTools.HNL.samples.samples_mc_2017_noskim   import TTJets, WJetsToLNu, WJetsToLNu_ext, ZZZ, WZZ, WWZ, WWW, WWTo2L2Nu, WGGJets, TTWJetsToLNu, TTZToLL_M10, TTZToLL_M1to10, ST_sch_lep, STbar_tch_inc, ST_tch_inc, STbar_tW_inc, ST_tW_inc, DYBB, DYJetsToLL_M10to50,DYJetsToLL_M50, DYJetsToLL_M50_ext, DY1JetsToLL_M50, DY2JetsToLL_M50, DY2JetsToLL_M50_ext, DY3JetsToLL_M50, DY3JetsToLL_M50_ext
from CMGTools.HNL.samples.samples_data_2017_noskim import Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F, Single_mu_2017B,  Single_mu_2017C,  Single_mu_2017D,  Single_mu_2017E,  Single_mu_2017F

from CMGTools.HNL.samples.samples_mc_2017_noskim   import W1JetsToLNu, W2JetsToLNu


def createSampleLists(analysis_dir='', 
                      server='t3',
                      channel='mmm',
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


   
    #Temporal data 
    samples_data = [
        SampleCfg(name='data_2017B', dir_name=dataB.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents =  5265969 
        SampleCfg(name='data_2017C', dir_name=dataC.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 10522062 
        SampleCfg(name='data_2017D', dir_name=dataD.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                           #nevents =  3829353
        SampleCfg(name='data_2017E', dir_name=dataE.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 10926946 
        SampleCfg(name='data_2017F', dir_name=dataF.name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 19122658 ; SUM of BCDEF = 49'666'988
    ]

    samples_TTJets = [
            SampleCfg(name='TTJets', 
                dir_name=TTJets.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=TTJets.xSection, 
                sumweights=TTJets.nGenEvents, 
                is_MC=True),
            ]

    samples_WJets = [
            SampleCfg(name='WJetsToLNu', 
                dir_name=WJetsToLNu.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=WJetsToLNu.xSection, 
                sumweights=WJetsToLNu.nGenEvents, 
                is_MC=True),
            SampleCfg(name='WJetsToLNu_ext', 
                dir_name=WJetsToLNu_ext.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=WJetsToLNu_ext.xSection, 
                sumweights=WJetsToLNu_ext.nGenEvents, 
                is_MC=True),
            ]

    samples_DYBB = [
            SampleCfg(name='DYBB', 
                dir_name=DYBB.name, 
                ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', 
                tree_prod_name=tree_prod_name, 
                xsec=DYBB.xSection, 
                sumweights=DYBB.nGenEvents, 
                is_DY=True),
            ]

    samples_DY = [
            # SampleCfg(name='DYJetsToLL_M10to50',
                # dir_name=DYJetsToLL_M10to50.name, 
                # ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', 
                # tree_prod_name=tree_prod_name, 
                # xsec=DYJetsToLL_M10to50.xSection, 
                # sumweights=DYJetsToLL_M10to50.nGenEvents, 
                # is_MC=True,
                # is_DY=True),
            # SampleCfg(name='DYJets_M50', 
                # dir_name=DYJetsToLL_M50.name, 
                # ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', 
                # tree_prod_name=tree_prod_name, 
                # xsec=DYJetsToLL_M50.xSection, 
                # sumweights=DYJetsToLL_M50.nGenEvents, 
                # is_MC=True,
                # is_DY=True),
            SampleCfg(name='DYJets_M50_ext', 
                dir_name=DYJetsToLL_M50_ext.name, 
                ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', 
                tree_prod_name=tree_prod_name, 
                xsec=DYJetsToLL_M50_ext.xSection, 
                sumweights=DYJetsToLL_M50_ext.nGenEvents, 
                is_MC=True,
                is_DY=True),
            ]

    # samples_Diboson = [
            # SampleCfg(name='ZZTo4L', 
                # dir_name=ZZTo4L.name, 
                # ana_dir=analysis_dir+bkg_dir, 
                # tree_prod_name=tree_prod_name, 
                # xsec=ZZTo4L.xSection, 
                # sumweights=ZZTo4L.nGenEvents, 
                # is_MC=True),
            # SampleCfg(name='WZTo3LNu', 
                # dir_name=WZTo3LNu.name, 
                # ana_dir=analysis_dir+bkg_dir, 
                # tree_prod_name=tree_prod_name, 
                # xsec=WZTo3LNu.xSection, 
                # sumweights=WZTo3LNu.nGenEvents, 
                # is_MC=True),
            # ]

    samples_conversion = [
        SampleCfg(name='Conversion_DYJetsToLL_M10to50',
            dir_name=DYJetsToLL_M10to50.name, 
            ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', 
            tree_prod_name=tree_prod_name, 
            xsec=DYJetsToLL_M10to50.xSection, 
            sumweights=DYJetsToLL_M10to50.nGenEvents, is_MC_Conversions=True),
        SampleCfg(name='Conversion_DYJets_M50', 
            dir_name=DYJetsToLL_M50.name, 
            ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', 
            tree_prod_name=tree_prod_name, 
            xsec=DYJetsToLL_M50.xSection, 
            sumweights=DYJetsToLL_M50.nGenEvents, 
            is_MC_Conversions=True),
        SampleCfg(name='Conversion_DYJets_M50_ext', 
            dir_name=DYJetsToLL_M50_ext.name, 
            ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', 
            tree_prod_name=tree_prod_name, 
            xsec=DYJetsToLL_M50_ext.xSection, 
            sumweights=DYJetsToLL_M50_ext.nGenEvents, 
            is_MC_Conversions=True),
        ]

    samples_Triboson = [
            SampleCfg(name='ZZZ', 
                dir_name=ZZZ.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=ZZZ.xSection, 
                sumweights=ZZZ.nGenEvents, 
                is_MC=True),
            SampleCfg(name='WZZ', 
                dir_name=WZZ.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=WZZ.xSection, 
                sumweights=WZZ.nGenEvents, 
                is_MC=True),
            SampleCfg(name='WWZ', 
                dir_name=WWZ.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=WWZ.xSection, 
                sumweights=WWZ.nGenEvents, 
                is_MC=True),
            SampleCfg(name='WWW', 
                dir_name=WWW.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=WWW.xSection, 
                sumweights=WWW.nGenEvents, 
                is_MC=True),
            ]


    samples_data_dde = [
        SampleCfg(name='data_2017', 
            dir_name='DDE', 
            ana_dir=analysis_dir+bkg_dir, 
            tree_prod_name='added_trees', 
            is_data=True),                                          
    ]


    # samples_mc = samples_TTJets + samples_WJets + samples_DY + samples_conversion  
    samples_mc = samples_DY + samples_conversion  
    samples_all = samples_mc + samples_data


    return samples_all



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
