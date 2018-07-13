import ROOT
import numpy as np

from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi

from CMGTools.H2TauTau.proto.analyzers.tauIDs import tauIDs, tauIDs_extra

class Variable():
    def __init__(self, name, function=None, type=float):
        self.name = name
        self.function = function
        if function is None:
            # Note: works for attributes, not member functions
            self.function = lambda x : getattr(x, self.name, np.nan) 
        self.type = type

def default():
    return np.nan

# event variables
event_vars = [
    Variable('run', type=int),
    Variable('lumi', type=int),
    Variable('event', lambda ev : ev.eventId, type=int),
    Variable('bx', lambda ev : (ev.input.eventAuxiliary().bunchCrossing() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('orbit_number', lambda ev : (ev.input.eventAuxiliary().orbitNumber() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('is_data', lambda ev: ev.input.eventAuxiliary().isRealData(), type=int),
#     Variable('nPU', lambda ev : -99 if getattr(ev, 'nPU', -1) is None else getattr(ev, 'nPU', -1)),
    Variable('nPU', lambda ev : np.nan if getattr(ev, 'nPU', -1) is None else getattr(ev, 'nPU', -1)),
    Variable('rho', lambda ev : ev.rho),
#     Variable('Flag_HBHENoiseFilter', type=int),
#     Variable('Flag_HBHENoiseIsoFilter', type=int),
#     Variable('Flag_EcalDeadCellTriggerPrimitiveFilter', type=int),
#     Variable('Flag_goodVertices', type=int),
#     Variable('Flag_eeBadScFilter', type=int),
#     Variable('Flag_globalTightHalo2016Filter', type=int),
#     Variable('passBadMuonFilter', type=int),
#     Variable('passBadChargedHadronFilter', type=int),
#     Variable('n_muons'    , lambda ev : len(ev.muons), type=int),
#     Variable('n_electrons', lambda ev : len(ev.electrons), type=int),
#     Variable('n_taus'     , lambda ev : len(ev.taus), type=int),
#     Variable('n_candidates', lambda ev : ev.ncands, type=int),
    Variable('n_vtx', lambda ev : len(ev.goodVertices), type=int),
    Variable('weight', lambda ev : ev.eventWeight, type=float),
    Variable('puweight', lambda ev : ev.puWeight, type=float),
]

# generic HNL reconstruction event variables
hnlreco_vars = [
    Variable('n_sMu', lambda ev : ev.n_sMu, type=int),
    Variable('n_dSAMu', lambda ev : ev.n_dSAMu, type=int),
    Variable('n_dMu', lambda ev : ev.n_dMu, type=int),
    Variable('n_pairs', lambda ev : ev.n_pairs, type=int),
    Variable('n_sMuOnly',      lambda ev : ev.n_sMuOnly, type=int),
    Variable('n_sMuRedundant', lambda ev : ev.n_sMuRedundant, type=int),
    Variable('n_dSAMuOnly',      lambda ev : ev.n_dSAMuOnly, type=int),
    Variable('n_dSAMuRedundant', lambda ev : ev.n_dSAMuRedundant, type=int),
    Variable('n_dimuon', lambda ev : ev.n_dimuon, type=int),
]

# Variables indicating the quality of HNL reconstruction
check_hnlreco_vars = [
    Variable('flag_matchedL1Chi2', lambda ev : ev.matchedL1Chi2,   ),
    Variable('flag_matchedL2Chi2', lambda ev : ev.matchedL2Chi2,   ),
    Variable('flag_matchedL1Dxy',  lambda ev : ev.matchedL1Dxy ,   ),
    Variable('flag_matchedL2Dxy',  lambda ev : ev.matchedL2Dxy ,   ),
    Variable('flag_matchedHNLChi2', lambda ev : ev.matchedHNLChi2 ,),
    Variable('flag_matchedHNLDxy', lambda ev : ev.matchedHNLDxy ,  ),
    Variable('flag_IsThereTHEDimuon', lambda ev : ev.flag_IsThereTHEDimuon , ),
    Variable('flag_MUCOsuccess', lambda ev : ev.flag_MUCOsuccess , ),


]

# generic DiMuon variables
dimuon_vars = [
    Variable('x', lambda hn : hn.vtx.x(), type = float), 
    Variable('y', lambda hn : hn.vtx.y(), type = float), 
    Variable('z', lambda hn : hn.vtx.z(), type = float), 
    Variable('dxy', lambda hn : hn.dxy(), type = float), 
    Variable('vtxFitChi2', lambda hn : hn.vtx.chi2(), type = float),
]

# generic DiMuon variables
displacedmuon_vars = [
    Variable('x'    , lambda p: p.vx() ),
    Variable('y'    , lambda p: p.vy() ),
    Variable('z'    , lambda p: p.vz() ),
    Variable('dxy'    , lambda p: p.dxy() ),
    Variable('pt'    , lambda p: p.pt() ),
    Variable('eta'   , lambda p: p.eta()),
    Variable('phi'   , lambda p: p.phi()),
    Variable('charge', lambda p: p.charge() if hasattr(p, 'charge') else 0), # charge may be non-integer for gen particles
    Variable('mass'  , lambda p: p.mass()),
    Variable('reco'  , lambda p: p.reco),
    Variable('redundancy'  , lambda p: p.redundancy),
]

# generic HNL variables
hnl_vars = [
    Variable('w_pt'           , lambda hn : getattr(hn, 'pt'          , default)()),
    Variable('w_eta'          , lambda hn : getattr(hn, 'eta'         , default)()),
    Variable('w_phi'          , lambda hn : getattr(hn, 'phi'         , default)()),
    Variable('w_q'            , lambda hn : getattr(hn, 'charge'      , default)()),
    Variable('w_m'            , lambda hn : getattr(hn, 'mass'        , default)()),
    Variable('w_sum_pt'       , lambda hn : getattr(hn, 'sumPt'       , default)()),
  
    Variable('w_vis_pt'       , lambda hn : getattr(hn, 'visPt'       , default)()),
    Variable('w_vis_eta'      , lambda hn : getattr(hn, 'visEta'      , default)()),
    Variable('w_vis_phi'      , lambda hn : getattr(hn, 'visPhi'      , default)()),
    Variable('w_vis_q'        , lambda hn : getattr(hn, 'charge'      , default)()),
    Variable('w_vis_m'        , lambda hn : getattr(hn, 'visMass'     , default)()),
    Variable('w_vis_sum_pt'   , lambda hn : getattr(hn, 'visSumPt'    , default)()),
  
    Variable('hn_pt'          , lambda hn : getattr(hn, 'hnPt'        , default)()),
    Variable('hn_eta'         , lambda hn : getattr(hn, 'hnEta'       , default)()),
    Variable('hn_phi'         , lambda hn : getattr(hn, 'hnPhi'       , default)()),
    Variable('hn_q'           , lambda hn : getattr(hn, 'hnCharge'    , default)()),
    Variable('hn_m'           , lambda hn : getattr(hn, 'hnMass'      , default)()),
    Variable('hn_sum_pt'      , lambda hn : getattr(hn, 'hnSumPt'     , default)()),
  
    Variable('hn_vis_pt'      , lambda hn : getattr(hn, 'hnVisPt'     , default)()),
    Variable('hn_vis_eta'     , lambda hn : getattr(hn, 'hnVisEta'    , default)()),
    Variable('hn_vis_phi'     , lambda hn : getattr(hn, 'hnVisPhi'    , default)()),
    Variable('hn_vis_q'       , lambda hn : getattr(hn, 'hnCharge'    , default)()),
    Variable('hn_vis_m'       , lambda hn : getattr(hn, 'hnVisMass'   , default)()),
    Variable('hn_vis_sum_pt'  , lambda hn : getattr(hn, 'hnVisSumPt'  , default)()),
  
    Variable('m_01'           , lambda hn : getattr(hn, 'mass01'      , default)()),
    Variable('m_02'           , lambda hn : getattr(hn, 'mass02'      , default)()),
    Variable('m_12'           , lambda hn : getattr(hn, 'mass12'      , default)()),
  
    Variable('q_01'           , lambda hn : getattr(hn, 'charge01'    , default)()),
    Variable('q_02'           , lambda hn : getattr(hn, 'charge02'    , default)()),
    Variable('q_12'           , lambda hn : getattr(hn, 'charge12'    , default)()),
  
    Variable('dr_01'          , lambda hn : getattr(hn, 'dR01'        , default)()),
    Variable('dr_02'          , lambda hn : getattr(hn, 'dR02'        , default)()),
    Variable('dr_12'          , lambda hn : getattr(hn, 'dR12'        , default)()),

    Variable('dphi_01'        , lambda hn : getattr(hn, 'dPhi01'      , default)()),
    Variable('dphi_02'        , lambda hn : getattr(hn, 'dPhi02'      , default)()),
    Variable('dphi_12'        , lambda hn : getattr(hn, 'dPhi12'      , default)()),
  
    Variable('dr_0met'        , lambda hn : getattr(hn, 'dR0MET'      , default)()),
    Variable('dr_1met'        , lambda hn : getattr(hn, 'dR1MET'      , default)()),
    Variable('dr_2met'        , lambda hn : getattr(hn, 'dR2MET'      , default)()),

    Variable('dphi_0met'      , lambda hn : getattr(hn, 'dPhi0MET'    , default)()),
    Variable('dphi_1met'      , lambda hn : getattr(hn, 'dPhi1MET'    , default)()),
    Variable('dphi_2met'      , lambda hn : getattr(hn, 'dPhi2MET'    , default)()),
  
    Variable('pt_01'          , lambda hn : getattr(hn, 'pt01'        , default)()),
    Variable('pt_02'          , lambda hn : getattr(hn, 'pt02'        , default)()),
    Variable('pt_12'          , lambda hn : getattr(hn, 'pt12'        , default)()),
  
    Variable('pt_0met'        , lambda hn : getattr(hn, 'pt0MET'      , default)()),
    Variable('pt_1met'        , lambda hn : getattr(hn, 'pt1MET'      , default)()),
    Variable('pt_2met'        , lambda hn : getattr(hn, 'pt2MET'      , default)()),

    Variable('dr_hn0'         , lambda hn : getattr(hn, 'dRHn0'       , default)()),
    Variable('dr_hnvis0'      , lambda hn : getattr(hn, 'dRvisHn0'    , default)()),
    Variable('dr_hnvismet'    , lambda hn : getattr(hn, 'dRvisHnMET'  , default)()),

    Variable('dphi_hn0'       , lambda hn : getattr(hn, 'dPhiHn0'     , default)()),
    Variable('dphi_hnvis0'    , lambda hn : getattr(hn, 'dPhiVisHn0'  , default)()),
    Variable('dphi_hnvismet'  , lambda hn : getattr(hn, 'dPhiVisHnMET', default)()),

    Variable('mt_0'           , lambda hn : getattr(hn, 'mt0'         , default)()),
    Variable('mt_1'           , lambda hn : getattr(hn, 'mt1'         , default)()),
    Variable('mt_2'           , lambda hn : getattr(hn, 'mt2'         , default)()),
    Variable('mt_hnvis'       , lambda hn : getattr(hn, 'mtVisHnMET'  , default)()),
]


# generic particle
particle_vars = [
    Variable('pt'    , lambda p: p.pt() ),
    Variable('eta'   , lambda p: p.eta()),
    Variable('phi'   , lambda p: p.phi()),
    Variable('charge', lambda p: p.charge() if hasattr(p, 'charge') else 0), # charge may be non-integer for gen particles
    Variable('mass'  , lambda p: p.mass()),
    Variable('pdgId' , lambda p: p.pdgId()),
]

# stage-2 L1 object
l1obj_vars = [
    Variable('iso'  , lambda p: p.hwIso()),
    Variable('qual' , lambda p: p.hwQual()),
    Variable('type' , lambda p: p.type),
    Variable('bx'   , lambda p: p.bx),
    Variable('index', lambda p: p.index),
]

# track-vertex vars
particle_vertex_vars = [
    Variable('dxy'      , lambda trk : trk.dxy()),
    Variable('dxy_error', lambda trk : trk.dxyError()),
    Variable('dz'       , lambda trk : trk.dz()),
    Variable('dz_error' , lambda trk : trk.dzError()),
]

# generic lepton
lepton_vars = [
    Variable('dxy'          , lambda lep : lep.dxy()),
    Variable('dxy_error'    , lambda lep : lep.edxy() if hasattr(lep, 'edxy') else lep.dxy_error()),
    Variable('dz'           , lambda lep : lep.leadChargedHadrCand().dz() if hasattr(lep, 'leadChargedHadrCand') else lep.dz()),
    Variable('dz_error'     , lambda lep : lep.edz() if hasattr(lep, 'edz') else -1.),
    Variable('weight_id'    , lambda lep : getattr(lep, 'idweight', 1.)),
    Variable('weight_id_unc', lambda lep : getattr(lep, 'idweightunc', 1.)),
    Variable('weight'),
#     Variable('weight_trigger', lambda lep : getattr(lep, 'weight_trigger', 1.)),
#     Variable('eff_trigger_data', lambda lep : getattr(lep, 'eff_data_trigger', -999.)),
#     Variable('eff_trigger_mc', lambda lep : getattr(lep, 'eff_mc_trigger', -999.)),
#     Variable('weight_idiso', lambda lep : getattr(lep, 'weight_idiso', 1.)),
#     Variable('eff_idiso_data', lambda lep : getattr(lep, 'eff_data_idiso', -999.)),
#     Variable('eff_idiso_mc', lambda lep : getattr(lep, 'eff_mc_idiso', -999.)),
]

# electron
electron_vars = [
    # Variable('eid_nontrigmva_loose', lambda ele : ele.mvaIDRun2("NonTrigPhys14", "Loose")),
    Variable('eid_nontrigmva_loose', lambda ele : ele.mvaRun2('NonTrigSpring15MiniAOD')),
    Variable('eid_nontrigmva_tight', lambda ele : ele.mvaIDRun2("NonTrigSpring15MiniAOD", "POG80")),
    Variable('eid_veto', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Veto')),
    Variable('eid_loose', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Loose')),
    Variable('eid_medium', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Medium')),
    Variable('eid_tight', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Tight')),
    Variable('nhits_missing', lambda ele : ele.physObj.gsfTrack().hitPattern().numberOfHits(1), int),
    Variable('pass_conv_veto', lambda ele : ele.passConversionVeto()),
    Variable('reliso05', lambda lep : lep.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0)),
    Variable('reliso05_04', lambda lep : lep.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0)),
    Variable('reliso05_04', lambda lep : lep.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0)),
    Variable('weight_tracking', lambda lep : getattr(lep, 'weight_tracking', 1.)),
]

# photon
photon_vars = [
    Variable('ch_iso'   , lambda ph : ph.chargedHadronIso     ()                           ),
    Variable('n_iso'    , lambda ph : ph.neutralHadronIso     ()                           ),
    Variable('r9_5x5'   , lambda ph : ph.full5x5_r9           ()                           ),
    Variable('sieie_5x5', lambda ph : ph.full5x5_sigmaIetaIeta()                           ),
    Variable('hoe'      , lambda ph : ph.hOVERe               ()                           ),
    Variable('id_l'     , lambda ph : ph.passPhotonID         ('POG_SPRING15_25ns_Loose' ) ),
    Variable('id_m'     , lambda ph : ph.passPhotonID         ('POG_SPRING15_25ns_Medium') ),
    Variable('id_t'     , lambda ph : ph.passPhotonID         ('POG_SPRING15_25ns_Tight' ) ),
    Variable('iso'      , lambda ph : ph.photonIso            ()                           ),
    Variable('r9'       , lambda ph : ph.r9                   ()                           ),
    Variable('sieie'    , lambda ph : ph.sigmaIetaIeta        ()                           ),
]

# vertex
vertex_vars = [
    Variable('covxx'         , lambda vtx : vtx.covariance(0,0)                         ),
    Variable('covyy'         , lambda vtx : vtx.covariance(1,1)                         ),
    Variable('covzz'         , lambda vtx : vtx.covariance(2,2)                         ),
    Variable('covxy'         , lambda vtx : vtx.covariance(0,1)                         ),
    Variable('covxz'         , lambda vtx : vtx.covariance(0,2)                         ),
    Variable('covyz'         , lambda vtx : vtx.covariance(1,2)                         ),
    Variable('chi2'          , lambda vtx : vtx.chi2()                                  ),
    Variable('dimension'                                                      , type=int),
    Variable('isValid'       , lambda vtx : vtx.isValid()                     , type=int),
    Variable('nTracks'       , lambda vtx : vtx.nTracks()                     , type=int),
    Variable('ndof'          , lambda vtx : vtx.ndof()                                  ),
    Variable('normalizedChi2', lambda vtx : vtx.normalizedChi2()              , type=int),
    Variable('x'             , lambda vtx : vtx.x()                                     ),
    Variable('y'             , lambda vtx : vtx.y()                                     ),
    Variable('z'             , lambda vtx : vtx.z()                                     ),
    Variable('xError'        , lambda vtx : vtx.xError()                                ),
    Variable('yError'        , lambda vtx : vtx.yError()                                ),
    Variable('zError'        , lambda vtx : vtx.zError()                                ),
    Variable('prob'          , lambda vtx : ROOT.TMath.Prob(vtx.chi2(), int(vtx.ndof()))),
    Variable('ls'                                                                       ),
    Variable('cos'                                                                      ),
]

# muon
muon_vars = [
    Variable('reliso05'   , lambda muon : muon.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0)),
    Variable('reliso05_03', lambda muon : muon.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0)),
    Variable('id_s'       , lambda muon : muon.isSoftMuon(muon.associatedVertex)            ),
    Variable('id_l'       , lambda muon : muon.muonID('POG_ID_Loose')                       ),
    Variable('id_m'       , lambda muon : muon.muonID('POG_ID_Medium')                      ),
    Variable('id_t'       , lambda muon : muon.muonID('POG_ID_Tight')                       ),
    Variable('id_tnv'     , lambda muon : muon.muonID('POG_ID_TightNoVtx')                  ),
    Variable('id_hpt'     , lambda muon : muon.muonID('POG_ID_HighPt')                      ),
    Variable('is_sa'      , lambda muon : muon.isStandAloneMuon()                           ),
    Variable('is_gl'      , lambda muon : muon.isGlobalMuon()                               ),
    Variable('is_tk'      , lambda muon : muon.isTrackerMuon()                              ),
    Variable('is_pf'      , lambda muon : muon.isPFMuon()                                   ),
]

# for an extensive summary of possibly interesting muon variables, have a look at
# https://github.com/trocino/MuonPOG/blob/master/Tools/plugins/MuonEventDumper.cc#L350-L377

muon_track_extra_vars = [
    Variable('sigma_pt_over_pt'               , lambda track : track.ptError()/track.pt()                       ),
    Variable('eta'                            , lambda track : track.eta()                                      ),
    Variable('phi'                            , lambda track : track.phi()                                      ),
    Variable('charge'                         , lambda track : track.charge()                                   ),
    Variable('ndof'                           , lambda track : track.ndof()                                     ),
    Variable('chi2_over_ndof'                 , lambda track : track.normalizedChi2()                           ),
    Variable('n_pix_hits'                     , lambda track : track.hitPattern().numberOfValidPixelHits()      ),
    Variable('n_trk_layers'                   , lambda track : track.hitPattern().trackerLayersWithMeasurement()),
    Variable('n_mu_hits'                      , lambda track : track.hitPattern().numberOfValidMuonHits()       ),
    Variable('n_mu_valid_hits'                , lambda track : track.hitPattern().numberOfMuonHits()            ),
    Variable('n_dt_valid_hits'                , lambda track : track.hitPattern().numberOfValidMuonDTHits()     ),
    Variable('n_csc_valid_hits'               , lambda track : track.hitPattern().numberOfValidMuonCSCHits()    ),
    Variable('n_rpc_valid_hits'               , lambda track : track.hitPattern().numberOfValidMuonRPCHits()    ),
    Variable('n_dt_bad_hits'                  , lambda track : track.hitPattern().numberOfBadMuonDTHits()       ),
    Variable('n_csc_bad_hits'                 , lambda track : track.hitPattern().numberOfBadMuonCSCHits()      ),
    Variable('n_rpc_bad_hits'                 , lambda track : track.hitPattern().numberOfBadMuonRPCHits()      ),
    Variable('n_dt_lost_hits'                 , lambda track : track.hitPattern().numberOfLostMuonDTHits()      ),
    Variable('n_csc_lost_hits'                , lambda track : track.hitPattern().numberOfLostMuonCSCHits()     ),
    Variable('n_rpc_lost_hits'                , lambda track : track.hitPattern().numberOfLostMuonRPCHits()     ),
    Variable('n_mu_st_w_valid_hits'           , lambda track : track.hitPattern().muonStationsWithValidHits()   ),
    Variable('n_dt_st_w_valid_hits'           , lambda track : track.hitPattern().dtStationsWithValidHits()     ),
    Variable('n_csc_st_w_valid_hits'          , lambda track : track.hitPattern().cscStationsWithValidHits()    ),
    Variable('n_rpc_st_w_valid_hits'          , lambda track : track.hitPattern().rpcStationsWithValidHits()    ),
    Variable('n_mu_st_w_valid_hits'           , lambda track : track.hitPattern().muonStationsWithAnyHits()     ),
    Variable('n_dt_st_w_valid_hits'           , lambda track : track.hitPattern().dtStationsWithAnyHits()       ),
    Variable('n_csc_st_w_valid_hits'          , lambda track : track.hitPattern().cscStationsWithAnyHits()      ),
    Variable('n_rpc_st_w_valid_hits'          , lambda track : track.hitPattern().rpcStationsWithAnyHits()      ),
]


muon_extra_vars = [
    # ask quality first...
    Variable('dxy_innertrack'   , lambda muon : muon.innerTrack().dxy(muon.associatedVertex.position())              ),
    Variable('dz_innertrack'    , lambda muon : muon.innerTrack().dz(muon.associatedVertex.position())               ),
    Variable('weight_tracking'  , lambda muon : getattr(muon, 'weight_tracking', 1.)                                 ),
    Variable('pdgIDoverweight'  , lambda muon : muon.pdgIDoverweight    if hasattr(muon, "pdgIDoverweight")  else default()),
    #BDT VARS 
    Variable('segComp'          , lambda muon : muon.segComp            if hasattr(muon, 'segComp')          else default()),
    Variable('chi2LocMom'       , lambda muon : muon.chi2LocMom         if hasattr(muon, 'chi2LocMom')       else default()),
    Variable('chi2LocPos'       , lambda muon : muon.chi2LocPos         if hasattr(muon, 'chi2LocPos')       else default()),
    Variable('glbTrackTailProb' , lambda muon : muon.glbTrackTailProb   if hasattr(muon, 'glbTrackTailProb') else default()),
    Variable('iValFrac'         , lambda muon : muon.iValFrac           if hasattr(muon, 'iValFrac')         else default()),
    Variable('LHW'              , lambda muon : muon.LHW                if hasattr(muon, 'LHW')              else default()),
    Variable('kinkFinder'       , lambda muon : muon.kinkFinder         if hasattr(muon, 'kinkFinder')       else default()),
    Variable('timeAtIpInOutErr' , lambda muon : muon.timeAtIpInOutErr   if hasattr(muon, 'timeAtIpInOutErr') else default()),
    Variable('outerChi2'        , lambda muon : muon.outerChi2          if hasattr(muon, 'outerChi2')        else default()),
    Variable('innerChi2'        , lambda muon : muon.innerChi2          if hasattr(muon, 'innerChi2')        else default()),
    Variable('trkRelChi2'       , lambda muon : muon.trkRelChi2         if hasattr(muon, 'trkRelChi2')       else default()),
    Variable('vMuonHitComb'     , lambda muon : muon.vMuonHitComb       if hasattr(muon, 'vMuonHitComb')     else default()),
    Variable('Qprod'            , lambda muon : muon.Qprod              if hasattr(muon, 'Qprod')            else default()),
    Variable('LogGlbKinkFinder' , lambda muon : muon.LogGlbKinkFinder   if hasattr(muon, 'LogGlbKinkFinder') else default()),
    #fake muons variables
    Variable('isFake'           , lambda muon : muon.isFake             if hasattr(muon, 'isFake')           else default()),
]

# tau
tau_vars = [
    Variable('decayMode', lambda tau : tau.decayMode()),
    Variable('zImpact', lambda tau : tau.zImpact()),
    Variable('dz_selfvertex', lambda tau : tau.vertex().z() - tau.associatedVertex.position().z()),
    Variable('ptScale', lambda tau : getattr(tau, 'ptScale', -999.)),
    Variable('NewMVAID'),
    Variable('NewMVAraw'),
]
for tau_id in tauIDs:
    if type(tau_id) is str:
        # Need to use eval since functions are otherwise bound to local
        # variables
        tau_vars.append(Variable(tau_id, eval('lambda tau : tau.tauID("{id}")'.format(id=tau_id))))
    else:
        sum_id_str = ' + '.join('tau.tauID("{id}")'.format(id=tau_id[0].format(wp=wp)) for wp in tau_id[1])
        tau_vars.append(Variable(tau_id[0].format(wp=''), 
            eval('lambda tau : ' + sum_id_str), int))

tau_vars_extra = []
for tau_id in tauIDs_extra:
    if type(tau_id) is str:
        # Need to use eval since functions are otherwise bound to local
        # variables
        tau_vars_extra.append(Variable(tau_id, eval('lambda tau : tau.tauID("{id}")'.format(id=tau_id))))
    else:
        sum_id_str = ' + '.join('tau.tauID("{id}")'.format(id=tau_id[0].format(wp=wp)) for wp in tau_id[1])
        tau_vars_extra.append(Variable(tau_id[0].format(wp=''), 
            eval('lambda tau : ' + sum_id_str), int))


# jet
jet_vars = [
    Variable('mva_pu', lambda jet : jet.puMva('pileupJetId:fullDiscriminant')),
    Variable('id_pu', lambda jet : jet.puJetId()),
    # Variable('id_loose', lambda jet : jet.looseJetId()),
    # Variable('id_pu', lambda jet : jet.puJetId() + jet.puJetId(wp='medium') + jet.puJetId(wp='tight')),
    # Variable('area', lambda jet : jet.jetArea()),
    Variable('flavour_parton', lambda jet : jet.partonFlavour()),
    Variable('csv', lambda jet : jet.btagMVA),
    Variable('genjet_pt', lambda jet : jet.matchedGenJet.pt() if hasattr(jet, 'matchedGenJet') and jet.matchedGenJet else default()),
]

# extended jet vars
jet_vars_extra = [
    Variable('nConstituents', lambda jet : getattr(jet, 'nConstituents', default)()),
    Variable('rawFactor', lambda jet : getattr(jet, 'rawFactor', default)()),
    Variable('chargedHadronEnergy', lambda jet : getattr(jet, 'chargedHadronEnergy', default)()),
    Variable('neutralHadronEnergy', lambda jet : getattr(jet, 'neutralHadronEnergy', default)()),
    Variable('neutralEmEnergy', lambda jet : getattr(jet, 'neutralEmEnergy', default)()),
    Variable('muonEnergy', lambda jet : getattr(jet, 'muonEnergy', default)()),
    Variable('chargedEmEnergy', lambda jet : getattr(jet, 'chargedEmEnergy', default)()),
    Variable('chargedHadronMultiplicity', lambda jet : getattr(jet, 'chargedHadronMultiplicity', default)()),
    Variable('chargedMultiplicity', lambda jet : getattr(jet, 'chargedMultiplicity', default)()),
    Variable('neutralMultiplicity', lambda jet : getattr(jet, 'neutralMultiplicity', default)()),
]


# gen info
geninfo_vars = [
    Variable('geninfo_mcweight', lambda ev : getattr(ev, 'mcweight', 1.)),
    Variable('geninfo_nup', lambda ev : getattr(ev, 'NUP', -1), type=int),
    Variable('geninfo_htgen', lambda ev : getattr(ev, 'genPartonHT', -1)),
    Variable('geninfo_invmass', lambda ev : getattr(ev, 'geninvmass', -1)),
    Variable('weight_gen'),
    Variable('genmet_pt'),
    # Variable('genmet_eta'),
    # Variable('genmet_e'),
    # Variable('genmet_px'),
    # Variable('genmet_py'),
    Variable('genmet_phi'),
]

vbf_vars = [
    Variable('mjj'),
    Variable('deta'),
    Variable('n_central20', lambda vbf : len(vbf.centralJets), int),
    Variable('n_central', lambda vbf : sum([1 for j in vbf.centralJets if j.pt() > 30.]), int),
    Variable('jdphi', lambda vbf : vbf.dphi),
    Variable('dijetpt'),
    Variable('dijetphi'),
    Variable('dphidijethiggs'),
    Variable('mindetajetvis', lambda vbf : vbf.visjeteta),
]
