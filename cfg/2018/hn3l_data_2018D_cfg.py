# heppy_batch.py -o data_2018ABC_15may20_v1 hn3l_data_2018ABC_cfg.py -B -b 'run_condor_simple.sh -t 2880 ./batchScript.sh'

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
from CMGTools.HNL.analyzers.FileCleaner         import FileCleaner
from CMGTools.HNL.analyzers.JSONAnalyzer        import JSONAnalyzer
from CMGTools.HNL.analyzers.SkimAnalyzerCount   import SkimAnalyzerCount
from CMGTools.HNL.analyzers.HNLAnalyzer         import HNLAnalyzer
from CMGTools.HNL.analyzers.HNLTreeProducer     import HNLTreeProducer
from CMGTools.HNL.analyzers.HNLTreeProducerBase import HNLTreeProducerBase
from CMGTools.HNL.analyzers.TriggerAnalyzer     import TriggerAnalyzer
from CMGTools.HNL.analyzers.JetAnalyzer         import JetAnalyzer
from CMGTools.HNL.analyzers.METFilter           import METFilter
from CMGTools.HNL.analyzers.EventFilter         import EventFilter
from pdb import set_trace

# import 2018 triggers
from CMGTools.HNL.triggers.triggers_2018 import triggers_ele_data, triggers_mu_data, triggers_and_filters_ele, triggers_and_filters_mu

from CMGTools.HNL.samples.samples_data_2018 import Single_ele_2018D
from CMGTools.HNL.samples.samples_data_2018 import Single_mu_2018D

###################################################
###                   OPTIONS                   ###
###################################################
# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally

pick_events = getHeppyOption('pick_events', False)

###################################################
###               HANDLE SAMPLES                ###
###################################################
samples = [Single_mu_2018D, Single_ele_2018D]
###################################################

# are trigger names and filters correct regardless of the year?
# triggers same for 2018: https://tomc.web.cern.ch/tomc/triggerPrescales/2018//?match=Ele
for sample in samples:
    sample.triggers = triggers_ele_data + triggers_mu_data

    sample.splitFactor = splitFactor(sample, 1e6)

selectedComponents = samples
###################################################
# set to True if you want to run interactively on a selected portion of samples/files/whatnot
testing = False 
if testing:
    # run on a single component
    comp = samples[0]
    
#     lxplus750 /tmp/manzoni/egamma_2018A.root, /tmp/manzoni/singlemu_2018B.root, ttbar_18.root
    comp.files = comp.files[:1]
    comp.files = ['egamma_2018A.root', 'singlemu_2018B.root']
    # comp.files = ['/tmp/manzoni/001784E5-D649-734B-A5FF-E151DA54CC02.root'] # one file from TTJets_ext on lxplus700
    # comp.fineSplitFactor = 10 # fine splitting, multicore
    samples = [comp]

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

##########################################################################################
# ONE HNL ANALYZER PER FINAL STATE
##########################################################################################

# Here we define the baseline selection for muons and electrons.
# These are the minimal requirements that leptons need to satisfy to be considered
# in building HNL candidates and be saved in the ntuples 
def preselect_mu(imu):
    if imu.pt() < 5.             : return False 
    if abs(imu.eta()) > 2.4      : return False
    if imu.relIsoFromEA(0.3) > 10: return False
    if not (imu.muonID('POG_ID_Medium')>0.5 or \
            imu.Medium() == 1): return False
    return True

def preselect_ele(iele):
    if iele.pt() < 5.             : return False 
    if abs(iele.eta()) > 2.5      : return False
    if iele.relIsoFromEA(0.3) > 10: return False
    if not (iele.LooseNoIsoID or \
            iele.electronID('mvaEleID-Fall17-noIso-V2-wp90'.replace('-','_')) or \
            iele.electronID('mvaEleID-Fall17-iso-V2-wp90'.replace('-','_')) ): return False
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
skimFilter = 'the_3lep_cand.charge12()==0 and the_3lep_cand.mass12()<20 and recoSv.disp2DFromBS_cos>0.'

