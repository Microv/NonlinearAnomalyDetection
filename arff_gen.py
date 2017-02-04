from NonlinearAnalyzer import NonlinearAnalyzer
from Slider import Slider
from constants import *
import subprocess, os, shutil


def test(dname, dataset, verbose=True):

    FILENAME_AGG = dname + '_nonlinear_agg.arff'
    FILENAME_CON = dname + '_nonlinear_con.arff'

    LAST_WINDOW = None

    if LAST_WINDOW:
        arf_agg = open(FILENAME_AGG, 'ab', 1)
        arf_con = open(FILENAME_CON, 'ab', 1)
    else:    
        arf_agg = open(FILENAME_AGG, 'wb', 1)
        arf_con = open(FILENAME_CON, 'wb', 1)
        with open('header.arff', 'rb') as f:
            for line in f:
                arf_agg.write(line)
                arf_con.write(line)

    nonlinearAnalyzer = NonlinearAnalyzer(verbose)
    slider = Slider(dataset=dataset, dim=WINDOW_DIM, sampling_rate=SAMP_RATE, verbose=verbose)
    windows = slider.slideWindows(TRAFFIC_FEATURE, LAST_WINDOW)

    for connections, aggregate in windows:
        
        timestamps = connections.getWindowTimestamps()
        
        for connection in connections:
            host1 = connection[0][0]
            host2 = connection[0][1]
            ts = connection[1]
            l = connection[2]
            if len(ts) >= MIN_INTERECTIONS:
                print '\nAnalysing connection ' + host1 + ' <-> ' + host2
                print '# Packets: ' + str(len(ts))
                print 'Label: ' + l
                result = nonlinearAnalyzer.evaluate(ts)
                dataline = ''
                for m in result:
                    dataline += str(result[m]) + ','
                dataline += l + '\n'
                arf_con.write(str(timestamps[0]) + ',' + str(len(ts)) + ',')
                arf_con.write(dataline)
        
        try:
            ts = aggregate.getTS([0, 0])
            l = aggregate.getLabel([0, 0])
            if len(ts) >= MIN_INTERECTIONS:
                print '\nAnalysing aggregate'
                print '# Packets: ' + str(len(ts))
                print 'Label: ' + l
                result = nonlinearAnalyzer.evaluate(ts, AGGREGATE_TD, AGGREGATE_ED)
                dataline = ''
                for m in result:
                    dataline += str(result[m]) + ','
                dataline += l + '\n'
                arf_agg.write(str(timestamps[0]) + ',' + str(len(ts)) + ',')
                arf_agg.write(dataline)
        except KeyError as e:
            print e
    

if __name__ == '__main__':
    
    DATASET = 'capture/testbed-11jun.pcap'
    #DATASET = 'capture/testbed-12jun.pcap'
    #DATASET = 'capture/testbed-13jun.pcap'
    #DATASET = 'capture/testbed-14jun.pcap'
    #DATASET = 'capture/testbed-15jun.pcap'
    #DATASET = 'capture/testbed-16jun.pcap'
    #DATASET = 'capture/testbed-17jun.pcap'

    # split original capture in chunks to speed the test
    tmpdir = 'tmp'
    try:
        os.stat(tmpdir)
        shutil.rmtree(tmpdir)
        os.mkdir(tmpdir)
    except:
        os.mkdir(tmpdir)

    bashCommand = 'sudo tcpdump -r ' + DATASET + ' -w ' + tmpdir + '/chunk -C 10'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    process.wait()
    output, error = process.communicate()
    
    test(DATASET.split('.')[0].replace('/', '_'), tmpdir + '/')


