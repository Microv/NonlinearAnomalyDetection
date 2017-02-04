from ISCXLabelsHandler import ISCXLabelsHandler
from DARPA2000LabelsHandler import DARPA2000LabelsHandler
import xml.sax
from os import listdir, path
import pickle
import pytz
import datetime, calendar

GROUND_TRUTH_DIR = 'labels/'


class ISCXLabelsReader():


    def __init__(self, verbose=False):
        
        self.parser = xml.sax.make_parser()
        self.anomalies = dict()

        self.verbose = verbose


    def read(self):

        anomaly_file = 'iscx_anomalies.pickle'
        if anomaly_file not in listdir('.'):
            if self.verbose:
                print 'Building dictionary of anomalies...'
            for filename in listdir(GROUND_TRUTH_DIR):
                if '.xml' in filename:
                    if self.verbose:
                        print 'Reading ' + filename
                    self.parser.setContentHandler(ISCXLabelsHandler(path.splitext(filename)[0], self.anomalies, self.verbose))
                    self.parser.parse(GROUND_TRUTH_DIR + filename)
            
            with open(anomaly_file, 'wb') as f:
                pickle.dump(self.anomalies, f)
        
        else:
            if self.verbose:
                print 'Reading dictionary of anomalies...'
            with open(anomaly_file, 'rb') as f:
                self.anomalies = pickle.load(f)
            if self.verbose:
                print 'Dictionary read'
                       
        return self.anomalies



class CTU13LabelsReader():


    def __init__(self, verbose=False):
        
        self.anomalies = dict()

        self.verbose = verbose


    def read(self):

        anomaly_file = 'ctu13_anomalies.pickle'
        if anomaly_file not in listdir('.'):
            if self.verbose:
                print 'Building dictionary of anomalies...'
            for filename in listdir(GROUND_TRUTH_DIR):
                if '.binetflow' in filename:
                    if self.verbose:
                        print 'Reading ' + filename
                    self.parseFile(filename)
            
            with open(anomaly_file, 'wb') as f:
                pickle.dump(self.anomalies, f)
        
        else:
            if self.verbose:
                print 'Reading dictionary of anomalies...'
            with open(anomaly_file, 'rb') as f:
                self.anomalies = pickle.load(f)
            if self.verbose:
                print 'Dictionary read'
                       
        return self.anomalies


    def parseFile(self, file):

        with open(GROUND_TRUTH_DIR + file, 'rb') as f:

            header = f.readline()

            while True:

                line = f.readline()
                if line == "":
                    break

                line = line[:-1].split(',')
                
                start_time = line[0]
                duration = line[1]
                source = line[3]
                destination = line[6]
                full_label = line[14]

                start_ts = self.timestamp(start_time)
                stop_ts = start_ts + float(duration)

                if 'Botnet' in full_label:
                    label = 'anomaly'
                else:
                    label = 'normal' 

                if self.verbose:
                    print start_time + '(' + str(start_ts) + ')', duration + '(' + str(stop_ts) + ')', source, destination, full_label + '(' + label + ')'

                if label == 'anomaly':
                    if source not in self.anomalies:
                        self.anomalies[source] = dict()
                        self.anomalies[source][destination] = list()
                    elif destination not in self.anomalies[source]:
                        self.anomalies[source][destination] = list()

                    self.anomalies[source][destination].append([start_ts,stop_ts])


    def timestamp(self, dateTime):
        
        TIMEZONE = 'Europe/Prague'
        local_tz = pytz.timezone(TIMEZONE)
        datetime_without_tz = datetime.datetime.strptime(dateTime, "%Y/%m/%d %H:%M:%S.%f")
        datetime_with_tz = local_tz.localize(datetime_without_tz, is_dst=None)
        datetime_in_utc = datetime_with_tz.astimezone(pytz.utc)
        timestamp = calendar.timegm(datetime_in_utc.timetuple())
        return timestamp


