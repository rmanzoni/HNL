import ROOT
from CMGTools.HNL.analyzers.TreeProducerBase import TreeProducerBase
from PhysicsTools.HeppyCore.utils.deltar import deltaR
from CMGTools.HNL.utils.utils import isAncestor, displacement2D, displacement3D, makeRecoVertex # utility functions

class HNLGenTreeProducer(TreeProducerBase):

    '''
    '''

    def declareVariables(self, setup):
        '''
        '''
        # event quantities
        self.bookEvent(self.tree)

        # the W->lN, N->llnu candidate
        self.bookHNL(self.tree, 'hnl')

        # the prompt lepton
        self.bookGenParticle(self.tree, 'l0')
        self.bookEle      (self.tree, 'l0_matched_electron'    )
        self.bookPhoton   (self.tree, 'l0_matched_photon'      )
        self.bookMuon     (self.tree, 'l0_matched_muon'        )
        self.bookMuonTrack(self.tree, 'l0_matched_muon_track'  )
        self.bookTau      (self.tree, 'l0_matched_tau'         )
        self.bookParticle (self.tree, 'l0_matched_dsmuon'      )
        self.bookMuonTrack(self.tree, 'l0_matched_dsmuon_track')
        self.bookParticle (self.tree, 'l0_matched_dgmuon'      )
        self.bookMuonTrack(self.tree, 'l0_matched_dgmuon_track')
       

        # displaced leptons (from the HN)
        self.bookGenParticle(self.tree, 'l1')
        self.bookEle      (self.tree, 'l1_matched_electron'    )
        self.bookPhoton   (self.tree, 'l1_matched_photon'      )
        self.bookMuon     (self.tree, 'l1_matched_muon'        )
        self.bookMuonTrack(self.tree, 'l1_matched_muon_track'  )
        self.bookTau      (self.tree, 'l1_matched_tau'         )
        self.bookParticle (self.tree, 'l1_matched_dsmuon'      )
        self.bookMuonTrack(self.tree, 'l1_matched_dsmuon_track')
        self.bookParticle (self.tree, 'l1_matched_dgmuon'      )
        self.bookMuonTrack(self.tree, 'l1_matched_dgmuon_track')
        self.bookGenParticle(self.tree, 'l2')
        self.bookEle      (self.tree, 'l2_matched_electron'    )
        self.bookPhoton   (self.tree, 'l2_matched_photon'      )
        self.bookMuon     (self.tree, 'l2_matched_muon'        )
        self.bookMuonTrack(self.tree, 'l2_matched_muon_track'  )
        self.bookTau      (self.tree, 'l2_matched_tau'         )
        self.bookParticle (self.tree, 'l2_matched_dsmuon'      )
        self.bookMuonTrack(self.tree, 'l2_matched_dsmuon_track')
        self.bookParticle (self.tree, 'l2_matched_dgmuon'      )
        self.bookMuonTrack(self.tree, 'l2_matched_dgmuon_track')

        # final neutrino
        self.bookGenParticle(self.tree, 'n')

        # true primary vertex
        self.var(self.tree, 'pv_x')
        self.var(self.tree, 'pv_y')
        self.var(self.tree, 'pv_z')

        # true HN decay vertex
        self.var(self.tree, 'sv_x')
        self.var(self.tree, 'sv_y')
        self.var(self.tree, 'sv_z')

        # reco HN decay vertex (when present)
        self.var(self.tree, 'sv_reco_x' )
        self.var(self.tree, 'sv_reco_y' )
        self.var(self.tree, 'sv_reco_z' )
        self.var(self.tree, 'sv_reco_xe')
        self.var(self.tree, 'sv_reco_ye')
        self.var(self.tree, 'sv_reco_ze')
        self.var(self.tree, 'sv_reco_prob')
        self.var(self.tree, 'sv_reco_cos')

        # displacements
        self.var(self.tree, 'hnl_2d_disp')
        self.var(self.tree, 'hnl_3d_disp')

        self.var(self.tree, 'hnl_2d_reco_disp')
        self.var(self.tree, 'hnl_3d_reco_disp')

        self.var(self.tree, 'hnl_2d_reco_disp_sig')
        self.var(self.tree, 'hnl_3d_reco_disp_sig')

        # flag if the event is in CMS acceptance |eta|<2.5
        self.var(self.tree, 'is_in_acc')

    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()
        # import pdb;pdb.set_trace() #zhud: debug

        if not eval(self.skimFunction):
            return False

        self.fillEvent(self.tree, event)
        self.fillHNL(self.tree, 'hnl', event.the_hnl)

        # the prompt lepton
        self.fillGenParticle(self.tree, 'l0' , event.the_hnl.l0())
        if hasattr(event.the_hnl.l0(), 'bestelectron'): self.fillEle     (self.tree, 'l0_matched_electron', event.the_hnl.l0().bestelectron)
        if hasattr(event.the_hnl.l0(), 'bestphoton'  ): self.fillPhoton  (self.tree, 'l0_matched_photon'  , event.the_hnl.l0().bestphoton  )
        if hasattr(event.the_hnl.l0(), 'bestmuon'    ): self.fillMuon    (self.tree, 'l0_matched_muon'    , event.the_hnl.l0().bestmuon    ) ; self.fillMuonTrack(self.tree, 'l0_matched_muon_track', event.the_hnl.l0().bestmuon.bestTrack())
        if hasattr(event.the_hnl.l0(), 'besttau'     ): self.fillTau     (self.tree, 'l0_matched_tau'     , event.the_hnl.l0().besttau     )
        if hasattr(event.the_hnl.l0(), 'bestdsmuon'  ): self.fillParticle(self.tree, 'l0_matched_dsmuon'  , event.the_hnl.l0().bestdsmuon  ) ; self.fillMuonTrack(self.tree, 'l0_matched_dsmuon_track', event.the_hnl.l0().bestdsmuon )
        if hasattr(event.the_hnl.l0(), 'bestdgmuon'  ): self.fillParticle(self.tree, 'l0_matched_dgmuon'  , event.the_hnl.l0().bestdgmuon  ) ; self.fillMuonTrack(self.tree, 'l0_matched_dgmuon_track', event.the_hnl.l0().bestdgmuon )
        
        # displaced leptons (from the HN)
        self.fillGenParticle(self.tree, 'l1', event.the_hnl.l1())
        if hasattr(event.the_hnl.l1(), 'bestelectron'): self.fillEle     (self.tree, 'l1_matched_electron', event.the_hnl.l1().bestelectron)
        if hasattr(event.the_hnl.l1(), 'bestphoton'  ): self.fillPhoton  (self.tree, 'l1_matched_photon'  , event.the_hnl.l1().bestphoton  )
        if hasattr(event.the_hnl.l1(), 'bestmuon'    ): self.fillMuon    (self.tree, 'l1_matched_muon'    , event.the_hnl.l1().bestmuon    ) ; self.fillMuonTrack(self.tree, 'l1_matched_muon_track', event.the_hnl.l1().bestmuon.bestTrack())        
        if hasattr(event.the_hnl.l1(), 'besttau'     ): self.fillTau     (self.tree, 'l1_matched_tau'     , event.the_hnl.l1().besttau     )
        if hasattr(event.the_hnl.l1(), 'bestdsmuon'  ): self.fillParticle(self.tree, 'l1_matched_dsmuon'  , event.the_hnl.l1().bestdsmuon  ) ; self.fillMuonTrack(self.tree, 'l1_matched_dsmuon_track', event.the_hnl.l1().bestdsmuon )
        if hasattr(event.the_hnl.l1(), 'bestdgmuon'  ): self.fillParticle(self.tree, 'l1_matched_dgmuon'  , event.the_hnl.l1().bestdgmuon  ) ; self.fillMuonTrack(self.tree, 'l1_matched_dgmuon_track', event.the_hnl.l1().bestdgmuon )

        self.fillGenParticle(self.tree, 'l2', event.the_hnl.l2())
        if hasattr(event.the_hnl.l2(), 'bestelectron'): self.fillEle     (self.tree, 'l2_matched_electron', event.the_hnl.l2().bestelectron)
        if hasattr(event.the_hnl.l2(), 'bestphoton'  ): self.fillPhoton  (self.tree, 'l2_matched_photon'  , event.the_hnl.l2().bestphoton  )
        if hasattr(event.the_hnl.l2(), 'bestmuon'    ): self.fillMuon    (self.tree, 'l2_matched_muon'    , event.the_hnl.l2().bestmuon    ) ; self.fillMuonTrack(self.tree, 'l2_matched_muon_track', event.the_hnl.l2().bestmuon.bestTrack())        
        if hasattr(event.the_hnl.l2(), 'besttau'     ): self.fillTau     (self.tree, 'l2_matched_tau'     , event.the_hnl.l2().besttau     )
        if hasattr(event.the_hnl.l2(), 'bestdsmuon'  ): self.fillParticle(self.tree, 'l2_matched_dsmuon'  , event.the_hnl.l2().bestdsmuon  ) ; self.fillMuonTrack(self.tree, 'l2_matched_dsmuon_track', event.the_hnl.l2().bestdsmuon )
        if hasattr(event.the_hnl.l2(), 'bestdgmuon'  ): self.fillParticle(self.tree, 'l2_matched_dgmuon'  , event.the_hnl.l2().bestdgmuon  ) ; self.fillMuonTrack(self.tree, 'l2_matched_dgmuon_track', event.the_hnl.l2().bestdgmuon )

        # final neutrino
        self.fillGenParticle(self.tree, 'n'  , event.the_hnl.met())

        # true primary vertex
        self.fill(self.tree, 'pv_x', event.the_hn.vx())
        self.fill(self.tree, 'pv_y', event.the_hn.vy())
        self.fill(self.tree, 'pv_z', event.the_hn.vz())

        # true HN decay vertex
        self.fill(self.tree, 'sv_x', event.the_hn.lep1.vertex().x()) # don't use the final lepton to get the vertex from!
        self.fill(self.tree, 'sv_y', event.the_hn.lep1.vertex().y()) # don't use the final lepton to get the vertex from!
        self.fill(self.tree, 'sv_z', event.the_hn.lep1.vertex().z()) # don't use the final lepton to get the vertex from!

        # displacements
        self.fill(self.tree, 'hnl_2d_disp', displacement2D(event.the_hn.lep1, event.the_hn))
        self.fill(self.tree, 'hnl_3d_disp', displacement3D(event.the_hn.lep1, event.the_hn))

        # reco secondary vertex and displacement
        if event.recoSv:
            self.fill(self.tree, 'sv_reco_x'   , event.recoSv.x()             )
            self.fill(self.tree, 'sv_reco_y'   , event.recoSv.y()             )
            self.fill(self.tree, 'sv_reco_z'   , event.recoSv.z()             )
            self.fill(self.tree, 'sv_reco_xe'  , event.recoSv.xError()        )
            self.fill(self.tree, 'sv_reco_ye'  , event.recoSv.yError()        )
            self.fill(self.tree, 'sv_reco_ze'  , event.recoSv.zError()        )
            self.fill(self.tree, 'sv_reco_prob', event.recoSv.prob            )
            self.fill(self.tree, 'sv_reco_cos' , event.recoSv.disp2DFromBS_cos)
    
            self.fill(self.tree, 'hnl_2d_reco_disp', event.recoSv.disp2DFromBS.value()) # from beamspot
            self.fill(self.tree, 'hnl_3d_reco_disp', event.recoSv.disp3DFromBS.value()) # from PV
    
            self.fill(self.tree, 'hnl_2d_reco_disp_sig', event.recoSv.disp2DFromBS_sig) # from beamspot
            self.fill(self.tree, 'hnl_3d_reco_disp_sig', event.recoSv.disp3DFromBS_sig) # from PV

        # flag if the event is in CMS acceptance |eta|<2.5
        is_in_acc =  abs(event.the_hnl.l0().eta())<2.5 and \
                     abs(event.the_hnl.l1().eta())<2.5 and \
                     abs(event.the_hnl.l2().eta())<2.5
 
        self.fill(self.tree, 'is_in_acc', is_in_acc)

        self.fillTree(event)
