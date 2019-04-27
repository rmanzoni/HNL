import copy
import os
import shutil
from collections import namedtuple
from operator import itemgetter
from ROOT import gROOT as gr

from shutil import copyfile
from numpy import array

from copy_reg import pickle       # to pickle methods for multiprocessing
from types    import MethodType   # to pickle methods for multiprocessing

from CMGTools.HNL.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.HNL.plotter.categories_HNL import cat_Inc
from CMGTools.HNL.plotter.HistCreator import CreateHists, createTrees
from CMGTools.HNL.plotter.HistDrawer import HistDrawer
from CMGTools.HNL.plotter.Variables import hnl_vars, test_vars, getVars,dde_vars
from CMGTools.HNL.samples.samples_mc_2017 import hnl_bkg
from pdb import set_trace
# from CMGTools.HNL.plotter.qcdEstimationMSSMltau import estimateQCDWMSSM, createQCDWHistograms
from CMGTools.HNL.plotter.defaultGroups import createDefaultGroups

from CMGTools.HNL.plotter.Samples import createSampleLists, setSumWeights
from CMGTools.HNL.plotter.metrics import ams_hists


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
Cut = namedtuple('Cut', ['name', 'cut'])

# int_lumi = 41000.0 # pb #### FIXME 
int_lumi = 41000.0 * (30564478/19122658) # [pb]; adapt to the amount of events done for the nonprompt analysis
#int_lumi = 80000.0 # pb #### FIXME 


## RICCARDO
# cuts.append(Cut('ttjetsloose', 'nbj>1'))
# cuts.append(Cut('zmmloose' , 'l1_pt>5  & l2_pt>5  & l1_q!=l2_q & l1_id_t & l2_id_t & l1_reliso05<0.2 & l2_reliso05<0.2 & abs(l1_dz)<0.2 & abs(l2_dz)<0.2 & abs(l1_dxy)<0.045 & abs(l2_dxy)<0.045 & nbj==0 & pass_e_veto & pass_m_veto'))
#     cuts.append(Cut('zmmhighpt', 'l1_pt>15  & l2_pt>15  & l1_q!=l2_q & l1_id_t & l2_id_t & l1_reliso05<0.2 & l2_reliso05<0.2 & abs(l1_dz)<0.2 & abs(l2_dz)<0.2 & abs(l1_dxy)<0.045 & abs(l2_dxy)<0.045 & nbj==0 & pass_e_veto & pass_m_veto'))
# cuts.append(Cut('zmm'      , 'l1_pt>10 & l2_pt>10 & l1_q!=l2_q & !l0_eid_mva_iso_loose & l0_reliso05>0.15 & l1_id_t & l2_id_t & l1_reliso05<0.2 & l2_reliso05<0.2 & abs(l1_dz)<0.2 & abs(l2_dz)<0.2 & abs(l1_dxy)<0.045 & abs(l2_dxy)<0.045 & nbj==0 & pass_e_veto & pass_m_veto'))

# cuts.append(Cut('inclusive'    , 'l0_pt>30 & l1_pt>4 & l2_pt>4 & l1_q != l2_q & l0_eid_mva_iso_loose & l0_reliso05<0.15'))
# cuts.append(Cut('inclusive'    , 'l0_pt>30 & l1_pt>4 & l2_pt>4 & l1_q != l2_q & l0_eid_mva_iso_loose & l0_reliso05<0.15 & l1_id_m & l2_id_m & l1_reliso05<0.2 & l2_reliso05<0.2'))
# cuts.append(Cut('inc_nobj'     , 'l0_pt>30 & l1_pt>4 & l2_pt>4 & l1_q != l2_q & l0_eid_mva_iso_loose & l0_reliso05<0.15 & l1_id_m & l2_id_m & l1_reliso05<0.2 & l2_reliso05<0.2 & nbj==0'))
# cuts.append(Cut('inc_nobj_veto', 'l0_pt>30 & l1_pt>4 & l2_pt>4 & l1_q != l2_q & l0_eid_mva_iso_loose & l0_reliso05<0.15 & l1_id_m & l2_id_m & l1_reliso05<0.2 & l2_reliso05<0.2 & nbj==0 & pass_e_veto & pass_m_veto'))
# cuts.append(Cut('stringent'    , 'l0_pt>30 & l1_pt>4 & l2_pt>4 & sv_prob>0.1 & sv_cos>0.9 & hnl_2d_disp_sig>3 & abs(hnl_w_q)==1 & hnl_iso_rel<0.2 & hnl_hn_q==0 & hnl_pt_12>20 & l0_eid_mva_iso_loose & l1_is_oot==0 & l2_is_oot==0 & pass_e_veto & pass_m_veto & l1_id_l & l2_id_l & l0_reliso05<0.2 & nbj==0 & hnl_2d_disp>2'))

