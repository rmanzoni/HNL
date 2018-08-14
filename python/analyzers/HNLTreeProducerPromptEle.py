import ROOT
from CMGTools.HNL.analyzers.TreeProducerBase import TreeProducerBase
from PhysicsTools.HeppyCore.utils.deltar import deltaR, bestMatch
from CMGTools.HNL.utils.utils import isAncestor, displacement2D, displacement3D, makeRecoVertex # utility functions
from pdb import set_trace

class HNLTreeProducerPromptEle(TreeProducerBase):
    '''
    RM: add more info:
    - gen impact parameter  ==> how to do it at gen level?
    - gen met including pu (all neutrinos)
    - di-lepton isolation
    make this iherit from a common reco tree producer, then specialise by lepton flavour
    '''
    def declareVariables(self, setup):
        '''
        '''
        # event variables
        self.bookEvent(self.tree)
        self.var      (self.tree, 'n_cands')
        
        # reco variables
        self.bookHNL (self.tree, 'hnl')
        self.var     (self.tree, 'hnl_iso_abs')
        self.var     (self.tree, 'hnl_iso_rel')
        self.bookEle (self.tree, 'l0' )
        self.bookMuon(self.tree, 'l1' )
        self.bookMuon(self.tree, 'l2' )
        
        # book the matched  gen particle
        self.bookParticle(self.tree, 'l0_gen_match')
        self.bookParticle(self.tree, 'l1_gen_match')
        self.bookParticle(self.tree, 'l2_gen_match')

        # relevant for signal: check if reco matched with gen, save a bool
        self.var(self.tree, 'l0_is_real')
        self.var(self.tree, 'l1_is_real')
        self.var(self.tree, 'l2_is_real')

        # reco primary vertex
        self.var(self.tree, 'pv_x')
        self.var(self.tree, 'pv_y')
        self.var(self.tree, 'pv_z')
        self.var(self.tree, 'pv_xe')
        self.var(self.tree, 'pv_ye')
        self.var(self.tree, 'pv_ze')

        # beamspot
        self.var(self.tree, 'bs_x')
        self.var(self.tree, 'bs_y')
        self.var(self.tree, 'bs_z')
        self.var(self.tree, 'bs_sigma_x')
        self.var(self.tree, 'bs_sigma_y')
        self.var(self.tree, 'bs_sigma_z')
        self.var(self.tree, 'bs_dxdz')
        self.var(self.tree, 'bs_dydz')
        
        # reco HN decay vertex (when present)
        self.var(self.tree, 'sv_x' )
        self.var(self.tree, 'sv_y' )
        self.var(self.tree, 'sv_z' )
        self.var(self.tree, 'sv_xe')
        self.var(self.tree, 'sv_ye')
        self.var(self.tree, 'sv_ze')
        self.var(self.tree, 'sv_prob')
        self.var(self.tree, 'sv_cos')

        # lepton vetoes
        self.var(self.tree, 'pass_e_veto')
        self.var(self.tree, 'pass_m_veto')
        
        # gen level particles
        self.bookHNL     (self.tree, 'hnl_gen')
        self.bookParticle(self.tree, 'l0_gen' )
        self.bookParticle(self.tree, 'l1_gen' )
        self.bookParticle(self.tree, 'l2_gen' )
        self.bookParticle(self.tree, 'n_gen'  )

        # gen primary vertex
        self.var(self.tree, 'pv_gen_x')
        self.var(self.tree, 'pv_gen_y')
        self.var(self.tree, 'pv_gen_z')

        # gen HN decay vertex
        self.var(self.tree, 'sv_gen_x')
        self.var(self.tree, 'sv_gen_y')
        self.var(self.tree, 'sv_gen_z')

        # displacements
        self.var(self.tree, 'hnl_2d_gen_disp')
        self.var(self.tree, 'hnl_3d_gen_disp')

        self.var(self.tree, 'hnl_2d_disp')
        self.var(self.tree, 'hnl_3d_disp')

        self.var(self.tree, 'hnl_2d_disp_sig')
        self.var(self.tree, 'hnl_3d_disp_sig')

        # jet/met information
        self.bookExtraMetInfo(self.tree)
        self.bookJet(self.tree, 'j1' , fill_extra=False)
        self.bookJet(self.tree, 'j2' , fill_extra=False)
        self.bookJet(self.tree, 'bj1', fill_extra=False)
        self.bookJet(self.tree, 'bj2', fill_extra=False)
        self.var(self.tree, 'htj' )
        self.var(self.tree, 'htbj')
        self.var(self.tree, 'nj'  )
        self.var(self.tree, 'nbj' )

    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

        # event variables 
        self.fillEvent(self.tree, event)

        self.fill(self.tree, 'n_cands', len(event.dimuonsvtx))

        # reco HNL
        self.fillHNL (self.tree, 'hnl'        , event.the_3lep_cand           )
        self.fill    (self.tree, 'hnl_iso_abs', event.the_3lep_cand.abs_ch_iso)
        self.fill    (self.tree, 'hnl_iso_rel', event.the_3lep_cand.rel_ch_iso)
        self.fillEle (self.tree, 'l0'         , event.the_3lep_cand.l0()      )
        self.fillMuon(self.tree, 'l1'         , event.the_3lep_cand.l1()      )
        self.fillMuon(self.tree, 'l2'         , event.the_3lep_cand.l2()      )

        # output of MC analysis ONLY FOR SIGNAL
        if hasattr(event, 'the_hnl'):
            self.fillHNL     (self.tree, 'hnl_gen', event.the_hnl      )
            self.fillParticle(self.tree, 'l0_gen' , event.the_hnl.l0() )
            self.fillParticle(self.tree, 'l1_gen' , event.the_hnl.l1() )
            self.fillParticle(self.tree, 'l2_gen' , event.the_hnl.l2() )
            self.fillParticle(self.tree, 'n_gen'  , event.the_hnl.met())

        # reco primary vertex
        pv = event.goodVertices[0]
        self.fill(self.tree, 'pv_x' , pv.x())
        self.fill(self.tree, 'pv_y' , pv.y())
        self.fill(self.tree, 'pv_z' , pv.z())
        self.fill(self.tree, 'pv_xe', pv.xError())
        self.fill(self.tree, 'pv_ye', pv.yError())
        self.fill(self.tree, 'pv_ze', pv.zError())
        
        # true primary vertex
        if hasattr(event, 'the_hnl'):
            self.fill(self.tree, 'pv_gen_x', event.the_hn.vx())
            self.fill(self.tree, 'pv_gen_y', event.the_hn.vy())
            self.fill(self.tree, 'pv_gen_z', event.the_hn.vz())

        # beamspot
        self.fill(self.tree, 'bs_x', event.beamspot.x0())
        self.fill(self.tree, 'bs_y', event.beamspot.y0())
        self.fill(self.tree, 'bs_z', event.beamspot.z0())
        self.fill(self.tree, 'bs_sigma_x', event.beamspot.BeamWidthX())
        self.fill(self.tree, 'bs_sigma_y', event.beamspot.BeamWidthY())
        self.fill(self.tree, 'bs_sigma_z', event.beamspot.sigmaZ())
        self.fill(self.tree, 'bs_dxdz', event.beamspot.dxdz())
        self.fill(self.tree, 'bs_dydz', event.beamspot.dydz())

        # true HN decay vertex
        if hasattr(event, 'the_hn'):
            self.fill(self.tree, 'sv_gen_x', event.the_hn.lep1.vertex().x()) # don't use the final lepton to get the vertex from!
            self.fill(self.tree, 'sv_gen_y', event.the_hn.lep1.vertex().y()) # don't use the final lepton to get the vertex from!
            self.fill(self.tree, 'sv_gen_z', event.the_hn.lep1.vertex().z()) # don't use the final lepton to get the vertex from!

            # displacements
            self.fill(self.tree, 'hnl_2d_gen_disp', displacement2D(event.the_hn.lep1, event.the_hn))
            self.fill(self.tree, 'hnl_3d_gen_disp', displacement3D(event.the_hn.lep1, event.the_hn))
        
        # reco secondary vertex and displacement
        self.fill(self.tree, 'sv_x'   , event.recoSv.x()             )
        self.fill(self.tree, 'sv_y'   , event.recoSv.y()             )
        self.fill(self.tree, 'sv_z'   , event.recoSv.z()             )
        self.fill(self.tree, 'sv_xe'  , event.recoSv.xError()        )
        self.fill(self.tree, 'sv_ye'  , event.recoSv.yError()        )
        self.fill(self.tree, 'sv_ze'  , event.recoSv.zError()        )
        self.fill(self.tree, 'sv_prob', event.recoSv.prob            )
        self.fill(self.tree, 'sv_cos' , event.recoSv.disp2DFromBS_cos)
    
        self.fill(self.tree, 'hnl_2d_disp', event.recoSv.disp2DFromBS.value()) # from beamspot
        self.fill(self.tree, 'hnl_3d_disp', event.recoSv.disp3DFromBS.value()) # from PV
    
        self.fill(self.tree, 'hnl_2d_disp_sig', event.recoSv.disp2DFromBS_sig) # from beamspot
        self.fill(self.tree, 'hnl_3d_disp_sig', event.recoSv.disp3DFromBS_sig) # from PV

        # jet/met variables
        self.fillExtraMetInfo(self.tree, event)

        if len(event.cleanJets )>0: self.fillJet(self.tree, 'j1' , event.cleanJets [0], fill_extra=False)
        if len(event.cleanJets )>1: self.fillJet(self.tree, 'j2' , event.cleanJets [1], fill_extra=False)
        if len(event.cleanBJets)>0: self.fillJet(self.tree, 'bj1', event.cleanBJets[0], fill_extra=False)
        if len(event.cleanBJets)>1: self.fillJet(self.tree, 'bj2', event.cleanBJets[1], fill_extra=False)

        self.fill(self.tree, 'htj' , event.HT_cleanJets   )
        self.fill(self.tree, 'htbj', event.HT_bJets       )
        self.fill(self.tree, 'nj'  , len(event.cleanJets) )
        self.fill(self.tree, 'nbj' , len(event.cleanBJets))

        # gen match
        stable_genp  = [pp for pp in event.genParticles if pp.status()==1]
        stable_genp += [pp for pp in event.genp_packed if pp.status()==1]
        
        tomatch = [(event.the_3lep_cand.l0(), 0.05*0.05),
                   (event.the_3lep_cand.l1(), 0.2 *0.2 ),
                   (event.the_3lep_cand.l2(), 0.2 *0.2 )]
    
        for ilep, idr2 in tomatch:
            bestmatch, dr2 = bestMatch(ilep, stable_genp)
            if dr2 < idr2:
                ilep.bestmatch = bestmatch

        # relevant for signal: check if reco matched with gen, save a bool
        if hasattr(event.the_3lep_cand.l0(), 'bestmatch'): self.fillParticle(self.tree, 'l0_gen_match', event.the_3lep_cand.l0().bestmatch)
        if hasattr(event.the_3lep_cand.l1(), 'bestmatch'): self.fillParticle(self.tree, 'l1_gen_match', event.the_3lep_cand.l1().bestmatch)
        if hasattr(event.the_3lep_cand.l2(), 'bestmatch'): self.fillParticle(self.tree, 'l2_gen_match', event.the_3lep_cand.l2().bestmatch)

        # FIXME! matching by pointer does not work, so let's trick it with deltaR
        if hasattr(event, 'the_hnl'):
            if hasattr(event.the_3lep_cand.l0(), 'bestmatch'): self.fill(self.tree, 'l0_is_real', deltaR(event.the_3lep_cand.l0().bestmatch,event.the_hnl.l0()) < 0.01)
            if hasattr(event.the_3lep_cand.l1(), 'bestmatch'): self.fill(self.tree, 'l1_is_real', deltaR(event.the_3lep_cand.l1().bestmatch,event.the_hnl.l1()) < 0.05)
            if hasattr(event.the_3lep_cand.l2(), 'bestmatch'): self.fill(self.tree, 'l2_is_real', deltaR(event.the_3lep_cand.l2().bestmatch,event.the_hnl.l2()) < 0.05)

        # extra lepton veto
        self.fill(self.tree, 'pass_e_veto', len(event.veto_eles)==0)
        self.fill(self.tree, 'pass_m_veto', len(event.veto_mus )==0)
        
        self.fillTree(event)


