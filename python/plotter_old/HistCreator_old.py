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

def createHistogram(hist_cfg, all_stack=False, verbose=False, friend_func=None):
    '''Method to create actual histogram (DataMCPlot) instance from histogram 
    config.
    '''
    plot = DataMCPlot(hist_cfg.var.name)
    plot.lumi = hist_cfg.lumi
    vcfg = hist_cfg.var
    for cfg in hist_cfg.cfgs:
        # First check whether it's a sub-histo or not
        if isinstance(cfg, HistogramCfg):
            hist = createHistogram(cfg, all_stack=True)
            hist._BuildStack(hist._SortedHistograms(), ytitle='Events')

            total_hist = plot.AddHistogram(cfg.name, hist.stack.totalHist.weighted, stack=True)

            if cfg.norm_cfg is not None:
                norm_hist = createHistogram(cfg.norm_cfg, all_stack=True)
                norm_hist._BuildStack(norm_hist._SortedHistograms(), ytitle='Events')
                total_hist.Scale(hist.stack.integral/total_hist.Yield())

            if cfg.total_scale is not None:
                total_hist.Scale(cfg.total_scale)
        else:
            # It's a sample cfg
            hname = '_'.join([hist_cfg.name, hashlib.md5(hist_cfg.cut).hexdigest(), cfg.name, vcfg.name, cfg.dir_name])
            if any(str(b) == 'xmin' for b in vcfg.binning):
                hist = TH1F(hname, '', vcfg.binning['nbinsx'],
                            vcfg.binning['xmin'], vcfg.binning['xmax'])
            else:
                hist = TH1F(hname, '', len(vcfg.binning)-1, vcfg.binning)

            initHist(hist, vcfg)

            file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree.root'])

            ttree = plot.readTree(file_name, cfg.tree_name, verbose=verbose, friend_func=friend_func)

            norm_cut = hist_cfg.cut
            shape_cut = hist_cfg.cut

            if cfg.norm_cut:
                norm_cut = cfg.norm_cut

            if cfg.shape_cut:
                shape_cut = cfg.shape_cut

            if cfg.cut_replace_func:
                norm_cut = cfg.cut_replace_func(norm_cut)
                shape_cut = cfg.cut_replace_func(norm_cut)

            weight = hist_cfg.weight
            if cfg.weight_expr:
                weight = '*'.join([weight, cfg.weight_expr])

            if hist_cfg.weight:
                norm_cut = '({c}) * {we}'.format(c=norm_cut, we=weight)
                shape_cut = '({c}) * {we}'.format(c=shape_cut, we=weight)

            ttree.Project(hname, vcfg.drawname, norm_cut)

            if shape_cut != norm_cut:
                scale = hist.Integral()
                ttree.Project(hname, vcfg.drawname, shape_cut)
                hist.Scale(scale/hist.Integral())

            stack = all_stack or (not cfg.is_data and not cfg.is_signal)

            hist.Scale(cfg.scale)

            if cfg.name in plot:
                # print 'Histogram', cfg.name, 'already exists; adding...', cfg.dir_name
                hist_to_add = Histogram(cfg.name, hist)
                if (not cfg.is_data) and (not cfg.is_dde):
                    hist_to_add.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                if cfg.is_dde:
                    # hist_to_add.SetWeight(hist_to_add.obj.GetEntries()/cfg.sumweights)
                    hist_to_add.SetWeight(cfg.sumweights)
                plot[cfg.name].Add(hist_to_add)
            else:
                plot_hist = plot.AddHistogram(cfg.name, hist, stack=stack)

                if (not cfg.is_data) and (not cfg.is_dde):
                    plot_hist.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                if cfg.is_dde:
                    # plot_hist.SetWeight(plot_hist.obj.GetEntries()/cfg.sumweights)
                    plot_hist.SetWeight(cfg.sumweights)

    plot._ApplyPrefs()
    return plot


