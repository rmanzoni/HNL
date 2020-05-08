from CMGTools.HNL.samples.signals_2016 import all_signals as sigs_16
from CMGTools.HNL.samples.signals_2017 import all_signals as sigs_17
from CMGTools.HNL.samples.signals_2018 import all_signals as sigs_18

for signals in [sigs_16, sigs_17, sigs_18]:

    if   signals == sigs_16: year = '16'
    elif signals == sigs_17: year = '17'
    elif signals == sigs_18: year = '18'

    with open('signals_%s.txt' %year, 'w') as f:

        for sig in signals:

            print >> f, '{name}  .ctau =        {ctau}'  .format(name= sig.name, ctau=sig.ctau)
            print >> f, '{name}  .v2 =          {v2}'    .format(name= sig.name, v2=sig.v2)
            print >> f, '{name}  .mass =        {m}'     .format(name= sig.name, m=sig.mass)
            print >> f, '{name}  .nGenEvents =  {nGenEv}'.format(name= sig.name, nGenEv=sig.nGenEvents)
            print >> f, '{name}  .xs =          {xs}'    .format(name= sig.name, xs=sig.xs)
            print >> f, '{name}  .xse =         {xse}'   .format(name= sig.name, xse=sig.xse)
            print >> f, '\n'

        f.close()
