# Spring 2020 installation recipe

### create a 106 release

```
cmsrel CMSSW_10_6_12
cd CMSSW_10_6_12/src
cmsenv
```

### create a new CMSSW repository
```
git cms-init
```

### checkout the only packages we need
```
git-cms-addpkg PhysicsTools/Heppy
git-cms-addpkg PhysicsTools/HeppyCore
```

### apply Ric's updates to Heppy
```
git cms-merge-topic rmanzoni:heppy_106X_hnl
```

### apply EGamma EgammaPostRecoTools  
needed to compute latest greatest electron IDs in 2016 and 2017
```
git clone git@github.com:cms-egamma/EgammaPostRecoTools.git  EgammaUser/EgammaPostRecoTools
cd  EgammaUser/EgammaPostRecoTools
git checkout master
cd -
```

### compile
```
scram b -rj 8
```

### checkout CMGTools
```
git clone -o cmg-central https://github.com/CERN-PH-CMG/cmgtools-lite.git -b 104X_dev CMGTools
cd CMGTools
```

### not all subpackages are needed, so sparse  checkout
```
git cms-sparse-checkout init
touch .git/info/sparse-checkout
echo "RootTools" >> .git/info/sparse-checkout
echo "Production" >> .git/info/sparse-checkout
git checkout 104X_dev
```

### compile
```
scram b -rj 8
```

### now add the HNL code
```
git clone git@github.com:rmanzoni/HNL.git
cd HNL
git checkout master
```

### compile
```
scram b -rj 8
```

### set your X509_USER_PROXY env variable
since you'll be using xrootd to access files remotely, and you'll use CERN batch facility, you need to make sure your voms proxy token is put in a `afs` shared directory.
If `echo $X509_USER_PROXY` returns nothing or returns some `tmp` path, follow these instructions https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookXrootdService#OpenCondor 


### run a test job
```
voms-proxy-init --voms cms --valid 198:0
cd cfg/2018
heppy test hn3l_mc_2018_test_cfg.py
```


### jobs resubmission
First, copy heppy scripts in your environment 
```
cp python/heppy_patch/* $CMSSW_BASE/bin/<architecture>/
```

Note: make sure that you have the rwx permissions on the files. If not: chmod 777 <file>

Then, copy submission scripts in the production directory. Typically do

```
cp scripts/resbmitter_data.sh cfg/<year>/<dataRep>/
cp scripts/resbmitter_mc.sh cfg/<year>/<mcRep>/
```

Finally run the scripts
```
cd cfg/<year>/<data|mcRep>/
source resubmitter_<data|mc>.sh
```




