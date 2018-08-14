import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

# FIXME! put the right cross sections
# FIXME! check in ComponentCreator how to cache the file fetching
# FIXME! create meaningful lists

TTJets_amcat                    = creator.makeMyPrivateMCComponent('TTJets_amcat'                  , '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/vstampf-HNLSKIM2017_TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                                         , 'PRIVATE', '*.root', 'phys03', xSec=831.76, useAAA=True)
TTJets_amcat        .nGenEvents = 153432257 
#.sigma = 831.76 pb; .nevents = 39769534

TTJets_mdgrph                   = creator.makeMyPrivateMCComponent('TTJets_madgraph'               , '/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/vstampf-HNLSKIM2017_TTJets_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                                           , 'PRIVATE', '*.root', 'phys03', xSec=831.76, useAAA=True)
TTJets_mdgrph       .nGenEvents = 615134
#.sigma = NOT FOUND pb; .nevents = 158461 
              
DYJetsToLL_M50                  = creator.makeMyPrivateMCComponent('DYJetsToLL_M50'                , '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/manzoni-HNLSKIM2017_DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                       , 'PRIVATE', '*.root', 'phys03', xSec=1921.8*3, useAAA=True)
DYJetsToLL_M50      .nGenEvents = 27413121
#.sigma = 1921.8*3 pb; .nevents = 11074873 
DYJetsToLL_M50_ext              = creator.makeMyPrivateMCComponent('DYJetsToLL_M50_ext'            , '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/manzoni-HNLSKIM2017_DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_ext-115d0bad8e8ff59118d83f903524e0b3/USER'                   , 'PRIVATE', '*.root', 'phys03', xSec=1921.8*3, useAAA=True)
DYJetsToLL_M50_ext  .nGenEvents = 158048935
#.sigma = 1921.8*3 pb; .nevents = 63912552; .L = 11085.536476220212 pb^-1 

WLLJJ_WToLNu_EWK                = creator.makeMyPrivateMCComponent('WLLJJ_WToLNu_EWK'              , '/WLLJJ_WToLNu_EWK_TuneCP5_13TeV_madgraph-madspin-pythia8/manzoni-HNLSKIM2017_WLLJJ_WToLNu_EWK_TuneCP5_13TeV_madgraph-madspin-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'             , 'PRIVATE', '*.root', 'phys03', useAAA=True)
WLLJJ_WToLNu_EWK    .nGenEvents = 880000
#.sigma = NOT FOUND pb

WW_DoubleScattering             = creator.makeMyPrivateMCComponent('WW_DoubleScattering'           , '/WW_DoubleScattering_13TeV-pythia8_TuneCP5/manzoni-HNLSKIM2017_WW_DoubleScattering_13TeV-pythia8_TuneCP5-115d0bad8e8ff59118d83f903524e0b3/USER'                                         , 'PRIVATE', '*.root', 'phys03', useAAA=True)
WW_DoubleScattering .nGenEvents = 1000000 
#.sigma = NOT FOUND pb
 
WZTo3LNu                        = creator.makeMyPrivateMCComponent('WZTo3LNu'                      , '/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/manzoni-HNLSKIM2017_WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                                     , 'PRIVATE', '*.root', 'phys03', useAAA=True)
WZTo3LNu            .nGenEvents = 10881896 
#.sigma = NOT FOUND pb

ZZTo4L                          = creator.makeMyPrivateMCComponent('ZZTo4L'                        , '/ZZTo4L_13TeV_powheg_pythia8/manzoni-HNLSKIM2017_ZZTo4L_13TeV_powheg_pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                                                                     , 'PRIVATE', '*.root', 'phys03', xSec=1.256, useAAA=True)
ZZTo4L              .nGenEvents = 6835701 
#.sigma = 1.256 pb

ZZTo4L_ext                      = creator.makeMyPrivateMCComponent('ZZTo4L_ext'                    , '/ZZTo4L_13TeV_powheg_pythia8/manzoni-HNLSKIM2017_ZZTo4L_13TeV_powheg_pythia8_ext-115d0bad8e8ff59118d83f903524e0b3/USER'                                                                 , 'PRIVATE', '*.root', 'phys03', xSec=1.256, useAAA=True)
ZZTo4L_ext          .nGenEvents = 98009599
#.sigma = 1.256 pb

WJetsToLNu_HT400To600           = creator.makeMyPrivateMCComponent('WJetsToLNu_HT400To600'         , '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'          , 'PRIVATE', '*.root', 'phys03', xSec=48.91, useAAA=True)
#.sigma = 48.91 ± 0.072 pb (LO); .nevents = 5572699 
WJetsToLNu_HT600To800           = creator.makeMyPrivateMCComponent('WJetsToLNu_HT600To800'         , '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'          , 'PRIVATE', '*.root', 'phys03', xSec=12.05, useAAA=True)
#.sigma = 12.05 ± 0.0073 pb (LO); .nevents = 4443563
WJetsToLNu_HT800To1200          = creator.makeMyPrivateMCComponent('WJetsToLNu_HT800To1200'        , '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'        , 'PRIVATE', '*.root', 'phys03', xSec=5.501, useAAA=True)
#.sigma = 5.501 ± 0.017 pb (LO); .nevents = 8675292 
WJetsToLNu_HT1200To2500         = creator.makeMyPrivateMCComponent('WJetsToLNu_HT1200To2500'       , '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'      , 'PRIVATE', '*.root', 'phys03', xSec=1.329, useAAA=True)
#.sigma = 1.329 ± 0.0025 pb (LO); .nevents = 5696067 
# WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8.sigma = 20508.9*3 pb
 
W1JetsToLNu_LHEWpT_250_400      = creator.makeMyPrivateMCComponent('W1JetsToLNu_LHEWpT_250_400'    , '/W1JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W1JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'    , 'PRIVATE', '*.root', 'phys03', useAAA=True)
#.sigma = NOT FOUND pb; .nevents = 11545472 
W1JetsToLNu_LHEWpT_400_inf      = creator.makeMyPrivateMCComponent('W1JetsToLNu_LHEWpT_400_inf'    , '/W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'    , 'PRIVATE', '*.root', 'phys03', useAAA=True)
#.sigma = NOT FOUND pb; .nevents = 2822947 
W1JetsToLNu_LHEWpT_400_inf_ext  = creator.makeMyPrivateMCComponent('W1JetsToLNu_LHEWpT_400_inf_ext', '/W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8_ext-115d0bad8e8ff59118d83f903524e0b3/USER', 'PRIVATE', '*.root', 'phys03', useAAA=True)
#.sigma = NOT FOUND pb; .nevents = 3139785 
 
W2JetsToLNu_LHEWpT_50_150       = creator.makeMyPrivateMCComponent('W2JetsToLNu_LHEWpT_50_150 '    , '/W2JetsToLNu_LHEWpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W2JetsToLNu_LHEWpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'      , 'PRIVATE', '*.root', 'phys03', useAAA=True)
#.sigma = NOT FOUND pb; .nevents = 10755628 
W2JetsToLNu_LHEWpT_100_150      = creator.makeMyPrivateMCComponent('W2JetsToLNu_LHEWpT_100_150'    , '/W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'    , 'PRIVATE', '*.root', 'phys03', useAAA=True)
#.sigma = NOT FOUND pb; .nevents = 14264210 
W2JetsToLNu_LHEWpT_250_400      = creator.makeMyPrivateMCComponent('W2JetsToLNu_LHEWpT_250_400'    , '/W2JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W2JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'    , 'PRIVATE', '*.root', 'phys03', useAAA=True)
#.sigma = NOT FOUND pb; .nevents = 38515628
W2JetsToLNu_LHEWpT_400_inf      = creator.makeMyPrivateMCComponent('W2JetsToLNu_LHEWpT_400_inf'    , '/W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'    , 'PRIVATE', '*.root', 'phys03', useAAA=True)
#.sigma = NOT FOUND pb; .nevents = 18636486 
 
W3JetsToLNu                     = creator.makeMyPrivateMCComponent('W3JetsToLNu'                   , '/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                                , 'PRIVATE', '*.root', 'phys03', xSec=993.4*1.17, useAAA=True)
#.sigma = 993.4*1.17 pb; .nevents = 6265138; .L = 5390.395413145565 pb^-1 
 
W4JetsToLNu                     = creator.makeMyPrivateMCComponent('W4JetsToLNu'                   , '/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                                , 'PRIVATE', '*.root', 'phys03', xSec=542.4*1.17, useAAA=True)
#.sigma = 542.4*1.17 pb; .nevents = 3356894; .L = 5289.712704535714 pb^-1  

# LINK for crosssections: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns

hnl_bkg = [
    TTJets_amcat                  ,
    TTJets_mdgrph                 ,
 
    DYJetsToLL_M50                ,
    DYJetsToLL_M50_ext            ,

    WLLJJ_WToLNu_EWK              ,
    WW_DoubleScattering           ,
    WZTo3LNu                      ,
    ZZTo4L                        ,
    ZZTo4L_ext                    ,

#    WJetsToLNu_HT400To600         ,
#    WJetsToLNu_HT600To800         ,
#    WJetsToLNu_HT800To1200        ,
#    WJetsToLNu_HT1200To2500       ,
 
#    W1JetsToLNu_LHEWpT_250_400    ,
#    W1JetsToLNu_LHEWpT_400_inf    ,
#    W1JetsToLNu_LHEWpT_400_inf_ext,
 
#    W2JetsToLNu_LHEWpT_50_150     ,
#    W2JetsToLNu_LHEWpT_100_150    ,
#    W2JetsToLNu_LHEWpT_250_400    ,
#    W2JetsToLNu_LHEWpT_400_inf    ,
 
    W3JetsToLNu                   ,
    W4JetsToLNu                   ,
] 