def fillIntoTree(out_tree, branches, cfg, hist_cfg, vcfgs, total_scale, plot, verbose, friend_func):
    if isinstance(cfg, HistogramCfg):
        # Loop over sub-cfgs and fill them
        total_scale *= cfg.total_scale if cfg.total_scale else 1.
        for sub_cfg in cfg.cfgs:
            fillIntoTree(out_tree, branches, sub_cfg, cfg, vcfgs, total_scale, plot, verbose, friend_func)
        return

    file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree.root'])

    # Attaches tree to plot
    ttree = plot.readTree(file_name, cfg.tree_name, verbose=verbose, friend_func=friend_func)

    norm_cut = hist_cfg.cut
    shape_cut = hist_cfg.cut

    if cfg.norm_cut:
        norm_cut = cfg.norm_cut

    if cfg.shape_cut:
        shape_cut = cfg.shape_cut

    full_weight = branches[-1]

    weight = hist_cfg.weight
    if cfg.weight_expr:
        weight = '*'.join([weight, cfg.weight_expr])

    if hist_cfg.weight:
        norm_cut = '({c}) * {we}'.format(c=norm_cut, we=weight)
        shape_cut = '({c}) * {we}'.format(c=shape_cut, we=weight)

    # and this one too
    sample_weight = cfg.scale * total_scale
    if not cfg.is_data:
        sample_weight *= hist_cfg.lumi*cfg.xsec/cfg.sumweights

    formula = TTreeFormula('weight_formula', norm_cut, ttree)
    formula.GetNdata()

    # Add weight as tree variable
    # Then loop over ttree
    # And save this to the other tree
    # 

    # Create TTreeFormulas for all vars
    for var in vcfgs:
        if var.drawname != var.name:
            var.formula = TTreeFormula('formula'+var.name, var.drawname, ttree)
            var.formula.GetNdata()

    for i in xrange(ttree.GetEntries()):
        ttree.GetEntry(i)
        w = formula.EvalInstance()
        if w == 0.:
            continue
        full_weight[0] = w * sample_weight
        if abs(full_weight[0]) > 1000.:
            print "WARNING, unusually large weight", w, sample_weight
            import pdb; pdb.set_trace()
            print '\nWeight:', full_weight[0]
            print cfg.name
            print norm_cut
        for branch, var in zip(branches, vcfgs):
            branch[0] = var.formula.EvalInstance() if hasattr(var, 'formula') else getattr(ttree, var.name)
        out_tree.Fill()


    if shape_cut != norm_cut:
        print 'WARNING: different norm and shape cuts currently not supported in HistCreator.createTrees'


def createTrees(hist_cfg, out_dir, verbose=False, friend_func=None):
    '''Writes out TTrees from histogram configuration for each contribution. 
    Takes list of variables attached to histogram config (hist_cfg.vars) to 
    create branches.
    '''
    plot = DataMCPlot(hist_cfg.name) # Used to cache TTrees
    vcfgs = hist_cfg.vars
    for cfg in hist_cfg.cfgs:
        
        out_file = TFile('/'.join([out_dir, hist_cfg.name + '_' + cfg.name + '.root']), 'RECREATE')
        out_tree = TTree('tree', '')

        # Create branches for all variables
        branches = [array('f', [0.]) for i in xrange(len(vcfgs))]
        for branch_name, branch in zip([v.name for v in vcfgs], branches):
            out_tree.Branch(branch_name, branch, branch_name+'/F')

        # Create branch with full weight including lumi x cross section
        full_weight = array('f', [0.])
        out_tree.Branch('full_weight', full_weight, 'full_weight/F')
        branches.append(full_weight)

        total_scale = hist_cfg.total_scale if hist_cfg.total_scale else 1.
        fillIntoTree(out_tree, branches, cfg, hist_cfg, vcfgs, total_scale, plot, verbose, friend_func)

        out_file.cd()
        out_tree.Write()
        out_file.Write()
        out_file.Close()
    return plot

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

    def createHistograms(self, hist_cfg, all_stack=False, verbose=False, friend_func=None, vcfgs=None, multiprocess = True):
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
       
        # if we don't use multiprocess, we compute the histos one by one - good for debugging.
        if multiprocess == False:
            for i, cfg in enumerate(self.hist_cfg.cfgs):
                # result = self.makealltheplots(self.hist_cfg.cfgs[i]) 
                try:
                    result = self.makealltheplots(self.hist_cfg.cfgs[i]) 
                except:
                    set_trace()

