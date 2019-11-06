# from CMGTools.HNL.samples.signals_2016 import all_signals
# from CMGTools.HNL.samples.signals_2017 import all_signals
from CMGTools.HNL.samples.signals_2018 import all_signals

with open('signals_18.txt', 'w') as f:

    for sig in all_signals:

        print >> f, '{name}  .ctau =        {ctau}'  .format(name= sig.name, ctau=sig.ctau)
        print >> f, '{name}  .v2 =          {v2}'    .format(name= sig.name, v2=sig.v2)
        print >> f, '{name}  .mass =        {m}'     .format(name= sig.name, m=sig.mass)
        print >> f, '{name}  .nGenEvents =  {nGenEv}'.format(name= sig.name, nGenEv=sig.nGenEvents)
        print >> f, '{name}  .xs =          {xs}'    .format(name= sig.name, xs=sig.xs)
        print >> f, '{name}  .xse =         {xse}'   .format(name= sig.name, xse=sig.xse)
        print >> f, '\n'

    f.close()
