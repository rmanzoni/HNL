import ROOT
import sys
import numpy as np
from CMGTools.HNL.analyzers.TreeProducerBase import TreeProducerBase
from CMGTools.HNL.analyzers.HNLSignalReweighter import new_v2s
from PhysicsTools.HeppyCore.utils.deltar import deltaR, bestMatch
from CMGTools.HNL.utils.utils import isAncestor, displacement2D, displacement3D, makeRecoVertex # utility functions
from pdb import set_trace

class HNLTreeProducerBase(TreeProducerBase):
    '''
    RM: add more info:
    - gen impact parameter  ==> how to do it at gen level?
    - gen met including pu (all neutrinos)
    - di-lepton isolation
    make this iherit from a common reco tree producer, then specialise by lepton flavour
    '''
    
    def __init__(self, *args):
        super(HNLTreeProducerBase, self).__init__(*args)
        
        self.skimFilter = 'True'
        if hasattr(self.cfg_ana, 'skimFilter'):
            self.skimFilter = self.cfg_ana.skimFilter

        self.finalStateFilter = 'True'
        if hasattr(self.cfg_ana, 'finalStateFilter'):
            self.finalStateFilter = self.cfg_ana.finalStateFilter

    def beginLoop(self, setup):
        super(HNLTreeProducerBase, self).beginLoop(setup)
        self.counters.addCounter('HNLTreeProducer')
        count = self.counters.counter('HNLTreeProducer')
        count.register('all events')
        count.register('pass final state')
        count.register('pass skim')
    
    def declareVariables(self, setup):
        '''
        '''
        # event variables
        self.bookEvent(self.tree)
        self.var      (self.tree, 'n_cands')
                    
        # reco variables
        self.bookHNL (self.tree, 'hnl')
        
        if self.cfg_ana.promptLepType == 'e':
            self.bookEle (self.tree, 'l0')
            self.var(self.tree, 'hlt_Ele25_eta2p1_WPTight_Gsf' )
            self.var(self.tree, 'hlt_Ele27_WPTight_Gsf'        )
            self.var(self.tree, 'hlt_Ele32_WPTight_Gsf'        )
            self.var(self.tree, 'hlt_Ele35_WPTight_Gsf'        )
            self.var(self.tree, 'hlt_Ele115_CaloIdVT_GsfTrkIdT')
            self.var(self.tree, 'hlt_Ele135_CaloIdVT_GsfTrkIdT')

        elif self.cfg_ana.promptLepType == 'm':
            self.bookMuon(self.tree, 'l0')
            self.var(self.tree, 'hlt_IsoMu22'         )
            self.var(self.tree, 'hlt_IsoTkMu22'       )
            self.var(self.tree, 'hlt_IsoMu22_eta2p1'  )
            self.var(self.tree, 'hlt_IsoTkMu22_eta2p1')
            self.var(self.tree, 'hlt_IsoMu24'         )
            self.var(self.tree, 'hlt_IsoTkMu24'       )
            self.var(self.tree, 'hlt_IsoMu27'         )
            self.var(self.tree, 'hlt_IsoTkMu27'       )
            self.var(self.tree, 'hlt_Mu50'            )
            self.var(self.tree, 'hlt_TkMu50'          )
        else:
            print 'ERROR: prompt lepton type non specified or missing! Exit'
            sys.exit(0)

        if self.cfg_ana.L1L2LeptonType == 'mm':
            self.bookMuon(self.tree, 'l1' )
            self.bookMuon(self.tree, 'l2' )
        if self.cfg_ana.L1L2LeptonType == 'ee':
            self.bookEle(self.tree, 'l1'  )
            self.bookEle(self.tree, 'l2'  )
        if self.cfg_ana.L1L2LeptonType == 'em':
            self.bookEle(self.tree, 'l1'  )
            self.bookMuon(self.tree, 'l2' )
        
        # book the matched  gen particle
        if not self.cfg_comp.isData:
            self.bookSimpleGenParticle(self.tree, 'l0_gen_match')
            self.bookSimpleGenParticle(self.tree, 'l1_gen_match')
            self.bookSimpleGenParticle(self.tree, 'l2_gen_match')

            # relevant for signal: check if reco matched with gen, save a bool
            self.var(self.tree, 'l0_is_real')
            self.var(self.tree, 'l1_is_real')
            self.var(self.tree, 'l2_is_real')

            self.var(self.tree, 'l0_good_match')
            self.var(self.tree, 'l1_good_match')
            self.var(self.tree, 'l2_good_match')

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
        self.bookVertex(self.tree, 'sv')

        # lepton vetoes
        self.var(self.tree, 'pass_e_veto')
        self.var(self.tree, 'pass_m_veto')
            
        # gen level particles
        if getattr(self.cfg_comp, 'isSignal', False):
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

        # met information
        self.bookExtraMetInfo(self.tree)

        # MET filters
        self.var(self.tree, 'pass_met_filters')
        
        # jet information
        self.bookJet(self.tree, 'j1' , fill_extra=False)
        self.bookJet(self.tree, 'j2' , fill_extra=False)
        self.bookJet(self.tree, 'bj1', fill_extra=False)
        self.bookJet(self.tree, 'bj2', fill_extra=False)
        self.var(self.tree, 'nj'  )
        self.var(self.tree, 'nj30')
        self.var(self.tree, 'nbj' )
        
        # LHE weight
        self.var(self.tree, 'lhe_weight')
        
        # weights for ctau reweighing (only for signal!)
        if 'HN3L' in self.cfg_comp.name:
            for iv2 in new_v2s:
                # reduce precision to avoid nasty numbers e.g. 6.000000000000001e-05
                iv2_name = np.format_float_scientific(iv2, unique=False, precision=1, exp_digits=2)
                # 'stringify' the coupling
                iv2_name = iv2_name.replace('-', 'm')
                self.var(self.tree, 'ctau_w_v2_%s' %iv2_name)
                self.var(self.tree, 'xs_w_v2_%s' %iv2_name  )
            self.bookParticle(self.tree, 'w_gen')

        # easy handles to address overlap removal
        self.var(self.tree, 'pass_mmm' )
        self.var(self.tree, 'pass_mem' )
        self.var(self.tree, 'pass_eee' )
        self.var(self.tree, 'pass_eem' )
        

    def process(self, event, fill=True):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

        self.counters.counter('HNLTreeProducer').inc('all events')        

        # save the event only if it is in the correct final state
        if not eval(self.finalStateFilter):
            return True
        self.counters.counter('HNLTreeProducer').inc('pass final state')
        
        # get ahold of the objects to save
        final_state = self.cfg_ana.promptLepType + self.cfg_ana.L1L2LeptonType
        dileptonsvtx  = event.dileptonsvtx_dict [final_state]
        the_3lep_cand = event.the_3lep_cand_dict[final_state]
        recoSv        = event.recoSv_dict       [final_state]

        # save the event only if it passes the skim selection (if it exists)
        # import pdb ; pdb.set_trace()
        if not eval(self.skimFilter):
            return True

        self.counters.counter('HNLTreeProducer').inc('pass skim')
        
        # also cleaned jet collections depend on the final state
        cleanJets   = event.cleanJets  [final_state]
        cleanBJets  = event.cleanBJets [final_state]
        cleanJets30 = event.cleanJets30[final_state]

        # adjust the weights, according to the final state
        event.eventWeight = getattr(event, 'puWeight', 1.)  * \
                            getattr(event, 'LHE_originalWeight', 1.)  * \
                            getattr(event, 'weight_%s' %final_state, 1.)
        
        the_3lep_cand.l0().weight          = getattr(the_3lep_cand.l0(), 'weight_%s'          %final_state, 1.)
        the_3lep_cand.l0().weight_id       = getattr(the_3lep_cand.l0(), 'weight_%s_id'       %final_state, 1.)
        the_3lep_cand.l0().weight_iso      = getattr(the_3lep_cand.l0(), 'weight_%s_iso'      %final_state, 1.)
        the_3lep_cand.l0().weight_reco     = getattr(the_3lep_cand.l0(), 'weight_%s_reco'     %final_state, 1.)
        the_3lep_cand.l0().weight_idiso    = getattr(the_3lep_cand.l0(), 'weight_%s_idiso'    %final_state, 1.)
        the_3lep_cand.l0().weight_trigger  = getattr(the_3lep_cand.l0(), 'weight_%s_trigger'  %final_state, 1.)
        the_3lep_cand.l0().weight_tracking = getattr(the_3lep_cand.l0(), 'weight_%s_tracking' %final_state, 1.)

        the_3lep_cand.l1().weight          = getattr(the_3lep_cand.l1(), 'weight_%s'          %final_state, 1.)
        the_3lep_cand.l1().weight_id       = getattr(the_3lep_cand.l1(), 'weight_%s_id'       %final_state, 1.)
        the_3lep_cand.l1().weight_iso      = getattr(the_3lep_cand.l1(), 'weight_%s_iso'      %final_state, 1.)
        the_3lep_cand.l1().weight_reco     = getattr(the_3lep_cand.l1(), 'weight_%s_reco'     %final_state, 1.)
        the_3lep_cand.l1().weight_idiso    = getattr(the_3lep_cand.l1(), 'weight_%s_idiso'    %final_state, 1.)
        the_3lep_cand.l1().weight_trigger  = getattr(the_3lep_cand.l1(), 'weight_%s_trigger'  %final_state, 1.)
        the_3lep_cand.l1().weight_tracking = getattr(the_3lep_cand.l1(), 'weight_%s_tracking' %final_state, 1.)

        the_3lep_cand.l2().weight          = getattr(the_3lep_cand.l2(), 'weight_%s'          %final_state, 1.)
        the_3lep_cand.l2().weight_id       = getattr(the_3lep_cand.l2(), 'weight_%s_id'       %final_state, 1.)
        the_3lep_cand.l2().weight_iso      = getattr(the_3lep_cand.l2(), 'weight_%s_iso'      %final_state, 1.)
        the_3lep_cand.l2().weight_reco     = getattr(the_3lep_cand.l2(), 'weight_%s_reco'     %final_state, 1.)
        the_3lep_cand.l2().weight_idiso    = getattr(the_3lep_cand.l2(), 'weight_%s_idiso'    %final_state, 1.)
        the_3lep_cand.l2().weight_trigger  = getattr(the_3lep_cand.l2(), 'weight_%s_trigger'  %final_state, 1.)
        the_3lep_cand.l2().weight_tracking = getattr(the_3lep_cand.l2(), 'weight_%s_tracking' %final_state, 1.)
        
        # event variables 
        self.fillEvent(self.tree, event)
        self.fill     (self.tree, 'n_cands', len(dileptonsvtx))
        # these are PRESELECTED leptons according to the preselection given via cfg

        # reco HNL
        self.fillHNL (self.tree, 'hnl', the_3lep_cand)
        if self.cfg_ana.L1L2LeptonType == 'mm':
            self.fillMuon(self.tree, 'l1', the_3lep_cand.l1())
            self.fillMuon(self.tree, 'l2', the_3lep_cand.l2())
        if self.cfg_ana.L1L2LeptonType == 'ee':
            self.fillEle(self.tree, 'l1', the_3lep_cand.l1())
            self.fillEle(self.tree, 'l2', the_3lep_cand.l2())
        if self.cfg_ana.L1L2LeptonType == 'em':
            self.fillEle (self.tree, 'l1', the_3lep_cand.l1())
            self.fillMuon(self.tree, 'l2', the_3lep_cand.l2())

        if self.cfg_ana.promptLepType == 'e': self.fillEle (self.tree, 'l0', the_3lep_cand.l0())
        if self.cfg_ana.promptLepType == 'm': self.fillMuon(self.tree, 'l0', the_3lep_cand.l0())

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

        # HLT bits & matches
        trig_list = [trig.name for trig in event.trigger_infos if trig.fired]
        if self.cfg_ana.promptLepType == 'e':
            self.fill(self.tree, 'hlt_Ele25_eta2p1_WPTight_Gsf' , any('HLT_Ele25_eta2p1_WPTight_Gsf'  in name for name in trig_list))
            self.fill(self.tree, 'hlt_Ele27_WPTight_Gsf'        , any('HLT_Ele27_WPTight_Gsf'         in name for name in trig_list))
            self.fill(self.tree, 'hlt_Ele32_WPTight_Gsf'        , any('HLT_Ele32_WPTight_Gsf'         in name for name in trig_list))
            self.fill(self.tree, 'hlt_Ele35_WPTight_Gsf'        , any('HLT_Ele35_WPTight_Gsf'         in name for name in trig_list))
            self.fill(self.tree, 'hlt_Ele115_CaloIdVT_GsfTrkIdT', any('HLT_Ele115_CaloIdVT_GsfTrkIdT' in name for name in trig_list))
            self.fill(self.tree, 'hlt_Ele135_CaloIdVT_GsfTrkIdT', any('HLT_Ele135_CaloIdVT_GsfTrkIdT' in name for name in trig_list))
        if self.cfg_ana.promptLepType == 'm':
            self.fill(self.tree, 'hlt_IsoMu22'         , any('HLT_IsoMu22'          in name for name in trig_list))
            self.fill(self.tree, 'hlt_IsoTkMu22'       , any('HLT_IsoTkMu22'        in name for name in trig_list))
            self.fill(self.tree, 'hlt_IsoMu22_eta2p1'  , any('HLT_IsoMu22_eta2p1'   in name for name in trig_list))
            self.fill(self.tree, 'hlt_IsoTkMu22_eta2p1', any('HLT_IsoTkMu22_eta2p1' in name for name in trig_list))
            self.fill(self.tree, 'hlt_IsoMu24'         , any('HLT_IsoMu24'          in name for name in trig_list))
            self.fill(self.tree, 'hlt_IsoTkMu24'       , any('HLT_IsoTkMu24'        in name for name in trig_list))
            self.fill(self.tree, 'hlt_IsoMu27'         , any('HLT_IsoMu27'          in name for name in trig_list))
            self.fill(self.tree, 'hlt_IsoTkMu27'       , any('HLT_IsoTkMu27'        in name for name in trig_list))
            self.fill(self.tree, 'hlt_Mu50'            , any('HLT_Mu50'             in name for name in trig_list))
            self.fill(self.tree, 'hlt_TkMu50'          , any('HLT_TkMu50'           in name for name in trig_list))
    
        # reco secondary vertex and displacement
        self.fillVertex(self.tree, 'sv' , recoSv)
    
        self.fill(self.tree, 'hnl_2d_disp', recoSv.disp2DFromBS.value()) # from beamspot
        self.fill(self.tree, 'hnl_3d_disp', recoSv.disp3DFromBS.value()) # from PV
    
        self.fill(self.tree, 'hnl_2d_disp_sig', recoSv.disp2DFromBS_sig) # from beamspot
        self.fill(self.tree, 'hnl_3d_disp_sig', recoSv.disp3DFromBS_sig) # from PV

        # jet/met variables
        self.fillExtraMetInfo(self.tree, event)

        # met filter flags
        self.fill(self.tree, 'pass_met_filters', event.pass_met_filters)

        if len(cleanJets )>0: self.fillJet(self.tree, 'j1' , cleanJets [0], fill_extra=False)
        if len(cleanJets )>1: self.fillJet(self.tree, 'j2' , cleanJets [1], fill_extra=False)
        if len(cleanBJets)>0: self.fillJet(self.tree, 'bj1', cleanBJets[0], fill_extra=False)
        if len(cleanBJets)>1: self.fillJet(self.tree, 'bj2', cleanBJets[1], fill_extra=False)

        self.fill(self.tree, 'nj'  , len(cleanJets)  )
        self.fill(self.tree, 'nj30', len(cleanJets30))
        self.fill(self.tree, 'nbj' , len(cleanBJets) )

        # FIXME! RM what is this?
        # gen match
        if self.cfg_comp.isMC == True and hasattr(event, 'genParticles'):
            stable_genp   =  [pp for pp in event.genParticles if pp.status() == 1] # and pp.vertex().z()!=0)]
            stable_genp   += [pp for pp in event.genp_packed  if pp.status() == 1] # and pp.vertex().z()!=0)] 
            # particle status: http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
            # 1 ... stable; 23 ... from hardest scattering subprocess
