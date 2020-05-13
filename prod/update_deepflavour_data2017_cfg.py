from CMGTools.HNL.update_deepflavour_base_cfg import process, cms
process.GlobalTag.globaltag = '102X_dataRun2_v12' 
print '\nINFO: using GT', process.GlobalTag.globaltag, '\n\n'

##########################################################################################
## RERUN EGAMMA ID Fall17V2
##########################################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMiniAODV2
# from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
# setupEgammaPostRecoSeq(process,
#                        runVID=True, #saves CPU time by not needlessly re-running VID, if you want the Fall17V2 IDs, set this to True or remove (default is True)
#                        era='2017-Nov17ReReco')  
#a sequence egammaPostRecoSeq has now been created and should be added to your path, eg process.p=cms.Path(process.egammaPostRecoSeq)

