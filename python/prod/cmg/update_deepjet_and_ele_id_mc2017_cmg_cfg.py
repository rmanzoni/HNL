from CMGTools.HNL.prod.update_deepjet_and_ele_id_mc2017_cfg import process, cms

print 'replacing - with _ in electron IDs'

new_low_pt_cut  = process.goodLowPtEles .cut.value().replace('mvaEleID-Fall17-noIso-V2-wp90', 'mvaEleID_Fall17_noIso_V2_wp90').replace('mvaEleID-Fall17-iso-V2-wp90', 'mvaEleID_Fall17_iso_V2_wp90')
new_high_pt_cut = process.goodHighPtEles.cut.value().replace('mvaEleID-Fall17-noIso-V2-wp90', 'mvaEleID_Fall17_noIso_V2_wp90').replace('mvaEleID-Fall17-iso-V2-wp90', 'mvaEleID_Fall17_iso_V2_wp90')

process.goodLowPtEles.cut  = cms.string(new_low_pt_cut )
process.goodHighPtEles.cut = cms.string(new_high_pt_cut)

