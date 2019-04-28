from pdb import set_trace
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
        datacut   = goodVertices + globalSuperTightHalo2016 + HBHENoise + HBHENoiseIso + EcalDeadCellTriggerPrimitive + BadPFMuon + BadChargedCandidate + eeBadSc + ecalBadCalib 
    if promptLeptonType == "mu": 
        datacut   = 'l0_id_t' #Placeholder

    return datacut

def Z_veto():
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
    return Z_veto

def CR_ttbar():
    selection = ('abs(hnl_m_12 - 91.18) > 15 ' #suppress Z 
                '& abs(hnl_w_vis_m - 91.18) > 15 ' #suppress conversions 
                '& hnl_m_12 > 12 ' #suppress conversions
                '& nbj >=1 '
                )
    selection = selection + Z_veto()
    return selection

def SR():
    selection = ('hnl_dr_12 < 1 ' 
                '& nbj == 0 '
                '& hnl_w_vis_m < 80 '
                # '& hnl_w_vis_m > 50 '
                # '& hnl_dr_01 > 1 '
                # '& hnl_dr_02 > 1 '
                )
    selection = selection + Z_veto()
    return selection

def DY():
    selection = ('abs(hnl_m_12 - 91.18) < 15'
                '& abs(hnl_w_vis_m - 91.18) > 15 '
                '& nbj == 0 ' 
                '& pfmet_pt < 30 '
                '& hnl_mt_0 < 30 '
                )
    return selection

def baseline(channel):
    if channel == 'mmm':
            selection = ('l0_id_t ' 
                        # '& l0_pt > 25 ' 
                        # '& l0_eta < 2.4 '
                        '& l0_reliso_rho_04 < 0.15 '
                        # '& l0_dxy < 0.05 '
                        # '& abs(l0_dz) < 0.1 '
                        # '& abs(l0_dxy) < 0.05 '
                        '& l1_id_l ' #TODO: use Martina's ID?
                        '& l2_id_l '
                        '& l1_pt > 5 ' #electron 10 GeV, muon 5 GeV
                        '& l2_pt > 5 '
                        # '& l1_eta < 2.4 ' #electron 2.5, muon 2.4 
                        # '& l2_eta < 2.4 '
                        # '& hnl_2d_disp > 0.5 ' #TODO: discuss whether we want this as baseline selection or SR?
                        '& hnl_2d_disp > 0.1 ' #TODO: discuss whether we want this as baseline selection or SR?
                        '& hnl_iso04_rel_rhoArea < 1 ' #loose definition
                        # '& l1_q != l2_q ' #opposite charge for the dilepton
                        # '& hnl_dr_01 > 0.05 ' #avoid mismatching
                        # '& hnl_dr_02 > 0.05 '
                        )
            
    return selection


def getSelection(channel, selection_name):
    if channel == 'mmm':
        #testing the old version
        if selection_name == 'baseline':
            selection = baseline(channel)
            
            selection = selection + Z_veto() 

        if selection_name == 'CR_ttbar':
            selection = CR_ttbar()

        if selection_name == 'SR':
            selection = SR()
                        
        if selection_name == 'CR_DY':
            selection = DY()
                        
        if selection_name == 'TT':
            selection = ('l1_reliso_rho_04 < 0.15 ' 
                        '& l2_reliso_rho_04 < 0.15 '
                        )
                        
        if selection_name == 'LT':
            selection = ('l1_reliso_rho_04 > 0.15 ' 
                        '& l2_reliso_rho_04 < 0.15 '
                        )
                        
        if selection_name == 'TL':
            selection = ('l1_reliso_rho_04 < 0.15 ' 
                        '& l2_reliso_rho_04 > 0.15 '
                        )
                        
        if selection_name == 'LL_uncorrelated':
            selection = ('l1_reliso_rho_04 > 0.15 ' 
                        '& l2_reliso_rho_04 > 0.15 '
                        )
                        
        if selection_name == 'LL_correlated':
            selection = ('abs(l1_jet_pt - l2_jet_pt) < 1 '
                        '& l1_reliso_rho_04 > 0.15 ' 
                        '& l2_reliso_rho_04 > 0.15 '
                        )
    
        if selection_name == 'datacut':
            selection = defineDataCut('mu')


 
    return selection

# class Region(object):
    # def __init__(self,name,channel,CR):
        # self.name                       = name
        # self.channel                    = channel
        # self.CR                         = CR
        # self.data                       = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'TT'),getSelection(channel,'datacut')]) + ')'
        # self.MC                         = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'TT')]) + ')'
        # self.signal                     = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'TT')]) + ')'
        # self.N_TL                       = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'TL')]) + ')'
        # self.N_LT                       = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'LT')]) + ')'
        # self.N_LL_uncorrelated          = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'LL_uncorrelated')]) + ')'
        # self.N_LL_correlated            = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'LL_correlated')]) + ')'
        # self.SF_TL                      = self.N_TL + ' * (weight_fr/(1-weight_fr))'  
        # self.SF_LT                      = self.N_LT + ' * (weight_fr/(1-weight_fr))'  
        # self.SF_LL_uncorrelated         = self.N_LL_uncorrelated + ' * (-1) * ((weight_fr/(1-weight_fr))*(weight_fr/(1-weight_fr)))'  
        # self.SF                         = self.SF_TL + ' + ' + self.SF_LT + ' + ' + self.SF_LL_uncorrelated
        # self.DF                         = self.N_LL_correlated + ' * (weight_fr/(1-weight_fr))'

