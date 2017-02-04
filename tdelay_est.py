from Slider import Slider
from constants import *
from NonlinearAnalyzer import NonlinearAnalyzer

DATASET = 'testbed-11jun.pcap'

out = open('tdelay_est.dat', 'wb', 1)

slider = Slider(DATASET, dim = 86400, sampling_rate = 0.1, aggregate = True , verbose = True)

nonlinearAnalyzer = NonlinearAnalyzer(verbose = True, doplot = True)

for connections in slider.slideWindows(INTER_ARRIVAL_TIMES):
    
    for connection in connections:

        ts = connection[1]
        ts = nonlinearAnalyzer.toFloatVector(ts)
        
        result = nonlinearAnalyzer.timeLag(ts)
        
        raw_input()
        
        out.write(str(result[0]) + '\n')
