import ROOT
import sys
import numpy as np
from CMGTools.HNL.analyzers.HNLTreeProducerBase import HNLTreeProducerBase
from CMGTools.HNL.analyzers.HNLSignalReweighter import new_v2s
from PhysicsTools.HeppyCore.utils.deltar import deltaR, bestMatch
from CMGTools.HNL.utils.utils import isAncestor, displacement2D, displacement3D, makeRecoVertex # utility functions
from pdb import set_trace

class HNLTreeProducer(HNLTreeProducerBase):
    '''
    Add more branches here
    '''
    def declareVariables(self, setup):
        '''
        '''
        # execute the corresponding method of the parent analyser
        super(HNLTreeProducer, self).declareVariables(setup)

        # event variables
        self.var(self.tree, 'n_lep')
        self.var(self.tree, 'n_ele')
        self.var(self.tree, 'n_mu')
        
        # reco variables
        self.var(self.tree, 'hnl_iso03_abs_rhoArea')
        self.var(self.tree, 'hnl_iso04_abs_rhoArea')
        self.var(self.tree, 'hnl_iso05_abs_rhoArea')
        self.var(self.tree, 'hnl_iso03_abs_deltaBeta')
        self.var(self.tree, 'hnl_iso04_abs_deltaBeta')
        self.var(self.tree, 'hnl_iso05_abs_deltaBeta')
        self.var(self.tree, 'hnl_iso03_rel_rhoArea')
        self.var(self.tree, 'hnl_iso04_rel_rhoArea')
        self.var(self.tree, 'hnl_iso05_rel_rhoArea')
        self.var(self.tree, 'hnl_iso03_rel_deltaBeta')
        self.var(self.tree, 'hnl_iso04_rel_deltaBeta')
        self.var(self.tree, 'hnl_iso05_rel_deltaBeta')
                
        # save vetoing lepton
        self.bookEle (self.tree, 'veto_ele')
        self.bookMuon(self.tree, 'veto_mu')
    
        # invariant masses with vetoing leptons
        self.var(self.tree, 'hnl_m_0Vele')
        self.var(self.tree, 'hnl_m_1Vele')
        self.var(self.tree, 'hnl_m_2Vele')
        self.var(self.tree, 'hnl_m_0Vmu')
        self.var(self.tree, 'hnl_m_1Vmu')
        self.var(self.tree, 'hnl_m_2Vmu')
        
        # MET filters
        self.var(self.tree, 'Flag_goodVertices')
        self.var(self.tree, 'Flag_globalSuperTightHalo2016Filter')
        self.var(self.tree, 'Flag_HBHENoiseFilter')
        self.var(self.tree, 'Flag_HBHENoiseIsoFilter')
        self.var(self.tree, 'Flag_EcalDeadCellTriggerPrimitiveFilter')
        self.var(self.tree, 'Flag_BadPFMuonFilter')
        self.var(self.tree, 'Flag_BadChargedCandidateFilter')
        self.var(self.tree, 'Flag_eeBadScFilter')
        self.var(self.tree, 'Flag_ecalBadCalibFilter')
        
        # sum energy information
        self.var(self.tree, 'htj' )
        self.var(self.tree, 'htbj')
        
        # LHE weight
        self.var(self.tree, 'lhe_weight')
                        
    def process(self, event):
        '''
        '''
#         import pdb ; pdb.set_trace()
        # execute the corresponding method of the parent analyser
        super(HNLTreeProducer, self).process(event, fill=False)