HNLTreeProducerBase_mmm = cfg.Analyzer(
    HNLTreeProducerBase,
    name             = 'HNLTreeProducer_mmm',
    promptLepType    = 'm',
    L1L2LeptonType   = 'mm',
    finalStateFilter = 'event.pass_mmm',
    skimFilter       = skimFilter,
)

HNLTreeProducerBase_mem = cfg.Analyzer(
    HNLTreeProducerBase,
    name             = 'HNLTreeProducer_mem',
    promptLepType    = 'm',
    L1L2LeptonType   = 'em',
    finalStateFilter = 'event.pass_mem',
    skimFilter       = skimFilter,
)

HNLTreeProducerBase_eee = cfg.Analyzer(
    HNLTreeProducerBase,
    name             = 'HNLTreeProducer_eee',
    promptLepType    = 'e',
    L1L2LeptonType   = 'ee',
    finalStateFilter = 'event.pass_eee',
    skimFilter       = skimFilter,
)

HNLTreeProducerBase_eem = cfg.Analyzer(
    HNLTreeProducerBase,
    name             = 'HNLTreeProducer_eem',
    promptLepType    = 'e',
    L1L2LeptonType   = 'em',
    finalStateFilter = 'event.pass_eem',
    skimFilter       = skimFilter,
)

# HNLTreeProducer = cfg.Analyzer(
#     HNLTreeProducer,
#     name='HNLExtendedTreeProducer',
#     L1L2LeptonType=L1L2LeptonType,
#     promptLepType=promptLeptonType,
# )
##########################################################################################

# see SM HTT TWiki
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SMTauTau2016#Jet_Energy_Corrections
jetAna = cfg.Analyzer(
    JetAnalyzer,
    name              = 'JetAnalyzer',
#     jetCol            = 'slimmedJets',
    jetCol            = 'selectedUpdatedPatJetsNewDFTraining', # updated JEC and DeepJet
    jetPt             = 20.,
    jetEta            = 5.,
    relaxJetId        = False, # relax = do not apply jet ID
    relaxPuJetId      = True, # relax = do not apply pileup jet ID
    jerCorr           = False,
    puJetIDDisc       = 'pileupJetId:fullDiscriminant',
    recalibrateJets   = False,
    applyL2L3Residual = 'MC',
    year              = 2018,
    btag_wp           = 'medium', # DeepFlavour
    mc_eff_file       = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/btag/eff/btag_deepflavour_wp_medium_efficiencies_2018.root',
    sf_file           = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/btag/sf/2018/DeepJet_102XSF_WP_V1.csv',
#    mcGT              = '94X_mc2017_realistic_v14',
#    dataGT            = '94X_dataRun2_v6',
#    jesCorr = 1., # Shift jet energy scale in terms of uncertainties (1 = +1 sigma)
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = cfg.Sequence([
    jsonAna,
    # skimAna,
    triggerAna,
    vertexAna,
    HNLAnalyzer_mmm,
    HNLAnalyzer_mem,
    HNLAnalyzer_eee,
    HNLAnalyzer_eem,
    HNLEventFilter,
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
prefetch = True
recompute_deepjet = True
if recompute_deepjet:
    fname = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/prod/update_deepjet_and_ele_id_data2018D_cfg.py'
    preprocessor = CmsswPreprocessor(fname, prefetch=prefetch, addOrigAsSecondary=False)
    EOSEventsWithDownload.aggressive = 2 # always fetch if running on Wigner
    EOSEventsWithDownload.long_cache = getHeppyOption('long_cache', False)
    prefetch = False
    sequence.append(fileCleaner)
else:
    preprocessor = None

# temporarily copy remote files using xrd
# event_class = EOSEventsWithDownload if prefetch else Events
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
    preprocessor = preprocessor,
    events_class = event_class
)

printComps(config.components, True)
