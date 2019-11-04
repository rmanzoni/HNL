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
from CMGTools.HNL.analyzers.MultiLeptonWeighter import MultiLeptonWeighter
from CMGTools.HNL.analyzers.EventFilter         import EventFilter
from pdb import set_trace

from CMGTools.HNL.samples.samples_mc_2018 import all_samples, TTJets, TTJets_ext, WJetsToLNu, DYBB, DYJetsToLL_M5to50, DYJetsToLL_M50, DYJetsToLL_M50_ext, WW, WZ, ZZ 

###################################################
###                   OPTIONS                   ###
###################################################
# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally

pick_events = getHeppyOption('pick_events', False)

SF_FILE = '$CMSSW_BASE/src/CMGTools/HNL/data/leptonsf/htt_scalefactors_2018_v1.root'

# Electron corrections, valid for l1 and l2
ELE_SFS = OrderedDict()
ELE_SFS['idiso'] = (SF_FILE, 'e_idiso_desy')
# Add trigger corrections for the prompt lepton l0
ELE_PROMPT_SFS = dc(ELE_SFS)
ELE_PROMPT_SFS['trigger'] = (SF_FILE, 'e_trgEle32orEle35_desy')

# Muon corrections, valid for l1 and l2
MU_SFS = OrderedDict()
MU_SFS['idiso'] = (SF_FILE, 'm_idiso_desy')
# Add trigger corrections for the prompt lepton l0
MU_PROMPT_SFS = dc(MU_SFS)
MU_PROMPT_SFS['trigger'] = (SF_FILE, 'm_trgIsoMu24orIsoMu27_desy')

###################################################
###               HANDLE SAMPLES                ###
###################################################
samples = all_samples

# FIXME! are trigger names and filters correct regardless of the year?
# triggers same for 2018: https://tomc.web.cern.ch/tomc/triggerPrescales/2018//?match=Ele
for sample in samples:

    sample.triggers  = ['HLT_Ele27_WPTight_Gsf_v%d'         %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele32_WPTight_Gsf_v%d'         %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele35_WPTight_Gsf_v%d'         %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele115_CaloIdVT_GsfTrkIdT_v%d' %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_Ele135_CaloIdVT_GsfTrkIdT_v%d' %i for i in range(1, 15)] #electron trigger
    sample.triggers += ['HLT_IsoMu24_v%d' %i for i in range(1, 15)] #muon trigger
    sample.triggers += ['HLT_IsoMu27_v%d' %i for i in range(1, 15)] #muon trigger
    sample.triggers += ['HLT_Mu50_v%d'    %i for i in range(1, 15)] #muon trigger

    sample.splitFactor = splitFactor(sample, 1e6)

    sample.puFileMC   = '$CMSSW_BASE/src/CMGTools/HNL/data/pileup/MC_PileUp_2018_Autumn18.root'
    sample.puFileData = '$CMSSW_BASE/src/CMGTools/HNL/data/pileup/Data_PileUp_2018_69p2.root'

selectedComponents = samples

###################################################
###                  ANALYZERS                  ###
###################################################
toSelect = []

eventSelector = cfg.Analyzer(
    EventSelector,
    name='EventSelector',
    toSelect=toSelect,
)

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

##########################################################################################
# ONE HNL ANALYZER PER FINAL STATE
##########################################################################################

# for each path specify which filters you want the electrons/muons to match to
triggers_and_filters_ele = OrderedDict()
triggers_and_filters_mu  = OrderedDict()

triggers_and_filters_ele['HLT_Ele27_WPTight_Gsf']         = 'hltEle27WPTightGsfTrackIsoFilter'
triggers_and_filters_ele['HLT_Ele32_WPTight_Gsf']         = 'hltEle32WPTightGsfTrackIsoFilter'
triggers_and_filters_ele['HLT_Ele35_WPTight_Gsf']         = 'hltEle35noerWPTightGsfTrackIsoFilter'
triggers_and_filters_ele['HLT_Ele115_CaloIdVT_GsfTrkIdT'] = 'hltEle115CaloIdVTGsfTrkIdTGsfDphiFilter'
triggers_and_filters_ele['HLT_Ele135_CaloIdVT_GsfTrkIdT'] = 'hltEle135CaloIdVTGsfTrkIdTGsfDphiFilter'