### VINZENZ
## CONTROL REGIONS
'''slide 14 - DY:     OSSF pair present; |M_ll - m_Z| < 15 GeV; |M_3l - m_Z| > 15 GeV; 0 b-jets; E_T^miss < 30GeV; M_T < 30GeV
   slide 15 - ttbar:  |M_ll - m_Z| > 15 GeV (if OSSF); |M_3l - m_Z| > 15 GeV (if OSSF); >= 1 b-jets; veto M_ll < 12 GeV (conversion)
   slide 17 - WZ:     OSSF pair present; |M_ll -m_Z|< 15 GeV; |M_3l -m_Z| > 15 GeV; 0 b-jets; E_T^miss > 50 GeV ; p_T > 25, 15, 10 GeV (l0,1,2)
   E_T^Miss == pfmet_pt, M_T == hnl_mt_0 
'''
mz = 91.18; mw = 80.4

ZVeto12    = '  &  abs(hnl_m_12 - 91.18) > 15'
ZVeto01    = '  &  abs(hnl_m_01 - 91.18) > 15'
ZVeto02    = '  &  abs(hnl_m_02 - 91.18) > 15'

CR_DY          = '  &  abs(hnl_m_12 - 91.18) < 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj == 0  &  pfmet_pt < 30  &  hnl_mt_0 < 30' 
CR_DY_noMcuts  = '  &  nbj == 0  &  pfmet_pt < 30  &  hnl_mt_0 < 30' 
CR_DYNoM3l     = '  &  abs(hnl_m_12 - 91.18) < 15  &  nbj == 0  &  pfmet_pt < 30  &  hnl_mt_0 < 30' 
CR_DYRic       = 'abs(l0_dz) < 0.2  &  l1_q != l2_q  &  l1_pt > 15  &  l2_pt > 10  &  abs(hnl_m_12 - 91.18) < 15  &  nbj == 0' 
CR_ttbar       = '  &  abs(hnl_m_12 - 91.18) > 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj >= 1  &  hnl_m_12 > 12'
CR_ttbarNoCV   = '  &  abs(hnl_m_12 - 91.18) > 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj >= 1'
CR_ttbarb0NoCV = '  &  abs(hnl_m_12 - 91.18) > 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj == 0'
CR_jpsi        = '  &  abs(hnl_m_12 - 91.18) > 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj >= 1'
CR_jpsiv2      = '  &  abs(hnl_m_12 - 91.18) > 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj >= 1  &  abs(hnl_m_12 - 3.09) < 0.2'
CR_ttbarb0     = '  &  abs(hnl_m_12 - 91.18) > 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj == 0  &  hnl_m_12 > 12'
CR_ttbarb1     = '  &  abs(hnl_m_12 - 91.18) > 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj <= 1  &  hnl_m_12 > 12'
CR_ttbarb2     = '  &  abs(hnl_m_12 - 91.18) > 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj >= 2  &  hnl_m_12 > 12'
CR_WZ          = '  &  abs(hnl_m_12 - 91.18) < 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj == 0  &  pfmet_pt > 50  &  l0_pt > 25  &  l1_pt > 15  &  l2_pt > 10'
CR_WJets       = '  &  abs(hnl_m_12 - 91.18) > 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj == 0  &  pfmet_pt > 50  &  hnl_mt_0 > 30  &  hnl_m_12 > 4'
NaiveSR        = '  &  hnl_pt_12 > 15  &  hnl_w_vis_m < 80.4  &  abs(hnl_m_12 - 91.18) > 10  &  hnl_iso_rel < 0.2  &  hnl_2d_disp_sig > 4  &  l1_id_tnv  &  l2_id_tnv'
NaiveSRNoId    = '  &  hnl_pt_12 > 15  &  hnl_w_vis_m < 80.4  &  abs(hnl_m_12 - 91.18) > 10  &  hnl_iso_rel < 0.2  &  hnl_2d_disp_sig > 4'
NaiveSRv2      = NaiveSR     + '  &  sv_cos > 0.99  &  nbj == 0  &  hnl_w_m > 50  &  abs(hnl_dphi_hnvis0) > 2  &  hnl_mt_0 < 60'
NaiveSRv2NoId  = NaiveSRNoId + '  &  sv_cos > 0.99  &  nbj == 0  &  hnl_w_m > 50  &  abs(hnl_dphi_hnvis0) > 2  &  hnl_mt_0 < 60'

prompt_e_loose  = '  &  l0_eid_mva_noniso_loose'
prompt_e_medium = '  &  l0_eid_cut_medium'
prompt_e_tight  = '  &  l0_eid_cut_tight'

prompt_mu_loose  = '  &&  l0_id_l'
prompt_mu_medium = '  &&  l0_id_m'
prompt_mu_tight  = '  &&  l0_id_t'

looser  = '  &  l1_reliso05 < 0.15  &  l2_reliso05 < 0.15  &  l1_id_m  &  l2_id_m'
# looser_dde  = '  &  l1_reliso_rho_05 < 0.15  &  l2_reliso_rho_05 < 0.15  &  l1_id_m  &  l2_id_m'
looser_dde  = '  & l1_id_m  &  l2_id_m'
tighter = '  &  abs(l1_dz) < 0.2  &  abs(l2_dz) < 0.2  &  l1_reliso05 < 0.15  &  l2_reliso05 < 0.15  &  l1_id_t  &  l2_id_t'
veto    = '  &  pass_e_veto  &  pass_m_veto'

