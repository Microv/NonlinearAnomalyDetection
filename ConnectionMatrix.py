from constants import *

class ConnectionMatrix():


    def __init__(self):

        self.sym_matrix = dict()
        self.timestamps = None


    def __getitem__(self, keys):

        key1, key2 = keys
        if key1 in self.sym_matrix and key2 in self.sym_matrix[key1]:
            return self.sym_matrix[key1][key2]

        if key2 in self.sym_matrix and key1 in self.sym_matrix[key2]:
            return self.sym_matrix[key2][key1]

        raise KeyError(str(key1) + ',' +str(key2))


    def getTS(self, keys):

        return self.__getitem__(keys)['ts'] 


    def getLabel(self, keys):

        return self.__getitem__(keys)['l'] 


    def addtoTS(self, keys, value):

        key1, key2 = keys
        if key1 in self.sym_matrix and key2 in self.sym_matrix[key1]:                
            self.sym_matrix[key1][key2]['ts'].append(value)
            
        elif key2 in self.sym_matrix and key1 in self.sym_matrix[key2]:
            self.sym_matrix[key2][key1]['ts'].append(value)

        elif key1 in self.sym_matrix:
            self.sym_matrix[key1][key2] = dict()
            self.sym_matrix[key1][key2]['ts'] = [value]
            self.sym_matrix[key1][key2]['l'] = NORMAL

        elif key2 in self.sym_matrix:
            self.sym_matrix[key2][key1] = dict()
            self.sym_matrix[key2][key1]['ts'] = [value]
            self.sym_matrix[key2][key1]['l'] = NORMAL
        
        else:
            self.sym_matrix[key1] = dict()
            self.sym_matrix[key1][key2] = dict()
            self.sym_matrix[key1][key2]['ts'] = [value]
            self.sym_matrix[key1][key2]['l'] = NORMAL


    def setLabel(self, keys, label):

        key1, key2 = keys
        if key1 in self.sym_matrix and key2 in self.sym_matrix[key1]:
            self.sym_matrix[key1][key2]['l'] = label

        elif key2 in self.sym_matrix and key1 in self.sym_matrix[key2]:
            self.sym_matrix[key2][key1]['l'] = label

        else:
            raise KeyError(str(key1) + ',' +str(key2))

    
    def setWindowTimestamps(self, timestamps):

        self.timestamps = timestamps

    
    def getWindowTimestamps(self):

        return self.timestamps    


    def iterator(self):

        for src in self.sym_matrix:
            for dst in self.sym_matrix[src]:
                yield [[src,dst], self.sym_matrix[src][dst]['ts'], self.sym_matrix[src][dst]['l']]


    def __iter__(self):

        return self.iterator()


    def __len__(self):

        l = 0
        for conn in self.__iter__():
            l += 1
        return l


        