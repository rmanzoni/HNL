'''
This is the main analyzer going through data and trying to identify HNL->3L events.
'''

import ROOT
from itertools import product, combinations
from math import sqrt, pow

from PhysicsTools.Heppy.analyzers.core.Analyzer      import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle    import AutoHandle
from PhysicsTools.Heppy.physicsobjects.GenParticle   import GenParticle
from PhysicsTools.Heppy.physicsobjects.Muon          import Muon
from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from CMGTools.HNL.utils.utils                     import isAncestor, displacement2D, displacement3D, makeRecoVertex, fitVertex
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi

from CMGTools.HNL.physicsobjects.DiLepton import DiLepton
from CMGTools.HNL.physicsobjects.DisplacedMuon import DisplacedMuon
from pdb import set_trace

# load custom library to ROOT. This contains the kinematic vertex fitter class
ROOT.gSystem.Load('libCMGToolsHNL')
from ROOT import HNLKinematicVertexFitter as VertexFitter

class HNLAnalyzer(Analyzer):
    '''
    '''

    def declareHandles(self):
        super(HNLAnalyzer, self).declareHandles()

        self.handles['ele']    = AutoHandle(('slimmedElectrons', '','PAT'), 'std::vector<pat::Electron>')
        self.handles['sMu']      = AutoHandle(('slimmedMuons','','PAT'),'std::vector<pat::Muon>')
        self.handles['dSAMu']    = AutoHandle(('displacedStandAloneMuons','','RECO'),'std::vector<reco::Track>')
        self.handles['dGMu']     = AutoHandle(('displacedGlobalMuons','','RECO'),'std::vector<reco::Track>')
        self.handles['pvs']      = AutoHandle(('offlineSlimmedPrimaryVertices','','PAT'),'std::vector<reco::Vertex>')
        self.handles['svs']      = AutoHandle(('slimmedSecondaryVertices','','PAT'),'std::vector<reco::VertexCompositePtrCandidate>')
        self.handles['beamspot'] = AutoHandle(('offlineBeamSpot','','RECO'),'reco::BeamSpot')
        self.handles['met']      = AutoHandle(('slimmedMETs','','PAT'),'std::vector<pat::MET>')

    def assignVtx(self, particles, vtx):    
        for ip in particles:
            ip.associatedVertex = vtx

    def beginLoop(self, setup):
        super(HNLAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('HNL')
        count = self.counters.counter('HNL')
        count.register('all events')
        count.register('good gen')
        count.register('pairs')
        count.register('dimuons')

        # initiate the VertexFitter
        self.vtxfit = VertexFitter()

        # create a std::vector<RecoChargedCandidate> to be passed to the fitter
        self.tofit = ROOT.std.vector('reco::RecoChargedCandidate')()

    def buildDisplacedMuons(self, collection):
        muons = [DisplacedMuon(mm, collection) for mm in collection]
        return muons

    def process(self, event):
        self.readCollections(event.input)
        self.counters.counter('HNL').inc('all events')

        #####################################################################################
        # produce collections and map our objects to convenient Heppy objects
        #####################################################################################

        event.sMu         = map(Muon,self.handles['sMu'].product())
        event.dSAMu       = self.buildDisplacedMuons(self.handles['dSAMu'].product())
        event.dGMu        = self.buildDisplacedMuons(self.handles['dGMu' ].product())

        # make vertex objects 
        event.pvs         = self.handles['pvs'     ].product()
        event.svs         = self.handles['svs'     ].product()
        event.beamspot    = self.handles['beamspot'].product()

        # make met object
        event.met         = self.handles['met'].product().at(0)

        # assign to the leptons the primary vertex, will be needed to compute a few quantities
        if len(event.pvs):
            myvtx = event.pvs[0]
        else:
            myvtx = event.beamspot
        
        self.assignVtx(event.sMu,myvtx)

        # store the number of sMu and dSAMu per event
        event.n_sMu   = len(event.sMu)
        event.n_dSAMu = len(event.dSAMu)
        event.n_dGMu  = len(event.dGMu)

        # ELECTRONS
        ele_cand = []
        matchable_ele = [ele for ele in event.ele]
        # selection
        ele_sel_eta = 2.5; ele_sel_pt = 3; ele_sel_vtx = 0.2 
        # match collections
        matchable_ele_sel_pt = [ele for ele in matchable_ele if (ele.pt() > ele_sel_pt)] 
        matchable_ele_sel_eta = [ele for ele in matchable_ele if (abs(ele.eta()) < ele_sel_eta)] 
        matchable_ele_sel_id = [ele for ele in matchable_ele if (ele.mvaIDRun2('NonTrigSpring15MiniAOD', 'POG90') == True)] 
        # https://github.com/rmanzoni/cmgtools-lite/blob/825_HTT/H2TauTau/python/proto/analyzers/TauEleAnalyzer.py#L193
        matchable_ele_sel_vtx = [ele for ele in matchable_ele if abs(ele.dz()) < ele_sel_vtx] # TODO what about dxy component ?
        
        ele_cand = [ele for ele in matchable_ele if (ele in matchable_ele_sel_pt and ele in matchable_ele_sel_eta and ele in matchable_ele_sel_id and ele in matchable_ele_sel_vtx)]
        
        prompt_cand = ele_cand 
        the_prompt_cand = None
        # EVALUATING THE PROMPT SELECTION: EFF / PUR
        event.prompt_ana_success = -99 # NO RECO FOUND
#        if not len(prompt_cand): return False
        if len(prompt_cand): 
        # selection: pick candidate with highest pt 
        # there must be something better; maybe if both are matched check some additional stuff
            the_prompt_cand = sorted(prompt_cand, key = lambda lep: lep.pt(), reverse = True)[0]
#            event.the_prompt_cand = the_prompt_cand # TODO WHEN TRIGGER STUFF IS DONE, MOVE THIS LINE AFTER TRIGGERS
            # REMOVING PROMPT LEPTON FROM MATCHES 
            if the_prompt_cand in ele_cand:
                event.ele.remove(the_prompt_cand)
                if hasattr(event.the_hnl.l0().bestmatch, 'physObj'):
                    if  the_prompt_cand.physObj == event.the_hnl.l0().bestmatch.physObj:
                        event.prompt_ana_success = 1
                else: event.prompt_ana_success = -11 # FAKE ELECTRONS
#            if event.the_prompt_cand in mu_cand:
#                event.muons.remove(event.the_prompt_cand)
#                event.prompt_ana_success = -13 # FAKE MUONS, FIXME REMOVE THIS IF NOT DEALING WITH E ON SHELL

        # TRIGGER MATCHING
        # match only if the trigger fired
        event.fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]

        # trigger matching
        if hasattr(self.cfg_ana, 'trigger_match') and len(self.cfg_ana.trigger_match.keys())>0:
                                   
            for ele in the_prompt_cand:
                