imp_par = '  &  abs(l1_dz) < 0.2  &  abs(l2_dz) < 0.2  &  abs(l1_dxy) < 0.045  &  abs(l2_dxy) < 0.045' 
IDlNoIso   = '  &  l1_id_l  &  l2_id_l'
IDmNoIso   = '  &  l1_id_m  &  l2_id_m'
IDlIso15   = IDlNoIso   + '  &  l1_reliso05 < 0.15  &  l2_reliso05 < 0.15'
IDmIso15   = IDmNoIso   + '  &  l1_reliso05 < 0.15  &  l2_reliso05 < 0.15'

d0p5noIDnorIso = '  &  hnl_2d_disp > 0.5' 
d0p5IDlNoIso   = d0p5noIDnorIso + '  &  l1_id_l  &  l2_id_l'                        
d0p5IDmNoIso   = d0p5noIDnorIso + '  &  l1_id_m  &  l2_id_m'
d0p5IDlIso15   = d0p5IDlNoIso   + '  &  l1_reliso05 < 0.15  &  l2_reliso05 < 0.15'
d0p5IDmIso15   = d0p5IDmNoIso   + '  &  l1_reliso05 < 0.15  &  l2_reliso05 < 0.15'

def defineDataCut(promptLeptonType):
    goodVertices                 = '  &  Flag_goodVertices'    
    globalSuperTightHalo2016     = '  &  Flag_globalSuperTightHalo2016Filter'    
    HBHENoise                    = '  &  Flag_HBHENoiseFilter'                   
    HBHENoiseIso                 = '  &  Flag_HBHENoiseIsoFilter'                
    EcalDeadCellTriggerPrimitive = '  &  Flag_EcalDeadCellTriggerPrimitiveFilter'
    BadPFMuon                    = '  &  Flag_BadPFMuonFilter'                   
    BadChargedCandidate          = '  &  Flag_BadChargedCandidateFilter'         
    eeBadSc                      = '  &  Flag_eeBadScFilter'                     
    ecalBadCalib                 = '  &  Flag_ecalBadCalibFilter'                

    if promptLeptonType == "ele": 
        met_filtered   = goodVertices + globalSuperTightHalo2016 + HBHENoise + HBHENoiseIso + EcalDeadCellTriggerPrimitive + BadPFMuon + BadChargedCandidate + eeBadSc + ecalBadCalib 
    if promptLeptonType == "mu": 
        met_filtered   = ''

    return met_filtered

def prepareCuts(promptLeptonType):
    cuts = []
    inc_cut =   'l1_pt > 4  &  l2_pt > 4  &  l0_pt > 35' #'.join([cat_Inc])
    inc_cut += '  &  l1_q != l2_q'
    inc_cut += '  &  l0_reliso05 < 0.15'
    inc_cut += '  &  abs(l0_dz) < 0.2'
    inc_cut += '  &  hnl_dr_01 > 0.05  &  hnl_dr_02 > 0.05' # avoid ele mu mismatching

    inc_cut_relxd =   'l1_pt > 4  &  l2_pt > 4  &  l0_pt > 35' #'.join([cat_Inc])
    inc_cut_relxd += '  &  abs(l0_dz) < 0.2'
    inc_cut_relxd += '  &  hnl_dr_01 > 0.05  &  hnl_dr_02 > 0.05' # avoid ele mu mismatching

    
    inc_cut_dde =   'l1_pt > 4  &  l2_pt > 4  &  l0_pt > 35' #'.join([cat_Inc])
    inc_cut_dde += '  &  l1_q != l2_q'
    # inc_cut_dde += '  &  l0_reliso_rho_05 < 0.15'
    inc_cut_dde += '  &  abs(l0_dz) < 0.2'
    inc_cut_dde += '  &  hnl_dr_01 > 0.05  &  hnl_dr_02 > 0.05' # avoid ele mu mismatching

    
    if promptLeptonType == "ele":
        l0_loose  = prompt_e_loose
        l0_medium = prompt_e_medium
        l0_tight  = prompt_e_tight
    if promptLeptonType == "mu":
        l0_loose  = prompt_mu_loose
        l0_medium = prompt_mu_medium
        l0_tight  = prompt_mu_tight

#### 29.10. ## redo SR plots for athens
    # cuts.append(Cut('NaiveSRv8_90fb'       , inc_cut + l0_tight + NaiveSRv2 + '  &  sv_prob > 0.05'))     ### DO THIS WITHOUT DATA! ## SETTING NORM TO 200 # REMOVING SINGAL SCALE^2


#### 18.9. ## adding all qcd_mu samples
#    cuts.append(Cut('CR_WJets'         , inc_cut_relxd + l0_tight + CR_WJets + '  &  hnl_dr_12 < 0.4  &  hnl_dr_hnvis0 > 1')) 
#    cuts.append(Cut('CR_DY'            , inc_cut_relxd + l0_tight + CR_DY + veto))

#### 14.9. ## adding some qcd samples
#    cuts.append(Cut('CR_WJets_imp_par'       , inc_cut_relxd + l0_tight + imp_par  + CR_WJets + '  &  hnl_dr_12 < 0.4  &  hnl_dr_hnvis0 > 1'))
#    cuts.append(Cut('CR_WJets_IDlNoIso'         , inc_cut_relxd + l0_tight + IDlNoIso + CR_WJets + '  &  hnl_dr_12 < 0.4  &  hnl_dr_hnvis0 > 1')) # NO IMP PAR! !!CHANGED!!

