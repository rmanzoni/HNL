from CMGTools.HNL.update_deepjet_and_ele_id_base_cfg import process, cms
process.GlobalTag.globaltag = '102X_mc2017_realistic_v7' 
print '\nINFO: using GT', process.GlobalTag.globaltag, '\n\n'

process.source.fileNames = cms.untracked.vstring(
    'root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/C6BB52E8-F341-E811-8A2F-001E677927EC.root',
)

process.output.fileName = cms.untracked.string('output_2017_mc.root')

##########################################################################################
## RERUN EGAMMA ID Fall17V2
##########################################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMiniAODV2
# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPostRecoRecipes#106X
# https://github.com/cms-egamma/EgammaPostRecoTools/blob/master/test/runEgammaPostRecoTools.py#L71-L79
from EgammaUser.EgammaPostRecoTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(
    process,
    runVID=True, #saves CPU time by not needlessly re-running VID, if you want the Fall17V2 IDs, set this to True or remove (default is True)
    phoIDModules=[], # do not fiddle with photons, we don't use them
    era='2017-Nov17ReReco',
)  

# SKIM TEMPORARILY DISABLED
# # find where the new IDs are needed first
# high_pt_ele_index = process.p.index(process.goodHighPtEles)
# # and then insert this rerun EGamma sequence just before that
# process.p.insert(high_pt_ele_index, process.egammaPostRecoSeq)
# 
# # and now replace the input collection of goodHighPtEles, must be the updated one with the new IDs
# process.goodHighPtEles.src = cms.InputTag('slimmedElectrons', '', process.name_())

process.p.insert(0, process.egammaPostRecoSeq)

# save the correct electron collection
process.output.outputCommands.append('drop patElectrons_slimmedElectrons__PAT')
process.output.outputCommands.append('keep patElectrons_slimmedElectrons__%s' %process.name_())
