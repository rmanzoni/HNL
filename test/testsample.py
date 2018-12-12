import ROOT
from DataFormats.FWLite import Events,Handle
from pdb import set_trace

genp_label  = "prunedGenParticles"
genp_handle = Handle("vector<reco::GenParticle>")

# events = Events('/afs/cern.ch/work/d/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/test/HN3L_M_2_V_0p00836660026534_e.root')
# events = Events(' root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_1.root') 
HN3L_M_2_V_0p00836660026534_e_massiveAndCKM_LO_files = [
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_1.root' ,
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_10.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_100.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_11.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_12.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_13.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_14.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_15.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_16.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_17.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_18.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_19.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_2.root' ,
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_20.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_21.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_22.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_23.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_24.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_25.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_26.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_27.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_28.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_29.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_3.root' ,
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_30.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_31.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_32.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_33.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_34.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_35.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_36.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_37.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_38.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_39.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_4.root' ,
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_40.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_41.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_42.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_43.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_44.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_45.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_46.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_47.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_48.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_49.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_5.root' ,
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_50.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_51.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_52.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_53.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_54.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_55.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_56.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_57.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_58.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_59.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_6.root' ,
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_60.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_61.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_62.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_63.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_64.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_65.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_66.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_67.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_68.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_69.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_7.root' ,
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_70.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_71.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_72.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_73.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_74.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_75.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_76.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_77.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_78.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_79.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_8.root' ,
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_80.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_81.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_82.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_83.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_84.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_85.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_86.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_87.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_88.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_89.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_9.root' ,
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_90.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_91.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_92.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_93.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_94.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_95.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_96.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_97.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_98.root',
    'root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_e_massiveAndCKM_LO/heavyNeutrino_99.root',
]

# events = Events(' root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_tau_massiveAndCKM_LO/heavyNeutrino_1.root') 
# files = [' root://cms-xrd-global.cern.ch//store/user/tomc/heavyNeutrinoMiniAOD/Moriond17_aug2018/displaced/HeavyNeutrino_trilepton_M-2_V-0.00836660026534_tau_massiveAndCKM_LO/heavyNeutrino_1.root'] 

files = ['/afs/cern.ch/work/d/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/test/testfile.root']

# files = HN3L_M_2_V_0p00836660026534_e_massiveAndCKM_LO_files
# files = [events]

nPromptTaus = 0
for file in files:
    print 'scanning %s'%(file)
    events = Events(file) 

    for i,event in enumerate(events):
        # if (event.eventAuxiliary().event()==80) or (event.eventAuxiliary().event()==87):
        event.getByLabel(genp_label,genp_handle)
        genp = genp_handle.product()

        for gg in genp:
            if abs(gg.pdgId())==15 and gg.isPromptDecayed():
                # set_trace()
                print 'found a prompt decayed tau!!! eventId: %d\tpdgId: %d\tpt: %.1f\tphi: %.1f\teta: %.1f\tnumberOfDaugters: %d' %(event.eventAuxiliary().event(),gg.pdgId(), gg.pt(), gg.eta(), gg.phi(), gg.numberOfDaughters())
                nPromptTaus += 1

print 'Scanning finished... found in total %d taus with .isPromptDecayed() = True'%(nPromptTaus)
