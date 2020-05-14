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

### run a test job
```
voms-proxy-init --voms cms --valid 198:0
cd cfg/2018
heppy test hn3l_mc_all_test.cfg.py
```
