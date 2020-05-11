import os
import ROOT

from collections import OrderedDict
from ROOT import TRandom3, TFile
ROOT.gSystem.Load('libCondToolsBTau')

class BTagSF(object):
    '''Translate heppy run 1 BTagSF class to python, and update to 2012.
    '''
    def __init__ (self, seed, mc_eff_file, sf_file, wp='medium', measurement='central') :
        self.randm = TRandom3(seed)

        self.mc_eff_file = TFile(mc_eff_file)

        # b-tag SFs from POG
        calib = ROOT.BTagCalibration('deepjet', sf_file)
        
        op_dict = OrderedDict()
        op_dict['loose' ] = 0
        op_dict['medium'] = 1
        op_dict['tight' ] = 2
        
        print 'Booking b/c reader'

        v_sys = getattr(ROOT, 'vector<string>')()
        v_sys.push_back('up')
        v_sys.push_back('down')
        
        self.reader_bc = ROOT.BTagCalibrationReader(op_dict[wp], measurement, v_sys)
        self.reader_bc.load(calib, 0, 'comb')
        self.reader_bc.load(calib, 1, 'comb')
        print 'Booking light reader'
        self.reader_light = ROOT.BTagCalibrationReader(op_dict[wp], measurement, v_sys)
        self.reader_light.load(calib, 2, 'incl')

    @staticmethod
    def getBTVJetFlav(flav):
        if abs(flav) == 5:
            return 0
        elif abs(flav) == 4:
            return 1
        return 2

    def getMCBTagEff(self, pt, eta, flavor, final_state='mmm'):
        
        eta_bin = 'barrel' if abs(eta)<=1.5 else 'endcap'
        if   flavor==5: flavour_bin = 'b'
        elif flavor==4: flavour_bin = 'c'
        else          : flavour_bin = 'udsg'

        histo_name = 'eff_%s_%s_%s' %(final_state, flavour_bin, eta_bin)
        
        hist = self.mc_eff_file.Get(histo_name)
        
        binx = hist.GetXaxis().FindFixBin(pt)
        eff = hist.GetBinContent(binx)
        return eff

    def getPOGSFB(self, pt, eta, flavor):
        if flavor in [4, 5]:
            return self.reader_bc.eval_auto_bounds('central', self.getBTVJetFlav(flavor), eta, pt)

        return self.reader_light.eval_auto_bounds('central', self.getBTVJetFlav(flavor), eta, pt)

    def isBTagged(self, pt, eta, deepjet, jetflavor, is_data, deepjet_cut=0.2770, final_state='mmm'):
        jetflavor = abs(jetflavor)

        if is_data or pt < 20. or abs(eta) > 2.4:
            if deepjet > deepjet_cut:
                return True
            else:
                return False

        SFb   = self.getPOGSFB   (pt, abs(eta), jetflavor)
        eff_b = self.getMCBTagEff(pt, abs(eta), jetflavor, final_state)

        promoteProb_btag = 0. # probability to promote to tagged
        demoteProb_btag = 0. # probability to demote from tagged

        self.randm.SetSeed((int)((eta+5)*100000))
        btagged = False

        if SFb < 1.:
            demoteProb_btag = abs(1. - SFb)
        else:
            if eff_b == 0.:
                promoteProb_btag = 0.
            else:
                promoteProb_btag = abs(SFb - 1.)/((SFb/eff_b) - 1.)

        if deepjet > deepjet_cut:
            btagged = True
            if demoteProb_btag > 0. and self.randm.Uniform() < demoteProb_btag:
                btagged = False
        else:
            btagged = False
            if promoteProb_btag > 0. and self.randm.Uniform() < promoteProb_btag:
                btagged = True

        return btagged


if __name__ == '__main__':

    btag = BTagSF(
        12345, 
        mc_eff_file = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/btag/eff/btag_deepflavour_wp_medium_efficiencies_2018.root',
        sf_file     = os.environ['CMSSW_BASE'] + '/src/CMGTools/HNL/data/btag/sf/2018/DeepJet_102XSF_WP_V1.csv',
    )
    
    print 'created BTagSF instance'
    print btag.isBTagged(25., 2.3, 0.9, 5, False)
    print btag.isBTagged(104.3933, -0.885529, 0.9720, 5, False)