triggers_and_filters_mu['HLT_IsoMu24'] = 'hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07'
triggers_and_filters_mu['HLT_IsoMu27'] = 'hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07'
triggers_and_filters_mu['HLT_Mu50']    = 'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q'
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
    
HNLAnalyzer_mmm = cfg.Analyzer(
    HNLAnalyzer,
    name                = 'HNLAnalyzer_mmm',
    promptLepton        = 'm',
    L1L2LeptonType      = 'mm',
    triggersAndFilters  = triggers_and_filters_mu,
    candidate_selection = 'maxpt',
    muon_preselection   = preselect_mu,
    ele_preselection    = preselect_ele,
)

HNLAnalyzer_eee = cfg.Analyzer(
    HNLAnalyzer,
    name                = 'HNLAnalyzer_eee',
    promptLepton        = 'e',
    L1L2LeptonType      = 'ee',
    triggersAndFilters  = triggers_and_filters_ele,
    candidate_selection = 'maxpt',
    muon_preselection   = preselect_mu,
    ele_preselection    = preselect_ele,
)

HNLAnalyzer_eem = cfg.Analyzer(
    HNLAnalyzer,
    name                = 'HNLAnalyzer_eem',
    promptLepton        = 'e',
    L1L2LeptonType      = 'em',
    triggersAndFilters  = triggers_and_filters_ele,
    candidate_selection = 'maxpt',
    muon_preselection   = preselect_mu,
    ele_preselection    = preselect_ele,
)

HNLAnalyzer_mem = cfg.Analyzer(
    HNLAnalyzer,
    name                = 'HNLAnalyzer_mem',
    promptLepton        = 'm',
    L1L2LeptonType      = 'em',
    triggersAndFilters  = triggers_and_filters_mu,
    candidate_selection = 'maxpt',
    muon_preselection   = preselect_mu,
    ele_preselection    = preselect_ele,
)

HNLEventFilter = cfg.Analyzer(
    EventFilter,
    name='EventFilter',
    skimFunction='event.pass_mmm or event.pass_mem or event.pass_eee or event.pass_eem',
)

##########################################################################################
# ONE TREE PRODUCER PER FINAL STATE FIXME! ADD THE EXTENDED PRODUCER
##########################################################################################
skimFunction   = 'event.the_3lep_cand.charge12()==0 and event.the_3lep_cand.mass12()<12 and event.recoSv.disp2DFromBS_cos>0.'

HNLTreeProducerBase_mmm = cfg.Analyzer(
    HNLTreeProducerBase,
    name           = 'HNLTreeProducer_mmm',
    L1L2LeptonType = 'mm',
    promptLepType  = 'm',
    skimFunction   = '(%s)*(%s)' %('event.pass_mmm', skimFunction)
)

HNLTreeProducerBase_mem = cfg.Analyzer(
    HNLTreeProducerBase,
    name           = 'HNLTreeProducer_mem',
    L1L2LeptonType = 'em',
    promptLepType  = 'm',
    skimFunction   = '(%s)*(%s)' %('event.pass_mem', skimFunction)
)

HNLTreeProducerBase_eee = cfg.Analyzer(
    HNLTreeProducerBase,
    name           = 'HNLTreeProducer_eee',
    L1L2LeptonType = 'ee',
    promptLepType  = 'e',
    skimFunction   = '(%s)*(%s)' %('event.pass_eee', skimFunction)
)

HNLTreeProducerBase_eem = cfg.Analyzer(
    HNLTreeProducerBase,
    name           = 'HNLTreeProducer_eem',
    L1L2LeptonType = 'em',
    promptLepType  = 'e',
    skimFunction   = '(%s)*(%s)' %('event.pass_eem', skimFunction)
)

# HNLTreeProducer = cfg.Analyzer(
#     HNLTreeProducer,
#     name='HNLExtendedTreeProducer',
#     L1L2LeptonType=L1L2LeptonType,
#     promptLepType=promptLeptonType,
# )
##########################################################################################


