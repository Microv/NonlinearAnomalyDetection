from constants import *
#from LabelsReader import CTU13LabelsReader as LabelsReader
#from LabelsReader import DARPALabelsReader as LabelsReader
#from LabelsReader import DARPA2000LabelsReader as LabelsReader
from LabelsReader import ISCXLabelsReader as LabelsReader
#from LabelsReader import MergedLabelsReader as LabelsReader
from ConnectionMatrix import ConnectionMatrix
from CaptureReader import RawChunkCaptureReader as RawCaptureReader


class Slider():


    def __init__(self, dataset, dim, sampling_rate = False, verbose=False):

        self.dataset = dataset
        self.capture = RawCaptureReader(self.dataset)

        self.dim = dim
        self.shift = float(self.dim)*25/100
        
        self.window_count = 0
        self.window_start = 0
        self.window_end = 0
        self.packet_count = 0
        self.connections = ConnectionMatrix()
        self.aggregate = ConnectionMatrix()
        self.timestamps = ConnectionMatrix()
        self.last_timestamp = None
        
        self.sampling_rate = sampling_rate

        self.verbose = verbose

        labelsReader = LabelsReader(verbose=self.verbose)
        self.anomalies = labelsReader.read()


    def slideWindows(self, feature, last_window=None):
        
        next_packet = 1
        while next_packet:

            if self.window_count == 0:
                self.window_start = self.capture.getFirstTimestamp()
                self.window_end = self.window_start + self.dim

            else:
                self.window_start = self.window_start + self.shift
                self.window_end = self.window_start + self.dim
            
            self.window_count += 1

            if last_window and self.window_count <= last_window:
                continue

            if self.verbose:
                print '\n\nWindow number    ' + str(self.window_count)
                print 'Window starts at '  + str(self.window_start)
                print 'Window ends at   '  + str(self.window_end)    
                print ''
        
                
            next_packet = self.parseConnection(feature)
            self.assignLabels()
            self.connections.setWindowTimestamps([self.window_start, self.window_end])
            self.aggregate.setWindowTimestamps([self.window_start, self.window_end])
            
            if self.verbose:
                print 'Number of packets: '+str(self.packet_count)
                
                for connection in self.connections:
                    out = '\n' + connection[0][0] + ' <-> ' + connection[0][1]
                    out += ' - # Packets: ' + str(len(connection[1]))
                    out += ' - Label: ' + connection[2]
                    print out
                    
            yield self.connections, self.aggregate


    def parseConnection(self, feature):

        self.packet_count = 0
        self.connections = ConnectionMatrix()
        self.aggregate = ConnectionMatrix()
        self.timestamps = ConnectionMatrix()
        self.last_timestamp = None

        for packet in self.capture.capture(self.window_start, self.window_end, self.sampling_rate):

            if packet == 1:
                return 1
            elif packet == 0:
                return 0
            else:
                
                self.packet_count += 1

                self.computeFeature(feature, packet)


    def computeFeature(self, feature, packet):

        src, dst = self.capture.extractSrcDst(packet)

        ts = self.capture.extractTS(packet)
        iplen = self.capture.extractIPLen(packet)

        self.timestamps.addtoTS([src, dst], (src, ts))

        if feature == BYTE_LENGTH:
            self.connections.addtoTS([src, dst], iplen)
            self.aggregate.addtoTS([0, 0], iplen)

        elif feature == INTER_ARRIVAL_TIMES:
            if len(self.timestamps.getTS([src, dst])) > 1:
                last_conn_timestamp = self.timestamps.getTS([src, dst])[-2][1]
                self.connections.addtoTS([src, dst], ts - last_conn_timestamp)
            if self.last_timestamp:    
                self.aggregate.addtoTS([0, 0], ts - self.last_timestamp)   

        elif feature == SIZE_MARKERS:
            if len(self.timestamps.getTS([src, dst])) > 1:
                last_sender = self.timestamps.getTS([src, dst])[-2][0]
                if src == last_sender:
                    last_markers = self.connections.getTS([src, dst])[-1]
                    self.connections.getTS([src, dst])[-1] = last_markers + iplen
                else:
                    self.connections.addtoTS([src, dst], iplen)
            else:
                self.connections.addtoTS([src, dst], iplen)

        self.last_timestamp = ts


    def assignLabels(self):

        for src in self.anomalies:
            for dst in self.anomalies[src]:
                for t in self.anomalies[src][dst]:
                    if (self.window_start <= t[0] and t[0] < int(self.window_end)) or \
                       (self.window_start < t[1] and t[1] <= self.window_end) or \
                       (t[0] < self.window_start and self.window_end < t[1]):
                        try:
                            self.connections.setLabel([src, dst], ANOMALY)            
                        except KeyError as e:
                            if self.verbose:
                                print 'Key error: ' + str(e) 

        normal_total_length = 0
        anomaly_total_length = 0
        for connection in self.connections:
            ts = connection[1]
            l = connection[2]
            if l == 'anomaly':
                anomaly_total_length += len(ts)
            else:
                normal_total_length += len(ts)

        try:
            if anomaly_total_length >= (anomaly_total_length + normal_total_length) * ANOMALY_THRESHOLD:
                self.aggregate.setLabel([0, 0], ANOMALY)
        except KeyError as e:
            if self.verbose:
                print 'Key error: ' + str(e) 
