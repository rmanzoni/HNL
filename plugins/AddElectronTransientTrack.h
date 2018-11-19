// -*- C++ -*-
//
// Package:    CMGTools/BKstLL
// Class:      AddElectronTransientTrack
// 
/**\class AddElectronTransientTrack AddElectronTransientTrack.cc CMGTools/BKstLL/src/AddElectronTransientTrack.cc
 Description: for each PAT muon extrapolates its coordinates to the second muon station, 
              so that the offline-L1 matching is done on an equal footing.
              Saves a map: each offline muon is associated to the extrapolated 4 vector. 
              
              Very much inspired to 
              https://github.com/cms-l1-dpg/Legacy-L1Ntuples/blob/6b1d8fce0bd2058d4309af71b913e608fced4b17/src/L1MuonRecoTreeProducer.cc
*/
//
// Original Author for the BKstLL Analysis:  Riccardo Manzoni
// Adapted to the LL-HNL Analysis by Dehua Zhu
//
//

#include <memory>

// ROOT
#include "TMath.h"
#include "TLorentzVector.h"

// framework
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"

// Data Formats
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/GeometrySurface/interface/Cylinder.h"
#include "DataFormats/GeometrySurface/interface/Plane.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

// Transient tracks (for extrapolations)
#include "TrackingTools/GeomPropagators/interface/Propagator.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/Records/interface/TrackingComponentsRecord.h"
#include "TrackingTools/TrajectoryState/interface/FreeTrajectoryState.h"
#include "TrackingTools/TrajectoryState/interface/TrajectoryStateOnSurface.h"
#include "TrackingTools/TrajectoryState/interface/TrajectoryStateTransform.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

// B Field
#include "MagneticField/Engine/interface/MagneticField.h"

namespace cmg{
  class AddElectronTransientTrack : public edm::EDProducer {
    public:
      explicit AddElectronTransientTrack(const edm::ParameterSet & iConfig);
      virtual ~AddElectronTransientTrack() { }
  
      virtual void produce(edm::Event & iEvent, const edm::EventSetup& iSetup) override;
      
    private:

      // reco electrons
      const edm::EDGetTokenT<edm::View<pat::Electron>> eleSrc_;
      edm::Handle<edm::View<pat::Electron>> electrons;

      // transien track builder handle
      edm::ESHandle<TransientTrackBuilder> ttrack_builder;
      
  };
}

cmg::AddElectronTransientTrack::AddElectronTransientTrack(const edm::ParameterSet & iConfig):
  eleSrc_( consumes<edm::View<pat::Electron>>(iConfig.getParameter<edm::InputTag>("patEleSrc") ) )
{ 
  // try with transient track record
  produces<std::vector<std::pair<edm::Ptr<pat::Electron>, reco::Track>>> ("eleTtkMap");
}


void 
cmg::AddElectronTransientTrack::produce(edm::Event & iEvent, const edm::EventSetup & iSetup)
{

  // unique pointers for the output
  std::unique_ptr< std::vector<std::pair<edm::Ptr<pat::Electron>, reco::Track>> > eleTtkMap_ptr(new std::vector<std::pair<edm::Ptr<pat::Electron>, reco::Track>>);
       
  // Get the transient track builder from the event setup
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", ttrack_builder);

  // Get the electrons
  iEvent.getByToken(eleSrc_, electrons);

  // loop over electrons
  for(edm::View<pat::Electron>::const_iterator iele = electrons->begin(); iele != electrons->end(); iele++){
    
    // Get the pointer to the muon in the collection
    unsigned int idx = iele - electrons->begin();
    edm::Ptr<pat::Electron> ptrEle = electrons->ptrAt(idx);

    // fill the map
    eleTtkMap_ptr -> push_back ( std::pair<edm::Ptr<pat::Electron>, reco::Track>(ptrEle, ttrack_builder->build(iele->gsfTrack()).track()) );

  }

  // put it back into the event
  iEvent.put(std::move(eleTtkMap_ptr), "eleTtkMap");

}
