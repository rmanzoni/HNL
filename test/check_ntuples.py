from glob import glob
from ROOT import TChain as tch
from ROOT import RDataFrame as rdf

# out_file = open('test_lepton_selection_bug_ntuples_17.txt', 'w')

# glob('/work/dezhu/4_production/*Data_mem/ntuples/*/HNLTreeProducer/tree.root')
# glob('/work/dezhu/4_production/*Bkg_mem/ntuples/*/HNLTreeProducer/tree.root')
# glob('/work/dezhu/4_production/*Signal_mem/ntuples/*/HNLTreeProducer/tree.root')

for ch in ['mmm', 'mem', 'eem', 'eee']:

    for ntuples in ['Data', 'Bkg', 'Signal']:

        test_files = glob('/work/dezhu/4_production/*{ntuples}_{ch}/ntuples/*/HNLTreeProducer/tree.root'.format(ntuples=ntuples, ch=ch))
        if not test_files: continue

        test_chain = tch('tree')

        for test_file in test_files:
            test_chain.Add(test_file)

        # test_frame = rdf(test_chain)

        # n_evts = test_frame.Count().GetValue()

        # n_bugs = test_frame.Filter('l0_pt == l1_pt || l0_pt == l2_pt').Count().GetValue()

        n_evts = test_chain.GetEntries()
        n_bugs = test_chain.GetEntries('l0_pt == l1_pt || l0_pt == l2_pt || l1_pt == l2_pt')

        print 'channel: {ch}, ntuples: {ntuples}, events: '.format(ntuples=ntuples, ch=ch), n_evts, ', occurrences (same pt or eta): ', n_bugs
        test_chain.Scan('l0_pt:l1_pt:l2_pt:l0_eta:l1_eta:l2_eta:l0_phi:l1_phi:l2_phi', 'l0_pt == l1_pt || l0_pt == l2_pt || l1_pt == l2_pt || l0_eta == l1_eta || l0_eta == l2_eta')