#            stable_genp += [pp for pp in event.genParticles if (pp.status()==23  and pp.vertex().z()!=0)]
#            stable_genp += [pp for pp in event.genp_packed  if (pp.status()==23  and pp.vertex().z()!=0)] 
        
            tomatch = [(the_3lep_cand.l0(), 0.05*0.05),
                       (the_3lep_cand.l1(), 0.2 *0.2 ),
                       (the_3lep_cand.l2(), 0.2 *0.2 )]
        
            for ilep, idr2 in tomatch:
                bestmatch, dr2 = bestMatch(ilep, stable_genp)
                if (dr2 < idr2 and abs((ilep.pt() - bestmatch.pt())/ilep.pt()) < 0.2 ): 
                    ilep.bestmatch = bestmatch

            # relevant for mc: check if reco matched with gen, save a float
            if hasattr(the_3lep_cand.l0(), 'bestmatch'):
                LEP0 = the_3lep_cand.l0()
                self.fillSimpleGenParticle(self.tree, 'l0_gen_match', LEP0.bestmatch)
                self.fill(self.tree, 'l0_good_match', deltaR(LEP0.bestmatch, LEP0))
#                if deltaR(LEP0.bestmatch, LEP0) < 0.04 and LEP0.pdgId() == LEP0.bestmatch.pdgId():
#                    self.fill(self.tree, 'l0_good_match', 1)


            if hasattr(the_3lep_cand.l1(), 'bestmatch'):
                LEP1 = the_3lep_cand.l1()
                self.fillSimpleGenParticle(self.tree, 'l1_gen_match', LEP1.bestmatch)
                self.fill(self.tree, 'l1_good_match', deltaR(LEP1.bestmatch, LEP1))
