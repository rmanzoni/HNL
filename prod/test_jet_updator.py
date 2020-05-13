import ROOT
from array import array
from collections import OrderedDict
from DataFormats.FWLite import Events, Handle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Jet, GenJet

# events = Events('output.root')
# events = Events('output_ttbar2017_102X_mc2017_realistic_v7.root')
# events = Events('output_ttbar2017_94X_mc2017_realistic_v17.root')
events = Events('../python/output.root')

maxevents = -1 # max events to process
totevents = events.size() # total number of events in the files

label_jets = ('slimmedJets', '', 'PAT')
handle_jets = Handle('std::vector<pat::Jet>')

label_jets_up = ('selectedUpdatedPatJetsNewDFTraining', '', 'NEWDF')
handle_jets_up = Handle('std::vector<pat::Jet>')

# start looping on the events
for i, ev in enumerate(events):
    
    ######################################################################################
    # controls on the events being processed
    if maxevents>0 and i>maxevents:
        break
        
    if i%100==0:
        print '===> processing %d / %d event' %(i, totevents)
    
    ######################################################################################
    # access the jets
    ev.getByLabel(label_jets, handle_jets)
    jets = map(Jet, handle_jets.product())

    ev.getByLabel(label_jets_up, handle_jets_up)
    jets_up = map(Jet, handle_jets_up.product())
    
    for jet in jets + jets_up:
        jet.deepflavour_prob_b    = jet.btag('pfDeepFlavourJetTags:probb')
        jet.deepflavour_prob_bb   = jet.btag('pfDeepFlavourJetTags:probbb')
        jet.deepflavour_prob_lepb = jet.btag('pfDeepFlavourJetTags:problepb')
        jet.deepflavour_score = jet.deepflavour_prob_b   + \
                                jet.deepflavour_prob_bb  + \
                                jet.deepflavour_prob_lepb
    
    print 'normal jets'
    for jet in jets:
        print jet, '\t', jet.partonFlavour(), '\t', jet.deepflavour_score

    print 'updated jets'
    for jet in jets_up:
        print jet, '\t', jet.partonFlavour(), '\t', jet.deepflavour_score
        
    import pdb ; pdb.set_trace()
    
    