#        workers = cpu_count()
#        result = []
#        batches = len(self.hist_cfg.cfgs) / workers + 1 if len(self.hist_cfg.cfgs) % workers != 0 else len(self.hist_cfg.cfgs) / workers
#        pool = Pool(processes=batches)
#        print('number of batches for filling histos (%i samples each): %i'%(workers, batches))
#        for i in range(batches):
#           try:    histlist = self.hist_cfg.cfgs[i*workers:(i+1)*workers] 
#           except: print('entering exception'); histlist = self.hist_cfg.cfgs[(batches-1)*workers:len(self.hist_cfg.cfgs)-1]
#           result += pool.map(self.makealltheplots, histlist)

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
#                hist = hists[vcfg.name]
                plot = self.plots[vcfg.name]

#                hist.Scale(cfg.scale)
                if cfg.name in plot:
                    # print 'Histogram', cfg.name, 'already exists; adding...', cfg.dir_name
                    hist_to_add = Histogram(cfg.name, hist)
                    if (not cfg.is_data) and (not cfg.is_dde):
                        hist_to_add.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                    plot[cfg.name].Add(hist_to_add)
                    if cfg.is_dde:
                        try:
                            # hist_to_add.SetWeight(hist_to_add.obj.GetEntries()/cfg.sumweights)
                            hist_to_add.SetWeight(cfg.sumweights)
                        except:
                            set_trace()
                else:
#                    print(cfg.name, hist.GetEntries(), stack)
                    plot_hist = plot.AddHistogram(cfg.name, hist, stack=stack)
