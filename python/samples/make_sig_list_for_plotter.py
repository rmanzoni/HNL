from CMGTools.HNL.samples.signals_2016 import all_signals_e as sigs_16_e
from CMGTools.HNL.samples.signals_2016 import all_signals_m as sigs_16_m
from CMGTools.HNL.samples.signals_2016 import all_signals_t as sigs_16_t

from CMGTools.HNL.samples.signals_2017 import all_signals_e as sigs_17_e
from CMGTools.HNL.samples.signals_2017 import all_signals_m as sigs_17_m
from CMGTools.HNL.samples.signals_2017 import all_signals_t as sigs_17_t

from CMGTools.HNL.samples.signals_2018 import all_signals_e as sigs_18_e
from CMGTools.HNL.samples.signals_2018 import all_signals_m as sigs_18_m
from CMGTools.HNL.samples.signals_2018 import all_signals_t as sigs_18_t

from re import sub
from pdb import set_trace

for signals in [sigs_16_e, sigs_16_m, sigs_16_t,
                sigs_17_e, sigs_17_m, sigs_17_t,
                sigs_18_e, sigs_18_m, sigs_18_t]:

    if signals == sigs_16_e: 
        year = '16'
        lepton = 'e'
    if signals == sigs_16_m: 
        year = '16'
        lepton = 'm'
    if signals == sigs_16_t: 
        year = '16'
        lepton = 't'

    if signals == sigs_17_e: 
        year = '17'
        lepton = 'e'
    if signals == sigs_17_m: 
        year = '17'
        lepton = 'm'
    if signals == sigs_17_t: 
        year = '17'
        lepton = 't'

    if signals == sigs_18_e: 
        year = '18'
        lepton = 'e'
    if signals == sigs_18_m: 
        year = '18'
        lepton = 'm'
    if signals == sigs_18_t: 
        year = '18'
        lepton = 't'

    with open('plotter_signals_%s_%s.txt' %(lepton, year), 'w') as f:

        for sig in signals:

            # set_trace()
            v2_label = sub('\.', 'p', '{v2:.1E}'.format(v2=sig.v2))
            v2_label = sub('-', 'm', v2_label)
            if  'Dirac_cc' in sig.name: 
                mode = 'Dirac_cc'
                mode_label = 'dirac_cc' 
            elif 'Dirac' in sig.name:
                mode = 'Dirac'
                mode_label = 'dirac' 
            elif not 'Dirac' in sig.name: 
                mode = 'Majorana'
                mode_label = 'majorana' 
            else:  assert False, 'ERROR: No mode could be determined. Check signal list.'

            label = 'hnl_m_{mass}_v2_{v2_label}_{mode_label}'.format(mass=sig.mass, v2_label=v2_label, mode_label=mode_label)
            if   sig.mass == 1:  color = 'darkorange'
            elif sig.mass == 2:  color = 'forestgreen'
            elif sig.mass == 3:  color = 'firebrick'
            elif sig.mass == 4:  color = 'indigo'
            elif sig.mass == 5:  color = 'chocolate'
            elif sig.mass == 6:  color = 'olive'
            elif sig.mass == 7:  color = 'peru'
            elif sig.mass == 8:  color = 'darkgray'
            elif sig.mass == 9:  color = 'plum'
            elif sig.mass == 10: color = 'teal'
            elif sig.mass == 11: color = 'seagreen'
            elif sig.mass == 12: color = 'coral'
            elif sig.mass == 15: color = 'gold'
            elif sig.mass == 20: color = 'crimson'
            else: assert False, 'ERROR: No mass could be determined. Check signal list.'

            print >> f, "Sample({name:62}, [{name:62}], channel, '{splitline}m={mass:4}, V^{S}={v2:.1E}{sep}{mode:9}{end}' , selection, {label:32},".format(name="'"+sig.name+"'", splitline='#splitline{', mass=sig.mass, \
                                                                                                                                 S='{2}', v2=sig.v2, sep='}{', mode=mode, end='}', label="'"+label+"'"), 
            print >> f, " {color:15}, 10, '/'.join([basedir, 'sig']), post_fix, False, True, True, 1., {xs:11}, toplot=False),".format(color="'"+color+"'", xs=sig.xs),
            print >> f, ''


    f.close()

