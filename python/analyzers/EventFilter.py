from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

class EventFilter( Analyzer ):

    def beginLoop(self, setup):
        super(EventFilter,self).beginLoop(setup)
        self.counters.addCounter('EventFilter')
        self.count = self.counters.counter('EventFilter')
        self.count.register('All Events')
        self.count.register('Passed Events')

    def process(self, event):
        self.counters.counter('EventFilter').inc('All Events')
        if not eval(self.cfg_ana.skimFunction):
            return False

        self.counters.counter('EventFilter').inc('Passed Events')
        return True
              