#### 13.9. ## MET FILTER AND VETO LEP MASSES
#    cuts.append(Cut('CR_WJets_imp_par'       , inc_cut_relxd + l0_tight + imp_par  + CR_WJets + '  &  hnl_dr_12 < 0.4  &  hnl_dr_hnvis0 > 1'))
#    cuts.append(Cut('CR_WJets_IDlNoIso'         , inc_cut_relxd + l0_tight + IDlNoIso + CR_WJets + '  &  hnl_dr_12 < 0.4  &  hnl_dr_hnvis0 > 1')) # NO IMP PAR! !!CHANGED!!

#### 10.9.
#    cuts.append(Cut('CR_WJets_imp_par'       , inc_cut_relxd + l0_tight + imp_par  + CR_WJets + '  &  hnl_dr_12 < 0.4  &  hnl_dr_hnvis0 > 1'))
#    cuts.append(Cut('CR_WJets_IDlNoIso'         , inc_cut_relxd + l0_tight + IDlNoIso    + CR_WJets + '  &  hnl_dr_12 < 0.4  &  hnl_dr_hnvis0 > 1'))
#    cuts.append(Cut('CR_WJets_IDlIso15'         , inc_cut_relxd + l0_tight + IDlIso15    + CR_WJets + '  &  hnl_dr_12 < 0.4  &  hnl_dr_hnvis0 > 1'))

#### 6.9.
#    cuts.append(Cut('CR_TTbarNoCV_d0p5IDmNoIso'    , inc_cut + l0_tight + d0p5IDmNoIso + CR_ttbarNoCV))
#    cuts.append(Cut('CR_TTbar_d0p5IDmNoIso_dxyz'   , inc_cut + l0_tight + d0p5IDmNoIso + imp_par + CR_ttbar))
#    cuts.append(Cut('CR_JPsi_d0p5IDmNoIsov'        , inc_cut + l0_tight + d0p5IDmNoIso   + CR_jpsiv2))   
#    cuts.append(Cut('CR_JPsi_IDmNoIsov2'           , inc_cut + l0_tight + IDmNoIso   + CR_jpsiv2))  # adding smaller2ddisp 
#    cuts.append(Cut('NaiveSRv6'          , inc_cut + l0_tight + NaiveSRv2 + '  &  sv_prob>0.05'))     ### DO THIS WITHOUT DATA! ## SETTING NORM TO 0.5 
#    cuts.append(Cut('NaiveSRv7'          , inc_cut + l0_tight + NaiveSRv2 + '  &  sv_prob>0.05'))     ### DO THIS WITHOUT DATA! ## SETTING NORM TO 200
#    cuts.append(Cut('NaiveSRv8'          , inc_cut + l0_tight + NaiveSRv2 + '  &  sv_prob>0.05'))     ### DO THIS WITHOUT DATA! ## SETTING NORM TO 200 # REMOVING SINGAL SCALE^2
#    cuts.append(Cut('NaiveSRv9'          , inc_cut + l0_tight + NaiveSRv2 + '  &  sv_prob>0.05  &  hnl_2d_disp_sig > 50'))     ### DO THIS WITHOUT DATA! 

#### 5.9.     ## incl proper LHE weighting
###  morning
#    cuts.append(Cut('CR_TTbar_d0p5imp_par'    , inc_cut + l0_tight + d0p5imp_par + CR_ttbar))
#    cuts.append(Cut('CR_TTbar_d0p5IDmNoIso'      , inc_cut + l0_tight + d0p5IDmNoIso   + CR_ttbar))
#    cuts.append(Cut('CR_TTbarb0_d0p5imp_par'  , inc_cut + l0_tight + d0p5imp_par + CR_ttbarb0))
#    cuts.append(Cut('CR_WZ_d0p5IDmIso15'         , inc_cut + l0_tight + d0p5IDmIso15   + CR_WZ))
###  afternoon  # CHECK IF PLOTS FROM LAST WEEK STILL MAKE SENSE WITH PROPER WEIGHTING
#    cuts.append(Cut('CR_TTbar_imp_parv4'    , inc_cut + l0_tight + imp_par + CR_ttbar))
#    cuts.append(Cut('CR_TTbar_IDmNoIsov3'      , inc_cut + l0_tight + IDmNoIso   + CR_ttbar))
#    cuts.append(Cut('CR_TTbarb0_imp_parv3'  , inc_cut + l0_tight + imp_par + CR_ttbarb0))
#    cuts.append(Cut('CR_WZ_IDmIso15v3'         , inc_cut + l0_tight + IDmIso15   + CR_WZ))
#    cuts.append(Cut('CR_DY_imp_parv3'     , inc_cut + l0_tight + imp_par + CR_DY + veto))
#    cuts.append(Cut('CR_DY_IDlNoIsov3'       , inc_cut + l0_tight + IDlNoIso   + CR_DY + veto))
#    cuts.append(Cut('CR_DY_IDlIso15v3'       , inc_cut + l0_tight + IDlIso15   + CR_DY + veto))
#    cuts.append(Cut('CR_WZ_IDmNoIsov3'         , inc_cut + l0_tight + IDmNoIso   + CR_WZ))
#    cuts.append(Cut('CR_WZ_IDlNoIsov3'         , inc_cut + l0_tight + IDlNoIso   + CR_WZ))
#    cuts.append(Cut('NaiveSRv4'          , inc_cut + l0_tight + NaiveSRv2))     ### DO THIS WITHOUT DATA!
### evening REVERT BACK TO INCL DY 
#    cuts.append(Cut('CR_WZ_IDmIso15v4'          , inc_cut + l0_tight + IDmIso15       + CR_WZ))
#    cuts.append(Cut('CR_TTbar_d0p5IDmNoIsov2'   , inc_cut + l0_tight + d0p5IDmNoIso   + CR_ttbar))
#    cuts.append(Cut('NaiveSRv5'          , inc_cut + l0_tight + NaiveSRv2))     ### DO THIS WITHOUT DATA! 
#    cuts.append(Cut('CR_JPsi_imp_par'          , inc_cut + l0_tight + imp_par + CR_jpsi))   
#    cuts.append(Cut('CR_JPsi_IDmNoIso'            , inc_cut + l0_tight + IDmNoIso   + CR_jpsi))   
#    cuts.append(Cut('CR_JPsi_IDmIso15'            , inc_cut + l0_tight + IDmIso15   + CR_jpsi))   
#    cuts.append(Cut('CR_JPsi_IDmNoIsov2'           , inc_cut + l0_tight + IDmNoIso   + CR_jpsiv2))   
#    cuts.append(Cut('CR_JPsi_IDlNoIso'             , inc_cut + l0_tight + IDlNoIso   + CR_jpsiv2))   

