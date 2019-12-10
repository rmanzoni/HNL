
# HNL FW for 2016, 2017 & 2018 (CMG 104X)

## automatic

`wget https://github.com/vinzenzstampf/HNL/setup.sh`

`. setup.sh`


## manually

### set up CMSSW 10.4

`export SCRAM_ARCH=slc7_amd64_gcc700`

`cmsrel CMSSW_10_4_0_patch1`

`cd CMSSW_10_4_0_patch1/src`

`cmsenv`

`git config --global user.github <GIT_USER_NAME>`

`git config --global user.name '<USER_NAME>'`

`git config --global user.email '<USER_MAIL>'`

`git cms-init`


### add CMG CMSSW 104X

`git remote add cmg-central https://github.com/CERN-PH-CMG/cmg-cmssw.git  -f  -t heppy_104X_dev`

`git remote add vstampf https://github.com/vinzenzstampf/cmg-cmssw.git -f -t heppy_104X_hnl`

`git checkout -b heppy_104X_dev cmg-central/heppy_104X_dev`

`git checkout -b heppy_104X_hnl vstampf/heppy_104X_hnl`

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

`git clone -o HNL https://github.com/vinzenzstampf/HNL.git -b HNL_18 HNL`

`cd HNL`

### compile

`cd $CMSSW_BASE; scram b -j 36`

### fix & add heppy scripts

`cp heppyMvBadChunks.py      $CMSSW_BASE/bin/slc7_amd64_gcc700/.`
`cp heppyMvGoodChunks.py     $CMSSW_BASE/bin/slc7_amd64_gcc700/.`
`cp heppyMvGoodNoChunks.py   $CMSSW_BASE/bin/slc7_amd64_gcc700/.`
`cp heppy_batch_slurm.py     $CMSSW_BASE/bin/slc7_amd64_gcc700/heppy_batch.py`

`chmod 777 $CMSSW_BASE/bin/slc7_amd64_gcc700/heppy*`
