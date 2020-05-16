from CMGTools.HNL.physicsobjects.Lepton import Lepton
from PhysicsTools.HeppyCore.utils.deltar import deltaR
import ROOT
import sys
from math import exp

def raw_to_normalized(raw):
    return 2.0/(1.0+exp(-2.0*raw))-1

class Electron( Lepton ):

    def __init__(self, *args, **kwargs):
        '''Lightweight Electron'''
        super(Electron, self).__init__(*args, **kwargs)
        self._physObjInit()

    def _physObjInit(self):
        self.associatedVertex = None
        self.rho              = None
        self.rhoHLT           = None

    def dEtaInSeed(self):
        if self.physObj.superCluster().isNonnull() and self.physObj.superCluster().seed().isNonnull(): return self.physObj.deltaEtaSuperClusterTrackAtVtx() - self.physObj.superCluster().eta() + self.physObj.superCluster().seed().eta()
        else: return sys.float_info.max

    def normalizedGsfChi2(self):
        if self.physObj.gsfTrack().isNonnull(): return self.physObj.gsfTrack().normalizedChi2()
        else: return sys.float_info.max

    def hltPFIso(self,isoType):
        SCEta = abs(self.superCluster().eta())
        hltEA = 0.0
        if isoType == 'ECALPFIsoEA': hltEA = 0.165 if SCEta < 1.4790 else 0.132
        elif isoType == 'HCALPFIsoEA': hltEA = 0.060 if SCEta < 1.4790 else 0.131
        if 'ECALPFIso' in isoType: isoValue = self.ecalPFClusterIso()
        elif 'HCALPFIso' in isoType: isoValue = self.hcalPFClusterIso()
        else: isoValue = -999
        return max(0, isoValue - self.rhoHLT*hltEA)

    def chargedHadronIso(self,R=0.4):
        if   R == 0.3: return self.physObj.pfIsolationVariables().sumChargedHadronPt
        elif R == 0.4: return self.physObj.chargedHadronIso()
        raise RuntimeError("Electron chargedHadronIso missing for R=%s" % R)

    def neutralHadronIso(self,R=0.4):
        if   R == 0.3: return self.physObj.pfIsolationVariables().sumNeutralHadronEt
        elif R == 0.4: return self.physObj.neutralHadronIso()
        raise RuntimeError("Electron neutralHadronIso missing for R=%s" % R)

    def photonIso(self,R=0.4):
        if   R == 0.3: return self.physObj.pfIsolationVariables().sumPhotonEt
        elif R == 0.4: return self.physObj.photonIso()
        raise RuntimeError("Electron photonIso missing for R=%s" % R)

    def chargedAllIso(self,R=0.4):
        if   R == 0.3: return self.physObj.pfIsolationVariables().sumChargedParticlePt
        raise RuntimeError("Electron chargedAllIso missing for R=%s" % R)

    def puChargedHadronIso(self,R=0.4):
        if   R == 0.3: return self.physObj.pfIsolationVariables().sumPUPt
        elif R == 0.4: return self.physObj.puChargedHadronIso()
        raise RuntimeError("Electron chargedHadronIso missing for R=%s" % R)

    def absIsoWithFSR(self, R=0.4, puCorr="rhoArea", dBetaFactor=0.5):
        '''
        Calculate Isolation, subtract FSR, apply specific PU corrections" 
        '''
        photonIso = self.photonIso(R)
        if hasattr(self,'fsrPhotons'):
            for gamma in self.fsrPhotons:
                dr = deltaR(gamma.eta(), gamma.phi(), self.physObj.eta(), self.physObj.phi())
                if (self.isEB() or dr > 0.08) and dr < R:
                    photonIso = max(photonIso-gamma.pt(),0.0)                
        if puCorr == "deltaBeta":
            offset = dBetaFactor * self.puChargedHadronIso(R)
        elif puCorr == "rhoArea":
            offset = self.rho*getattr(self,"EffectiveArea"+(str(R).replace(".","")))
        elif puCorr in ["none","None",None]:
            offset = 0
        else:
             raise RuntimeError("Unsupported PU correction scheme %s" % puCorr)
        return self.chargedHadronIso(R)+max(0.,photonIso+self.neutralHadronIso(R)-offset)            

    def dxy(self, vertex=None):
        '''Returns dxy.
        Computed using vertex (or self.associatedVertex if vertex not specified),
        and the gsf track.
        '''
        if vertex is None:
            vertex = self.associatedVertex
        return self.gsfTrack().dxy( vertex.position() )

    def edxy(self):
        '''returns the uncertainty on dxy (from gsf track)'''
        return self.gsfTrack().dxyError()

    def p4(self):
        return ROOT.reco.Candidate.p4(self.physObj)

    def dz(self, vertex=None):
        '''Returns dz.
        Computed using vertex (or self.associatedVertex if vertex not specified),
        and the gsf track.
        '''
        if vertex is None:
            vertex = self.associatedVertex
        return self.gsfTrack().dz( vertex.position() )

    def edz(self):
        '''returns the uncertainty on dxz (from gsf track)'''
        return self.gsfTrack().dzError()

    def lostInner(self) :
        if hasattr(self.gsfTrack(),"trackerExpectedHitsInner") :
            return self.gsfTrack().trackerExpectedHitsInner().numberOfLostHits()
        else :
            return self.gsfTrack().hitPattern().numberOfLostHits(ROOT.reco.HitPattern.MISSING_INNER_HITS)

    def validCandidateP4Kind(self):
        raw = self.physObj.candidateP4Kind()
        return raw in (0,1,2) 

    def ptErr(self):
        return self.p4Error(self.candidateP4Kind())*self.pt()/self.p() if self.validCandidateP4Kind() else None

    ###################################
               ## HNL IDs ##
    ###################################

    def f_hadronicOverEM(self):       
        hOverE_CE = 1.12 if self.isEB() else 0.5
        hOverE_Cr = 0.0368 if self.isEB() else 0.201
        return self.hadronicOverEm() - (hOverE_CE  + hOverE_Cr * self.rho)/(self.superCluster().energy())

    def f_InvEminusInvP(self):        
        return abs(1.0/self.ecalEnergy() - self.eSuperClusterOverP()/self.ecalEnergy()) if self.ecalEnergy()>0. else 9e9

    # LooseNoIso
    def LooseNoIsoID(self):

        if not (self.isEB() or self.isEE())                                                       : return False
        if (self.full5x5_sigmaIetaIeta()               >= ( 0.11    if self.isEB() else 0.0314 ) ): return False
        if (abs(self.dEtaInSeed())                     >= ( 0.00477 if self.isEB() else 0.00868) ): return False
        if (abs(self.deltaPhiSuperClusterTrackAtVtx()) >= ( 0.222   if self.isEB() else 0.213  ) ): return False
        if (self.f_hadronicOverEM()                    >= ( 0.298   if self.isEB() else 0.101  ) ): return False
        if (self.f_InvEminusInvP()                     >= ( 0.241   if self.isEB() else 0.14   ) ): return False

        return True

    # MediumNoIso
    def MediumNoIsoID(self):

        if not (self.isEB() or self.isEE())                                                       : return False
        if (self.full5x5_sigmaIetaIeta()               >= ( 0.00998 if self.isEB() else 0.0298 ) ): return False
        if (abs(self.dEtaInSeed())                     >= ( 0.00311 if self.isEB() else 0.00609) ): return False
        if (abs(self.deltaPhiSuperClusterTrackAtVtx()) >= ( 0.103   if self.isEB() else 0.045  ) ): return False
        if (self.f_hadronicOverEM()                    >= ( 0.253   if self.isEB() else 0.0878 ) ): return False
        if (self.f_InvEminusInvP()                     >= ( 0.134   if self.isEB() else 0.13   ) ): return False

        return True

    # MediumWithIso
    def MediumWithIsoID(self):

        if not (self.isEB() or self.isEE())                                                       : return False
        if (self.full5x5_sigmaIetaIeta()               >= ( 0.00998 if self.isEB() else 0.0292 ) ): return False
        if (abs(self.dEtaInSeed())                     >= ( 0.00308 if self.isEB() else 0.00605) ): return False
        if (abs(self.deltaPhiSuperClusterTrackAtVtx()) >= ( 0.0816  if self.isEB() else 0.0394 ) ): return False
        if (self.f_hadronicOverEM()                    >= ( 0.0414  if self.isEB() else 0.0641 ) ): return False
        if (self.f_InvEminusInvP()                     >= ( 0.0129  if self.isEB() else 0.0129 ) ): return False      
            
        return True
