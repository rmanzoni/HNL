import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

HN_3L_M10V_0p01_M = creator.makeMCComponentFromLocal('HN_3L_M10V_0p01_M', 'XXX', path=os.environ['CMSSW_BASE']+'/src/HNL/HNL/python/samples', pattern='.*dummy')

HN_3L_M10V_0p01_M.files = [
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_1.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_10.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_100.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_101.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_102.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_103.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_104.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_105.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_106.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_107.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_108.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_109.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_11.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_110.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_111.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_112.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_113.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_114.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_115.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_116.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_117.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_118.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17/displaced/HeavyNeutrino_trilepton_M-3_V-0.01_mu_onshell_pre2017_NLO/heavyNeutrino_119.root',
]
