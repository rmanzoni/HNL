import hashlib
from multiprocessing import Pool, Process, cpu_count
# from multiprocessing.dummy import Pool, Process, cpu_count

from array import array

# Adds MultiDraw method to ROOT.TTree
import CMGTools.HNL.plotter.MultiDraw

from CMGTools.HNL.plotter.PlotConfigs import HistogramCfg
from CMGTools.HNL.plotter.DataMCPlot import DataMCPlot

from CMGTools.RootTools.DataMC.Histogram import Histogram
from pdb import set_trace

from ROOT import TH1F, TFile, TTree, TTreeFormula

def initHist(hist, vcfg):
    hist.Sumw2()
    xtitle = vcfg.xtitle
    if vcfg.unit:
        xtitle += ' ({})'.format(vcfg.unit)
    hist.GetXaxis().SetTitle(xtitle)
    hist.SetStats(False)

class CreateHists(object):
    def __init__(self, hist_cfg):
        self.hist_cfg = hist_cfg
        if self.hist_cfg.vars:
            self.vcfgs = hist_cfg.vars

        if not self.vcfgs:
            print 'ERROR in createHistograms: No variable configs passed', self.hist_cfg.name

        self.plots = {}

        for vcfg in self.vcfgs:
            plot = DataMCPlot(vcfg.name)
            plot.lumi = hist_cfg.lumi
            if vcfg.name in self.plots:
                print 'Adding variable with same name twice', vcfg.name, 'not yet foreseen; taking the last'
            self.plots[vcfg.name] = plot

    def createHistograms(self, hist_cfg, all_stack=False, verbose=False,  vcfgs=None, multiprocess = True):
        '''Method to create actual histogram (DataMCPlot) instances from histogram 
        config; this version handles multiple variables via MultiDraw.
        '''
        
        print('###########################################################')
        print('# creating histograms for %i sample(s)...'%len(self.hist_cfg.cfgs))
        if multiprocess == True:
            print('# multiprocess-mode: ON')
        if multiprocess == False:
            print('# multiprocess-mode: OFF')
        print('###########################################################')

        if multiprocess == True:
            #using multiprocess to create the histograms
            pool = Pool(processes=len(self.hist_cfg.cfgs))
            result = pool.map(self.makealltheplots, self.hist_cfg.cfgs) 
       
        # DO NOT USE IT FOR PRODUCTION, ONLY FOR DEBUGGING: if we don't use multiprocess, we compute the histos one by one - good for debugging.
        if multiprocess == False:
            for i, cfg in enumerate(self.hist_cfg.cfgs):
                # result = self.makealltheplots(self.hist_cfg.cfgs[i]) 
                try:
                    result = self.makealltheplots(self.hist_cfg.cfgs[i]) 
                except:
                    set_trace()


        for i, cfg in enumerate(self.hist_cfg.cfgs):
            stack = not cfg.is_data and not cfg.is_signal
#            print(cfg.name, stack)
            for vcfg in self.vcfgs:
                try:
                    hist = result[i][vcfg.name].histos[0].obj # result[0]['CR_hnl_m_12'].histos[0]
                except:
                    try:
                        hist = result[vcfg.name].histos[0].obj # result[0]['CR_hnl_m_12'].histos[0]
                    except:
                        set_trace()
                plot = self.plots[vcfg.name]

               # hist.Scale(cfg.scale)
                if cfg.name in plot:
                    # print 'Histogram', cfg.name, 'already exists; adding...', cfg.dir_name
                    hist_to_add = Histogram(cfg.name, hist)
                    if (not cfg.is_data) and (not cfg.is_dde):
                        hist_to_add.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                        # hist_to_add.SetWeight(1)
                    plot[cfg.name].Add(hist_to_add)
                else:
#                    print(cfg.name, hist.GetEntries(), stack)
                    plot_hist = plot.AddHistogram(cfg.name, hist, stack=stack)
