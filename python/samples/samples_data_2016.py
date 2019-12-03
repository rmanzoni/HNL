import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

# FIXME! put the right cross sections

''' makeMyPrivateDataComponent is a copy of MakeMyPrivateMCComponent in ComponentCreator.py
    this should be adjusted (i guess) to include some data only attributes, like lumi, etc.
'''
json = '$CMSSW_BASE/src/CMGTools/HNL/data/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'

Single_ele_2016B  = creator.makeDataComponent('Single_ele_2016B', '/SingleElectron/Run2016B-17Jul2018_ver1-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_ele_2016C  = creator.makeDataComponent('Single_ele_2016C', '/SingleElectron/Run2016C-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_ele_2016D  = creator.makeDataComponent('Single_ele_2016D', '/SingleElectron/Run2016D-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_ele_2016E  = creator.makeDataComponent('Single_ele_2016E', '/SingleElectron/Run2016E-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_ele_2016F  = creator.makeDataComponent('Single_ele_2016F', '/SingleElectron/Run2016F-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_ele_2016G  = creator.makeDataComponent('Single_ele_2016G', '/SingleElectron/Run2016G-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_ele_2016H  = creator.makeDataComponent('Single_ele_2016H', '/SingleElectron/Run2016H-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
                                                                                                                            
Single_mu_2016B  = creator.makeDataComponent('Single_mu_2016B', '/SingleMuon/Run2016B-17Jul2018_ver1-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_mu_2016C  = creator.makeDataComponent('Single_mu_2016C', '/SingleMuon/Run2016C-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_mu_2016D  = creator.makeDataComponent('Single_mu_2016D', '/SingleMuon/Run2016D-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_mu_2016E  = creator.makeDataComponent('Single_mu_2016E', '/SingleMuon/Run2016E-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_mu_2016F  = creator.makeDataComponent('Single_mu_2016F', '/SingleMuon/Run2016F-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_mu_2016G  = creator.makeDataComponent('Single_mu_2016G', '/SingleMuon/Run2016G-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)
Single_mu_2016H  = creator.makeDataComponent('Single_mu_2016H', '/SingleMuon/Run2016H-17Jul2018-v1/MINIAOD', 'CMS', '.*root', json, useAAA=True)

Single_ele_2016 = [
    Single_ele_2016B,
    Single_ele_2016C,
    Single_ele_2016D,
    Single_ele_2016E,
    Single_ele_2016F,
    Single_ele_2016G,
    Single_ele_2016H,
]

Single_mu_2016 = [
    Single_mu_2016B,
    Single_mu_2016C,
    Single_mu_2016D,
    Single_mu_2016E,
    Single_mu_2016F,
    Single_mu_2016G,
    Single_mu_2016H,
] 
