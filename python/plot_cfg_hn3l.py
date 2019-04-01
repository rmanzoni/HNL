import copy
import os
from collections import namedtuple
from operator import itemgetter
from ROOT import gROOT as gr

import shutil
from shutil import copyfile, copytree
from numpy import array

from copy_reg import pickle       # to pickle methods for multiprocessing
from types    import MethodType   # to pickle methods for multiprocessing

from CMGTools.HNL.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.HNL.plotter.HistCreator import CreateHists
from CMGTools.HNL.plotter.HistDrawer import HistDrawer
from CMGTools.HNL.plotter.Variables import hnl_vars, test_vars, getVars,dde_vars
from CMGTools.HNL.plotter.Selections import getSelection, Region
from CMGTools.HNL.samples.samples_mc_2017 import hnl_bkg
from pdb import set_trace
# from CMGTools.HNL.plotter.qcdEstimationMSSMltau import estimateQCDWMSSM, createQCDWHistograms

from CMGTools.HNL.plotter.Samples import createSampleLists, setSumWeights


def _pickle_method(method): 
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)

pickle(MethodType, _pickle_method, _unpickle_method)

gr.SetBatch(True) # NEEDS TO BE SET FOR MULTIPROCESSING OF plot.Draw()

int_lumi = 41000.0 # pb #### FIXME 
# int_lumi = 1000.0 # pb #### FIXME 
# int_lumi = 41000.0 * (3829353/49666988) # serves only for era B and mmm
# int_lumi = 41000.0 * (30564478/19122658) # [pb]; adapt to the amount of events done for the nonprompt analysis
#int_lumi = 80000.0 # pb #### FIXME 



def prepareRegions(channel):
    regions = []
    # regions.append(Region('SR','mmm','SR'))
    # regions.append(Region('CR_ttbar','mmm','CR_ttbar'))
    # regions.append(Region('DY','mmm','CR_DY'))
    regions.append(Region('DY_test','mmm','CR_DY_test'))
    # regions.append(Region('DY_test_l2Iso','mmm','CR_DY_test'))

    print('###########################################################')
    print('# setting analysis regions')
    print('###########################################################')

    for r in regions: print r.name

    return regions

def createSamples(channel, analysis_dir, total_weight, server, add_data_cut=None):
    sample_dict = {}
    print "creating samples from %s"%(analysis_dir)
    samples_mc, samples_signal_mc, samples_data, samples, all_samples_dde, all_samples_mc, sampleDict, samples_essential, samples_essential_data, samples_dde, samples_data_dde, samples_dde_data, samples_bkg, samples_DY_data = createSampleLists(analysis_dir=analysis_dir, server = server, channel=channel, add_data_cut=add_data_cut)

    #select here the samples you wish to use
    # working_samples = samples_dde_data
    # working_samples = samples_essential
    # working_samples = samples_mc
    # working_samples = all_samples_dde
    # working_samples = all_samples_mc
    # working_samples = samples_signal_mc
    # working_samples = samples_bkg
    # working_samples = samples_dde
    # working_samples = samples_data
    # working_samples = samples_data_dde
    working_samples = samples_DY_data

    working_samples = setSumWeights(working_samples)
    sample_dict['working_samples'] = working_samples

    #TODO implement a code to print the samples
    print('###########################################################')
    print'# samples to be used:'
    print('###########################################################')
    for w in working_samples: print w.name + ', ',
    print '(%d sample(s))'%(len(working_samples))

    return sample_dict

def createVariables(rebin=None):
    # Taken from Variables.py; can get subset with e.g. getVars(['mt', 'mvis'])
#    variables = CR_vars
    DoNotRebin = ['_norm_', 'n_vtx', 'nj', 'nbj',] 
    # variables = hnl_vars
    variables = dde_vars
    # variables = test_vars
    if rebin>0:
        for ivar in hnl_vars:
            if ivar.name in DoNotRebin: continue
            ivar.binning['nbinsx'] = int(ivar.binning['nbinsx']/rebin)

    return variables

