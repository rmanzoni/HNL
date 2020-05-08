export SCRAM_ARCH=slc7_amd64_gcc700

cmsrel CMSSW_10_4_0_patch1

cd CMSSW_10_4_0_patch1/src

cmsenv

git cms-init

git remote add cmg-central https://github.com/CERN-PH-CMG/cmg-cmssw.git -f -t heppy_104X_dev
git remote add vstampf https://github.com/vinzenzstampf/cmg-cmssw.git -f -t heppy_104X_hnl

git checkout -b heppy_104X_dev cmg-central/heppy_104X_dev
git checkout -b heppy_104X_hnl vstampf/heppy_104X_hnl

git cms-addpkg /EgammaAnalysis/ElectronTools/
git cms-addpkg /PhysicsTools/
git cms-addpkg /RecoEgamma/EgammaTools/
git cms-addpkg /RecoEgamma/ElectronIdentification/
git cms-addpkg /RecoEgamma/PhotonIdentification/
git cms-addpkg /RecoTauTag/RecoTau/

git clone -o vstampf https://github.com/vinzenzstampf/cmgtools-lite.git -b 104X_HNL CMGTools
cd CMGTools

git clone -o HNL https://github.com/vinzenzstampf/HNL.git -b HNL_18 HNL

cd $CMSSW_BASE; scram b -j 36

cp heppyMvBadChunks.py      $CMSSW_BASE/bin/slc7_amd64_gcc700/.
cp heppyMvGoodChunks.py     $CMSSW_BASE/bin/slc7_amd64_gcc700/.
cp heppyMvGoodNoChunks.py   $CMSSW_BASE/bin/slc7_amd64_gcc700/.
cp heppy_batch_slurm.py     $CMSSW_BASE/bin/slc7_amd64_gcc700/heppy_batch.py

chmod 777 $CMSSW_BASE/bin/slc7_amd64_gcc700/heppy*
