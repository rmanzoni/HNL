#define G__DICTIONARY

#include <atomic>

#include "DataFormats/Common/interface/Wrapper.h"
#include "CMGTools/HNL/interface/HNLKinematicVertexFitter.h"
#include "CMGTools/HNL/interface/HNLKalmanVertexFitter.h"

namespace {
  struct CMG_HNL {
    HNLKinematicVertexFitter hnlKinVtx_;
    HNLKalmanVertexFitter hnlKalVtx_;
  };
}