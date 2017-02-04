from scapy.all import *
from os import listdir, path

class RawChunksPcapReader():


    def __init__(self, dataset, window_start=None, window_end=None):

        self.dataset = dataset
        self.window_start = window_start
        self.window_end = window_end


    def read_packet(self):
        
        capture = RawPcapReader(self.dataset + 'chunk')
        return capture.read_packet()


    def iterator(self):

        chunks = len(listdir(self.dataset))

        for chunk in range(chunks):
            
            if chunk:
                fname = 'chunk' + str(chunk)
            else:
                fname = 'chunk'

            capture = RawPcapReader(self.dataset + fname)
            for packet in capture:
                yield packet


    def __iter__(self):

        return self.iterator()