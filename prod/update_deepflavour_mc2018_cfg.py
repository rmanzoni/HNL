from CMGTools.HNL.update_deepflavour_base_cfg import process, cms
process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v20' 
print '\nINFO: using GT', process.GlobalTag.globaltag, '\n\n'

process.source.fileNames = cms.untracked.vstring(
        ## HNL signal 2018
    'file:/afs/cern.ch/work/m/manzoni/HNL/cmg/CMSSW_10_4_0_patch1/src/CMGTools/HNL/cfg/2018/heavyNeutrino_1.root',
)

process.output.fileName = cms.untracked.string('output_2018_mc.root')

process.output.outputCommands.append('drop patElectrons_slimmedElectrons__PAT')
process.output.outputCommands.append('keep patElectrons_slimmedElectrons__%s' %process.name_())

##########################################################################################
## RERUN EGAMMA ID Fall17V2
##########################################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMiniAODV2
# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPostRecoRecipes#106X
# https://github.com/cms-egamma/EgammaPostRecoTools/blob/master/test/runEgammaPostRecoTools.py#L71-L79
from EgammaUser.EgammaPostRecoTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(
    process,
    era='2018-Prompt'
    phoIDModules=[], # do not fiddle with photons, we don't use them
)  

# find where the new IDs are needed first
high_pt_ele_index = process.p.index(process.goodHighPtEles)
# and then insert this rerun EGamma sequence just before that
process.p.insert(high_pt_ele_index, process.egammaPostRecoSeq)

# and now replace the input collection of goodHighPtEles, must be the updated one with the new IDs
process.goodHighPtEles.src = cms.InputTag('slimmedElectrons', '', process.name_())
