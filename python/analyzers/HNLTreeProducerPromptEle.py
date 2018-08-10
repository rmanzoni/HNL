import ROOT
from CMGTools.HNL.analyzers.TreeProducerBase import TreeProducerBase
from PhysicsTools.HeppyCore.utils.deltar import deltaR
from CMGTools.HNL.utils.utils import isAncestor, displacement2D, displacement3D, makeRecoVertex # utility functions
from pdb import set_trace

class HNLTreeProducerPromptEle(TreeProducerBase):
    '''
    RM: add more info:
    - reco-gen matching
    - beamspot
    - primary vertex
    - jet associated to the lepton
    - check lepton iso and id variables
    - ??
    
    make this iherit from a common reco tree producer, then specialise by lepton flavour
    '''
    def declareVariables(self, setup):
        '''
        '''
        # event variables
        self.bookEvent(self.tree)
        self.var      (self.tree, 'n_cands')
        
        # gen level particles
        self.bookHNL        (self.tree, 'hnl_gen')
        self.bookGenParticle(self.tree, 'l0_gen' )
        self.bookGenParticle(self.tree, 'l1_gen' )
        self.bookGenParticle(self.tree, 'l2_gen' )
        self.bookGenParticle(self.tree, 'n_gen'  )

        # gen primary vertex
        self.var(self.tree, 'pv_gen_x')
        self.var(self.tree, 'pv_gen_y')
        self.var(self.tree, 'pv_gen_z')

        # gen HN decay vertex
        self.var(self.tree, 'sv_gen_x')
        self.var(self.tree, 'sv_gen_y')
        self.var(self.tree, 'sv_gen_z')

        # reco variables
        self.bookHNL     (self.tree, 'hnl')
        self.bookEle     (self.tree, 'l0' )
        self.bookMuon    (self.tree, 'l1' )
        self.bookMuon    (self.tree, 'l2' )

        # reco primary vertex
        self.var(self.tree, 'pv_x')
        self.var(self.tree, 'pv_y')
        self.var(self.tree, 'pv_z')
        
        # reco HN decay vertex (when present)
        self.var(self.tree, 'sv_x' )
        self.var(self.tree, 'sv_y' )
        self.var(self.tree, 'sv_z' )
        self.var(self.tree, 'sv_xe')
        self.var(self.tree, 'sv_ye')
        self.var(self.tree, 'sv_ze')
        self.var(self.tree, 'sv_prob')
        self.var(self.tree, 'sv_cos')

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
        self.fillHNL     (self.tree, 'hnl', event.the_3lep_cand     )
        import pdb ; pdb.set_trace()
        self.fillEle     (self.tree, 'l0' , event.the_3lep_cand.l0())
        self.fillMuon    (self.tree, 'l1' , event.the_3lep_cand.l1())
        self.fillMuon    (self.tree, 'l2' , event.the_3lep_cand.l2())

        # output of MC analysis
        self.fillHNL        (self.tree, 'hnl_gen', event.the_hnl      )
        self.fillGenParticle(self.tree, 'l0_gen' , event.the_hnl.l0() )
        self.fillGenParticle(self.tree, 'l1_gen' , event.the_hnl.l1() )
        self.fillGenParticle(self.tree, 'l2_gen' , event.the_hnl.l2() )
        self.fillGenParticle(self.tree, 'n_gen'  , event.the_hnl.met())

        # true primary vertex
        self.fill(self.tree, 'pv_x', event.the_hn.vx())
        self.fill(self.tree, 'pv_y', event.the_hn.vy())
        self.fill(self.tree, 'pv_z', event.the_hn.vz())

        # true HN decay vertex
        self.fill(self.tree, 'sv_x', event.the_hn.lep1.vertex().x()) # don't use the final lepton to get the vertex from!
        self.fill(self.tree, 'sv_y', event.the_hn.lep1.vertex().y()) # don't use the final lepton to get the vertex from!
        self.fill(self.tree, 'sv_z', event.the_hn.lep1.vertex().z()) # don't use the final lepton to get the vertex from!

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
    
        self.fill(self.tree, 'hnl_2d_reco_disp', event.recoSv.disp2DFromBS.value()) # from beamspot
        self.fill(self.tree, 'hnl_3d_reco_disp', event.recoSv.disp3DFromBS.value()) # from PV
    
        self.fill(self.tree, 'hnl_2d_reco_disp_sig', event.recoSv.disp2DFromBS_sig) # from beamspot
        self.fill(self.tree, 'hnl_3d_reco_disp_sig', event.recoSv.disp3DFromBS_sig) # from PV

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

        self.fillTree(event)