#                triplet.hltmatched = [] # initialise to no match
                ele.hltmatched = [] # initialise to no match
                
#               triplet.trig_objs = OrderedDict()
#               triplet.trig_objs[1] = [] # initialise to no trigger objct matches
#               triplet.trig_objs[2] = [] # initialise to no trigger objct matches
#               triplet.trig_objs[3] = [] # initialise to no trigger objct matches
                ele.trig_objs = OrderedDict()
                ele.trig_objs[1] = [] # initialise to no trigger objct matches
    
#               triplet.trig_matched = OrderedDict()
#               triplet.trig_matched[1] = False # initialise to no match
#               triplet.trig_matched[2] = False # initialise to no match
#               triplet.trig_matched[3] = False # initialise to no match
                ele.trig_matched = OrderedDict()
                ele.trig_matched[1] = False # initialise to no match

#               triplet.best_trig_match = OrderedDict()
#               triplet.best_trig_match[1] = OrderedDict()
#               triplet.best_trig_match[2] = OrderedDict()
#               triplet.best_trig_match[3] = OrderedDict()
                ele.best_trig_match = OrderedDict()
                ele.best_trig_match[1] = OrderedDict()

                # add all matched objects to each muon
                for info in event.trigger_infos:
                                    
                    mykey = '_'.join(info.name.split('_')[:-1])

                    # start with simple matching