def makePlots(plotDir,channel_name,variables, regions, total_weight, sample_dict, make_plots=True, create_trees=False, multiprocess = True):
    ams_dict = {}
    sample_names = set()
    for region in regions:
        regionDir = plotDir+region.name
        if not os.path.exists(regionDir):
            os.mkdir(regionDir)
            print "Directory ", regionDir, "Created "
        else:
            print "Directory ", regionDir, "already exists, overwriting it!"
            os.system("rm -rf %s"%(regionDir))
            os.system("mkdir %s"%(regionDir))

        cfg_main = HistogramCfg(name=region.name, var=None, cfgs=sample_dict['working_samples'], region=region, lumi=int_lumi, weight=total_weight)
        cfg_main.vars = variables
        
        HISTS = CreateHists(cfg_main)

        plots = HISTS.createHistograms(cfg_main, verbose=False, multiprocess = multiprocess)
        #plots.legendPos = 'right'
        for variable in variables:
        # for plot in plots.itervalues():
            plot = plots[variable.name]

            if channel_name == "e#mu#mu":
                plot.Group('data_obs', ['data_2017B', 'data_2017C', 'data_2017D', 'data_2017E', 'data_2017F'])
                plot.Group('single t', ['ST_tW_inc', 'STbar_tW_inc', 'ST_sch_lep', 'STbar_tch_inc', 'ST_tch_inc'])
                plot.Group('Diboson', ['WZTo3LNu', 'ZZTo4L', 'WWTo2L2Nu'])
                plot.Group('Triboson', ['ZZZ', 'WWW', 'WGGJets', 'WZZ', 'WWZ'])
                plot.Group('ttV', ['TTZToLL_M10', 'TTWJetsToLNu', 'TTZToLL_M1to10'])
                plot.Group('DY', ['DYJets_ext', 'DYJets',  'DYJetsToLL_M10to50'])
                plot.Group('QCD',['QCD_pt_15to20_em', 'QCD_pt_20to30_em', 'QCD_pt_30to50_em', 'QCD_pt_50to80_em', 'QCD_pt_120to170_em', 'QCD_pt_300toInf_em', 
                                  'QCD_pt_20to30_bcToE', 'QCD_pt_30to80_bcToE', 'QCD_pt_80to170_bcToE', 'QCD_pt_170to250_bcToE', 'QCD_pt_250toInf_bcToE'])
                plot.Group('WJets', ['W1JetsToLNu', 'W2JetsToLNu', 'W3JetsToLNu', 'W4JetsToLNu'])

            if channel_name == "#mu#mu#mu":
                plot.Group('data_obs', ['data_2017B', 'data_2017C', 'data_2017D', 'data_2017E', 'data_2017F'])
                plot.Group('Diboson', ['WZTo3LNu','ZZTo4L'])
                # plot.Group('ttV', ['TTWJetsToLNu'])
                plot.Group('DY', ['DYJets_ext','DYBB','DYJetsToLL_M10to50'])
                # plot.Group('Conversions',['Conversion_DYBB','Conversion_DYJetsToLL_M10to50'])
                plot.Group('Conversions',['Conversion_DYJets_ext','Conversion_DYBB','Conversion_DYJetsToLL_M10to50','Conversion_WJetsToLNu'])
                plot.Group('QCD',['QCD_pt_15to20_mu', 'QCD_pt_20to30_mu', 'QCD_pt_30to50_mu', 'QCD_pt_50to80_mu', 'QCD_pt_80to120_mu'])
                plot.Group('WJets', ['W1JetsToLNu', 'W2JetsToLNu', 'W3JetsToLNu', 'W4JetsToLNu'])
            if make_plots:
                HistDrawer.draw(plot, channel = channel_name, plot_dir = plotDir+region.name)

    print '\nOptimisation results:'

    all_vals = ams_dict.items()
    for sample_name in sample_names:
        vals = [v for v in all_vals if sample_name + '_' in v[0]]
        vals.sort(key=itemgetter(1))
        for key, item in vals:
            print item, key

        print '\nBy variable'
        for variable in variables:
            name = variable.name
            print '\nResults for variable', name
            for key, item in vals:
                if key.startswith(name + '__'):
                    print item, key


def producePlots(promptLeptonType, L1L2LeptonType, server):

    if server == 't3':
        plotDirBase = '/work/dezhu/3_figures/1_DataMC/FinalStates/'
    if server == 'lxplus':
        plotDirBase = '/eos/user/d/dezhu/HNL/plots/FinalStates/'

    if promptLeptonType == "ele":
        channel_name = 'e'
        if L1L2LeptonType == "ee":
            plotDir = plotDirBase + 'eee/'
            channel_name += 'ee'
            channel = 'eee'
        if L1L2LeptonType == "em":
            plotDir = plotDirBase + 'eem/'
            channel_name += 'e#mu'
            channel = 'eem'
        if L1L2LeptonType == "mm":
            plotDir = plotDirBase + 'emm/'
            channel_name += '#mu#mu'
            channel = 'emm'
    if promptLeptonType == "mu":
        channel_name = '#mu'
        if L1L2LeptonType == "ee":
            plotDir = plotDirBase + 'mee/'
            channel_name += 'ee'
            channel = 'mee'
        if L1L2LeptonType == "em":
            plotDir = plotDirBase + 'mem/'
            channel_name += '#mu'
            channel = 'mem'
        if L1L2LeptonType == "mm":
            plotDir = plotDirBase + 'mmm/'
            channel_name += '#mu#mu'
            channel = 'mmm'
    
    if server == "lxplus":
        analysis_dir = '/eos/user/v/vstampf/ntuples/'
   
    if server == "t3":
        analysis_dir = 'root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv1.0/' + channel + '/'

    total_weight = 'weight * lhe_weight'
    # total_weight = '1'

    print total_weight

    regions = prepareRegions(channel)
    

    # variables = createVariables(rebin = 2.5)
    variables = createVariables()

    sample_dict = createSamples(channel,analysis_dir, total_weight, server=server)


    makePlots(
        plotDir,
        channel_name,
        variables, 
        regions, 
        total_weight, 
        sample_dict, 
        make_plots=True,
        multiprocess=True
    )

    for i in regions:
        copyfile('/t3home/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/plotting/plot_cfg_hn3l_'+channel+'.py', plotDir+i.name+'/plot_cfg.py')
        copyfile('/t3home/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/python/plot_cfg_hn3l.py', plotDir+i.name+'/plot_cfg_base.py')
        copyfile('/t3home/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/python/plotter/Selections.py', plotDir+i.name+'/Selections.py')
        print 'cfg file stored in "', plotDir + i.name + '/plot_cfg.py"'
        print 'cfg_base file stored in "', plotDir + i.name + '/plot_cfg_base.py"'
        # copytree(plotDir+i.name,'/t3home/dezhu/eos/t3/figures/1_DataMC/FinalStates/mmm/'+i.name)
        os.system("cp -rf %s %s"%(plotDir+i.name,'/t3home/dezhu/eos/t3/figures/1_DataMC/FinalStates/mmm/'+i.name)) 
        print 'directory %s copied to /t3home/dezhu/eos/t3/figures/1_DataMC/FinalStates/mmm!'%(i.name)
