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
        self.bookParticle(self.tree, 'l0_matched_electron')
        self.bookParticle(self.tree, 'l0_matched_photon')
        self.bookParticle(self.tree, 'l0_matched_muon')
        self.bookParticle(self.tree, 'l0_matched_tau')
        self.bookParticle(self.tree, 'l0_matched_dsmuon')
        self.bookParticle(self.tree, 'l0_matched_dgmuon')
       

        # displaced leptons (from the HN)
        self.bookGenParticle(self.tree, 'l1')
        self.bookParticle(self.tree, 'l1_matched_electron')
        self.bookParticle(self.tree, 'l1_matched_photon')
        self.bookParticle(self.tree, 'l1_matched_muon')
        self.bookParticle(self.tree, 'l1_matched_tau')
        self.bookParticle(self.tree, 'l1_matched_dsmuon')
        self.bookParticle(self.tree, 'l1_matched_dgmuon')
        self.bookGenParticle(self.tree, 'l2')
        self.bookParticle(self.tree, 'l2_matched_electron')
        self.bookParticle(self.tree, 'l2_matched_photon')
        self.bookParticle(self.tree, 'l2_matched_muon')
        self.bookParticle(self.tree, 'l2_matched_tau')
        self.bookParticle(self.tree, 'l2_matched_dsmuon')
        self.bookParticle(self.tree, 'l2_matched_dgmuon')

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

        # displacements
        self.var(self.tree, 'hnl_2d_disp')
        self.var(self.tree, 'hnl_3d_disp')

        # flag if the event is in CMS acceptance |eta|<2.5
        self.var(self.tree, 'is_in_acc')

    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

        if not eval(self.skimFunction):
            return False

        self.fillEvent(self.tree, event)
        self.fillHNL(self.tree, 'hnl', event.the_hnl)

        # the prompt lepton
        self.fillGenParticle(self.tree, 'l0' , event.the_hnl.l0())
        if hasattr(event.the_hnl.l0(), 'bestelectron'):
            self.fillParticle(self.tree, 'l0_matched_electron', event.the_hnl.l0().bestelectron)
        if hasattr(event.the_hnl.l0(), 'bestphoton'):
            self.fillParticle(self.tree, 'l0_matched_photon', event.the_hnl.l0().bestphoton)
        if hasattr(event.the_hnl.l0(), 'bestmuon'):
            self.fillParticle(self.tree, 'l0_matched_muon', event.the_hnl.l0().bestmuon)
        if hasattr(event.the_hnl.l0(), 'besttau'):
            self.fillParticle(self.tree, 'l0_matched_tau', event.the_hnl.l0().besttau)
        if hasattr(event.the_hnl.l0(), 'bestdsmuon'):
            self.fillParticle(self.tree, 'l0_matched_dsmuon', event.the_hnl.l0().bestdsmuon)
        if hasattr(event.the_hnl.l0(), 'bestdgmuon'):
            self.fillParticle(self.tree, 'l0_matched_dgmuon', event.the_hnl.l0().bestdgmuon)
        
        # displaced leptons (from the HN)
        self.fillGenParticle(self.tree, 'l1', event.the_hnl.l1())
        if hasattr(event.the_hnl.l1(), 'bestelectron'):
            self.fillParticle(self.tree, 'l1_matched_electron', event.the_hnl.l1().bestelectron)
        if hasattr(event.the_hnl.l1(), 'bestphoton'):
            self.fillParticle(self.tree, 'l1_matched_photon', event.the_hnl.l1().bestphoton)
        if hasattr(event.the_hnl.l1(), 'bestmuon'):
            self.fillParticle(self.tree, 'l1_matched_muon', event.the_hnl.l1().bestmuon)
        if hasattr(event.the_hnl.l1(), 'besttau'):
            self.fillParticle(self.tree, 'l1_matched_tau', event.the_hnl.l1().besttau)
        if hasattr(event.the_hnl.l1(), 'bestdsmuon'):
            self.fillParticle(self.tree, 'l1_matched_dsmuon', event.the_hnl.l1().bestdsmuon)
        if hasattr(event.the_hnl.l1(), 'bestdgmuon'):
            self.fillParticle(self.tree, 'l1_matched_dgmuon', event.the_hnl.l1().bestdgmuon)
        self.fillGenParticle(self.tree, 'l2', event.the_hnl.l2())
        if hasattr(event.the_hnl.l2(), 'bestelectron'):
            self.fillParticle(self.tree, 'l2_matched_electron', event.the_hnl.l2().bestelectron)
        if hasattr(event.the_hnl.l2(), 'bestphoton'):
            self.fillParticle(self.tree, 'l2_matched_photon', event.the_hnl.l2().bestphoton)
        if hasattr(event.the_hnl.l2(), 'bestmuon'):
            self.fillParticle(self.tree, 'l2_matched_muon', event.the_hnl.l2().bestmuon)
        if hasattr(event.the_hnl.l2(), 'besttau'):
            self.fillParticle(self.tree, 'l2_matched_tau', event.the_hnl.l2().besttau)
        if hasattr(event.the_hnl.l2(), 'bestdsmuon'):
            self.fillParticle(self.tree, 'l2_matched_dsmuon', event.the_hnl.l2().bestdsmuon)
        if hasattr(event.the_hnl.l2(), 'bestdgmuon'):
            self.fillParticle(self.tree, 'l2_matched_dgmuon', event.the_hnl.l2().bestdgmuon)

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

        # flag if the event is in CMS acceptance |eta|<2.5
        is_in_acc =  abs(event.the_hnl.l0().eta())<2.5 and \
                     abs(event.the_hnl.l1().eta())<2.5 and \
                     abs(event.the_hnl.l2().eta())<2.5
 
        self.fill(self.tree, 'is_in_acc', is_in_acc)

        self.fillTree(event)