#                    these_objects1 = sorted([obj for obj in info.objects if deltaR(triplet.mu1(), obj)<0.15], key = lambda x : deltaR(x, triplet.mu1()))
#                    these_objects2 = sorted([obj for obj in info.objects if deltaR(triplet.mu2(), obj)<0.15], key = lambda x : deltaR(x, triplet.mu2()))
#                    these_objects3 = sorted([obj for obj in info.objects if deltaR(triplet.mu3(), obj)<0.15], key = lambda x : deltaR(x, triplet.mu3()))
                    these_objects = sorted([obj for obj in info.objects if deltaR(ele, obj)<0.15], key = lambda x : deltaR(x, ele))

#                   triplet.trig_objs[1] += these_objects1
#                   triplet.trig_objs[2] += these_objects2
#                   triplet.trig_objs[3] += these_objects3
                    ele.trig_objs[1] += these_objects

                    # get the set of trigger types from the cfg 
                    trigger_types_to_match = self.cfg_ana.trigger_match[mykey][1]
                    
                    # list of tuples of matched objects
                    good_matches = []

                    # initialise the matching to None
#                    triplet.best_trig_match[1][mykey] = None
#                    triplet.best_trig_match[2][mykey] = None
#                    triplet.best_trig_match[3][mykey] = None
                    ele.best_trig_match[1][mykey] = None

                    # investigate all the possible matches (eles, pairs or singlets)
                   # for to1, to2, to3 in product(these_objects1, these_objects2, these_objects3):
                    for t_o in these_objects:
                        # avoid double matches!
                        # if to1==to2 or to1==to3 or to2==to3:
                        #    continue

                        # intersect found trigger types to desired trigger types
                        itypes = Counter()
                        for ikey in trigger_types_to_match.keys():
                           # itypes[ikey] = sum([1 for iobj in [to1, to2, to3] if iobj.triggerObjectTypes()[0]==ikey])
                            itypes[ikey] = sum([1 for iobj in t_o if iobj.triggerObjectTypes()[0]==ikey])
                                            
                        # all the types to match are matched then assign the 
                        # corresponding trigger object to each ele
                        if itypes & trigger_types_to_match == trigger_types_to_match:
                            #good_matches.append((to1, to2, to3))
                            good_matches.append(t_o)
                    
                    
                    if len(good_matches):
                        # good_matches.sort(key = lambda x : deltaR(x[0], ele.mu1()) + deltaR(x[1], ele.mu2()) + deltaR(x[2], ele.mu3()))        
                        good_matches.sort(key = lambda x : deltaR(x, ele))        

                        # ONLY for HLT_DoubleMu3_Trk_Tau3mu
                        # it might happen that more than one combination of trk mu mu is found,
                        # make sure that the online 3-body mass cut is satisfied by the matched objects
#                       if mykey == 'HLT_DoubleMu3_Trk_Tau3mu':
#                          
#                          good_matches_tmp = []
#                          
#                          for im in good_matches:
#                              p4_1 = ROOT.TLorentzVector()
#                              p4_2 = ROOT.TLorentzVector()
#                              p4_3 = ROOT.TLorentzVector()
#
#                              p4_1.SetPtEtaPhiM(im[0].pt(), im[0].eta(), im[0].phi(), 0.10565999895334244)                        
#                              p4_2.SetPtEtaPhiM(im[1].pt(), im[1].eta(), im[1].phi(), 0.10565999895334244)
#                              p4_3.SetPtEtaPhiM(im[2].pt(), im[2].eta(), im[2].phi(), 0.10565999895334244)
#                                      
#                              totp4 = p4_1 + p4_2 + p4_3
#                              
#                              if totp4.M()>1.6 and totp4.M()<2.02:
#                                  good_matches_tmp.append(im)
#                          
#                          good_matches = good_matches_tmp
#                          
#                      ele.best_trig_match[1][mykey] = good_matches[0][0] if len(good_matches) and len(good_matches[0])>0 else None
#                      ele.best_trig_match[2][mykey] = good_matches[0][1] if len(good_matches) and len(good_matches[0])>1 else None
#                      ele.best_trig_match[3][mykey] = good_matches[0][2] if len(good_matches) and len(good_matches[0])>2 else None
                
                # iterate over the path:filters dictionary
                #     the filters MUST be sorted correctly: i.e. first filter in the dictionary 
                #     goes with the first muons and so on
                for k, vv in self.cfg_ana.trigger_match.iteritems():

                    if not any(k in name for name in event.fired_triggers):
                         continue
                    
                    v = vv[0]
                                                                 
                    for ii, filters in enumerate(v):
                        if not ele.best_trig_match[ii+1][k]:
                            continue
                        if set([filters]) & set(ele.best_trig_match[ii+1][k].filterLabels()):
                            ele.trig_matched[ii+1] = True                 
                    
                    ismatched = sum(ele.trig_matched.values())            
                                
                    if len(v) == ismatched:
                        ele.hltmatched.append(k)

