from CMGTools.HNL.update_deepjet_and_ele_id_base_cfg import process, cms
process.GlobalTag.globaltag = '102X_dataRun2_v12' 
print '\nINFO: using GT', process.GlobalTag.globaltag, '\n\n'

process.source.fileNames = cms.untracked.vstring(
    'root://cms-xrd-global.cern.ch//store/data/Run2017F/SingleMuon/MINIAOD/31Mar2018-v1/100000/70F7C6A6-A739-E811-A1B8-0CC47A4D7674.root'
)

process.output.fileName = cms.untracked.string('output_2017_data.root')

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

# for data, use skims
process.lowPtSkimSequence = cms.Sequence(
    process.goodLowPtEles     +
    process.goodLowPtMuons    +
    process.goodLeptons       
)
process.p.insert(0, process.lowPtSkimSequence)

process.highPtSkimSequence = cms.Sequence(
    process.goodHighPtEles    +
    process.goodHighPtMuons   +
    process.goodHighPtLeptons 
)
process.p.insert(1, process.highPtSkimSequence)

# find where the new IDs are needed first
high_pt_ele_index = process.p.index(process.highPtSkimSequence)
# and then insert this rerun EGamma sequence just before that
process.p.insert(high_pt_ele_index, process.egammaPostRecoSeq)

# and now replace the input collection of goodHighPtEles, must be the updated one with the new IDs
process.goodHighPtEles.src = cms.InputTag('slimmedElectrons', '', process.name_())

# save the correct electron collection
process.output.outputCommands.append('drop patElectrons_slimmedElectrons__PAT')
process.output.outputCommands.append('keep patElectrons_slimmedElectrons__%s' %process.name_())
