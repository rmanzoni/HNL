
# HNL FW for 2018 (CMG 104X)


### set up CMSSW 10.4

`cmsrel CMSSW_10_4_0_patch1`

`cd CMSSW_10_4_0_patch1/src`

`cmsenv`

`git config --global user.github <GIT_USER_NAME>`

`git config --global user.name '<USER_NAME>'`

`git config --global user.email '<USER_MAIL>'`

`git cms-init`


### sparse-checkout

edit the sparse-checkout: `vim .git/info/sparse-checkout`

here replace everything by

`/.clang-format`

`/.clang-tidy`

`/.gitignore`

`/EgammaAnalysis/ElectronTools/`

`/PhysicsTools/`

`/RecoEgamma/EgammaTools/`

`/RecoEgamma/ElectronIdentification/`

`/RecoEgamma/PhotonIdentification/`

`/RecoTauTag/RecoTau/`

### add CMG 104X

`git remote add vstampf https://github.com/vinzenzstampf/cmg-cmssw.git -f -t hnl_104X`

`git checkout -b hnl_104X vstampf/hnl_104X`

add needed packages:

`git cms-addpkg /EgammaAnalysis/ElectronTools/`

`git cms-addpkg /PhysicsTools/`

`git cms-addpkg /RecoEgamma/EgammaTools/`

`git cms-addpkg /RecoEgamma/ElectronIdentification/`

`git cms-addpkg /RecoEgamma/PhotonIdentification/`

`git cms-addpkg /RecoTauTag/RecoTau/`


### add CMGTools

`git clone -o vstampf https://github.com/vinzenzstampf/cmgtools-lite.git -b 104X_HNL CMGTools`

`cd CMGTools`


### add HNL

`git clone -o HNL https://github.com/HNLETHZ/HNL.git -b HNL_18 HNL`

`cd HNL`

### adding some scale-factors

`cp /afs/cern.ch/work/d/dwinterb/public/MSSM2016/tagging_efficiencies_Moriond2017.root data/.`

`cd data/leptonsf/`

`wget https://github.com/jandrejk/ProductionFromNano/tree/SM2018/utils/CorrectionWorkspaces/htt_scalefactors_2018_v1.root`

`wget https://github.com/CMS-HTT/CorrectionsWorkspace/raw/2017_17NovReRecoData_Fall17MC/htt_scalefactors_v17_1.root`

### compile

`cd $CMSSW_BASE; scram b -j 8`

`cd src; scram b -j 8`

`cd CMGTools; scram b -j 8`

`cd HNL; scram b -j 8`