#            seltau3mu = [triplet for triplet in seltau3mu if len(triplet.hltmatched)>0]
            the_prompt_cand = [ele for ele in the_prompt_cand if len(ele.hltmatched)>0]
            
#            if len(the_prompt_cand) == 0:
#                return False #TODO  UNCOMMENT THIS IN FINAL VERSION
#            self.counters.counter('Tau3Mu').inc('trigger matched')

#        event.seltau3mu = seltau3mu

#        event.tau3mu = self.bestTriplet(event.seltau3mu)                        
        event.the_prompt_cand = the_prompt_cand

#        return True #TODO  UNCOMMENT THIS IN FINAL VERSION

       
        #####################################################################################
        # Merge Reco Muons
        # Create an array of DisplacedMuon objects, summarizing all sMu, dSAMu and dGMu into a single array
        # Comment those out which are not needed for the current run
        #####################################################################################
        dMus = []

        for smu in event.sMu:
            dmu = smu
            dmu.reco = 1 # sMu = 1, dSAMu = 2
            dmu.redundancy = 0 
            dMus.append(dmu)
            event.n_sMuOnly += 1

        # for dsa in event.dSAMu:
            # dmu = dsa
            # dmu.reco = 2 # sMu = 1, dSAMu = 2
            # dmu.redundancy = 0 
            # dMus.append(dmu)
            # event.n_dSAMuOnly += 1

        # for dg in event.dGMu:
            # dmu = dg
            # dmu.reco = 3 # sMu = 1, dSAMu = 2, dGMu = 3
            # dmu.redundancy = 0
            # dMus.append(dmu)
            # event.n_dGMuOnly += 1

       
        event.n_dMu = len(dMus) # important to understand how well the "Merge Reco Muons" process went. 
       
        #####################################################################################
        # Qualify the performance of the MUCO
        #####################################################################################
        event.flag_MUCOsuccess = False    
        l1matched=False
        l2matched=False
        if len(dMus) > 1 and hasattr(event.the_hnl.l1().bestmatch, 'physObj') and hasattr(event.the_hnl.l2().bestmatch,'physObj'):
            for dmu in dMus:
                if dmu.physObj == event.the_hnl.l1().bestmatch.physObj:
                    l1matched = True
                if dmu.physObj == event.the_hnl.l2().bestmatch.physObj:
                    l2matched = True
        if l1matched and l2matched:
            event.flag_MUCOsuccess = True


        #####################################################################################
        # select only events with good gen events
        #####################################################################################
        if not( abs(event.the_hnl.l1().pdgId())==13   and \
                abs(event.the_hnl.l2().pdgId())==13   and \
                abs(event.the_hnl.l1().eta())   < 2.4 and \
                abs(event.the_hnl.l2().eta())   < 2.4 and \
                abs(event.the_hnl.l0().eta())   < 2.4): 
            return False

        if (not hasattr(event.the_hnl.l1(), 'bestmatch')) or (event.the_hnl.l1().bestmatch is None):
            return False
        if (not hasattr(event.the_hnl.l2(), 'bestmatch')) or (event.the_hnl.l2().bestmatch is None):
            return False

        self.counters.counter('HNL').inc('good gen')

        # #####################################################################################
        # Preselection for the reco muons before pairing them
        # #####################################################################################

        # some simple preselection based on pt
        event.sMu   = [imu for imu in event.sMu   if imu.pt()>3.]
        event.dSAMu = [imu for imu in event.dSAMu if imu.pt()>3.]
        event.dGMu  = [imu for imu in event.dGMu  if imu.pt()>3.]


        #####################################################################################
        # collect all muon pairs
        #####################################################################################
        pairs = [pair for pair in combinations(dMus,2)] 
        pairs = [(mu1,mu2) for mu1, mu2 in pairs if deltaR(mu1,mu2)>0.01] 
        event.n_pairs = len(pairs)
        event.flag_IsThereTHEDimuon = False

        event.n_dimuon = 0
        if len(pairs) == 0:
            pass

        self.counters.counter('HNL').inc('pairs')

        ########################################################################################
        # Vertex Fit: Select only dimuon pairs with mutual vertices
        ########################################################################################
        dimuons = []
        for pair in pairs:
            sv = None
            # print pair[0]
            # print pair[1]
            if not pair[0]==pair[1]:
                sv = fitVertex(pair)
                if sv != None:
                    dimuons.append(DiLepton(pair,sv,myvtx,event.beamspot))

        #####################################################################################
        # Check whether the correct dimuon is part of the collection dimuons
        #####################################################################################
        if len(dimuons) > 0:
            for dimu in dimuons:
                dMu1 = dimu.lep1()
                dMu2 = dimu.lep2() 
                if (dMu1.physObj == event.the_hnl.l1().bestmatch.physObj or dMu1.physObj == event.the_hnl.l2().bestmatch.physObj) and (dMu2.physObj == event.the_hnl.l1().bestmatch.physObj or dMu2.physObj == event.the_hnl.l2().bestmatch.physObj):
                    event.flag_IsThereTHEDimuon = True


        #####################################################################################
        # select the best dimuon pairs 
        #####################################################################################
        event.n_dimuon = len(dimuons)
        if len(dimuons) > 0:
            self.counters.counter('HNL').inc('dimuons')
             
            # select the dimuon with lowest vertex fit chi2 as the HNL dimuon candidate
            dimuonChi2 = sorted(dimuons, key = lambda x: (x.isSS(),x.chi2()), reverse = False)[0] 
            event.dimuonChi2 = dimuonChi2
            event.dMu1Chi2 = dimuonChi2.lep1()
            event.dMu2Chi2 = dimuonChi2.lep2()
            
            # select the dimuon with largest displacement
            dimuonDxy = sorted(dimuons, key = lambda x: (x.isSS(),x.disp2DFromBS()), reverse = True)[0] 
            event.dimuonDxy = dimuonDxy
            event.dMu1Dxy = dimuonDxy.lep1()
            event.dMu2Dxy = dimuonDxy.lep2()

            # select leptons ito added momenta's pt
            dimuonMaxPt = sorted(dimuons, key = lambda x: (x.isSS(),x.pt()), reverse = True)[0] 
            event.dimuonMaxPt = dimuonMaxPt
            event.dMu1MaxPt = dimuonMaxPt.lep1()
            event.dMu2MaxPt = dimuonMaxPt.lep2()

            # select closest leptons ito dr
            dimuonMinDr12 = sorted(dimuons, key = lambda x: (x.isSS(),x.dr()), reverse = False)[0]
            event.dimuonMinDr12 = dimuonMinDr12
            event.dMu1MinDr12 = dimuonMinDr12.lep1()
            event.dMu2MinDr12 = dimuonMinDr12.lep2()

            # select smallest backpointing angle in the transverse plane
            dimuonMaxCosBPA = sorted(dimuons, key = lambda x : (x.isSS(), -x.cosTransversePointingAngleBS()), reverse=False)[0]
            event.dimuonMaxCosBPA = dimuonMaxCosBPA
            event.dMu1MaxCosBPA = dimuonMaxCosBPA.lep1()
            event.dMu2MaxCosBPA = dimuonMaxCosBPA.lep2()


        #####################################################################################
        # TODO: Final Qualification and 'ok' to nominate the selection dimuon as HNL candidate
        #####################################################################################



        return True