#DY_prompt
class Region(object):
    def __init__(self,name,channel,CR):
        self.name                       = name
        self.channel                    = channel
        self.CR                         = CR
        self.baseline = ('l0_pt>25 & abs(l0_eta)<2.4 & (l0_q != l1_q) '
                     '& l1_pt > 15 & abs(l1_eta) < 2.4 '
                     '& abs(l0_dxy) < 0.05 & abs(l0_dz) < 0.2 '
                     '& abs(l1_dxy) < 0.05 & abs(l1_dz) < 0.2 '
                     '& nbj == 0 '
                     '& l0_id_t '
                     '& l1_id_t '
                     '& l2_id_m '
                     '& l0_reliso_rho_03 < 0.20 '
                     '& l1_reliso_rho_03 < 0.20 '
                     '& l2_reliso_rho_03 < 0.20 '
                     # '& abs(hnl_m_01 - 91.2) < 15 '
                     # '& abs(hnl_dphi_hnvis0) > 2.0 '
                     # '& abs(hnl_dphi_hnvis0) < 3.0 '
                     )
        # self.data                       = 'l0_pt > 25 & l1_pt > 15 & l2_pt > 15 & abs(l0_eta) < 2.4 & abs(l2_eta) < 2.4 & '
        # self.data                       = 'l1_pt > 4  &  l2_pt > 4  &  l0_pt > 35  &  l1_q != l2_q  &  l0_reliso_rho_03 < 0.15  &  abs(l0_dz) < 0.2  &  hnl_dr_01 > 0.05  &  hnl_dr_02 > 0.05  &&  l0_id_l  &  l1_reliso_rho_03 < 0.15  &  l2_reliso_rho_03 < 0.15  &  l1_id_m  &  l2_id_m  &  abs(hnl_m_12 - 91.18) < 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj == 0  &  pfmet_pt < 30  &  hnl_mt_0 < 30'
        # self.MC                         = self.data + '& abs(l2_gen_match_pdgid) != 22 & l2_gen_match_isPromptFinalState == 0 '
        # self.MC_Conversions             = self.data + '& abs(l2_gen_match_pdgid) == 22 & l2_gen_match_isPromptFinalState == 1 '
        self.data                       = self.baseline
        self.MC                         = self.baseline 
        self.SF                         = self.baseline 
        # self.MC                         = self.data + '& abs(l2_gen_match_pdgid) != 22 '
        # self.MC_Conversions             = self.data + '& abs(l2_gen_match_pdgid) == 22 '

# #------------------------------------
# #TTbar_prompt
# class Region(object):
    # def __init__(self,name,channel,CR):
        # self.name                       = name
        # self.channel                    = channel
        # self.CR                         = CR
        # self.data = (
                     # 'l0_pt > 35 & abs(l0_eta) < 2.4'
                     # '& l1_pt > 10 & abs(l1_eta) < 2.5'
                     # '& l2_pt > 10 & abs(l2_eta) < 2.4'
                     # '& nbj > 0 '
                     # '& hnl_m_01 > 15'
                     # '& hnl_m_02 > 15'
                     # '& hnl_m_12 > 15'
                     # # '& abs(hnl_w_vis_m - 91.2) > 15'
                     # '& abs(l0_dxy) < 0.05 & abs(l0_dz) < 0.2 '
                     # '& abs(l1_dxy) < 0.05 & abs(l1_dz) < 0.2 '
                     # # '& l0_reliso_rho_03 < 0.12 '
                     # # '& l1_reliso_rho_03 < 0.12 '
                     # # '& l2_reliso_rho_03 < 0.12 '
                     # # '& ((l0_q != l1_q & hnl_m_01 > 12) | (l0_q == l1_q))'
                     # # '& ((l0_q != l2_q & hnl_m_02 > 12) | (l0_q == l1_q))'
                     # # '& ((l1_q != l2_q & hnl_m_12 > 12) | (l1_q == l2_q))'
                     # )
        # # self.data = self.data + Z_veto()
        # # self.data                       = 'l0_pt > 25 & l1_pt > 15 & l2_pt > 15 & abs(l0_eta) < 2.4 & abs(l2_eta) < 2.4 & '
        # # self.data                       = 'l1_pt > 4  &  l2_pt > 4  &  l0_pt > 35  &  l1_q != l2_q  &  l0_reliso05 < 0.15  &  abs(l0_dz) < 0.2  &  hnl_dr_01 > 0.05  &  hnl_dr_02 > 0.05  &&  l0_id_l  &  l1_reliso05 < 0.15  &  l2_reliso05 < 0.15  &  l1_id_m  &  l2_id_m  &  abs(hnl_m_12 - 91.18) < 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj == 0  &  pfmet_pt < 30  &  hnl_mt_0 < 30'
        # # self.MC                         = self.data + '& abs(l2_gen_match_pdgid) != 22 & l2_gen_match_isPromptFinalState == 0 '
        # # self.MC_Conversions             = self.data + '& abs(l2_gen_match_pdgid) == 22 & l2_gen_match_isPromptFinalState == 1 '
        # self.MC                         = self.data 
        # self.MC_DY                      = self.data + '& abs(l2_gen_match_pdgid) != 22 '
        # self.MC_Conversions             = self.data + '& abs(l2_gen_match_pdgid) == 22 '
        # # self.MC                         = self.data + '& abs(l2_gen_match_pdgid) != 22 '
        # # self.MC_Conversions             = self.data + '& abs(l2_gen_match_pdgid) == 22 '








