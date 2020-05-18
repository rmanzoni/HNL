from CMGTools.HNL.prod.update_deepjet_and_ele_id_base_cfg import process, cms
process.GlobalTag.globaltag = '102X_dataRun2_v12' 
print '\nINFO: using GT', process.GlobalTag.globaltag, '\n\n'

process.source.fileNames = cms.untracked.vstring(
    'root://cms-xrd-global.cern.ch//store/data/Run2018B/SingleMuon/MINIAOD/17Sep2018-v1/1010000/CDBE64B8-6D1D-5F47-A4C8-6722D7D385A1.root',
)

process.output.fileName = cms.untracked.string('output_2018ABC_data.root')

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
process.goodLowPtEles.src = cms.InputTag('slimmedElectrons', '', process.name_())

