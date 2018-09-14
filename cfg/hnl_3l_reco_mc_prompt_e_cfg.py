import os
from collections import OrderedDict
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config     import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
from CMGTools.RootTools.utils.splitFactor import splitFactor

# import Heppy analyzers:
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer      import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount
from PhysicsTools.Heppy.analyzers.core.EventSelector     import EventSelector
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer    import PileUpAnalyzer
from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer  import GeneratorAnalyzer
from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer  import LHEWeightAnalyzer

from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer   import TriggerAnalyzer

# import HNL analyzers:
from CMGTools.HNL.analyzers.HNLAnalyzer        import HNLAnalyzer
from CMGTools.HNL.analyzers.HNLTreeProducer    import HNLTreeProducer
from CMGTools.HNL.analyzers.HNLGenTreeAnalyzer import HNLGenTreeAnalyzer
from CMGTools.HNL.analyzers.TriggerAnalyzer    import TriggerAnalyzer
from CMGTools.HNL.analyzers.JetAnalyzer        import JetAnalyzer
from CMGTools.HNL.analyzers.METFilter          import METFilter
from CMGTools.HNL.analyzers.LeptonWeighter     import LeptonWeighter

# import samples, signal
# from CMGTools.HNL.samples.localsignal import HN3L_M_2p5_V_0p0173205080757_e_onshell, HN3L_M_2p5_V_0p00707106781187_e_onshell
# from CMGTools.HNL.samples.localsignal import TTJets_amcat as ttbar
# from CMGTools.HNL.samples.samples_mc_2017 import DYJetsToLL_M50, hnl_bkg_essentials
# from CMGTools.HNL.samples.samples_mc_2017_noskim import DYJetsToLL_M5to50
from CMGTools.HNL.samples.samples_mc_2017_noskim import DYJetsToLL_M50
from CMGTools.HNL.samples.signal import signals_e
from CMGTools.HNL.samples.samples_mc_2017_noskim import qcd, W1JetsToLNu, W2JetsToLNu

###################################################
###                   OPTIONS                   ###
###################################################
# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally

production         = getHeppyOption('production' , False)
# production         = getHeppyOption('production' , False)
pick_events        = getHeppyOption('pick_events', False)

###################################################
###               HANDLE SAMPLES                ###
###################################################
#samples = hnl_bkg_essentials
#samples = [DYJetsToLL_M50]
#samples = qcd+[W1JetsToLNu,W2JetsToLNu]
samples = signals_e
auxsamples = [] #[ttbar, DYJetsToLL_M50]

#samples = [comp for comp in samples if comp.name=='TTJets_amcat']

for sample in samples+auxsamples:
    sample.triggers  = ['HLT_Ele27_WPTight_Gsf_v%d'          %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele32_WPTight_Gsf_v%d'          %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele35_WPTight_Gsf_v%d'          %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele115_CaloIdVT_GsfTrkIdT_v%d'  %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele135_CaloIdVT_GsfTrkIdT_v%d'  %i for i in range(1, 15)] #electron trigger

    sample.splitFactor = splitFactor(sample, 1e5)

selectedComponents = samples

###################################################
###                  ANALYSERS                  ###
###################################################
eventSelector = cfg.Analyzer(
    EventSelector,
    name='EventSelector',
    toSelect=[326]
)

lheWeightAna = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
    useLumiInfo=False
)

jsonAna = cfg.Analyzer(
    JSONAnalyzer,
    name='JSONAnalyzer',
)

skimAna = cfg.Analyzer(
    SkimAnalyzerCount,
    name='SkimAnalyzerCount'
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
    processName='RECO',
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

genAna = GeneratorAnalyzer.defaultConfig
genAna.allGenTaus = True # save in event.gentaus *ALL* taus, regardless whether hadronic / leptonic decay

# for each path specify which filters you want the muons to match to
triggers_and_filters = OrderedDict()
triggers_and_filters['HLT_Ele27_WPTight_Gsf']         = 'hltEle27WPTightGsfTrackIsoFilter'
triggers_and_filters['HLT_Ele32_WPTight_Gsf']         = 'hltEle32WPTightGsfTrackIsoFilter'
triggers_and_filters['HLT_Ele35_WPTight_Gsf']         = 'hltEle35noerWPTightGsfTrackIsoFilter'
triggers_and_filters['HLT_Ele115_CaloIdVT_GsfTrkIdT'] = 'hltEle115CaloIdVTGsfTrkIdTGsfDphiFilter'
triggers_and_filters['HLT_Ele135_CaloIdVT_GsfTrkIdT'] = 'hltEle135CaloIdVTGsfTrkIdTGsfDphiFilter'

HNLAnalyzer = cfg.Analyzer(
    HNLAnalyzer,
    name='HNLAnalyzer',
    promptLepton='ele',
    triggersAndFilters=triggers_and_filters,
    candidate_selection='maxpt',
)

eleWeighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_prompt_ele',
    scaleFactorFiles={
        'trigger' :('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_v17_1.root', 'e_trg_SingleEle_Ele32OREle35_desy'),
        'idiso'   :('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_v17_1.root', 'e_id'),
        'tracking':('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_v17_1.root', 'e_iso'),
    },
    dataEffFiles={
        # 'trigger':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_2.root', 'm_trgIsoMu22orTkIsoMu22_desy'),
    },
    getter = lambda event : event.the_3lep_cand.l0(),
    disable=False
)

muonWeighterl1 = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_disp_mu_1',
    scaleFactorFiles={
        'idiso'   :('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_v17_1.root', 'm_id'),
        'tracking':('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_v17_1.root', 'm_iso'),
    },
    dataEffFiles={
        # 'trigger':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_2.root', 'm_trgIsoMu22orTkIsoMu22_desy'),
    },
    getter = lambda event : event.the_3lep_cand.l1(),
    disable=True
)

muonWeighterl2 = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_disp_mu_2',
    scaleFactorFiles={
        'idiso'   :('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_v17_1.root', 'm_id'),
        'tracking':('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_v17_1.root', 'm_iso'),
    },
    dataEffFiles={
        # 'trigger':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_2.root', 'm_trgIsoMu22orTkIsoMu22_desy'),
    },
    getter = lambda event : event.the_3lep_cand.l2(),
    disable=True
)

HNLTreeProducer = cfg.Analyzer(
    HNLTreeProducer,
    name='HNLTreeProducer',
    promptLepType='ele',
)

HNLGenTreeAnalyzer = cfg.Analyzer(
    HNLGenTreeAnalyzer,
    name='HNLGenTreeAnalyzer',
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
sequence = cfg.Sequence([
#     eventSelector,
    lheWeightAna, # les houches
    jsonAna,
#    skimAna,
    triggerAna,
    vertexAna,
    pileUpAna,
    genAna,
    HNLGenTreeAnalyzer,
    HNLAnalyzer,
    eleWeighter,
    muonWeighterl1,
    muonWeighterl2,
    jetAna,
    metFilter,
    HNLTreeProducer,
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
#     comp                 = HN3L_M_2p5_V_0p0173205080757_e_onshell
#    comp                 = HN3L_M_2p5_V_0p00707106781187_e_onshell
    comp                 = signals_e[0]
#     comp                 = ttbar
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
    comp.files           = comp.files[:50]

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(
    components   = selectedComponents,
    sequence     = sequence,
    services     = [],
    preprocessor = None,
    events_class = Events
)

printComps(config.components, True)