#### 4.9.
#    cuts.append(Cut('CR_TTbar_d1imp_par'    , inc_cut + l0_tight + d1imp_par + CR_ttbar))
#    cuts.append(Cut('CR_TTbar_d1IDmNoIso'      , inc_cut + l0_tight + d1IDmNoIso   + CR_ttbar))
#    cuts.append(Cut('CR_TTbarb0_d1imp_par'  , inc_cut + l0_tight + d1imp_par + CR_ttbarb0))
#    cuts.append(Cut('CR_WZ_d1IDmIso15'         , inc_cut + l0_tight + d1IDmIso15   + CR_WZ))
#    cuts.append(Cut('NaiveSRNoIdv2'            , inc_cut + l0_tight + NaiveSRNoId))
#    cuts.append(Cut('NaiveSRv2NoIdv2'          , inc_cut + l0_tight + NaiveSRv2NoId))

#### 3.9.
#    cuts.append(Cut('CR_TTbarb0v2', inc_cut + l0_tight + imp_par + CR_ttbarb0))
#    cuts.append(Cut('CR_TTbarb0v3', inc_cut + l0_tight + imp_par + CR_ttbarb0))  # NEW SAMPLES
#    cuts.append(Cut('test_batch_multi_CR_TTbarb0v3', inc_cut + l0_tight + imp_par + CR_ttbarb0))  # NEW SAMPLES
#    cuts.append(Cut('TTbar_disp1' , inc_cut + l0_tight + CR_ttbar + '  &  hnl_2d_disp > 1'))
### evening ## NEW SAMPLES FOR DY
#    cuts.append(Cut('TTbar_disp1v2'          , inc_cut + l0_tight + CR_ttbar   + '  &  hnl_2d_disp > 1')) # NEW SAMPLES
#    cuts.append(Cut('CR_TTbar_imp_parv3'  , inc_cut + l0_tight + imp_par + CR_ttbar))
#    cuts.append(Cut('CR_TTbarb0_imp_parv2', inc_cut + l0_tight + imp_par + CR_ttbarb0))
#    cuts.append(Cut('CR_TTbarb0NoCVv2'       , inc_cut + l0_tight + imp_par + CR_ttbarb0NoCV))
#    cuts.append(Cut('CR_DY_imp_parv2'     , inc_cut + l0_tight + imp_par + CR_DY + veto))
#    cuts.append(Cut('CR_DY_IDlNoIsov2'       , inc_cut + l0_tight + IDlNoIso   + CR_DY + veto))
#    cuts.append(Cut('CR_DY_IDlIso15v2'       , inc_cut + l0_tight + IDlIso15   + CR_DY + veto))

#### 2.9.
#    cuts.append(Cut('CR_TTbarb1_imp_parv2', inc_cut + l0_tight + imp_par + CR_ttbarb1))
#    cuts.append(Cut('CR_TTbarb1_IDlNoIsov2'  , inc_cut + l0_tight + IDlNoIso   + CR_ttbarb1))
#    cuts.append(Cut('CR_TTbarb1_IDlIso15v2'  , inc_cut + l0_tight + IDlIso15   + CR_ttbarb1))
#    cuts.append(Cut('CR_TTbarb2_imp_parv2', inc_cut + l0_tight + imp_par + CR_ttbarb2))
#    cuts.append(Cut('CR_TTbarb2_IDlNoIsov2'  , inc_cut + l0_tight + IDlNoIso   + CR_ttbarb2))
#    cuts.append(Cut('CR_TTbarb2_IDlIso15v2'  , inc_cut + l0_tight + IDlIso15   + CR_ttbarb2))
# 
#    cuts.append(Cut('CR_WZ_imp_parv2'   , inc_cut + l0_tight + imp_par + CR_WZ))
#    cuts.append(Cut('CR_WZ_IDmNoIsov2'   , inc_cut + l0_tight + IDmNoIso + CR_WZ))
#    cuts.append(Cut('CR_WZ_IDmIso15v2'   , inc_cut + l0_tight + IDmIso15 + CR_WZ))
#    cuts.append(Cut('CR_WZ_IDlNoIsov2'   , inc_cut + l0_tight + IDlNoIso + CR_WZ))
#    cuts.append(Cut('CR_WZ_IDlIso15v2'   , inc_cut + l0_tight + IDlIso15 + CR_WZ))

