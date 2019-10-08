cp /afs/cern.ch/work/d/dwinterb/public/MSSM2016/tagging_efficiencies_Moriond2017.root data/.

cp /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt data/.

cd data/leptonsf/

wget https://github.com/jandrejk/ProductionFromNano/tree/SM2018/utils/CorrectionWorkspaces/htt_scalefactors_2018_v1.root

wget https://github.com/CMS-HTT/CorrectionsWorkspace/raw/2017_17NovReRecoData_Fall17MC/htt_scalefactors_v17_1.root

cd $CMSSW_BASE/src

git checkout hnl_104X PhysicsTools/Heppy/python/analyzers/core/PileUpAnalyzer.py

git checkout hnl_104X PhysicsTools/Heppy/python/physicsobjects/Electron.py

git checkout hnl_104X PhysicsTools/Heppy/python/physicsobjects/Muon.py

git checkout hnl_104X PhysicsTools/Heppy/python/physicsobjects/Lepton.py

git checkout hnl_104X PhysicsTools/HeppyCore/python/framework/event.py

git checkout hnl_104X PhysicsTools/HeppyCore/python/framework/looper.py

