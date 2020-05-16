from PhysicsTools.Heppy.physicsobjects.PhysicsObject import *
from PhysicsTools.Heppy.physicsutils.EffectiveAreas import is_ea_table, effective_area

import ROOT

class Lepton( PhysicsObject):

    def ip3D(self):
        '''3D impact parameter value.'''
        return abs(self.dB(self.PV3D))
 
    def sip3D(self):
        '''3D impact parameter significance.'''
        db, edb = self.dB(self.PV3D), self.edB(self.PV3D)
        return abs(db/edb) if edb > 0 else 999.

    def absIso(self, cone_size, iso_type, dbeta_factor=None, 
               area_table=None, all_charged = False):
        iso_ch = None
        if all_charged:
            iso_ch = self.chargedAllIso(cone_size)
        else:
            iso_ch = self.chargedHadronIso(cone_size)
        iso_photon = self.photonIso(cone_size)
        iso_nh = self.neutralHadronIso(cone_size)
        corr_neutral = None
        if iso_type == 'EA':
            if dbeta_factor:  
                raise ValueError('using EA iso, do not specify dbeta_factor')
            else:
                area_cone_size = str(cone_size).replace('.','')
                area = self.effective_area(area_cone_size, area_table)
            corr_neutral = self.rho * area
        elif iso_type == 'dbeta': 
            if area_table: 
                raise ValueError('using delta beta iso, do not specify area table')
            if dbeta_factor is None: 
                raise ValueError('using delta beta iso, provide dbeta_factor')
            iso_photon = self.photonIso(cone_size)
            iso_ch = self.chargedHadronIso(cone_size)
            iso_nh = self.neutralHadronIso(cone_size)
            iso_puch =  self.puChargedHadronIso(cone_size)
            corr_neutral = dbeta_factor * iso_puch
        elif iso_type == 'raw':
            if area_table or dbeta_factor: 
                raise ValueError('using raw iso, do not specify area table, or dbeta factor')
            corr_neutral = 0.
        else: 
            raise ValueError('unknown isolation type: '+iso_type)
        return iso_ch + max(0., iso_photon + iso_nh - corr_neutral)     

    def relIso(self, cone_size, iso_type, dbeta_factor=None,
               area_table=None, all_charged = False):
        return self.absIso(cone_size, iso_type, 
                           dbeta_factor=dbeta_factor, 
                           area_table=area_table, 
                           all_charged=all_charged) / self.pt()

    def effective_area(self, area_cone_size, area_table):
        '''Return effective area for this lepton. 
        area_cone_size: should be e.g. '03' or '04'.
        area_table: defines the table of effective areas. 
        It can either be a string EffectiveArea+area_cone_size, e.g. EffectiveArea03, 
        or have be a dict like: 
        
         { '03' : 
              [ (1.000, 0.13),
              (1.479, 0.14),
              (2.000, 0.07),
              (2.200, 0.09),
              (2.300, 0.11),
              (2.400, 0.11),
              (2.500, 0.14) ],
           '04' : 
              [ (1.000, 0.208),
              (1.479, 0.209),
              (2.000, 0.115),
              (2.200, 0.143),
              (2.300, 0.183),
              (2.400, 0.194),
              (2.500, 0.261) ],
           'eta' : lambda x: x.superCluster().eta()
         }
        
        Please see PhysicsTools/Heppy/python/physicsutils/EffectiveAreas.py for 
        more information.

        If a string is provided, the corresponding attribute must be added to the 
        Lepton object beforehand: lepton.EffectiveArea03 = <the_area_table>, 
        or to its class: Electron.EffectiveArea03 = <the_area_table>. 
        '''
        if area_table and not is_ea_table(area_table):
            raise ValueError('area_table is not an area table')
        if area_table is None: 
            # area table not provided by the user as argument to the isolation method.
            # try to find it in the object or its class
            ea_attr_name = ''.join(['EffectiveArea',area_cone_size])
            area_table = getattr(self, ea_attr_name, None)
            if area_table is None: 
                area_table = getattr(self.__class__, ea_attr_name, None)
                if area_table is None: 
                    raise ValueError(ea_attr_name + ' not found. It should be added to the lepton object as an attribute or a class attribute.')
        return effective_area(self, area_cone_size, area_table)


    def absIsoFromEA(self, dRCone):
        '''Calculate Isolation using the effective area approach.'''
        return self.chargedHadronIso(dRCone) + max( 0., self.photonIso(dRCone) + self.neutralHadronIso(dRCone) - self.offsetEA(dRCone) )            

    def offsetEA(self, dRCone):
        area = 0.0
        eta = self.eta()
	# muons
	if self.pdgId() % 13 == 0:
		if abs(eta) < 0.8000: area = 0.0566
		if abs(eta) > 0.8000 and abs(eta) < 1.3000: area = 0.0562
		if abs(eta) > 1.3000 and abs(eta) < 2.0000: area = 0.0363
		if abs(eta) > 2.0000 and abs(eta) < 2.2000: area = 0.0119
		if abs(eta) > 2.2000 and abs(eta) < 2.4000: area = 0.0064
	# electrons  # from Tom / Martina https://github.com/cms-sw/cmssw/blob/master/RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_94X.txt
	if self.pdgId() % 11 == 0: 
		if abs(eta) < 1.0000: area = 0.1440
		if abs(eta) > 1.0000 and abs(eta) < 1.4790: area = 0.1562
		if abs(eta) > 1.4790 and abs(eta) < 2.0000: area = 0.1032
		if abs(eta) > 2.0000 and abs(eta) < 2.2000: area = 0.0859
		if abs(eta) > 2.2000 and abs(eta) < 2.3000: area = 0.1116
		if abs(eta) > 2.3000 and abs(eta) < 2.4000: area = 0.1321
		if abs(eta) > 2.4000 and abs(eta) < 2.5000: area = 0.1654
	
	if dRCone != 0.3: area *= ( (dRCone ** 2) / (0.3 **2) )
        return area * self.rho

    def relIsoFromEA(self, dRCone):
        return self.absIsoFromEA(dRCone)/self.pt() if self.pt()>0 else -999
    
    def lostInner(self):
        if hasattr(self.innerTrack(),"trackerExpectedHitsInner") :
		return self.innerTrack().trackerExpectedHitsInner().numberOfLostHits()
	else :	
		return self.innerTrack().hitPattern().numberOfLostHits(ROOT.reco.HitPattern.MISSING_INNER_HITS)	

    def p4WithFSR(self):
        ret = self.p4()
        for p in getattr(self, 'ownFsrPhotons', getattr(self, 'fsrPhotons', [])):
            ret += p.p4()
        return ret

    def __str__(self):
        ptc = super(Lepton, self).__str__()
        return '{ptc}, iso={iso:5.2f}'.format(ptc=ptc, 
                                              iso=self.relIso(0.4, 'dbeta', dbeta_factor=0.5))