#                    print('added histo %s'%vcfg.name)


                    if (not cfg.is_data) and (not cfg.is_dde):
                        plot_hist.SetWeight(self.hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                        # plot_hist.SetWeight(1)
#                print(cfg.name, vcfg.name, len(plot.histos))
    
        print('###########################################################')
        print('# initializing histos done, making stacks...')
        for plot in self.plots.itervalues():
            try:
                plot._ApplyPrefs()
            except:
                set_trace() #if this error is raised, check in HNLStyle.py whether the style is defined coffectly
        print('# number of plots to draw: %i'%len(self.plots))
        print('###########################################################')


        procs = []
        for i, plot in enumerate(self.plots.itervalues()):
            proc = Process(target=plot.Draw, args=())
            procs.append(proc)
            proc.start()
     
        for proc in procs:
            proc.join()       

#        for plot in self.plots.itervalues():
#            plot._ApplyPrefs()
#            plot.Draw()

        return self.plots

    def makealltheplots(self, cfg):
        verbose=False
        all_stack=False
    #    for cfg in [hist_cfg.cfgs[0]]:
    #    for cfg in hist_cfg.cfgs:
            # First check whether it's a sub-histo or not
        if isinstance(cfg, HistogramCfg):
            hists = createHistograms(cfg, all_stack=True, vcfgs=self.vcfgs)
            for h in hists: print(h)
            for vcfg in self.vcfgs:
                hist = hists[vcfg.name]
                plot = self.plots[vcfg.name]
                hist._BuildStack(hist._SortedHistograms(), ytitle='Events')
                print('stack built')
                total_hist = plot.AddHistogram(cfg.name, hist.stack.totalHist.weighted, stack=True)

                if cfg.norm_cfg is not None:
                    norm_hist = createHistogram(cfg.norm_cfg, all_stack=True)
                    norm_hist._BuildStack(norm_hist._SortedHistograms(), ytitle='Events')
                    total_hist.Scale(hist.stack.integral/total_hist.Yield())

                if cfg.total_scale is not None:
                    total_hist.Scale(cfg.total_scale)
                    # print 'Scaling total', hist_cfg.name, 'by', cfg.total_scale
        else:
            # print('building histgrams for %s'%cfg.name)
            # It's a sample cfg

            # Now read the tree
            file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree.root'])

            # attach the trees to the first DataMCPlot
            plot = self.plots[self.vcfgs[0].name]
            try:
                ttree = plot.readTree(file_name, cfg.tree_name, verbose=verbose)
            except:
                set_trace()

            if cfg.is_dde == True:
                ttree.AddFriend('tree',cfg.fr_tree_path)
                #to test the friendtree, you can set trace here and do ttree.GetEntries('tree.fover1minusf021 > 0.01')

            #define the cuts for different stackplots
            if cfg.is_dde == True and cfg.is_singlefake == True:
                norm_cut  = self.hist_cfg.region.SF
                shape_cut = self.hist_cfg.region.SF
                norm_cut = '({c}) * {we}'.format(c=norm_cut, we='tree.fover1minusf021')
                shape_cut = '({c}) * {we}'.format(c=shape_cut, we='tree.fover1minusf021')

            if cfg.is_dde == True and cfg.is_doublefake == True:
                norm_cut  = self.hist_cfg.region.DF
                shape_cut = self.hist_cfg.region.DF

            if cfg.is_MC == True and cfg.is_MC_Conversions == False:
                norm_cut  = self.hist_cfg.region.MC
                shape_cut = self.hist_cfg.region.MC

            # if cfg.is_DY == True:
                # norm_cut  = self.hist_cfg.region.DY
                # shape_cut = self.hist_cfg.region.DY

            if cfg.is_MC_Conversions == True:
                norm_cut  = self.hist_cfg.region.MC_Conversions
                shape_cut = self.hist_cfg.region.MC_Conversions

            if cfg.is_data == True:
                norm_cut  = self.hist_cfg.region.data
                shape_cut = self.hist_cfg.region.data

            if cfg.is_signal == True:
                norm_cut  = self.hist_cfg.region.signal
                shape_cut = self.hist_cfg.region.signal

            weight = self.hist_cfg.weight
            if cfg.weight_expr:
                weight = '*'.join([weight, cfg.weight_expr])

            if self.hist_cfg.weight:
                norm_cut = '({c}) * {we}'.format(c=norm_cut, we=weight)
                shape_cut = '({c}) * {we}'.format(c=shape_cut, we=weight)



            # print '#### FULL CUT ####', norm_cut

            #adapt branch names to different software versions
            if not ttree.FindBranch("l0_reliso_rho_03"): 
                norm_cut = norm_cut.replace('l0_reliso_rho_03','l0_reliso05')
                shape_cut = shape_cut.replace('l0_reliso_rho_03','l0_reliso05')
                norm_cut = norm_cut.replace('l1_reliso_rho_03','l1_reliso05')
                shape_cut = shape_cut.replace('l1_reliso_rho_03','l1_reliso05')
                norm_cut = norm_cut.replace('l2_reliso_rho_03','l2_reliso05')
                shape_cut = shape_cut.replace('l2_reliso_rho_03','l2_reliso05')
 
            if not ttree.FindBranch("hnl_iso03_rel_rhoArea"): 
                norm_cut = norm_cut.replace('hnl_iso04_rel_rhoArea','hnl_iso_rel')
                shape_cut = shape_cut.replace('hnl_iso04_rel_rhoArea','hnl_iso_rel')


            # Initialise all hists before the multidraw
            hists = {}

            for vcfg in self.vcfgs:
                # hname = '_'.join([self.hist_cfg.name, hashlib.md5(self.hist_cfg.cut).hexdigest(), cfg.name, vcfg.name, cfg.dir_name])
                hname = '_'.join([self.hist_cfg.name, hashlib.md5(norm_cut).hexdigest(), cfg.name, vcfg.name, cfg.dir_name])
                if any(str(b) == 'xmin' for b in vcfg.binning):
                    hist = TH1F(hname, '', vcfg.binning['nbinsx'],
                                vcfg.binning['xmin'], vcfg.binning['xmax'])
                else:
                    hist = TH1F(hname, '', len(vcfg.binning)-1, vcfg.binning)

                initHist(hist, vcfg)
                hists[vcfg.name] = hist


            var_hist_tuples = []

            for vcfg in self.vcfgs:
                var_hist_tuples.append('{var} >> {hist}'.format(var=vcfg.drawname, hist=hists[vcfg.name].GetName()))

                        

            # Implement the multidraw.
            # set_trace()
            try:
                print 'drawing %s with the following cut: '%(cfg.name) + norm_cut
                ttree.MultiDraw(var_hist_tuples, norm_cut)
            except:
                set_trace()
        

            # Do another multidraw here, if needed, and reset the scales in a separate loop
            if shape_cut != norm_cut:
                scale = hist.Integral()
                ttree.Project(hname, vcfg.drawname, shape_cut)
                try:
                    hist.Scale(scale/hist.Integral())
                except:
                    set_trace()

            stack = all_stack or (not cfg.is_data and not cfg.is_signal)


            # Loop again over the variables and add histograms to self.plots one by one
            for vcfg in self.vcfgs:
                hist = hists[vcfg.name]
                plot = self.plots[vcfg.name]

                hist.Scale(cfg.scale)

                if cfg.name in plot:
                    # print 'Histogram', cfg.name, 'already exists; adding...', cfg.dir_name
                    hist_to_add = Histogram(cfg.name, hist)
                    if (not cfg.is_data) and (not cfg.is_dde):
                        hist_to_add.SetWeight(self.hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                        # hist_to_add.SetWeight(1)
    
                    plot[cfg.name].Add(hist_to_add)
                else:
#                    print(cfg.name, hist.GetEntries(), stack)
                    plot_hist = plot.AddHistogram(cfg.name, hist, stack=stack)
#                    print('added histo %s for %s'%(vcfg.name,cfg.name))

                    if (not cfg.is_data) and (not cfg.is_dde):
                        plot_hist.SetWeight(self.hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                        # plot_hist.SetWeight(1)
            print('added histograms for %s'%cfg.name)
            PLOTS = self.plots
        return PLOTS
