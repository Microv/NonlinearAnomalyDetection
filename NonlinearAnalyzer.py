from rpy2.robjects.packages import importr
from rpy2.robjects import FloatVector
from collections import OrderedDict
from constants import *

MIN_EMBEDDING_DIM = 40
MAX_EMBEDDING_DIM = 1000
EMBEDDING_INCREMENT = 5

class NonlinearAnalyzer():


    def __init__(self, verbose=False, doplot=False):
                
        self.verbose = verbose
        self.doplot = doplot

        self.import_libreries()        

    
    def import_libreries(self):
        
        if self.verbose:    
            print 'Importing nonlinearTseries library...'

        self.nonlinearTseries = importr('nonlinearTseries')
        
        if self.verbose:
            print 'Library imported'
            print 'Importing base library...'

        self.base = importr('base')
        
        if self.verbose:
            print 'Library imported'


    def timeLag(self, series):

        try:
            tau_ami = self.nonlinearTseries.timeLag(series, technique = "ami", do_plot = self.doplot)
        except:
            return 1

        if self.verbose:
            print 'Time delay: ' + str(tau_ami[0])

        return tau_ami


    def embeddingDimension(self, series, timelag):

        max = MIN_EMBEDDING_DIM
        emb_dim = self.nonlinearTseries.estimateEmbeddingDim(series, time_lag = timelag, max_embedding_dim = max, do_plot=self.doplot)
        while emb_dim[0] == 0:
            max *=  2
            if max > MAX_EMBEDDING_DIM:
                return
            self.nonlinearTseries.estimateEmbeddingDim(series, time_lag = timelag, max_embedding_dim = max, do_plot=self.doplot)

        if self.verbose:    
            print 'Embedding dimension: ' + str(emb_dim[0])

        return emb_dim


    def correlationDimension(self, series, emb_dim, timelag) :   

        try:
            emb_dim = emb_dim[0]
            cd = self.nonlinearTseries.corrDim(series, min_embedding_dim = emb_dim, max_embedding_dim = (emb_dim + EMBEDDING_INCREMENT), time_lag = timelag, min_radius = CD_MIN_RADIUS, max_radius = CD_MAX_RADIUS, n_points_radius = CD_POINTS_RADIUS, do_plot = self.doplot)
            cd_est = self.nonlinearTseries.estimate(cd)

            if self.verbose:
                print 'Correlation dimension estimate: ' + str(cd_est[0])
        
        except:
            cd = ['NA']
            cd_est = ['NA']

        return cd, cd_est

    
    def maxLyapunovExponent(self, series, emb_dim, timelag):

        max = LLE_MIN_STEPS
        emb_dim = emb_dim[0]
        while max <= LLE_MAX_STEPS:
            try:
                ml = self.nonlinearTseries.maxLyapunov(series, min_embedding_dim = emb_dim, max_embedding_dim = (emb_dim + EMBEDDING_INCREMENT), time_lag = timelag, radius = LLE_RADIUS, max_time_steps = max, do_plot = self.doplot)
                ml_est = self.nonlinearTseries.estimate(ml)
                break
            except:
                max +=500#*= 2
                if self.verbose:
                    print 'Error: incrementing max time steps: ' + str(max)
        else:
            return None

        if self.verbose:
            print 'Maximal Lyapunov Exponent estimate: ' + str(ml_est[0])

        return ml, ml_est


    def sampleEntropy(self, cd):
        
        try:
            se = self.nonlinearTseries.sampleEntropy(cd, do_plot = self.doplot)
            se_est = self.nonlinearTseries.estimate(se, do_plot = self.doplot)
            se_est_mean = self.base.mean(se_est)

            if self.verbose:
                print 'Sample entropy estimate: ' + str(se_est_mean[0])

        except:
            se = ['NA']
            se_est_mean = ['NA']

        return se, se_est_mean
        


    def rqa(self, series, emb_dim, timelag):

        emb_dim = emb_dim[0]
        rqa = self.nonlinearTseries.rqa(time_series = series, embedding_dim=emb_dim, time_lag=timelag, radius=RQA_RADIUS, do_plot=self.doplot)
        rec = rqa[1]
        det = rqa[3]
        ent = rqa[8]
        trend = rqa[9]
        lam = rqa[10]
        
        if self.verbose:
            print 'RQA:%REC:  ' + str(rec[0])
            print 'RQA:%DET:  ' + str(det[0])
            print 'RQA:ENTR:  ' + str(ent[0])
            print 'RQA:TREND: ' + str(trend[0])
            print 'RQA:LAM:   ' + str(lam[0])
                
        return [rqa, rec, det, ent, trend, lam]


    def evaluate(self, timeseries, time_lag = None, emb_dim = None):
        
        series = FloatVector(timeseries)

        if not time_lag:
            time_lag = self.timeLag(series)
        if not emb_dim:
            emb_dim = self.embeddingDimension(series, time_lag)
        
        cd, cd_est = self.correlationDimension(series, emb_dim, time_lag)
        ml, ml_est = self.maxLyapunovExponent(series, emb_dim, time_lag)
        se, se_est_mean = self.sampleEntropy(cd)        
        rqa = self.rqa(series, emb_dim, time_lag)
        
        result = OrderedDict()
        result['ed'] = emb_dim[0]
        result['cd'] = cd_est[0]
        result['lle'] = ml_est[0]
        result['sampen'] = se_est_mean[0]
        result['rec'] = rqa[1][0]
        result['det'] = rqa[2][0]
        result['ent'] = rqa[3][0]
        result['trend'] = rqa[4][0]
        result['lam'] = rqa[5][0]

        return result

        
    def toFloatVector(self, series):

        return FloatVector(series)

