def getSelection(channel, selection_name):
    if channel == 'mmm':
        if selection_name == 'baseline':
            selection = ('l0_id_t ' 
                        '& l0_pt > 25 ' 
                        '& l0_eta < 2.4 '
                        '& l0_reliso_rho_04 < 0.1 '
                        '& l0_dxy < 0.05 '
                        '& abs(l0_dz) < 0.1 '
                        '& abs(l0_dxy) < 0.05 '
                        '& l1_id_l ' #TODO: use Martina's ID?
                        '& l2_id_l '
                        '& l1_pt > 5 ' #electron 10 GeV, muon 5 GeV
                        '& l2_pt > 5 '
                        '& l1_eta < 2.4 ' #electron 2.5, muon 2.4 
                        '& l2_eta < 2.4 '
                        '& hnl_2d_disp > 0.5 ' #TODO: discuss whether we want this as baseline selection or SR?
                        '& hnl_iso04_rel_rhoArea < 1 ' #loose definition
                        '& l1_q != l2_q ' #opposite charge for the dilepton
                        '& hnl_dr_01 > 0.05 ' #avoid mismatching
                        '& hnl_dr_02 > 0.05 '
                        )

        if selection_name == 'CR_ttbar':
            selection = ('abs(hnl_m_12 - 91.18) > 15 ' #suppress Z 
                        '& abs(hnl_w_vis_m - 91.18) > 15 ' #suppress conversions 
                        '& hnl_m_12 > 12 ' #suppress conversions
                        '& nbj >=1 '
                        )
                        
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
    
    return selection