###################################################
###                  LEPTON SF                  ###
###################################################
Weighter_mmm = cfg.Analyzer(
    MultiLeptonWeighter,
    name           = 'LeptonWeighter_mmm',
    finalState     = 'mmm',
    scaleFactor_l0 = MU_PROMPT_SFS,
    scaleFactor_l1 = MU_SFS,
    scaleFactor_l2 = MU_SFS,
    skimFunction   = 'event.pass_mmm',
    getter         = lambda event : event.the_3lep_cand_dict['mmm'],
    disable        = False,
)

Weighter_mem = cfg.Analyzer(
    MultiLeptonWeighter,
    name           = 'LeptonWeighter_mem',
    finalState     = 'mem',
    scaleFactor_l0 = MU_PROMPT_SFS,
    scaleFactor_l1 = ELE_SFS,
    scaleFactor_l2 = MU_SFS,
    skimFunction   = 'event.pass_mem',
    getter         = lambda event : event.the_3lep_cand_dict['mem'],
    disable        = False,
)

Weighter_eee = cfg.Analyzer(
    MultiLeptonWeighter,
    name           = 'LeptonWeighter_eee',
    finalState     = 'eee',
    scaleFactor_l0 = ELE_PROMPT_SFS,
    scaleFactor_l1 = ELE_SFS,
    scaleFactor_l2 = ELE_SFS,
    skimFunction   = 'event.pass_eee',
    getter         = lambda event : event.the_3lep_cand_dict['eee'],
    disable        = False,
)

Weighter_eem = cfg.Analyzer(
    MultiLeptonWeighter,
    name           = 'LeptonWeighter_eem',
    finalState     = 'eem',
    scaleFactor_l0 = ELE_PROMPT_SFS,
    scaleFactor_l1 = ELE_SFS,
    scaleFactor_l2 = MU_SFS,
    skimFunction   = 'event.pass_eem',
    getter         = lambda event : event.the_3lep_cand_dict['eem'],
    disable        = False,
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
    skimAna,
    triggerAna,
    vertexAna,
    pileUpAna,
    genAna,
    HNLGenTreeAnalyzer,
    # RecoGenAnalyzer,
    HNLAnalyzer_mmm,
    HNLAnalyzer_mem,
    HNLAnalyzer_eee,
    HNLAnalyzer_eem,
    HNLEventFilter,
    Weighter_mmm, 
    Weighter_mem, 
    Weighter_eee, 
    Weighter_eem, 
    jetAna,
    metFilter,
    HNLTreeProducerBase_mmm,
    HNLTreeProducerBase_mem,
    HNLTreeProducerBase_eee,
    HNLTreeProducerBase_eem,
])

saveBigTree = False

if saveBigTree:
    sequence.insert(-1, HNLTreeProducer)

isSignal = False

if isSignal:
    sequence.insert(1, signalReweighAna)

if len(toSelect):
    print 'Cherry picking the following events to process:'
    for iev in toSelect:
        print '\t', iev
    sequence.insert(0, eventSelector)

###################################################
###            HNLAnalyzer                      ###
###################################################

# find the indices of all HNLAnalyzer instances and set all but the last to return True
# (don't filter) and just save a flag whether the event is selected or not.
# This is a dirty way of 'emulating' parallel sequences which are not possible in CMGTools, 
# but it's a toad to swallow
for ii in range(len(sequence)):
    if sequence[ii].class_object.__module__ == HNLAnalyzer.__module__:
        sequence[ii].pass_through = True

###################################################
###            PREPROCESSOR                     ###
###################################################

###################################################
# set to True if you want to run interactively on a selected portion of samples/files/whatnot
testing = True 
if testing:
    # run on a single component
    comp = TTJets_ext
        
    # comp.files = comp.files[:1]
    comp.files = ['/tmp/manzoni/001784E5-D649-734B-A5FF-E151DA54CC02.root'] # one file from TTJets_ext on lxplus700
    # comp.fineSplitFactor = 10 # fine splitting, multicore
    samples = [comp]

    selectedComponents = samples
###################################################

# temporary copy remote files using xrd
# event_class = EOSEventsWithDownload if prefetch else Events

# FIXME! for some reason, Events doesn't work anymore in 10_4
prefetch = False
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
