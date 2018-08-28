import copy
from collections import namedtuple
from operator import itemgetter

from numpy import array

from CMGTools.HNL.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.HNL.plotter.categories_HNL import cat_Inc
from CMGTools.HNL.plotter.HistCreator import createHistograms, createTrees
from CMGTools.HNL.plotter.HistDrawer import HistDrawer
from CMGTools.HNL.plotter.Variables import hnl_vars, getVars
from CMGTools.HNL.samples.samples_mc_2017 import hnl_bkg
from pdb import set_trace
# from CMGTools.HNL.plotter.qcdEstimationMSSMltau import estimateQCDWMSSM, createQCDWHistograms
from CMGTools.HNL.plotter.defaultGroups import createDefaultGroups

from CMGTools.HNL.plotter.Samples import createSampleLists
from CMGTools.HNL.plotter.metrics import ams_hists

Cut = namedtuple('Cut', ['name', 'cut'])

int_lumi = 41000.0 # pb #### FIXME 
#int_lumi = 80000.0 # pb #### FIXME 

def prepareCuts():
    cuts = []

    inc_cut = '&&'.join([cat_Inc])
    inc_cut += '  &&  l1_q != l2_q'
    inc_cut += '  &&  l0_reliso05 < 0.15'
    inc_cut += '  &&  l0_dz < 0.2'

#     cuts.append(Cut('ttjetsloose', 'nbj>1'))
#     cuts.append(Cut('zmmloose' , 'l1_pt>5  & l2_pt>5  & l1_q!=l2_q & l1_id_t & l2_id_t & l1_reliso05<0.2 & l2_reliso05<0.2 & l1_dz<0.2 & l2_dz<0.2 & l1_dxy<0.045 & l2_dxy<0.045 & nbj==0 & pass_e_veto & pass_m_veto'))
#     cuts.append(Cut('zmmhighpt', 'l1_pt>15  & l2_pt>15  & l1_q!=l2_q & l1_id_t & l2_id_t & l1_reliso05<0.2 & l2_reliso05<0.2 & l1_dz<0.2 & l2_dz<0.2 & l1_dxy<0.045 & l2_dxy<0.045 & nbj==0 & pass_e_veto & pass_m_veto'))
#     cuts.append(Cut('zmm'      , 'l1_pt>10 & l2_pt>10 & l1_q!=l2_q & !l0_eid_mva_iso_loose & l0_reliso05>0.15 & l1_id_t & l2_id_t & l1_reliso05<0.2 & l2_reliso05<0.2 & l1_dz<0.2 & l2_dz<0.2 & l1_dxy<0.045 & l2_dxy<0.045 & nbj==0 & pass_e_veto & pass_m_veto'))

#     cuts.append(Cut('inclusive'    , 'l0_pt>30 & l1_pt>4 & l2_pt>4 & l1_q != l2_q && l0_eid_mva_iso_loose & l0_reliso05<0.15'))
#     cuts.append(Cut('inclusive'    , 'l0_pt>30 & l1_pt>4 & l2_pt>4 & l1_q != l2_q && l0_eid_mva_iso_loose & l0_reliso05<0.15 & l1_id_m & l2_id_m & l1_reliso05<0.2 & l2_reliso05<0.2'))
#     cuts.append(Cut('inc_nobj'     , 'l0_pt>30 & l1_pt>4 & l2_pt>4 & l1_q != l2_q && l0_eid_mva_iso_loose & l0_reliso05<0.15 & l1_id_m & l2_id_m & l1_reliso05<0.2 & l2_reliso05<0.2 & nbj==0'))
#     cuts.append(Cut('inc_nobj_veto', 'l0_pt>30 & l1_pt>4 & l2_pt>4 & l1_q != l2_q && l0_eid_mva_iso_loose & l0_reliso05<0.15 & l1_id_m & l2_id_m & l1_reliso05<0.2 & l2_reliso05<0.2 & nbj==0 & pass_e_veto & pass_m_veto'))
#     cuts.append(Cut('stringent'    , 'l0_pt>30 & l1_pt>4 & l2_pt>4 & sv_prob>0.1 & sv_cos>0.9 & hnl_2d_disp_sig>3 & abs(hnl_w_q)==1 & hnl_iso_rel<0.2 & hnl_hn_q==0 & hnl_pt_12>20 & l0_eid_mva_iso_loose & l1_is_oot==0 & l2_is_oot==0 & pass_e_veto & pass_m_veto & l1_id_l & l2_id_l & l0_reliso05<0.2 & nbj==0 & hnl_2d_disp>2'))

    # vinzenz
    looser  = '  &&  l1_reliso05 < 0.15  &&  l2_reliso05 < 0.15  &&  l1_id_m  &&  l2_id_m'
    tighter = '  &&  l1_dz < 0.2  &&  l2_dz < 0.2  &&  l1_reliso05 < 0.15  &&  l2_reliso05 < 0.15  &&  l1_id_t  &&  l2_id_t'

    '''slide 14 - DY:     OSSF pair present; |M_ll - m_Z| < 15 GeV; |M_3l - m_Z| > 15 GeV; 0 b-jets; E_T^miss < 30GeV; M_T < 30GeV
       slide 15 - ttbar:  |M_ll - m_Z| > 15 GeV (if OSSF); |M_3l - m_Z| > 15 GeV (if OSSF); >= 1 b-jets; veto M_ll < 12 GeV (conversion)
       slide 17 - WZ:     OSSF pair present; |M_ll -m_Z|< 15 GeV; |M_3l -m_Z| > 15 GeV; 0 b-jets; E_T^miss > 50 GeV ; p_T > 25, 15, 10 GeV (l0,1,2)
       E_T^Miss == puppimet_pt, M_T == hnl_mt_0 + hnl_mt_1 + hnl_mt_2
    '''
    mz = 91.18
    CR_DY    = '  &&  abs(hnl_m_12 - 91.18) < 15  &&  abs(hnl_w_vis_m - 91.18) > 15  &&  nbj == 0  &&  puppimet_pt < 30  &&  (hnl_mt_0 + hnl_mt_1 + hnl_mt_2) < 30'
    CR_ttbar = '  &&  abs(hnl_m_12 - 91.18) > 15  &&  abs(hnl_w_vis_m - 91.18) > 15  &&  nbj >= 1  &&  hnl_m_12 > 12'
    CR_WZ    = '  &&  abs(hnl_m_12 - 91.18) < 15  &&  abs(hnl_w_vis_m - 91.18) > 15  &&  nbj == 0  &&  puppimet_pt > 50  &&  l0_pt > 25  &&  l1_pt > 15  &&  l2_pt > 10'

    cuts.append(Cut('DY'   , inc_cut + '  && l0_eid_mva_noniso_loose' + looser + CR_DY))
    cuts.append(Cut('TTbar', inc_cut + '  && l0_eid_mva_noniso_loose' + looser + CR_ttbar))
    cuts.append(Cut('WZ'   , inc_cut + '  && l0_eid_mva_noniso_loose' + looser + CR_WZ))