#                if deltaR(LEP1.bestmatch, LEP1) < 0.04 and LEP1.pdgId() == LEP1.bestmatch.pdgId():
#                    self.fill(self.tree, 'l1_good_match', 1)


            if hasattr(the_3lep_cand.l2(), 'bestmatch'):
                LEP2 = the_3lep_cand.l2()
                self.fillSimpleGenParticle(self.tree, 'l2_gen_match', LEP2.bestmatch)
                self.fill(self.tree, 'l2_good_match', deltaR(LEP2.bestmatch, LEP2))
#                if deltaR(LEP2.bestmatch, LEP2) < 0.04 and LEP2.pdgId() == LEP2.bestmatch.pdgId():
#                    self.fill(self.tree, 'l2_good_match', 1)

            # matching by pointer does not work, so let's trick it with deltaR
            if hasattr(event, 'the_hnl'):
                if hasattr(the_3lep_cand.l0(), 'bestmatch'): self.fill(self.tree, 'l0_is_real', deltaR(the_3lep_cand.l0().bestmatch,event.the_hnl.l0()) < 0.01)
                if hasattr(the_3lep_cand.l1(), 'bestmatch'): self.fill(self.tree, 'l1_is_real', deltaR(the_3lep_cand.l1().bestmatch,event.the_hnl.l1()) < 0.05)
                if hasattr(the_3lep_cand.l2(), 'bestmatch'): self.fill(self.tree, 'l2_is_real', deltaR(the_3lep_cand.l2().bestmatch,event.the_hnl.l2()) < 0.05)

            # print('event:', event.eventId, 'lumi:', event.lumi)

        # extra lepton veto
        self.fill(self.tree, 'pass_e_veto', len(event.veto_eles)==0)
        self.fill(self.tree, 'pass_m_veto', len(event.veto_mus )==0)

        # LHE weight
        self.fill(self.tree, 'lhe_weight', np.sign(getattr(event, 'LHE_originalWeight', 1.)))

        # weights for ctau reweighing (only for signal!)
        if 'HN3L' in self.cfg_comp.name:
            for iv2 in new_v2s:
                # 'stringify' the coupling
                # reduce precision to avoid nasty numbers e.g. 6.000000000000001e-05
                iv2_name = np.format_float_scientific(iv2, unique=False, precision=1, exp_digits=2)
                iv2_name = iv2_name.replace('-', 'm')
                self.fill(self.tree, 'ctau_w_v2_%s' %iv2_name, event.ctau_weights[iv2]['ctau_weight'])
                self.fill(self.tree, 'xs_w_v2_%s' %iv2_name  , event.ctau_weights[iv2]['xs_weight'  ])
            if event.the_gen_w is not None:
                self.fillParticle(self.tree, 'w_gen', event.the_gen_w)

        self.fill(self.tree, 'pass_mmm', getattr(event, 'pass_mmm', -1.))
        self.fill(self.tree, 'pass_mem', getattr(event, 'pass_mem', -1.))
        self.fill(self.tree, 'pass_eee', getattr(event, 'pass_eee', -1.))
        self.fill(self.tree, 'pass_eem', getattr(event, 'pass_eem', -1.))

#         import pdb ; pdb.set_trace()
                                        
        if fill:                   
            self.fillTree(event)