#                    print('added histo %s'%vcfg.name)


                    if (not cfg.is_data) and (not cfg.is_dde):
                        plot_hist.SetWeight(self.hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                    if cfg.is_dde:
                        # plot_hist.SetWeight(plot_hist.obj.GetEntries()/cfg.sumweights)
                        plot_hist.SetWeight(cfg.sumweights)
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
        friend_func=None
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
                set_trace()
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
            if cfg.dir_name == "DDE":
                # file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree_fr_DR_data_v2.root'])
                file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree_fr_DR_data_v2_oldVars.root'])

            else:
                file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree.root'])

            # attach the trees to the first DataMCPlot
            plot = self.plots[self.vcfgs[0].name]
            try:
                ttree = plot.readTree(file_name, cfg.tree_name, verbose=verbose, friend_func=friend_func)
            except:
                set_trace()

            set_trace()
            norm_cut = self.hist_cfg.cut
            shape_cut = self.hist_cfg.cut
            set_trace()

            if cfg.norm_cut:
#                norm_cut = cfg.norm_cut
                norm_cut += cfg.norm_cut  # to add met filters only for data
#            print('sample = %s, cuts = %s'%(cfg.name, norm_cut))
            if cfg.shape_cut:
                shape_cut = cfg.shape_cut

            weight = self.hist_cfg.weight
            if cfg.weight_expr:
                weight = '*'.join([weight, cfg.weight_expr])

            if cfg.cut_replace_func:
                norm_cut = cfg.cut_replace_func(norm_cut)
                shape_cut = cfg.cut_replace_func(norm_cut)


            #if needed, apply the loose selection for the non-prompt region
            if cfg.is_dde == True:
                norm_cut = norm_cut.replace('l1_reliso_rho_04 < 0.15 & l2_reliso_rho_04 < 0.15 & hnl_iso04_rel_rhoArea < 1','(l1_reliso05 > 0.15 | l2_reliso05 > 0.15) & hnl_iso04_rel_rhoArea < 1')
                shape_cut = shape_cut.replace('l1_reliso_rho_04 < 0.15 & l2_reliso_rho_04 < 0.15 & hnl_iso04_rel_rhoArea < 1','(l1_reliso05 > 0.15 | l2_reliso05 > 0.15) & hnl_iso04_rel_rhoArea < 1')

            if 'Conversion' in cfg.name:
                norm_cut = norm_cut + ' & (l0_gen_match_pdgid == 22 | l1_gen_match_pdgid == 22 | l2_gen_match_pdgid ==22)'
                shape_cut = shape_cut + ' & (l0_gen_match_pdgid == 22 | l1_gen_match_pdgid == 22 | l2_gen_match_pdgid ==22)'

            if self.hist_cfg.weight:
                norm_cut = '({c}) * {we}'.format(c=norm_cut, we=weight)
                shape_cut = '({c}) * {we}'.format(c=shape_cut, we=weight)

            #insert the fake rate weight for doublefakes
            if cfg.is_dde == True and cfg.is_doublefake == True:
                norm_cut = '({c}) * {we}'.format(c=norm_cut, we='weight_fr/(1-weight_fr)')
                shape_cut = '({c}) * {we}'.format(c=shape_cut, we='weight_fr/(1-weight_fr)')

            #insert the fake rate weight for singlefakes
            if cfg.is_dde == True and cfg.is_singlefake == True:
                norm_cut = '({c}) * {we}'.format(c=norm_cut, we='((weight_fr/(1-weight_fr))-((weight_fr/(1-weight_fr))*(weight_fr/(1-weight_fr))))')
                shape_cut = '({c}) * {we}'.format(c=shape_cut, we='((weight_fr/(1-weight_fr))-((weight_fr/(1-weight_fr))*(weight_fr/(1-weight_fr))))')

            # print '#### FULL CUT ####', norm_cut

            #adapt branch names to different software versions
            if not ttree.FindBranch("l0_reliso_rho_04"): 
                norm_cut = norm_cut.replace('l0_reliso_rho_04','l0_reliso05')
                shape_cut = shape_cut.replace('l0_reliso_rho_04','l0_reliso05')
                norm_cut = norm_cut.replace('l1_reliso_rho_04','l1_reliso05')
                shape_cut = shape_cut.replace('l1_reliso_rho_04','l1_reliso05')
                norm_cut = norm_cut.replace('l2_reliso_rho_04','l2_reliso05')
                shape_cut = shape_cut.replace('l2_reliso_rho_04','l2_reliso05')
 
            if not ttree.FindBranch("hnl_iso04_rel_rhoArea"): 
                norm_cut = norm_cut.replace('hnl_iso04_rel_rhoArea','hnl_iso_rel')
                shape_cut = shape_cut.replace('hnl_iso04_rel_rhoArea','hnl_iso_rel')


            # Initialise all hists before the multidraw
            hists = {}

            for vcfg in self.vcfgs:
                hname = '_'.join([self.hist_cfg.name, hashlib.md5(self.hist_cfg.cut).hexdigest(), cfg.name, vcfg.name, cfg.dir_name])
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
            try:
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

            # set_trace()

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
                    if cfg.is_dde:
                        # hist_to_add.SetWeight(hist_to_add.obj.GetEntries()/cfg.sumweights)
                        hist_to_add.SetWeight(cfg.sumweights)
    
                    plot[cfg.name].Add(hist_to_add)
                else:
#                    print(cfg.name, hist.GetEntries(), stack)
                    plot_hist = plot.AddHistogram(cfg.name, hist, stack=stack)
#                    print('added histo %s for %s'%(vcfg.name,cfg.name))

                    if (not cfg.is_data) and (not cfg.is_dde):
                        plot_hist.SetWeight(self.hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                    if cfg.is_dde:
                        try:
                            # plot_hist.SetWeight(plot_hist.obj.GetEntries()/cfg.sumweights)
                            plot_hist.SetWeight(cfg.sumweights)
                        except:
                            set_trace()
            print('added histograms for %s'%cfg.name)
            PLOTS = self.plots
        return PLOTS
