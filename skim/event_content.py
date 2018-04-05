from Configuration.EventContent.EventContent_cff import *

miniaod_event_content_data = MINIAODEventContent   .outputCommands
miniaod_event_content_mc   = MINIAODSIMEventContent.outputCommands

aod_event_content = [
    'keep recoTracks_displacedGlobalMuons__RECO',
    'keep recoTracks_displacedStandAloneMuons__RECO',
    'keep recoTrackExtras_displacedGlobalMuons__RECO',
    'keep recoTrackExtras_displacedStandAloneMuons__RECO',
]