#### 1.9.
### testing multiprocessing
#    cuts.append(Cut('test_multi_ttbar', inc_cut + l0_tight + imp_par + CR_ttbarb0))
#    cuts.append(Cut('test_multi', inc_cut + l0_tight + tighter))
###                            ## NEW hnl_dr_01>0.05 AND hnl_dr_02>0.05 AND UPDATED BINNING FOR reliso (UP TO 0.5) 
#    cuts.append(Cut('NaiveSRv3'          , inc_cut + l0_tight + NaiveSRv2))
#    cuts.append(Cut('CR_DY_imp_parv2'   , inc_cut + l0_tight + imp_par + CR_DY + veto))
#    cuts.append(Cut('CR_DY_IDmNoIsov2'   , inc_cut + l0_tight + IDmNoIso + CR_DY + veto))
#    cuts.append(Cut('CR_DY_IDmIso15v2'   , inc_cut + l0_tight + IDmIso15 + CR_DY + veto))
#    cuts.append(Cut('CR_DYNoM3l_IDlNoIsov2'  , inc_cut + l0_tight + CR_DYNoM3l + veto + IDlNoIso))
#    cuts.append(Cut('CR_DYNoM3l_IDlIso15v2'  , inc_cut + l0_tight + CR_DYNoM3l + veto + IDlIso15))

#    cuts.append(Cut('CR_TTbar_imp_parv2', inc_cut + l0_tight + imp_par + CR_ttbar))
#    cuts.append(Cut('CR_TTbar_IDmNoIsov2', inc_cut + l0_tight + IDmNoIso + CR_ttbar))
#    cuts.append(Cut('CR_TTbar_IDmIso15v2', inc_cut + l0_tight + IDmIso15 + CR_ttbar))

#### 31.8.
#    cuts.append(Cut('CR_TTbarb0_imp_par', inc_cut + l0_tight + imp_par + CR_ttbarb0))
#    cuts.append(Cut('CR_TTbarb0NoCV_imp_par', inc_cut + l0_tight + imp_par + CR_ttbarb0NoCV))
#    cuts.append(Cut('NaiveSRNoId'            , inc_cut + l0_tight + NaiveSRNoId))
#    cuts.append(Cut('test_multi', inc_cut + l0_tight + tighter))

#### 30.8.
###  morning
#    cuts.append(Cut('tight_imp_par'     , inc_cut + l0_tight + imp_par))
#    cuts.append(Cut('CR_DYRic'             , CR_DYRic + looser))
#    cuts.append(Cut('CR_DYNoM3l_imp_par', inc_cut + l0_tight + CR_DYNoM3l + veto + imp_par))
#    cuts.append(Cut('CR_DYNoM3l_IDmNoIso'  , inc_cut + l0_tight + CR_DYNoM3l + veto + IDmNoIso))
#    cuts.append(Cut('CR_DYNoM3l_IDmIso15'  , inc_cut + l0_tight + CR_DYNoM3l + veto + IDmIso15))
#    cuts.append(Cut('NaiveSR'              , inc_cut + l0_tight + NaiveSR))
###  afternoon
#    cuts.append(Cut('CR_DYNoM3l_IDlNoIso'  , inc_cut + l0_tight + CR_DYNoM3l + veto + IDlNoIso))
#    cuts.append(Cut('CR_DYNoM3l_IDlIso15'  , inc_cut + l0_tight + CR_DYNoM3l + veto + IDlIso15))
#    cuts.append(Cut('CR_TTbarb2_imp_par', inc_cut + l0_tight + imp_par + CR_ttbarb2))
#    cuts.append(Cut('CR_TTbarb2_IDlNoIso'  , inc_cut + l0_tight + IDlNoIso   + CR_ttbarb2))
#    cuts.append(Cut('CR_TTbarb2_IDlIso15'  , inc_cut + l0_tight + IDlIso15   + CR_ttbarb2))
#    cuts.append(Cut('NaiveSRv2'            , inc_cut + l0_tight + NaiveSRv2))
#    cuts.append(Cut('CR_WZ_IDlNoIso'   , inc_cut + l0_tight + IDlNoIso + CR_WZ))
#    cuts.append(Cut('CR_WZ_IDlIso15'   , inc_cut + l0_tight + IDlIso15 + CR_WZ))
###  night
#    cuts.append(Cut('CR_TTbarb1_imp_par', inc_cut + l0_tight + imp_par + CR_ttbarb1))
#    cuts.append(Cut('CR_TTbarb1_IDlNoIso'  , inc_cut + l0_tight + IDlNoIso   + CR_ttbarb1))
#    cuts.append(Cut('CR_TTbarb1_IDlIso15'  , inc_cut + l0_tight + IDlIso15   + CR_ttbarb1))

