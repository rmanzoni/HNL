import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

# FIXME! put the right cross sections
# FIXME! check in ComponentCreator how to cache the file fetching
# FIXME! create meaningful lists

TTJets_amcat                    = creator.makeMyPrivateMCComponent('TTJets_amcat'                  , '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/vstampf-HNLSKIM2017_TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                                         , 'PRIVATE', '*.root', 'phys03', useAAA=True)
TTJets_mdgrph                   = creator.makeMyPrivateMCComponent('TTJets_madgraph'               , '/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/vstampf-HNLSKIM2017_TTJets_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                                           , 'PRIVATE', '*.root', 'phys03', useAAA=True)
               
DYJetsToLL_M50                  = creator.makeMyPrivateMCComponent('DYJetsToLL_M50'                , '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/manzoni-HNLSKIM2017_DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                       , 'PRIVATE', '*.root', 'phys03', useAAA=True)
DYJetsToLL_M50_ext              = creator.makeMyPrivateMCComponent('DYJetsToLL_M50_ext'            , '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/manzoni-HNLSKIM2017_DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_ext-115d0bad8e8ff59118d83f903524e0b3/USER'                   , 'PRIVATE', '*.root', 'phys03', useAAA=True)
    
WJetsToLNu_HT400To600           = creator.makeMyPrivateMCComponent('WJetsToLNu_HT400To600'         , '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'          , 'PRIVATE', '*.root', 'phys03', useAAA=True)
WJetsToLNu_HT600To800           = creator.makeMyPrivateMCComponent('WJetsToLNu_HT600To800'         , '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'          , 'PRIVATE', '*.root', 'phys03', useAAA=True)
WJetsToLNu_HT800To1200          = creator.makeMyPrivateMCComponent('WJetsToLNu_HT800To1200'        , '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'        , 'PRIVATE', '*.root', 'phys03', useAAA=True)
WJetsToLNu_HT1200To2500         = creator.makeMyPrivateMCComponent('WJetsToLNu_HT1200To2500'       , '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'      , 'PRIVATE', '*.root', 'phys03', useAAA=True)

W1JetsToLNu_LHEWpT_250_400      = creator.makeMyPrivateMCComponent('W1JetsToLNu_LHEWpT_250_400'    , '/W1JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W1JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'    , 'PRIVATE', '*.root', 'phys03', useAAA=True)
W1JetsToLNu_LHEWpT_400_inf      = creator.makeMyPrivateMCComponent('W1JetsToLNu_LHEWpT_400_inf'    , '/W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'    , 'PRIVATE', '*.root', 'phys03', useAAA=True)
W1JetsToLNu_LHEWpT_400_inf_ext  = creator.makeMyPrivateMCComponent('W1JetsToLNu_LHEWpT_400_inf_ext', '/W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8_ext-115d0bad8e8ff59118d83f903524e0b3/USER', 'PRIVATE', '*.root', 'phys03', useAAA=True)

W2JetsToLNu_LHEWpT_50_150       = creator.makeMyPrivateMCComponent('W2JetsToLNu_LHEWpT_50_150 '    , '/W2JetsToLNu_LHEWpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W2JetsToLNu_LHEWpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'      , 'PRIVATE', '*.root', 'phys03', useAAA=True)
W2JetsToLNu_LHEWpT_100_150      = creator.makeMyPrivateMCComponent('W2JetsToLNu_LHEWpT_100_150'    , '/W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'    , 'PRIVATE', '*.root', 'phys03', useAAA=True)
W2JetsToLNu_LHEWpT_250_400      = creator.makeMyPrivateMCComponent('W2JetsToLNu_LHEWpT_250_400'    , '/W2JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W2JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'    , 'PRIVATE', '*.root', 'phys03', useAAA=True)
W2JetsToLNu_LHEWpT_400_inf      = creator.makeMyPrivateMCComponent('W2JetsToLNu_LHEWpT_400_inf'    , '/W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8/lshchuts-HNLSKIM2017_W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'    , 'PRIVATE', '*.root', 'phys03', useAAA=True)

W3JetsToLNu                     = creator.makeMyPrivateMCComponent('W3JetsToLNu'                   , '/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                                , 'PRIVATE', '*.root', 'phys03', useAAA=True)
W4JetsToLNu                     = creator.makeMyPrivateMCComponent('W4JetsToLNu'                   , '/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/lshchuts-HNLSKIM2017_W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8-115d0bad8e8ff59118d83f903524e0b3/USER'                                , 'PRIVATE', '*.root', 'phys03', useAAA=True)


hnl_bkg = [
    TTJets_amcat                  ,
    TTJets_mdgrph                 ,

    DYJetsToLL_M50                ,
    DYJetsToLL_M50_ext            ,

    WJetsToLNu_HT400To600         ,
    WJetsToLNu_HT600To800         ,
    WJetsToLNu_HT800To1200        ,
    WJetsToLNu_HT1200To2500       ,

    W1JetsToLNu_LHEWpT_250_400    ,
    W1JetsToLNu_LHEWpT_400_inf    ,
    W1JetsToLNu_LHEWpT_400_inf_ext,

    W2JetsToLNu_LHEWpT_50_150     ,
    W2JetsToLNu_LHEWpT_100_150    ,
    W2JetsToLNu_LHEWpT_250_400    ,
    W2JetsToLNu_LHEWpT_400_inf    ,

    W3JetsToLNu                   ,
    W4JetsToLNu                   ,
]






# '/SingleMuon/dezhu-HNLSKIM2017-6c435cbb87e441358a32d522d9d7cdf0/USER' , 'PRIVATE', '*.root', 'phys03', useAAA=True)

 