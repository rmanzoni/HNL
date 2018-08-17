import copy
from collections import namedtuple
from operator import itemgetter

from numpy import array

from CMGTools.HNL.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.HNL.plotter.categories_TauMu import cat_Inc
from CMGTools.HNL.plotter.HistCreator import createHistograms, createTrees
from CMGTools.HNL.plotter.HistDrawer import HistDrawer
from CMGTools.HNL.plotter.Variables import taumu_vars, hnl_vars, getVars
from CMGTools.HNL.plotter.helper_methods import getVertexWeight
from CMGTools.HNL.samples.samples_mc_2017 import hnl_bkg
from pdb import set_trace
# from CMGTools.HNL.plotter.qcdEstimationMSSMltau import estimateQCDWMSSM, createQCDWHistograms
from CMGTools.HNL.plotter.defaultGroups import createDefaultGroups

from CMGTools.HNL.plotter.Samples import createSampleLists
from CMGTools.HNL.plotter.metrics import ams_hists

Cut = namedtuple('Cut', ['name', 'cut'])

int_lumi = 41000.0 # pb #### FIXME 

def prepareCuts():
    cuts = []
    inc_cut = '&&'.join([cat_Inc])
    # inc_cut += '&& l2_decayModeFinding'

    cuts.append(Cut('inclusive', inc_cut + '&&  l1_q != l2_q'))

    return cuts

def createSamples(analysis_dir, total_weight, qcd_from_same_sign, w_qcd_mssm_method, r_qcd_os_ss):
    hist_dict = {}
    sample_dict = {}
#    set_trace()
    samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

    sample_dict['all_samples'] = all_samples

    return sample_dict, hist_dict

def createVariables():
    # Taken from Variables.py; can get subset with e.g. getVars(['mt', 'mvis'])
    # variables = taumu_vars
    # variables = getVars(['_norm_', 'mt', 'mvis', 'l1_pt', 'l2_pt', 'l1_eta', 'l2_eta', 'n_vertices', 'n_jets', 'n_bjets'])
    variables = hnl_vars

    return variables

def makePlots(variables, cuts, total_weight, sample_dict, hist_dict, qcd_from_same_sign, w_qcd_mssm_method, mt_cut, friend_func, dc_postfix, make_plots=True, create_trees=False):
    ams_dict = {}
    sample_names = set()
    for cut in cuts:
        cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=sample_dict['all_samples'], cut=cut.cut, lumi=int_lumi, weight=total_weight)
    
        cfg_main.vars = variables

        plots = createHistograms(cfg_main, verbose=False, friend_func=friend_func)
        for variable in variables:
        # for plot in plots.itervalues():
            plot = plots[variable.name]
            createDefaultGroups(plot)
            if make_plots:
                HistDrawer.draw(plot, plot_dir='plots/'+cut.name)

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

if __name__ == '__main__':
        
    data2016G = False

    friend_func = None
    
    qcd_from_same_sign = True
    w_qcd_mssm_method = True
    r_qcd_os_ss = 1.17

    run_central = True
    add_ttbar_sys = False
    add_tes_sys = False

    analysis_dir = '/eos/user/v/vstampf/ntuples/bkg_mc_prompt_e/' # input

    total_weight = 'weight'
# FIXME fix this 
#    total_weight = 'weight * (1. - 0.0772790*(l2_gen_match == 5 && l2_decayMode==0) - 0.138582*(l2_gen_match == 5 && l2_decayMode==1) - 0.220793*(l2_gen_match == 5 && l2_decayMode==10) )' # Tau ID eff scale factor

    if data2016G:
        total_weight = '(' + total_weight + '*' + getVertexWeight(True) + ')'

    print total_weight

    cuts = prepareCuts()

    variables = createVariables()

    sample_dict, hist_dict = createSamples(analysis_dir, total_weight, qcd_from_same_sign=False, w_qcd_mssm_method=False, r_qcd_os_ss=None)
    makePlots(variables, cuts, total_weight, sample_dict, hist_dict={}, qcd_from_same_sign=False, w_qcd_mssm_method=False, mt_cut='', friend_func=lambda f: f.replace('TESUp', 'TESUpMultiMVA'), dc_postfix='_CMS_scale_t_mt_13TeVUp', make_plots=True)



