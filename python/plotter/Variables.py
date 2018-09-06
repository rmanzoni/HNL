from math import pi

from CMGTools.HNL.plotter.PlotConfigs import VariableCfg as VCfg

from CMGTools.HNL.plotter.binning import binning_svfitMass_finer, binning_mttotal, binning_mttotal_fine

hnl_vars = [
    VCfg(name='CR_l0_pt_cone' , drawname='l0_pt * (1 + l0_reliso05)'  , binning={'nbinsx':16, 'xmin':0.  , 'xmax':200.}, unit='GeV', xtitle='p_{T}^{Cone} (leading)'),
    VCfg(name='CR_l2_pt_cone' , drawname='l2_pt * (1 + l2_reliso05)'  , binning={'nbinsx':16, 'xmin':0.  , 'xmax':200.}, unit='GeV', xtitle='p_{T}^{Cone} (trailing)'),
    VCfg(name='CR_hnl_m_12'   , drawname='hnl_m_12'   , binning={'nbinsx':24, 'xmin':0   , 'xmax':150 }, unit='GeV', xtitle='dimuon mass'),
    VCfg(name='CR_hnl_mt_0'   , drawname='hnl_mt_0'   , binning={'nbinsx':16, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='M_{T} (leading)'),
    VCfg(name='CR_hnl_w_vis_m', drawname='hnl_w_vis_m', binning={'nbinsx':24, 'xmin':50  , 'xmax':300 }, unit='GeV', xtitle='3 lepton mass'),

    VCfg(name='_norm_'     , drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),

    VCfg(name='n_vtx', binning={'nbinsx':101, 'xmin':-0.5, 'xmax':100.5}, unit=None, xtitle='N_{vertices}'),

    VCfg(name='l0_pt'      , binning={'nbinsx':40, 'xmin':0.  , 'xmax':100.}, unit='GeV', xtitle='prompt lepton p_{T}'),
    VCfg(name='l0_eta'     , binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='prompt lepton #eta'),
    VCfg(name='l0_phi'     , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi  }, unit='rad', xtitle='prompt lepton #phi'),
    VCfg(name='l1_pt'      , binning={'nbinsx':40, 'xmin':0.  , 'xmax':100.}, unit='GeV', xtitle='1st muon p_{T}'),
    VCfg(name='l1_eta'     , binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='1st muon #eta'),
    VCfg(name='l1_phi'     , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi  }, unit='rad', xtitle='1st muon #phi'),
    VCfg(name='l2_pt'      , binning={'nbinsx':40, 'xmin':0.  , 'xmax':100.}, unit='GeV', xtitle='2nd muon p_{T}'),
    VCfg(name='l2_eta'     , binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='2nd muon #eta'),
    VCfg(name='l2_phi'     , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi  }, unit='rad', xtitle='2nd muon #phi'),

    VCfg(name='l0_dxy', binning={'nbinsx':100, 'xmin':-2. , 'xmax':2. }, unit='cm', xtitle='prompt lepton d_{xy}'),
    VCfg(name='l0_dz' , binning={'nbinsx':100, 'xmin':-3. , 'xmax':3. }, unit='cm', xtitle='prompt lepton d_{z}'),
    VCfg(name='l1_dxy', binning={'nbinsx':100, 'xmin':-4. , 'xmax':4. }, unit='cm', xtitle='1st muon d_{xy}'),
    VCfg(name='l1_dxy_coarse', drawname='l1_dxy', binning={'nbinsx':40, 'xmin':-1. , 'xmax':1. }, unit='cm', xtitle='1st muon d_{xy}'),
    VCfg(name='l1_dz' , binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit='cm', xtitle='1st muon d_{z}'),
    VCfg(name='l2_dxy', binning={'nbinsx':100, 'xmin':-4. , 'xmax':4. }, unit='cm', xtitle='2nd muon d_{xy}'),
    VCfg(name='l2_dxy_coarse', drawname='l2_dxy', binning={'nbinsx':40, 'xmin':-1. , 'xmax':1. }, unit='cm', xtitle='2nd muon d_{xy}'),
    VCfg(name='l2_dz' , binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit='cm', xtitle='2nd muon d_{z}'),

    VCfg(name='l0_reliso05', binning={'nbinsx':20, 'xmin':0., 'xmax':0.5}, unit=None, xtitle='prompt lepton relative isolation cone 0.4'),
    VCfg(name='l1_reliso05', binning={'nbinsx':20, 'xmin':0., 'xmax':0.5}, unit=None, xtitle='1st muon relative isolation cone 0.4'),
    VCfg(name='l2_reliso05', binning={'nbinsx':20, 'xmin':0., 'xmax':0.5}, unit=None, xtitle='2nd muon relative isolation cone 0.4'),

    VCfg(name='hnl_m_01', binning={'nbinsx':40, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='mass(l_{0},#mu_{1})'),
    VCfg(name='hnl_m_02', binning={'nbinsx':40, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='mass(l_{0},#mu_{2})'),

    VCfg(name='hnl_m_12_wide', drawname='hnl_m_12', binning={'nbinsx':80, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='dimuon mass'),
    VCfg(name='hnl_m_12_z'   , drawname='hnl_m_12', binning={'nbinsx':40, 'xmin':70  , 'xmax':110 }, unit='GeV', xtitle='dimuon mass'),
    VCfg(name='hnl_m_12_jpsi', drawname='hnl_m_12', binning={'nbinsx':50, 'xmin':2.5 , 'xmax':3.5 }, unit='GeV', xtitle='dimuon mass'),
    VCfg(name='hnl_m_12_low' , drawname='hnl_m_12', binning={'nbinsx':40, 'xmin':0   , 'xmax':10  }, unit='GeV', xtitle='dimuon mass'),

    VCfg(name='hnl_hn_pt' , binning={'nbinsx':80, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='dimuon p_{T}'),
    VCfg(name='hnl_hn_eta', binning={'nbinsx':40, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='dimuon #eta'),
    VCfg(name='hnl_hn_phi', binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi  }, unit='rad', xtitle='dimuon #phi'),

    VCfg(name='hnl_dr_01'        , binning={'nbinsx':40, 'xmin':0   , 'xmax':6 }, unit=None, xtitle='#DeltaR (l_{0}, #mu_{1})'),
    VCfg(name='hnl_dr_02'        , binning={'nbinsx':40, 'xmin':0   , 'xmax':6 }, unit=None, xtitle='#DeltaR (l_{0}, #mu_{2})'),
    VCfg(name='hnl_dr_12'        , binning={'nbinsx':40, 'xmin':0   , 'xmax':6 }, unit=None, xtitle='#DeltaR (#mu_{1}, #mu_{2})'),
    VCfg(name='hnl_dr_hnvis0'    , binning={'nbinsx':40, 'xmin':0   , 'xmax':6 }, unit=None, xtitle='#DeltaR (dimuon, l_{0})'),

    VCfg(name='hnl_dphi_0met'    , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (l_{0}, E_{T}^{miss})'),
    VCfg(name='hnl_dphi_1met'    , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (#mu_{1}, E_{T}^{miss})'),
    VCfg(name='hnl_dphi_2met'    , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (#mu_{2}, E_{T}^{miss})'),
    VCfg(name='hnl_dphi_hnvismet', binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (dimuon, E_{T}^{miss})'),

    VCfg(name='hnl_dphi_01'      , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (l_{0}, #mu_{1})'),
    VCfg(name='hnl_dphi_02'      , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (l_{0}, #mu_{2})'),
    VCfg(name='hnl_dphi_12'      , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (#mu_{1}, #mu_{2})'),
    VCfg(name='hnl_dphi_hnvis0'  , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (dimuon, l_{0})'),

    VCfg(name='hnl_w_vis_m', binning={'nbinsx':40, 'xmin':0   , 'xmax':250 }, unit='GeV', xtitle='3 lepton mass'),
    VCfg(name='hnl_2d_disp', binning={'nbinsx':40, 'xmin':0   , 'xmax':100 }, unit='cm' , xtitle='2D displacement'),
    VCfg(name='hnl_2d_small_disp', drawname='hnl_2d_disp', binning={'nbinsx':20, 'xmin':0   , 'xmax':40 }, unit='cm' , xtitle='2D displacement'),
    VCfg(name='hnl_3d_disp', binning={'nbinsx':40, 'xmin':0   , 'xmax':200 }, unit='cm' , xtitle='3D displacement'),

    VCfg(name='pfmet_phi' , binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='E_{T}^{miss} #Phi (PF)'),
    VCfg(name='pfmet_pt'  , binning={'nbinsx':40, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='E_{T}^{miss} (PF)'),

    VCfg(name='sv_prob'        , binning={'nbinsx':40 , 'xmin':0   , 'xmax':1   }, unit=None, xtitle='SV probability'),
    VCfg(name='sv_cos'         , binning={'nbinsx':40 , 'xmin':-1  , 'xmax':1   }, unit=None, xtitle='SV cos'),
    VCfg(name='hnl_2d_disp_sig', binning={'nbinsx':40 , 'xmin':0   , 'xmax':20  }, unit=None, xtitle='SV L/#sigma'),
    VCfg(name='hnl_2d_disp_sig_extended', drawname='hnl_2d_disp_sig', binning={'nbinsx':100 , 'xmin':0   , 'xmax':1000  }, unit=None, xtitle='SV L/#sigma'),

    VCfg(name='nj' , binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets}'),
    VCfg(name='nbj', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{b-jets}'),

    VCfg(name='hnl_iso_rel', binning={'nbinsx':40, 'xmin':0., 'xmax':3.} , unit=None, xtitle='rel. dimuon isolation'),
    VCfg(name='hnl_iso_abs', binning={'nbinsx':40, 'xmin':0., 'xmax':50.}, unit=None, xtitle='abs. dimuon isolation'),

]

test = [VCfg(name='hnl_2d_smaller_disp', drawname='hnl_2d_disp', binning={'nbinsx':20, 'xmin':0   , 'xmax':5 }, unit='cm' , xtitle='2D displacement'),]

def getVars(names, channel='all'):
    return [dict_channel_vars[channel][n] for n in names]
    
