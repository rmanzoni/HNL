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
from CMGTools.HNL.analyzers.LeptonWeighter     import LeptonWeighter

# import samples, signal
# from CMGTools.HNL.samples.localsignal import TTJets_amcat as ttbar
# from CMGTools.HNL.samples.samples_mc_2017 import DYJetsToLL_M50, hnl_bkg_essentials
# from CMGTools.HNL.samples.signal import all_signals_mu
from CMGTools.HNL.samples.samples_mc_2017_noskim import DYJetsToLL_M5to50


###################################################
###                   OPTIONS                   ###
###################################################
# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally

production         = getHeppyOption('production' , True)
# production         = getHeppyOption('production' , False)
pick_events        = getHeppyOption('pick_events', False)

###################################################
###               HANDLE SAMPLES                ###
###################################################
# samples = hnl_bkg_essentials
samples = [DYJetsToLL_M5to50]
auxsamples = []#[ttbar, DYJetsToLL_M50]

# samples = [comp for comp in samples if comp.name=='TTJets_amcat']

for sample in samples+auxsamples:
    sample.triggers  = ['HLT_IsoMu24_v%d'%i for i in range(1, 15)] #muon trigger
    sample.triggers += ['HLT_IsoMu27_v%d'%i for i in range(1, 15)] #muon trigger
    sample.triggers += ['HLT_Mu50_v%d'   %i for i in range(1, 15)] #muon trigger

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

genAna = GeneratorAnalyzer.defaultConfig
genAna.allGenTaus = True # save in event.gentaus *ALL* taus, regardless whether hadronic / leptonic decay

# for each path specify which filters you want the muons to match to
triggers_and_filters = OrderedDict()
triggers_and_filters['HLT_IsoMu24'] = 'hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07'
#hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09' #2016
triggers_and_filters['HLT_IsoMu27'] = 'hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07'
triggers_and_filters['HLT_Mu50']    = 'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q'

HNLAnalyzer = cfg.Analyzer(
    HNLAnalyzer,
    name='HNLAnalyzer',
    promptLepton='mu',
    triggersAndFilters=triggers_and_filters,
    candidate_selection='maxpt',
)

muonWeighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_prompt_mu',
    scaleFactorFiles={
        'trigger' :('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_v17_1.root', 'm_trg_SingleMu_Mu24ORMu27_desy'),
        'idiso'   :('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_v17_1.root', 'm_id'),
        'tracking':('$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_v17_1.root', 'm_iso'),
    },
    dataEffFiles={
        # 'trigger':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_2.root', 'm_trgIsoMu22orTkIsoMu22_desy'),
    },
    getter = lambda event : event.the_3lep_cand.l0(),
    disable=False
)

HNLTreeProducer = cfg.Analyzer(
    HNLTreeProducer,
    name='HNLTreeProducer',
    promptLepType='mu',
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
    muonWeighter,
    jetAna,
    HNLTreeProducer,
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
#     comp                 = ttbar
    comp                 = DYJetsToLL_M5to50
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

