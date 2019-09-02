#!/usr/bin/env python
import ROOT
import imp
import json
from array import array
wsptools = imp.load_source('wsptools', 'workspaceTools.py')


def GetFromTFile(str):
    f = ROOT.TFile(str.split(':')[0])
    obj = f.Get(str.split(':')[1]).Clone()
    f.Close()
    return obj

# Boilerplate
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.RooWorkspace.imp = getattr(ROOT.RooWorkspace, 'import')
ROOT.TH1.AddDirectory(0)
ROOT.gROOT.LoadMacro("CrystalBallEfficiency.cxx+")

w = ROOT.RooWorkspace('w')

### DESY electron/muon tag and probe results
loc = 'inputs/LeptonEfficiencies'

desyHistsToWrap = [
    (loc+'/Muon/Run2018/Muon_Run2018_IdIso.root',               'MC',   'm_idiso_desy_mc'),
    (loc+'/Muon/Run2018/Muon_Run2018_IdIso.root',               'Data', 'm_idiso_desy_data'),  
    (loc+'/Muon/Run2018/Muon_Run2018_IsoMu24orIsoMu27.root',    'MC',   'm_trgIsoMu24orIsoMu27_desy_mc'),
    (loc+'/Muon/Run2018/Muon_Run2018_IsoMu24orIsoMu27.root',    'Data', 'm_trgIsoMu24orIsoMu27_desy_data'),
    (loc+'/Muon/Run2018/Muon_Run2018_IsoMu27.root',             'MC',   'm_trgIsoMu27_desy_mc'),
    (loc+'/Muon/Run2018/Muon_Run2018_IsoMu27.root',             'Data', 'm_trgIsoMu27_desy_data'),
    (loc+'/Muon/Run2018/Muon_Run2018_IsoMu20.root',             'MC',   'm_trgIsoMu20_desy_mc'),
    (loc+'/Muon/Run2018/Muon_Run2018_IsoMu20.root',             'Data', 'm_trgIsoMu20_desy_data')
]

for task in desyHistsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          wsptools.ProcessDESYLeptonSFs(task[0], task[1], task[2]), name=task[2])
for t in ['idiso_desy','trgIsoMu24orIsoMu27_desy','trgIsoMu27_desy','trgIsoMu20_desy']:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))

desyHistsToWrap = [
    (loc+'/Electron/Run2018/Electron_Run2018_IdIso.root',          'MC',   'e_idiso_desy_mc'),
    (loc+'/Electron/Run2018/Electron_Run2018_IdIso.root',          'Data', 'e_idiso_desy_data'),  
    (loc+'/Electron/Run2018/Electron_Run2018_Ele32orEle35.root',   'MC',   'e_trgEle32orEle35_desy_mc'),
    (loc+'/Electron/Run2018/Electron_Run2018_Ele32orEle35.root',   'Data', 'e_trgEle32orEle35_desy_data'),
    (loc+'/Electron/Run2018/Electron_Run2018_Ele35.root',          'MC',   'e_trgEle35_desy_mc'),
    (loc+'/Electron/Run2018/Electron_Run2018_Ele35.root',          'Data', 'e_trgEle35_desy_data'),
    (loc+'/Electron/Run2018/Electron_Run2018_Ele24.root',          'MC',   'e_trgEle24leg_desy_mc'),
    (loc+'/Electron/Run2018/Electron_Run2018_Ele24.root',          'Data', 'e_trgEle24leg_desy_data')
]

for task in desyHistsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          wsptools.ProcessDESYLeptonSFs(task[0], task[1], task[2]), name=task[2])

for t in ['idiso_desy','trgEle32orEle35_desy','trgEle35_desy','trgEle24leg_desy']:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))


# ### LO DYJetsToLL Z mass vs pT correction
# histsToWrap = [
#     ('inputs/zpt_weights_2017.root:zptmass_histo'                 , 'zpt_weight_nom'         )
# ]

# for task in histsToWrap:
#     wsptools.SafeWrapHist(w, ['z_gen_mass', 'z_gen_pt'],
#                           GetFromTFile(task[0]), name=task[1])
# w.importClassCode('CrystalBallEfficiency')

### LO DYJetsToLL Z mass vs pT correction
# wsptools.SafeWrapHist(w, ['z_gen_mass', 'z_gen_pt'],
#                       GetFromTFile('inputs/zpt_weights_2017.root:zptmass_histo'), name='zptmass_weight_nom')

wsptools.SafeWrapHist(w, ['z_gen_mass', 'z_gen_pt'],
                      GetFromTFile('inputs/Zpt_weights_2018.root:zptmass_weights'), name='zptmass_weight_nom')

w.importClassCode('CrystalBallEfficiency')


w.Print()
w.writeToFile('htt_scalefactors_2018_v1.root')
w.Delete()
