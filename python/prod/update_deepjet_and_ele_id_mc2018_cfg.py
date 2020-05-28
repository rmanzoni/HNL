# cmsRun update_deepjet_and_ele_id_mc2018_cfg.py runFullCfg=False

from CMGTools.HNL.prod.update_deepjet_and_ele_id_base_cfg import process, cms
process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v20' 
print '\nINFO: using GT', process.GlobalTag.globaltag, '\n\n'

process.source.fileNames = cms.untracked.vstring(
    ## HNL signal 2018
#     'file:/afs/cern.ch/work/m/manzoni/HNL/cmg/CMSSW_10_4_0_patch1/src/CMGTools/HNL/cfg/2018/heavyNeutrino_1.root',
#     'file:/tmp/manzoni/heavyNeutrino_1-ade416da5bf6e9f.root'
    'root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v2/10000/C3F9C740-9829-9B49-BDB1-A14748939E81.root',
#     'file:C3F9C740-9829-9B49-BDB1-A14748939E81.root',
)

process.output.fileName = cms.untracked.string('output_2018_mc.root')

##########################################################################################
## RERUN EGAMMA ID Fall17V2
##########################################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMiniAODV2
# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPostRecoRecipes#106X
# https://github.com/cms-egamma/EgammaPostRecoTools/blob/master/test/runEgammaPostRecoTools.py#L71-L79
from EgammaUser.EgammaPostRecoTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(
    process,
    era='2018-Prompt',
    phoIDModules=[], # do not fiddle with photons, we don't use them
)  

# SKIM TEMPORARILY DISABLED
# find where the new IDs are needed first
# and then insert this rerun EGamma sequence just before that
process.p.insert(0, process.egammaPostRecoSeq)

# do not filter!
process.p.remove(process.goodLeptons)
process.p.remove(process.goodHighPtLeptons)