####  29.8.
#    cuts.append(Cut('CR_DY_imp_par'   , inc_cut + l0_tight + imp_par + CR_DY + veto))
#    cuts.append(Cut('CR_TTbar_imp_par', inc_cut + l0_tight + imp_par + CR_ttbar))
#    cuts.append(Cut('CR_WZ_imp_par'   , inc_cut + l0_tight + imp_par + CR_WZ))

#    cuts.append(Cut('CR_DY_IDmNoIso'   , inc_cut + l0_tight + IDmNoIso + CR_DY + veto))
#    cuts.append(Cut('CR_TTbar_IDmNoIso', inc_cut + l0_tight + IDmNoIso + CR_ttbar))
#    cuts.append(Cut('CR_WZ_IDmNoIso'   , inc_cut + l0_tight + IDmNoIso + CR_WZ))

#    cuts.append(Cut('CR_DY_IDmIso15'   , inc_cut + l0_tight + IDmIso15 + CR_DY + veto))
#    cuts.append(Cut('CR_TTbar_IDmIso15', inc_cut + l0_tight + IDmIso15 + CR_ttbar))
#    cuts.append(Cut('CR_WZ_IDmIso15'   , inc_cut + l0_tight + IDmIso15 + CR_WZ))

    cuts.append(Cut('CR_DY', inc_cut + l0_loose + looser + CR_DY))
    # cuts.append(Cut('CR_TTbar', inc_cut + l0_loose + looser + CR_ttbar))
    # cuts.append(Cut('CR_TTbar_dde', inc_cut_dde  + l0_loose + looser_dde + CR_ttbar))
#    cuts.append(Cut('CR_WZ', inc_cut + l0_loose + looser + CR_WZ))
 
#### 24.8.
#    cuts.append(Cut('looser', inc_cut + l0_loose + '  &  l1_id_m & l2_id_m'))
#    cuts.append(Cut('tighter_e_loose', inc_cut + l0_loose + tighter))
#    cuts.append(Cut('tighter_e_medium', inc_cut + l0_medium' + tighter))
#    cuts.append(Cut('tighter_e_tight', inc_cut + l0_tight + tighter))

#### 20190205 MC + DDE
    Z_veto_01       = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  (l0_q + l2_q != 0)  &  (l1_q + l2_q != 0)'
    Z_veto_02       = '(l0_q + l1_q != 0)  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  (l1_q + l2_q != 0)'
    Z_veto_12       = '(l0_q + l1_q != 0)  &  (l0_q + l2_q != 0)  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )' 

    Z_veto_01_02    = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  (l1_q + l2_q != 0)'  
    Z_veto_01_12    = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  (l0_q + l2_q != 0)  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )'  
    Z_veto_02_12    = '(l0_q + l1_q != 0)  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )'  

    Z_veto_01_02_12 = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )'

    single_Z_veto = '(  ' + Z_veto_01 + '   |   ' + Z_veto_02 + '   |   ' + Z_veto_12 + '  )'
    double_Z_veto = '(  ' + Z_veto_01_02 + '   |   ' + Z_veto_01_12 + '   |   ' + Z_veto_02_12 + '  )'

    Z_veto = ' & (   ' + single_Z_veto + '    |    ' + double_Z_veto + '    |    ' + Z_veto_01_02_12 + '   )' 

    tight = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2 & l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso_rho_04 < 0.15 & l1_id_l & l2_id_l & l1_reliso_rho_04 < 0.15 & l2_reliso_rho_04 < 0.15 & hnl_iso04_rel_rhoArea < 1'
    loose = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2 & l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso_rho_04 < 0.15 & l1_id_l & l2_id_l & l1_reliso_rho_04 > 0.15 & l2_reliso_rho_04 > 0.15 & hnl_iso04_rel_rhoArea < 1'

    tight += ' & ' + Z_veto

    DDE1       = '& nbj == 0 & abs(hnl_w_vis_m) > 80 '
    LooseNotTight  = ' & l1_reliso05 > 0.15 & l2_reliso05 > 0.15 & l1_id_m & l2_id_m & nbj == 0 & abs(hnl_w_vis_m) > 80 & abs(l1_jet_pt-l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2 & hnl_iso04_rel_rhoArea < 1'
    # cuts.append(Cut('AR_DDE1', inc_cut + l0_loose + LooseNotTight))
    # cuts.append(Cut('AR_DDE2', 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2 & l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso05 < 0.15 & l1_id_l & l2_id_l & (l1_reliso05 > 0.15 | l2_reliso05 > 0.15) & hnl_iso04_rel_rhoArea < 1'))
    # cuts.append(Cut('AR_DDE3', 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2 & l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso05 < 0.15 & l1_id_l & l2_id_l & (l1_reliso05 > 0.15 | l2_reliso05 > 0.15) & hnl_iso04_rel_rhoArea < 1'))



    dde_tight  = '  &  l1_reliso05 < 0.15  &  l2_reliso05 < 0.15  &  l1_id_l  &  l2_id_l'
    # cuts.append(Cut('CR_DY', inc_cut + l0_tight + looser + CR_DY + Z_veto))
    # cuts.append(Cut('CR_ttbar', inc_cut + l0_tight + dde_tight + CR_ttbar))

    # cuts.append(Cut('AR_DDE2', tight + Z_veto))



    print('###########################################################')
    print('# setting cuts')
    print('###########################################################')
    print cuts

    return cuts