#    cuts.append(Cut('looser', inc_cut + '  &&  l0_eid_mva_noniso_loose  &&  l1_id_m & l2_id_m'))
#    cuts.append(Cut('tighter_e_loose', inc_cut + '  &&  l0_eid_mva_noniso_loose' + tighter))
#    cuts.append(Cut('tighter_e_medium', inc_cut + '  &&  l0_eid_cut_medium' + tighter))
#    cuts.append(Cut('tighter_e_tight', inc_cut + '  &&  l0_eid_cut_tight' + tighter))

    return cuts

def createSamples(analysis_dir, total_weight, qcd_from_same_sign, w_qcd_mssm_method, r_qcd_os_ss):
    hist_dict = {}
    sample_dict = {}
#    set_trace()
    samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

    sample_dict['all_samples'] = all_samples

    return sample_dict, hist_dict

def createVariables(rebin=None):
    # Taken from Variables.py; can get subset with e.g. getVars(['mt', 'mvis'])
    # variables = taumu_vars
    # variables = getVars(['_norm_', 'mt', 'mvis', 'l1_pt', 'l2_pt', 'l1_eta', 'l2_eta', 'n_vertices', 'n_jets', 'n_bjets'])
    variables = hnl_vars

    if rebin>0:
        for ivar in hnl_vars:
            if ivar.name in ['_norm_', 'n_vtx']: continue
            ivar.binning['nbinsx'] = int(ivar.binning['nbinsx']/rebin)

    return variables

def makePlots(variables, cuts, total_weight, sample_dict, hist_dict, qcd_from_same_sign, w_qcd_mssm_method, mt_cut, friend_func, dc_postfix, make_plots=True, create_trees=False):
    ams_dict = {}
    sample_names = set()
    for cut in cuts:
        cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=sample_dict['all_samples'], cut=cut.cut, lumi=int_lumi, weight=total_weight)
    
        cfg_main.vars = variables

        plots = createHistograms(cfg_main, verbose=False, friend_func=friend_func)
        #plots.legendPos = 'right'
        for variable in variables:
        # for plot in plots.itervalues():
            plot = plots[variable.name]
            plot.Group('data_obs', ['data_2017B_e', 'data_2017C_e', 'data_2017D_e', 'data_2017E_e', 'data_2017F_e'])
            plot.Group('Diboson', ['WZTo3LNu_e', 'ZZTo4L_e'])
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
        
    friend_func = None
    
    qcd_from_same_sign = True
    w_qcd_mssm_method = True
    r_qcd_os_ss = 1.17

    run_central = True
    add_ttbar_sys = False
    add_tes_sys = False

    analysis_dir = '/eos/user/v/vstampf/ntuples/'#bkg_mc_prompt_e/' # input

    total_weight = 'weight'
# FIXME fix this 
#    total_weight = 'weight * (1. - 0.0772790*(l2_gen_match == 5 && l2_decayMode==0) - 0.138582*(l2_gen_match == 5 && l2_decayMode==1) - 0.220793*(l2_gen_match == 5 && l2_decayMode==10) )' # Tau ID eff scale factor

    print total_weight

    cuts = prepareCuts()

    variables = createVariables(2.5)
#     import pdb ; pdb.set_trace()

    sample_dict, hist_dict = createSamples(analysis_dir, total_weight, qcd_from_same_sign=False, w_qcd_mssm_method=False, r_qcd_os_ss=None)
    makePlots(variables, cuts, total_weight, sample_dict, hist_dict={}, qcd_from_same_sign=False, w_qcd_mssm_method=False, mt_cut='', friend_func=lambda f: f.replace('TESUp', 'TESUpMultiMVA'), dc_postfix='_CMS_scale_t_mt_13TeVUp', make_plots=True)