#         import pdb ; pdb.set_trace()

        # event variables 
        # these are PRESELECTED leptons according to the preselection given via cfg
        self.fill(self.tree, 'n_lep', len(event.electrons) + len(event.muons))
        self.fill(self.tree, 'n_ele', len(event.electrons))
        self.fill(self.tree, 'n_mu' , len(event.muons))

        
        # FIXME: one day, move all those single variables into groups like bookHNL/fillHNL
        self.fill(self.tree, 'hnl_iso03_abs_rhoArea'  , event.the_3lep_cand.abs_tot_iso03_rhoArea)
        self.fill(self.tree, 'hnl_iso04_abs_rhoArea'  , event.the_3lep_cand.abs_tot_iso04_rhoArea)
        self.fill(self.tree, 'hnl_iso05_abs_rhoArea'  , event.the_3lep_cand.abs_tot_iso05_rhoArea)
        self.fill(self.tree, 'hnl_iso03_abs_deltaBeta', event.the_3lep_cand.abs_tot_iso03_deltaBeta)
        self.fill(self.tree, 'hnl_iso04_abs_deltaBeta', event.the_3lep_cand.abs_tot_iso04_deltaBeta)
        self.fill(self.tree, 'hnl_iso05_abs_deltaBeta', event.the_3lep_cand.abs_tot_iso05_deltaBeta)
        self.fill(self.tree, 'hnl_iso03_rel_rhoArea'  , event.the_3lep_cand.rel_tot_iso03_rhoArea)
        self.fill(self.tree, 'hnl_iso04_rel_rhoArea'  , event.the_3lep_cand.rel_tot_iso04_rhoArea)
        self.fill(self.tree, 'hnl_iso05_rel_rhoArea'  , event.the_3lep_cand.rel_tot_iso05_rhoArea)
        self.fill(self.tree, 'hnl_iso03_rel_deltaBeta', event.the_3lep_cand.rel_tot_iso03_deltaBeta)
        self.fill(self.tree, 'hnl_iso04_rel_deltaBeta', event.the_3lep_cand.rel_tot_iso04_deltaBeta)
        self.fill(self.tree, 'hnl_iso05_rel_deltaBeta', event.the_3lep_cand.rel_tot_iso05_deltaBeta)

        # true HN decay vertex
        if hasattr(event, 'the_hn'):
            self.fill(self.tree, 'sv_gen_x', event.the_hn.lep1.vertex().x()) # don't use the final lepton to get the vertex from!
            self.fill(self.tree, 'sv_gen_y', event.the_hn.lep1.vertex().y()) # don't use the final lepton to get the vertex from!
            self.fill(self.tree, 'sv_gen_z', event.the_hn.lep1.vertex().z()) # don't use the final lepton to get the vertex from!

            # displacements
            self.fill(self.tree, 'hnl_2d_gen_disp', displacement2D(event.the_hn.lep1, event.the_hn))
            self.fill(self.tree, 'hnl_3d_gen_disp', displacement3D(event.the_hn.lep1, event.the_hn))

        # met filter flags
        self.fill(self.tree, 'Flag_goodVertices'                      , event.Flag_goodVertices                      )
        self.fill(self.tree, 'Flag_globalSuperTightHalo2016Filter'    , event.Flag_globalSuperTightHalo2016Filter    )
        self.fill(self.tree, 'Flag_HBHENoiseFilter'                   , event.Flag_HBHENoiseFilter                   )
        self.fill(self.tree, 'Flag_HBHENoiseIsoFilter'                , event.Flag_HBHENoiseIsoFilter                )
        self.fill(self.tree, 'Flag_EcalDeadCellTriggerPrimitiveFilter', event.Flag_EcalDeadCellTriggerPrimitiveFilter)
        self.fill(self.tree, 'Flag_BadPFMuonFilter'                   , event.Flag_BadPFMuonFilter                   )
        self.fill(self.tree, 'Flag_BadChargedCandidateFilter'         , event.Flag_BadChargedCandidateFilter         )
        self.fill(self.tree, 'Flag_eeBadScFilter'                     , event.Flag_eeBadScFilter                     )
        self.fill(self.tree, 'Flag_ecalBadCalibFilter'                , event.Flag_ecalBadCalibFilter                )

        self.fill(self.tree, 'htj' , event.HT_cleanJets   )
        self.fill(self.tree, 'htbj', event.HT_bJets       )

        # save vetoing lepton invariant masses
        if len(event.veto_eles):
                self.fillEle(self.tree, 'veto_ele', event.veto_save_ele)
                self.fill(self.tree, 'hnl_m_0Vele', (event.veto_save_ele.p4() + event.the_3lep_cand.l0().p4()).mass())
                self.fill(self.tree, 'hnl_m_1Vele', (event.veto_save_ele.p4() + event.the_3lep_cand.l1().p4()).mass())
                self.fill(self.tree, 'hnl_m_2Vele', (event.veto_save_ele.p4() + event.the_3lep_cand.l2().p4()).mass())
        if len(event.veto_mus):
                self.fillMuon(self.tree, 'veto_mu', event.veto_save_mu)
                self.fill(self.tree, 'hnl_m_0Vmu', (event.veto_save_mu.p4() + event.the_3lep_cand.l0().p4()).mass())
                self.fill(self.tree, 'hnl_m_1Vmu', (event.veto_save_mu.p4() + event.the_3lep_cand.l1().p4()).mass())
                self.fill(self.tree, 'hnl_m_2Vmu', (event.veto_save_mu.p4() + event.the_3lep_cand.l2().p4()).mass())
        
        self.fillTree(event)


