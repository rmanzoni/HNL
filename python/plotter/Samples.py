import os
import pickle

import ROOT
from ROOT import gSystem, gROOT
from collections import OrderedDict

from pdb import set_trace

from CMGTools.HNL.plotter.PlotConfigs import SampleCfg, HistogramCfg

from CMGTools.HNL.samples.samples_mc_2017_noskim   import TTJets, WJetsToLNu, WJetsToLNu_ext, ZZZ, WZZ, WWZ, WWW, WWTo2L2Nu, WGGJets, TTWJetsToLNu, TTZToLL_M10, TTZToLL_M1to10, ST_sch_lep, STbar_tch_inc, ST_tch_inc, STbar_tW_inc, ST_tW_inc, DYBB, DYJetsToLL_M10to50,DYJetsToLL_M50, DYJetsToLL_M50_ext, DY1JetsToLL_M50, DY2JetsToLL_M50, DY2JetsToLL_M50_ext, DY3JetsToLL_M50, DY3JetsToLL_M50_ext, WW, WZ, ZZ

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
            # data_dir = 'root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/data/'
            data_dir = '/work/dezhu/4_production/production_20190411_Data_mmm/ntuples'
            bkg_dir = 'production_20190411_Bkg_mmm/ntuples/'
            # bkg_dir = 'production_20190306_BkgMC/mmm/ntuples/'
            sig_dir = 'signal/ntuples'
            DY_dir = analysis_dir + bkg_dir
        dataB = Single_mu_2017B; dataC = Single_mu_2017C; dataD = Single_mu_2017D; dataE = Single_mu_2017E; dataF = Single_mu_2017F; 

    if channel == 'mem':
        if server == 'lxplus':
            data_dir = '/eos/user/v/vstampf/ntuples/data_2017_m_noskim/'
            bkg_dir = 'bkg_mc_m/'
            sig_dir = 'sig_mc_m/ntuples/'
            DY_dir = analysis_dir + bkg_dir
        if server == 't3':
            # data_dir = analysis_dir + 'data/'
            # data_dir = 'root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/data/'
            data_dir = '/work/dezhu/4_production/vinz'
            bkg_dir = 'vinz'
            # bkg_dir = 'production_20190306_BkgMC/mmm/ntuples/'
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
                # sumweights=TTJets.nGenEvents, 
                sumweights=None, 
                is_MC=True),
            ]

    samples_WJets = [
            SampleCfg(name='WJetsToLNu', 
                dir_name=WJetsToLNu.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=WJetsToLNu.xSection, 
                # sumweights=WJetsToLNu.nGenEvents, 
                # sumweights=76666716, 
                sumweights=None, 
                is_MC=True),
            # SampleCfg(name='WJetsToLNu_ext', 
                # dir_name=WJetsToLNu_ext.name, 
                # ana_dir=analysis_dir+bkg_dir, 
                # tree_prod_name=tree_prod_name, 
                # xsec=WJetsToLNu_ext.xSection, 
                # # sumweights=WJetsToLNu_ext.nGenEvents, 
                # sumweights=76666716, 
                # is_MC=True),
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
                # # ana_dir=analysis_dir+bkg_dir, 
                # ana_dir='/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples', 
                # # ana_dir='root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/background/montecarlo/production_20190318_BkgMC', 
                # tree_prod_name=tree_prod_name, 
                # xsec=DYJetsToLL_M10to50.xSection, 
                # # sumweights=DYJetsToLL_M10to50.nGenEvents, 
                # sumweights=None, 
                # # sumweights=1652621.0, 
                # is_MC=True,
                # is_DY=True),
            # SampleCfg(name='DYJets_M50', 
                # dir_name=DYJetsToLL_M50.name, 
                # # ana_dir=analysis_dir+bkg_dir, 
                # ana_dir='/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples', 
                # tree_prod_name=tree_prod_name, 
                # xsec=DYJetsToLL_M50.xSection, 
                # # sumweights=DYJetsToLL_M50.nGenEvents, 
                # sumweights=133395135, 
                # is_MC=True,
                # is_DY=True),
            SampleCfg(name='DYJets_M50_ext', 
                dir_name=DYJetsToLL_M50_ext.name, 
                ana_dir=analysis_dir+bkg_dir, 
                # ana_dir='/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples', 
                # ana_dir='root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/background/montecarlo/production_20190318_BkgMC', 
                tree_prod_name=tree_prod_name, 
                xsec=DYJetsToLL_M50_ext.xSection, 
                # sumweights=DYJetsToLL_M50_ext.nGenEvents, 
                # sumweights=133395135, 
                sumweights=None, 
                is_MC=True,
                is_DY=True),
            ]

    samples_Diboson = [
            SampleCfg(name='ZZ', 
                dir_name=ZZ.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=ZZ.xSection, 
                # sumweights=ZZ.nGenEvents, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='WZ', 
                dir_name=WZ.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=WZ.xSection, 
                # sumweights=WZ.nGenEvents, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='WW', 
                dir_name=WW.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=WW.xSection, 
                # sumweights=WW.nGenEvents, 
                sumweights=None, 
                is_MC=True),
            ]

    samples_SingleTop = [
            SampleCfg(name='ST_sch_lep', 
                dir_name=ST_sch_lep.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=ST_sch_lep.xSection, 
                # sumweights=ZZ.nGenEvents, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='ST_tch_inc', 
                dir_name=ST_tch_inc.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=ST_tch_inc.xSection, 
                # sumweights=ZZ.nGenEvents, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='STbar_tch_inc', 
                dir_name=STbar_tch_inc.name, 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=STbar_tch_inc.xSection, 
                # sumweights=ZZ.nGenEvents, 
                sumweights=None, 
                is_MC=True),
            ]

    samples_conversion = [
            SampleCfg(name='Conversion_DYJets_M50_ext', 
                dir_name=DYJetsToLL_M50_ext.name, 
                ana_dir=analysis_dir+bkg_dir, 
                # ana_dir='/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples', 
                # ana_dir='root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/background/montecarlo/production_20190318_BkgMC', 
                tree_prod_name=tree_prod_name, 
                xsec=DYJetsToLL_M50_ext.xSection, 
                # sumweights=DYJetsToLL_M50_ext.nGenEvents, 
                # sumweights=133395135, 
                sumweights=None, 
                is_MC=True,
                is_MC_Conversions=True),
            ]

    # samples_conversion = [
        # SampleCfg(name='Conversion_DYJetsToLL_M10to50',
            # dir_name=DYJetsToLL_M10to50.name, 
            # ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', 
            # tree_prod_name=tree_prod_name, 
            # xsec=DYJetsToLL_M10to50.xSection, 
            # sumweights=DYJetsToLL_M10to50.nGenEvents, is_MC_Conversions=True),
        # SampleCfg(name='Conversion_DYJets_M50', 
            # dir_name=DYJetsToLL_M50.name, 
            # ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', 
            # tree_prod_name=tree_prod_name, 
            # xsec=DYJetsToLL_M50.xSection, 
            # sumweights=DYJetsToLL_M50.nGenEvents, 
            # is_MC_Conversions=True),
        # SampleCfg(name='Conversion_DYJets_M50_ext', 
            # dir_name=DYJetsToLL_M50_ext.name, 
            # ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', 
            # tree_prod_name=tree_prod_name, 
            # xsec=DYJetsToLL_M50_ext.xSection, 
            # sumweights=DYJetsToLL_M50_ext.nGenEvents, 
            # is_MC_Conversions=True),
        # ]

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

    samples_dde = [
        SampleCfg(name='DDE_data_2017B_singlefake', 
            dir_name=dataB.name, 
            ana_dir=data_dir, 
            tree_prod_name=tree_prod_name, 
            is_data=False,
            is_singlefake=True,
            is_dde = True,
            fr_tree_path = '/work/dezhu/5_Miscellaneous/20190320_FRStudies/SFR/data/20190405_MakeSFRTree/fr_021_mmm_sfr_190403_17h_41m.root'),                                          
    ]


    # samples_mc = samples_TTJets + samples_WJets + samples_DY + samples_conversion  
    # samples_mc = samples_TTJets + samples_WJets + samples_DY 
    samples_mc = samples_DY 
    # samples_mc = samples_DY +samples_WJets + samples_TTJets + samples_Diboson + samples_SingleTop 
    # samples_mc = samples_DY +samples_WJets + samples_TTJets + samples_conversion 
    samples_bkg = samples_mc 
    # samples_bkg = samples_dde
    samples_all = samples_bkg + samples_data


    return samples_all



def setSumWeights(samples, weight_dir='SkimAnalyzerCount', norm=True):
    print '###########################################################'
    print '# setting sum weights for the samples...'
    print '###########################################################'

    
    for sample in samples:
        try:
            if isinstance(sample, HistogramCfg) or sample.is_data:
                continue
        except:
            set_trace()

        if sample.sumweights is not None:
            print 'Set sum weights for sample', sample.name, ' (manually!) to', sample.sumweights

        if sample.sumweights is None:
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

            print 'Sum weights from sample',sample.name, 'taken from pckl file. Setting it to', sample.sumweights

    return samples
