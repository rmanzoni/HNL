def generateKeyConfigs(samples, 
                       promptLeptonType, 
                       L1L2LeptonType, 
                       isData, 
                       isSignal, 
                       prefetch=False, 
                       year=2018,
                       toSelect=[],
                       saveBigTree=True,):
    import os
    from copy import deepcopy as dc
    from collections import OrderedDict
    import PhysicsTools.HeppyCore.framework.config as cfg
    from PhysicsTools.HeppyCore.framework.config import printComps
    from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
    from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
    from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

    from CMGTools.HNL.utils.EOSEventsWithDownload import EOSEventsWithDownload
    from CMGTools.RootTools.utils.splitFactor import splitFactor

    # import Heppy analyzers:
    from PhysicsTools.Heppy.analyzers.core.EventSelector     import EventSelector
    from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
    from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer  import GeneratorAnalyzer
#     from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer  import LHEWeightAnalyzer

    # import HNL analyzers:
    from CMGTools.HNL.analyzers.PileUpAnalyzer      import PileUpAnalyzer
    from CMGTools.HNL.analyzers.JSONAnalyzer        import JSONAnalyzer
    from CMGTools.HNL.analyzers.SkimAnalyzerCount   import SkimAnalyzerCount
    from CMGTools.HNL.analyzers.HNLAnalyzer         import HNLAnalyzer
    from CMGTools.HNL.analyzers.HNLTreeProducer     import HNLTreeProducer
    from CMGTools.HNL.analyzers.HNLTreeProducerBase import HNLTreeProducerBase
    from CMGTools.HNL.analyzers.HNLGenTreeAnalyzer  import HNLGenTreeAnalyzer
    from CMGTools.HNL.analyzers.HNLSignalReweighter import HNLSignalReweighter
    from CMGTools.HNL.analyzers.RecoGenAnalyzer     import RecoGenAnalyzer
    from CMGTools.HNL.analyzers.TriggerAnalyzer     import TriggerAnalyzer
    from CMGTools.HNL.analyzers.JetAnalyzer         import JetAnalyzer
    from CMGTools.HNL.analyzers.METFilter           import METFilter
    from CMGTools.HNL.analyzers.LeptonWeighter      import LeptonWeighter
    from pdb import set_trace


    ###################################################
    ###                   OPTIONS                   ###
    ###################################################
    # Get all heppy options; set via "-o production" or "-o production=True"
    # production = True run on batch, production = False (or unset) run locally

    pick_events = getHeppyOption('pick_events', False)

    if year == 2017: 
        SF_FILE = 'htt_scalefactors_v17_1.root'

        # Electron corrections, valid for l1 and l2
        ELE_SFS = OrderedDict()
        ELE_SFS['idiso'   ] = ('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/'+SF_FILE, 'e_id')
        ELE_SFS['tracking'] = ('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/'+SF_FILE, 'e_iso')
        # Add trigger corrections for the prompt lepton l0
        ELE_PROMPT_SFS = ELE_SFS
        ELE_PROMPT_SFS['trigger' ] = ('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/'+SF_FILE, 'e_trg_SingleEle_Ele32OREle35_desy')

        # Muon corrections, valid for l1 and l2
        MU_SFS = OrderedDict()
        MU_SFS['idiso'   ] = ('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/'+SF_FILE, 'm_id')
        MU_SFS['tracking'] = ('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/'+SF_FILE, 'm_iso')
        # Add trigger corrections for the prompt lepton l0
        MU_PROMPT_SFS = MU_SFS
        MU_PROMPT_SFS['trigger' ] = ('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/'+SF_FILE, 'm_trg_SingleMu_Mu24ORMu27_desy')

    if year == 2018: 
        SF_FILE = 'htt_scalefactors_2018_v1.root'

        # Electron corrections, valid for l1 and l2
        ELE_SFS = OrderedDict()
        ELE_SFS['idiso'] = ('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/'+SF_FILE, 'e_idiso_desy')
        # Add trigger corrections for the prompt lepton l0
        ELE_PROMPT_SFS = dc(ELE_SFS)
        ELE_PROMPT_SFS['trigger'] = ('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/'+SF_FILE, 'e_trgEle32orEle35_desy')

        # Muon corrections, valid for l1 and l2
        MU_SFS = OrderedDict()
        MU_SFS['idiso'] = ('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_2018_v1.root', 'm_idiso_desy')
        # Add trigger corrections for the prompt lepton l0
        MU_PROMPT_SFS = dc(MU_SFS)
        MU_PROMPT_SFS['trigger'] = ('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_2018_v1.root', 'm_trgIsoMu24orIsoMu27_desy')

    ###################################################
    ###               HANDLE SAMPLES                ###
    ###################################################

    # FIXME! are trigger names and filters correct regardless of the year?
    if promptLeptonType == 'e':
        for sample in samples:
            sample.triggers  = ['HLT_Ele27_WPTight_Gsf_v%d'          %i for i in range(1, 15)] #electron trigger
            sample.triggers += ['HLT_Ele32_WPTight_Gsf_v%d'          %i for i in range(1, 15)] #electron trigger
            sample.triggers += ['HLT_Ele35_WPTight_Gsf_v%d'          %i for i in range(1, 15)] #electron trigger
            sample.triggers += ['HLT_Ele115_CaloIdVT_GsfTrkIdT_v%d'  %i for i in range(1, 15)] #electron trigger
            sample.triggers += ['HLT_Ele135_CaloIdVT_GsfTrkIdT_v%d'  %i for i in range(1, 15)] #electron trigger
            sample.splitFactor = splitFactor(sample, 1e6)
    # triggers same for 2018: https://tomc.web.cern.ch/tomc/triggerPrescales/2018//?match=Ele
    if promptLeptonType == 'm':
        for sample in samples:
            sample.triggers  = ['HLT_IsoMu24_v%d' %i for i in range(1, 15)] #muon trigger
            sample.triggers += ['HLT_IsoMu27_v%d' %i for i in range(1, 15)] #muon trigger
            sample.triggers += ['HLT_Mu50_v%d'    %i for i in range(1, 15)] #muon trigger
            sample.splitFactor = splitFactor(sample, 1e6)
    # triggers same for 2018: https://tomc.web.cern.ch/tomc/triggerPrescales/2018//?match=Ele

    selectedComponents = samples

    ###################################################
    ###                  ANALYZERS                  ###
    ###################################################
    eventSelector = cfg.Analyzer(
        EventSelector,
        name='EventSelector',
        toSelect=toSelect,
    )

