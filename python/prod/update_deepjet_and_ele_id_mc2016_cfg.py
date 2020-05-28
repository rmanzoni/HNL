from CMGTools.HNL.prod.update_deepjet_and_ele_id_base_cfg import process, cms
process.GlobalTag.globaltag = '102X_mcRun2_asymptotic_v7' 
print '\nINFO: using GT', process.GlobalTag.globaltag, '\n\n'

process.source.fileNames = cms.untracked.vstring(
    'root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv3/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/40000/E0277B98-6F16-E911-8C5F-B083FED42B3A.root',
)

process.output.fileName = cms.untracked.string('output_2016_mc.root')

##########################################################################################
## RERUN EGAMMA ID Fall17V2
##########################################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMiniAODV2
# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPostRecoRecipes#106X
# https://github.com/cms-egamma/EgammaPostRecoTools/blob/master/test/runEgammaPostRecoTools.py#L71-L79
from EgammaUser.EgammaPostRecoTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(
    process,
    runVID=True,
    phoIDModules=[], # do not fiddle with photons, we don't use them
    runEnergyCorrections=False, # no point in re-running them, they are already fine
    era='2016-Legacy',
)  # era is new to select between 2016 / 2017,  it defaults to 2017

# SKIM TEMPORARILY DISABLED
# find where the new IDs are needed first
# and then insert this rerun EGamma sequence just before that
process.p.insert(0, process.egammaPostRecoSeq)

# do not filter!
process.p.remove(process.goodLeptons)
process.p.remove(process.goodHighPtLeptons)