def createSamples(channel, analysis_dir, total_weight,server, qcd_from_same_sign, w_qcd_mssm_method, r_qcd_os_ss, add_data_cut=None):
    hist_dict = {}
    sample_dict = {}
    print "creating samples from %s"%(analysis_dir)
    samples_mc, samples_signal_mc, samples_data, samples, all_samples, sampleDict, samples_essential, samples_essential_data, samples_dde, samples_data_dde, samples_dde_data, samples_bkg = createSampleLists(analysis_dir=analysis_dir, server = server, channel=channel, add_data_cut=add_data_cut)

    #select here the samples you wish to use
    # working_samples = samples_dde_data
    # working_samples = samples_essential
    # working_samples = samples_mc
    working_samples = all_samples
    # working_samples = samples_signal_mc
    # working_samples = samples_bkg
    # working_samples = samples_dde
    # working_samples = samples_data
    # working_samples = samples_data_dde

    working_samples = setSumWeights(working_samples)

    sample_dict['working_samples'] = working_samples

    #TODO implement a code to print the samples
    print('###########################################################')
    print'# samples to be used:'
    print('###########################################################')
    for w in working_samples: print w.name + ', ',
    print '(%d sample(s))'%(len(working_samples))
    


    return sample_dict, hist_dict

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

def makePlots(plotDir,channel_name,variables, cuts, total_weight, sample_dict, hist_dict, qcd_from_same_sign, w_qcd_mssm_method, mt_cut, friend_func, dc_postfix, make_plots=True, create_trees=False, multiprocess = True):
    ams_dict = {}
    sample_names = set()
    for cut in cuts:
        cutDir = plotDir+cut.name
        if not os.path.exists(cutDir):
            os.mkdir(cutDir)
            print "Directory ", cutDir, "Created "
        else:
            print "Directory ", cutDir, "already exists, overwriting it!"
            shutil.rmtree(cutDir)
            os.mkdir(cutDir)

        cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=sample_dict['working_samples'], cut=cut.cut, lumi=int_lumi, weight=total_weight)
    
        cfg_main.vars = variables
        
        HISTS = CreateHists(cfg_main)

        plots = HISTS.createHistograms(cfg_main, verbose=False, friend_func=friend_func,multiprocess = multiprocess)
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
                plot.Group('Conversions',['Conversion_DYBB','Conversion_DYJetsToLL_M10to50','Conversion_WJetsToLNu'])
                plot.Group('QCD',['QCD_pt_15to20_mu', 'QCD_pt_20to30_mu', 'QCD_pt_30to50_mu', 'QCD_pt_50to80_mu', 'QCD_pt_80to120_mu'])
                plot.Group('WJets', ['W1JetsToLNu', 'W2JetsToLNu', 'W3JetsToLNu', 'W4JetsToLNu'])
            # createDefaultGroups(plot)
            if make_plots:
                HistDrawer.draw(plot, channel = channel_name, plot_dir = plotDir+cut.name)

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
        friend_func = None
    
    qcd_from_same_sign = True
    w_qcd_mssm_method = True
    r_qcd_os_ss = 1.17

    run_central = True
    add_ttbar_sys = False
    add_tes_sys = False

    if server == "lxplus":
        analysis_dir = '/eos/user/v/vstampf/ntuples/'
   
    if server == "t3":
        analysis_dir = 'root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv1.0/' + channel + '/'

    total_weight = 'weight * lhe_weight'

    print total_weight

    cuts = prepareCuts(promptLeptonType)

    # variables = createVariables(2.5)
    variables = createVariables()


    met_filtered = defineDataCut(promptLeptonType)

    sample_dict, hist_dict = createSamples(channel,analysis_dir, total_weight, server=server, qcd_from_same_sign=False, w_qcd_mssm_method=False, r_qcd_os_ss=None, add_data_cut=met_filtered)


    makePlots(
        plotDir,
        channel_name,
        variables, 
        cuts, 
        total_weight, 
        sample_dict, 
        hist_dict={}, 
        qcd_from_same_sign=False, 
        w_qcd_mssm_method=False, 
        mt_cut='', 
        friend_func=lambda f: f.replace('TESUp', 'TESUpMultiMVA'), 
        dc_postfix='_CMS_scale_t_mt_13TeVUp', 
        make_plots=True,
        multiprocess=True
    )

    for i in cuts:
        copyfile('/t3home/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/plotting/plot_cfg_hn3l_'+channel+'.py', plotDir+i.name+'/plot_cfg.py')
        copyfile('/t3home/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/python/plot_cfg_hn3l.py', plotDir+i.name+'/plot_cfg_base.py')
        print 'cfg file stored in "', plotDir + i.name + '/plot_cfg.py"'
        print 'cfg_base file stored in "', plotDir + i.name + '/plot_cfg_base.py"'