class DARPALabelsReader():

    def __init__(self, verbose=False):
        
        self.anomalies = dict()

        self.verbose = verbose


    def read(self):

        anomaly_file = 'darpa_anomalies.pickle'
        if anomaly_file not in listdir('.'):
            if self.verbose:
                print 'Building dictionary of anomalies...'
            for filename in listdir(GROUND_TRUTH_DIR):
                if '.list' in filename:
                    if self.verbose:
                        print 'Reading ' + filename
                    self.parseFile(filename)
            
            with open(anomaly_file, 'wb') as f:
                pickle.dump(self.anomalies, f)
        
        else:
            if self.verbose:
                print 'Reading dictionary of anomalies...'
            with open(anomaly_file, 'rb') as f:
                self.anomalies = pickle.load(f)
            if self.verbose:
                print 'Dictionary read'
                       
        return self.anomalies


    def parseFile(self, filename):

        attack = None
        with open(GROUND_TRUTH_DIR + filename, 'rb') as f:

            while True:

                line = f.readline()
                if line == "":
                    break

                line = line[:-1].split(' ')
                if len(line) < 2:
                    continue
                name = line[0]
                value = line[1]
                if name == 'ID:':
                    if attack:
                        
                        start_ts = self.timestamp(attack['date'] + '-' + attack['start_time'])
                        duration = self.timestamp('01/01/1970-' + attack['duration']) 
                        stop_ts = start_ts + duration

                        if self.verbose:
                            for key in attack:
                                print key + ':', attack[key] 

                            print start_ts
                            print stop_ts

                        # if noisy
                        sources = attack['attacker']
                        destinations = attack['victim']

                        for source in sources:
                            if source not in self.anomalies:
                                self.anomalies[source] = dict()
                                for destination in destinations:
                                    self.anomalies[source][destination] = list()
                            else:
                                for destination in destinations:
                                    if destination not in self.anomalies[source]:
                                        self.anomalies[source][destination] = list()

                        for source in sources:
                            for destination in destinations:
                                self.anomalies[source][destination].append([start_ts,stop_ts])
                  
                    attack = dict()
                    attack['id'] = value
                elif name == 'Date:':
                    attack['date'] = value
                elif name == 'Name:':
                    attack['name'] = value
                elif name == 'Category':
                    attack['category'] = value
                elif name == 'Start_Time:':
                    attack['start_time'] = value
                elif name == 'Duration:':
                    attack['duration'] = value
                elif name == 'Attacker:':
                    attack['attacker'] = list()
                    values = value.split(',')
                    for value in values:
                        value = value.split('.')
                        if len(value) == 4 and value[0] != 'login': 
                            ip = ''
                            for i in range(len(value)):
                                if '-' in value[i]:
                                    ls = value[i].split('-')
                                    first = int(ls[0])
                                    last = int(ls[1])
                                    for j in range(first, last):
                                        attack['attacker'].append(ip + str(int(j)))
                                    continue
                                else:    
                                    ip += str(int(value[i])) + '.'
                            attack['attacker'].append(ip[:-1])
                        else:
                            attack['attacker'].append(value[0])
                elif name == 'Victim:':
                    attack['victim'] = list()
                    values = value.split(',')
                    for value in values:
                        value = value.split('.')
                        if len(value) == 4: 
                            ip = ''
                            for i in range(len(value)):
                                if value[i] == '*':
                                    for j in range(0, 255):
                                        attack['victim'].append(ip + str(int(j)))
                                    continue
                                if '-' in value[i]:
                                    ls = value[i].split('-')
                                    first = int(ls[0])
                                    last = int(ls[1])
                                    for j in range(first, last):
                                        attack['victim'].append(ip + str(int(j)))
                                    continue
                                else:    
                                    ip += str(int(value[i])) + '.'
                            attack['victim'].append(ip[:-1])
                        else:
                            attack['victim'].append(value[0])


    def timestamp(self, dateTime):
        
        TIMEZONE = 'America/New_York'
        local_tz = pytz.timezone(TIMEZONE)
        datetime_without_tz = datetime.datetime.strptime(dateTime, "%m/%d/%Y-%H:%M:%S")
        datetime_with_tz = local_tz.localize(datetime_without_tz, is_dst=None)
        datetime_in_utc = datetime_with_tz.astimezone(pytz.utc)
        timestamp = calendar.timegm(datetime_in_utc.timetuple())
        return timestamp



