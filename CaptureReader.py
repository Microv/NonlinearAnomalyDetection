from scapy.all import *
from os import listdir, path
import re


class CaptureReader():
    

    def __init__(self, dataset):

        self.dataset = dataset


    def capture(self, window_start, window_end, sampling_rate=None):

        capture = PcapReader(self.dataset)
        last_timestamp = None
        
        for packet in capture:

            if sampling_rate:
                if last_timestamp:
                    current_timestamp = self.extractTS(packet)
                    if current_timestamp - last_timestamp < sampling_rate:
                        continue
                last_timestamp = self.extractTS(packet)    


            if packet.getlayer(IP) == None:
                continue

            timestamp = float(packet.time)

            if timestamp < window_start:
                continue

            if timestamp <= window_end: 
                
                yield packet

            else:

                yield 1 # There is a packet with timestamp > window_end

        yield 0 # No packets with timestamp > window_end: no more windows


    def getFirstTimestamp(self):

        capture = PcapReader(self.dataset)
        ts = float(capture.read_packet().time)
        return ts


    def extractSrcDst(self, packet):

        return [packet.getlayer(IP).src, packet.getlayer(IP).dst]


    def extractTS(self, packet):

        return float(packet.time)


    def extractIPLen(self, packet):

        return len(packet.getlayer(IP))



class RawCaptureReader():
    

    def __init__(self, dataset):

        self.dataset = dataset


    def capture(self, window_start, window_end, sampling_rate=None):

        capture = RawPcapReader(self.dataset)

        last_timestamp = None

        for packet in capture:

            if sampling_rate:
                if last_timestamp:
                    current_timestamp = self.extractTS(packet)
                    if current_timestamp - last_timestamp < sampling_rate:
                        continue
                last_timestamp = self.extractTS(packet) 

            ipHdr = self.extractIPheader(packet)

            v = (ipHdr[0] & 0xF0) / 16
            if v != 4:
                continue

            timestamp = self.extractTS(packet)

            if timestamp < window_start:
                continue

            if timestamp <= window_end: 
                
                yield packet

            else:

                yield 1 # There is a packet with timestamp > window_end

        yield 0 # No packets with timestamp > window_end: no more windows


    def getFirstTimestamp(self):

        capture = RawPcapReader(self.dataset)
        first = capture.read_packet()
        ts = self.extractTS(first)
        return ts


    def extractSrcDst(self, packet):
        
        ipHdr = self.extractIPheader(packet)
        src = socket.inet_ntoa(ipHdr[8])
        dst = socket.inet_ntoa(ipHdr[9])

        return [src, dst]


    def extractTS(self, packet):

        sec = packet[1][0]
        usec = packet[1][1]
        return sec + 0.000001*usec


    def extractIPLen(self, packet):
        
        ipHdr = self.extractIPheader(packet)

        return ipHdr[2]


    def extractIPheader(self, packet):
        
        ipHeader=packet[0][14:34]
        # !  big-endian
        # B   8 bit version + IHL
        # B   8 bit ToS
        # H  16 bit total length
        # H  16 bit identification
        # H  16 bit flag + offset
        # B   8 bit TTL
        # B   8 bit protocol
        # H  16 bit header checksum 
        # 4s 32 bit source address
        # 4s 32-bit destination address
        return struct.unpack("!BBHHHBBH4s4s",ipHeader)



class RawChunkCaptureReader(RawCaptureReader):

    
    def capture(self, window_start, window_end, sampling_rate=None):

        chunks = listdir(self.dataset)
        chunks.sort(key=self.alphanum_key)

        last_timestamp = None

        for chunk in chunks:

            print 'Reading chunk:', chunk

            capture = RawPcapReader(self.dataset + chunk)
            delete = True

            for packet in capture:

                if sampling_rate:
                    if last_timestamp:
                        current_timestamp = self.extractTS(packet)
                        if current_timestamp - last_timestamp < sampling_rate:
                            continue
                    last_timestamp = self.extractTS(packet) 

                ipHdr = self.extractIPheader(packet)
                
                v = (ipHdr[0] & 0xF0) / 16
                if v != 4:
                    continue

                timestamp = self.extractTS(packet)

                if timestamp < window_start:
                    continue

                delete = False
                
                if timestamp <= window_end: 
                    
                    yield packet

                else:

                    yield 1 # There is a packet with timestamp > window_end

            if delete:
                os.remove(self.dataset + chunk)

        yield 0 # No packets with timestamp > window_end: no more windows


    def getFirstTimestamp(self):

        capture = RawPcapReader(self.dataset + 'chunk')
        first = capture.read_packet()
        ts = self.extractTS(first)
        return ts


    def tryint(self, s):
        try:
            return int(s)
        except:
            return s

    def alphanum_key(self, s):
        """ Turn a string into a list of string and number chunks.
            "z23a" -> ["z", 23, "a"]
        """
        return [self.tryint(c) for c in re.split('([0-9]+)', s) ]


        