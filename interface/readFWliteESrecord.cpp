#include "FWCore/FWLite/interface/FWLiteEnabler.h"
#include "PhysicsTools/CondLiteIO/interface/RecordWriter.h"
#include "DataFormats/FWLite/interface/Record.h"
#include "DataFormats/FWLite/interface/EventSetup.h"
#include "DataFormats/FWLite/interface/ESHandle.h"
//#include "MagneticField/VolumeBasedEngine/interface/VolumeBasedMagneticField.h"
//#include "MagneticField/VolumeBasedEngine/interface/MagGeometry.h"

FWLiteEnabler::enable();

std::cout << "Test!!!" << std::endl << std::endl;

TFile f("bfield_bkp1.root","READ");
fwlite::EventSetup es(&f);
es.exists("IdealMagneticFieldRecord")
fwlite::RecordID testRecID = es.recordID("IdealMagneticFieldRecord");
es.syncTo(edm::EventID(1,0,0),edm::Timestamp());
std::cout << "Got record ID " << testRecID << std::endl << es.get(testRecID).startSyncValue().eventID()<<std::endl;

fwlite::ESHandle< VolumeBasedMagneticField > fieldHandle;
fwlite::ESHandle<MagneticField > bfHandle;
record = es.get(testRecID)
record.name()
record.typeAndLabelOfAvailableData()

es.get(testRecID).get(bfHandle,"IdealMagneticFieldRecord")


/*

make a foo

*/


//VolumeBasedMagneticField *volumeField = new VolumeBasedMagneticField(foo);