class DARPA2000LabelsReader():


    def __init__(self, verbose=False):
        
        self.parser = xml.sax.make_parser()
        self.anomalies = dict()

        self.verbose = verbose


    def read(self):

        anomaly_file = 'darpa2000_anomalies.pickle'
        if anomaly_file not in listdir('.'):
            if self.verbose:
                print 'Building dictionary of anomalies...'
            for filename in listdir(GROUND_TRUTH_DIR):
                if '.xml' in filename:
                    if self.verbose:
                        print 'Reading ' + filename
                    self.parser.setContentHandler(DARPA2000LabelsHandler(self.anomalies, self.verbose))
                    self.parser.parse(GROUND_TRUTH_DIR + filename)
            
            with open(anomaly_file, 'wb') as f:
                pickle.dump(self.anomalies, f)
        
        else:
            if self.verbose:
                print 'Reading dictionary of anomalies...'
            with open(anomaly_file, 'rb') as f:
                self.anomalies = pickle.load(f)
            if self.verbose:
                print 'Dictionary read'
                       
        return self.anomalies


class MergedLabelsReader():


    def __init__(self, verbose=False):
        
        self.anomalies = dict()

        self.verbose = verbose


    def read(self):

        # CTU botnet
        self.anomalies['147.32.84.165'] = dict()
        self.anomalies['147.32.84.165']['147.32.96.69'] = list()
        self.anomalies['147.32.84.165']['147.32.96.69'].append([1483706040, 1483706520])
        self.anomalies['147.32.84.165']['147.32.96.69'].append([1483711200, 1483711680])
        self.anomalies['147.32.84.165']['147.32.96.69'].append([1483722000, 1483722480])
        self.anomalies['147.32.84.165']['147.32.96.69'].append([1483729200, 1483729680])
        self.anomalies['147.32.84.165']['147.32.96.69'].append([1483735980, 1483736460])
        self.anomalies['147.32.84.165']['147.32.96.69'].append([1483745400, 1483745880])

        # CAIDA 2007 DDoS
        IP_FILE = 'ip_addr_caida.txt'
        with open(GROUND_TRUTH_DIR + IP_FILE, 'rb') as f:

            while True:

                line = f.readline()
                if line == "":
                    break

                line = line[:-1].split(',')

                src = line[0]
                dst = line[1]

                if self.verbose:
                    print 'Attack'
                    print 'From: ' + src
                    print 'To:   ' + dst

                if src not in self.anomalies:
                    self.anomalies[src] = dict()
                    self.anomalies[src][dst] = list()
                elif dst not in self.anomalies[src]: 
                    self.anomalies[src][dst] = list()
                self.anomalies[src][dst].append([1484557200, 1484559796])
                self.anomalies[src][dst].append([1484571600, 1484574173])
                self.anomalies[src][dst].append([1484586000, 1484588580])

        # Simulated Attacks
        FILENAME = 'merged_dataset_log.csv'
        with open(GROUND_TRUTH_DIR + FILENAME, 'rb') as f:

            header = f.readline()

            while True:

                line = f.readline()
                if line == "":
                    break

                line = line[:-1].split(';')
                
                source = line[2]
                target = line[3]
                start_timestamp = int(line[4])
                stop_timestamp = int(line[5])

                if self.verbose:
                    print 'Attack'
                    print 'From: ' + source
                    print 'To:   ' + target
                    print 'Begins: ' + str(start_timestamp)
                    print 'Ends:   ' + str(stop_timestamp) 
 
                if source not in self.anomalies:
                    self.anomalies[source] = dict()
                    self.anomalies[source][target] = list()
                elif target not in self.anomalies[source]: 
                    self.anomalies[source][target] = list()
                    
                self.anomalies[source][target].append([start_timestamp, stop_timestamp])

                       
        return self.anomalies


