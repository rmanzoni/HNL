import numpy as np
from collections import OrderedDict
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.statistics.average import Average

from CMGTools.HNL.utils.ScaleFactor import ScaleFactor

class MultiLeptonWeighter(Analyzer):

    '''Gets lepton efficiency weight and puts it in the event'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(MultiLeptonWeighter, self).__init__(cfg_ana, cfg_comp, looperName)

        self.getter     = self.cfg_ana.getter 
        self.finalState = self.cfg_ana.finalState

        self.scaleFactors = OrderedDict()
        
        for ii in xrange(3):
            self.scaleFactors[ii] = OrderedDict()
            for sf_name, sf_file in getattr(self.cfg_ana, 'scaleFactor_l%d'%ii).iteritems():
                self.scaleFactors[ii][sf_name] = ScaleFactor(sf_file[0], sf_file[1])


    def beginLoop(self, setup):
        print self, self.__class__
        super(MultiLeptonWeighter, self).beginLoop(setup)
        
        # total per-event average weight
        self.averages.add('weight_%s' %self.finalState, Average('weight_%s' %self.finalState))

        # per-lepton and per-component weight
        for ii in xrange(3):
            self.averages.add('weight_%s_l%d' %(self.finalState, ii), Average('weight_%s_l%d' %(self.finalState, ii) ))
            for sf_name in self.scaleFactors[ii].keys():
                self.averages.add('weight_%s_l%d_%s' %(self.finalState, ii, sf_name), Average('weight_%s_l%d_%s' %(self.finalState, ii, sf_name)))
        
    def process(self, event):
                        
        # don't run if not needed
        if not (self.cfg_comp.isMC or self.cfg_comp.isEmbed):
            return True
        if getattr(self.cfg_ana, 'disable', False):
            return True
        if not eval(self.cfg_ana.skimFunction):
            return True
                        
        # get the leptons
        l0 = self.getter(event).l0()                
        l1 = self.getter(event).l1()                
        l2 = self.getter(event).l2()                

        # initialise final state specific trigger weight
        setattr(event, 'triggerWeight_%s' %self.finalState, getattr(event, 'triggerWeight_%s' %self.finalState, 1.))
        
        # Get the scale factors and apply them
        isFake = False # only weighing genuine leptons
        for ii, ilep in enumerate([l0, l1, l2]):            
            # initialise the lepton weight to 1.
            setattr(ilep, 'weight_%s' %self.finalState, 1.)
            for sf_name, sf in self.scaleFactors[ii].iteritems():
                # initialise each lepton weight to 1
                setattr(ilep, 'weight_%s_%s' %(self.finalState, sf_name), 1.)
                # lepton kinematics and iso, etc...
                pt    = ilep.pt()
                eta   = ilep.eta()
                # FIXME! doesn't work when passing iso and dm, check if these are the right SFs
                # pdgid = abs(ilep.pdgId())
                # dm    = ilep.decayMode() if hasattr(ilep, 'decayMode') else None # only relevant for taus
                # iso   = ilep.relIso(cone_size    = (0.4*(pdgid==13) + 0.3 * (pdgid==11)), 
                #                     iso_type     = 'dbeta',
                #                     dbeta_factor = 0.5,
                #                     all_charged  = 0) # different cones for ele and mu
                # import pdb ; pdb.set_trace()
                # scale_factor = sf.getScaleFactor(pt, eta, isFake, iso=iso, dm=dm)
                scale_factor = sf.getScaleFactor(pt, eta)
                setattr(ilep, 'weight_%s_%s' %(self.finalState, sf_name), scale_factor)
                # apply the weight
                current_weight = getattr(ilep, 'weight_%s' %self.finalState)
                new_weight     = current_weight * scale_factor
                setattr(ilep, 'weight_%s' %self.finalState, new_weight)
                # per-event trigger weight
                if 'trigger' in sf_name:
                    current_trigger_weight = getattr(event, 'triggerWeight_%s' %self.finalState)
                    new_trigger_weight = current_trigger_weight * scale_factor
                    setattr(event, 'triggerWeight_%s' %self.finalState, new_trigger_weight)
                # update the per-lepton and per-component weight
                self.averages['weight_%s_l%d_%s' %(self.finalState, ii, sf_name)].add(scale_factor)
                # update the per-lepton weight
                self.averages['weight_%s_l%d' %(self.finalState, ii)].add(scale_factor)

        # product of all lepton weights, ID and trigger
        event_weight = np.product([getattr(ilep, 'weight_%s' %self.finalState) for ilep in [l0, l1, l2]])
        
        # set it as an event weight
        setattr(event, 'weight_%s' %self.finalState, event_weight)

        # and update the per event average weight
        self.averages['weight_%s' %self.finalState].add(event_weight)