#     lheWeightAna = cfg.Analyzer(
#         LHEWeightAnalyzer, name="LHEWeightAnalyzer",
#         useLumiInfo=False
#     )

    jsonAna = cfg.Analyzer(
        JSONAnalyzer,
        name='JSONAnalyzer',
    )

    skimAna = cfg.Analyzer(
        SkimAnalyzerCount,
        name='SkimAnalyzerCount'
    )

    signalReweighAna = cfg.Analyzer(
        HNLSignalReweighter,
        name='HNLSignalReweighter'
    )

    triggerAna = cfg.Analyzer(
        TriggerAnalyzer,
        name='TriggerAnalyzer',
        addTriggerObjects=True,
        requireTrigger=True,
        usePrescaled=False,
        unpackLabels=True,
    )

    vertexAna = cfg.Analyzer(
        VertexAnalyzer,
        name='VertexAnalyzer',
        fixedWeight=1,
        keepFailingEvents=False,
        verbose=False
    )

    pileUpAna = cfg.Analyzer(
        PileUpAnalyzer,
        name='PileUpAnalyzer',
        true=True
    )

    metFilter = cfg.Analyzer(
        METFilter,
        name='METFilter',
        processName='PAT', #mschoene: Filters very much do exist in MC and most of them should be applied to MC as well, but not all!
        fallbackProcessName = 'RECO',
        triggers=[
            'Flag_goodVertices',
            'Flag_globalSuperTightHalo2016Filter',
            'Flag_HBHENoiseFilter',
            'Flag_HBHENoiseIsoFilter',
            'Flag_EcalDeadCellTriggerPrimitiveFilter',
            'Flag_BadPFMuonFilter',
            'Flag_BadChargedCandidateFilter',
            'Flag_eeBadScFilter',
            'Flag_ecalBadCalibFilter',
        ]
    )

    HNLTreeProducer = cfg.Analyzer(
        HNLTreeProducer,
        name='HNLExtendedTreeProducer',
        L1L2LeptonType=L1L2LeptonType,
        promptLepType=promptLeptonType,
    )

    HNLTreeProducerBase = cfg.Analyzer(
        HNLTreeProducerBase,
        name='HNLTreeProducer',
        L1L2LeptonType=L1L2LeptonType,
        promptLepType=promptLeptonType,
        skimFunction='event.the_3lep_cand.charge12()==0 and event.the_3lep_cand.mass12()<12 and event.recoSv.disp2DFromBS_cos>0.'
    )

    HNLGenTreeAnalyzer = cfg.Analyzer(
        HNLGenTreeAnalyzer,
        name='HNLGenTreeAnalyzer',
    )

    RecoGenAnalyzer = cfg.Analyzer(
        RecoGenAnalyzer,
        name='RecoGenAnalyzer',
    )

    genAna = GeneratorAnalyzer.defaultConfig
    genAna.allGenTaus = True # save in event.gentaus *ALL* taus, regardless whether hadronic / leptonic decay

    # for each path specify which filters you want the electrons/muons to match to
    triggers_and_filters = OrderedDict()

    if promptLeptonType == 'e':
        triggers_and_filters['HLT_Ele27_WPTight_Gsf']         = 'hltEle27WPTightGsfTrackIsoFilter'
        triggers_and_filters['HLT_Ele32_WPTight_Gsf']         = 'hltEle32WPTightGsfTrackIsoFilter'
        triggers_and_filters['HLT_Ele35_WPTight_Gsf']         = 'hltEle35noerWPTightGsfTrackIsoFilter'
        triggers_and_filters['HLT_Ele115_CaloIdVT_GsfTrkIdT'] = 'hltEle115CaloIdVTGsfTrkIdTGsfDphiFilter'
        triggers_and_filters['HLT_Ele135_CaloIdVT_GsfTrkIdT'] = 'hltEle135CaloIdVTGsfTrkIdTGsfDphiFilter'

    if promptLeptonType == 'm':
        triggers_and_filters['HLT_IsoMu24'] = 'hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07'
        triggers_and_filters['HLT_IsoMu27'] = 'hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07'
        triggers_and_filters['HLT_Mu50']    = 'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q'
    # TODO: add (HLT_IsoTkMu24_v*) and (HLT_TkMu50_v*); but only later for 2016 dataset

    # Here we define the baseline selection for muons and electrons.
    # These are the minimal requirements that leptons need to satisfy to be considered
    # in building HNL candidates and be saved in the ntuples 
    def preselect_mu(imu):
        if imu.pt() < 5.             : return False 
        if abs(imu.eta()) > 2.4      : return False
        if imu.relIsoFromEA(0.3) > 10: return False
        if not (imu.isSoftMuon(imu.associatedVertex) or \
                imu.muonID('POG_ID_Loose')           or \
                imu.Medium == 1): return False
        return True

    def preselect_ele(iele):
        if iele.pt() < 5.             : return False 
        if abs(iele.eta()) > 2.5      : return False
        if iele.relIsoFromEA(0.3) > 10: return False
        if not (iele.LooseNoIsoID or \
                iele.electronID("MVA_ID_nonIso_Fall17_Loose")): return False
        return True
        
    HNLAnalyzer = cfg.Analyzer(
        HNLAnalyzer,
        name='HNLAnalyzer',
        promptLepton=promptLeptonType,
        L1L2LeptonType=L1L2LeptonType,
        triggersAndFilters=triggers_and_filters,
        candidate_selection='maxpt',
        muon_preselection=preselect_mu,
        ele_preselection=preselect_ele,
    )

    if promptLeptonType == 'e':
        Weighter_l0 = cfg.Analyzer(
            LeptonWeighter,
            name='LeptonWeighter_l0',
            scaleFactorFiles=ELE_PROMPT_SFS,
            dataEffFiles={},
            getter=lambda event : event.the_3lep_cand.l0(),
            disable=False
        )

    if promptLeptonType == 'm':
        Weighter_l0 = cfg.Analyzer(
            LeptonWeighter,
            name='LeptonWeighter_l0',
            scaleFactorFiles=MU_PROMPT_SFS,
            dataEffFiles={},
            getter=lambda event : event.the_3lep_cand.l0(),
            disable=False
        )

    if L1L2LeptonType == 'mm':
        Weighter_l1 = cfg.Analyzer(
            LeptonWeighter,
            name='LeptonWeighter_l1',
            scaleFactorFiles=MU_SFS,
            dataEffFiles={},
            getter=lambda event : event.the_3lep_cand.l1(),
            disable=False,
        )
        Weighter_l2 = cfg.Analyzer(
            LeptonWeighter,
            name='LeptonWeighter_l2',
            scaleFactorFiles=MU_SFS,
            dataEffFiles={},
            getter=lambda event : event.the_3lep_cand.l2(),
            disable=False,
        )

    if L1L2LeptonType == 'em':
        Weighter_l1 = cfg.Analyzer(
            LeptonWeighter,
            name='LeptonWeighter_l1',
            scaleFactorFiles=ELE_SFS,
            dataEffFiles={},
            getter=lambda event : event.the_3lep_cand.l1(),
            disable=False,
        )
        Weighter_l2 = cfg.Analyzer(
            LeptonWeighter,
            name='LeptonWeighter_l2',
            scaleFactorFiles=MU_SFS,
            dataEffFiles={},
            getter=lambda event : event.the_3lep_cand.l2(),
            disable=False
        )

    if L1L2LeptonType == 'ee':
        Weighter_l1 = cfg.Analyzer(
            LeptonWeighter,
            name='LeptonWeighter_l1',
            scaleFactorFiles=ELE_SFS,
            dataEffFiles={},
            getter=lambda event : event.the_3lep_cand.l1(),
            disable=False
        )
        Weighter_l2 = cfg.Analyzer(
            LeptonWeighter,
            name='LeptonWeighter_l2',
            scaleFactorFiles=ELE_SFS,
            dataEffFiles={},
            getter=lambda event : event.the_3lep_cand.l2(),
            disable=False
        )

    # see SM HTT TWiki
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SMTauTau2016#Jet_Energy_Corrections
    jetAna = cfg.Analyzer(
        JetAnalyzer,
        name              = 'JetAnalyzer',
        jetCol            = 'slimmedJets',
        jetPt             = 20.,
        jetEta            = 5.,
        relaxJetId        = False, # relax = do not apply jet ID
        relaxPuJetId      = True, # relax = do not apply pileup jet ID
        jerCorr           = False,
        puJetIDDisc       = 'pileupJetId:fullDiscriminant',
        recalibrateJets   = False,
        applyL2L3Residual = 'MC',
        # RM: FIXME! check the GTs
    #    mcGT              = '94X_mc2017_realistic_v14',
    #    dataGT            = '94X_dataRun2_v6',
        #jesCorr = 1., # Shift jet energy scale in terms of uncertainties (1 = +1 sigma)
    )
    ###################################################
    ###                  SEQUENCE                   ###
    ###################################################
    if isData == True:
        sequence = cfg.Sequence([
            jsonAna,
            # skimAna,
            triggerAna,
            vertexAna,
            # pileUpAna,
            HNLAnalyzer,
            jetAna,
            metFilter,
            HNLTreeProducerBase,
        ])

    if isData == False:
        if isSignal == True:
            sequence = cfg.Sequence([
#                 lheWeightAna, # les houches
                #jsonAna,
                skimAna,
                signalReweighAna,
                triggerAna,
                vertexAna,
                pileUpAna,
                genAna,
                HNLGenTreeAnalyzer,
                # RecoGenAnalyzer,
                HNLAnalyzer,
                Weighter_l0, 
                Weighter_l1, 
                Weighter_l2, 
                jetAna,
                metFilter,
                HNLTreeProducerBase,
            ])
        if isSignal == False:
            sequence = cfg.Sequence([
#                 lheWeightAna, # les houches
                #jsonAna,
                skimAna,
                triggerAna,
                vertexAna,
                pileUpAna,
                genAna,
                HNLGenTreeAnalyzer,
                HNLAnalyzer,
                Weighter_l0, 
                Weighter_l1, 
                Weighter_l2, 
                jetAna,
                metFilter,
                HNLTreeProducerBase,
            ])
    
    if saveBigTree:
        sequence.insert(-1, HNLTreeProducer)
    
    if len(toSelect):
        print 'Cherry picking the following events to process:'
        for iev in toSelect:
            print '\t', iev
        sequence.insert(0, eventSelector)
    
    ###################################################
    ###            PREPROCESSOR                     ###
    ###################################################

    # temporary copy remote files using xrd
#     event_class = EOSEventsWithDownload if prefetch else Events
    
    # FIXME! for some reason, Events doesn't work anymore in 10_4
    event_class = EOSEventsWithDownload  
    if prefetch:
        EOSEventsWithDownload.aggressive = 2 # always fetch if running on Wigner
        EOSEventsWithDownload.long_cache = getHeppyOption('long_cache', False)
    
    # the following is declared in case this cfg is used in input to the heppy.py script
    # from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
    config = cfg.Config(
        components   = selectedComponents,
        sequence     = sequence,
        services     = [],
        preprocessor = None,
        events_class = event_class
    )
    
    printComps(config.components, True)

    return config
