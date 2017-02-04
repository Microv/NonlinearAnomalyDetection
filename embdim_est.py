from Slider import Slider
from constants import *
from NonlinearAnalyzer import NonlinearAnalyzer

DATASET = 'testbed-11jun.pcap'

LAST_WINDOW = None

out = open('embdim_est.dat', 'ab', 1)

verbose = True
doplot = True
slider = Slider(DATASET, dim = 180, sampling_rate = 0.1, aggregate = True , verbose = verbose)
nonlinearAnalyzer = NonlinearAnalyzer(verbose = True, doplot = doplot)

for connections in slider.slideWindows(INTER_ARRIVAL_TIMES, LAST_WINDOW):
    
    for connection in connections:

        ts = connection[1]
        ts = nonlinearAnalyzer.toFloatVector(ts)
        
        l = connection[2]

        if l == ANOMALY: 
        	continue

        result = nonlinearAnalyzer.embeddingDimension(ts, 1)
        
        if doplot:
        	raw_input()
        
        out.write(str(result[0]) + '\n')
