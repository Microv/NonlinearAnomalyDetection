INTER_ARRIVAL_TIMES = 0
BYTE_LENGTH = 1
SIZE_MARKERS = 2

NORMAL = 'normal'
ANOMALY = 'anomaly'


#  Config 0

TRAFFIC_FEATURE = INTER_ARRIVAL_TIMES

WINDOW_DIM = 180
SAMP_RATE = 0.1

MIN_INTERECTIONS = 1000
ANOMALY_THRESHOLD = 0.5

AGGREGATE_TD = 1
AGGREGATE_ED = [22]

CD_MIN_RADIUS = 0.001
CD_MAX_RADIUS = 50
CD_POINTS_RADIUS = 100

LLE_RADIUS = 1
LLE_MIN_STEPS = 1000
LLE_MAX_STEPS = 10000

RQA_RADIUS = 0.001

"""
# Config 1

TRAFFIC_FEATURE = INTER_ARRIVAL_TIMES

WINDOW_DIM = 180
SAMP_RATE = 0.1

MIN_INTERECTIONS = 1000
ANOMALY_THRESHOLD = 0.6

AGGREGATE_TD = 1
AGGREGATE_ED = [22]

CD_MIN_RADIUS = 0.001
CD_MAX_RADIUS = 50
CD_POINTS_RADIUS = 100

LLE_RADIUS = 1
LLE_MIN_STEPS = 1000
LLE_MAX_STEPS = 10000

RQA_RADIUS = 0.001
"""
"""
#  Config 2

TRAFFIC_FEATURE = INTER_ARRIVAL_TIMES

WINDOW_DIM = 180
SAMP_RATE = 0.1

MIN_INTERECTIONS = 1000
ANOMALY_THRESHOLD = 0.8

AGGREGATE_TD = 1
AGGREGATE_ED = [22]

CD_MIN_RADIUS = 0.001
CD_MAX_RADIUS = 50
CD_POINTS_RADIUS = 100

LLE_RADIUS = 1
LLE_MIN_STEPS = 1000
LLE_MAX_STEPS = 10000

RQA_RADIUS = 0.001
"""
"""
#  Config 3

TRAFFIC_FEATURE = BYTE_LENGTH

WINDOW_DIM = 180
SAMP_RATE = 0.1

MIN_INTERECTIONS = 1000
ANOMALY_THRESHOLD = 0.8

AGGREGATE_TD = 1
AGGREGATE_ED = [22]

CD_MIN_RADIUS = 0.001
CD_MAX_RADIUS = 5000
CD_POINTS_RADIUS = 100

LLE_RADIUS = 1000
LLE_MIN_STEPS = 10
LLE_MAX_STEPS = 10000

RQA_RADIUS = 0.001
"""
"""
#  Config 4

TRAFFIC_FEATURE = INTER_ARRIVAL_TIMES

WINDOW_DIM = 5
SAMP_RATE = None

MIN_INTERECTIONS = 1000
ANOMALY_THRESHOLD = 0.8

AGGREGATE_TD = 1
AGGREGATE_ED = [22]

CD_MIN_RADIUS = 0.001
CD_MAX_RADIUS = 50
CD_POINTS_RADIUS = 100

LLE_RADIUS = 1
LLE_MIN_STEPS = 1000
LLE_MAX_STEPS = 10000

RQA_RADIUS = 0.001
"""
"""
#  Config 5

TRAFFIC_FEATURE = INTER_ARRIVAL_TIMES

WINDOW_DIM = 86400
SAMP_RATE = 0.1

MIN_INTERECTIONS = 1000
ANOMALY_THRESHOLD = 0.8

AGGREGATE_TD = 1
AGGREGATE_ED = [22]

CD_MIN_RADIUS = 0.001
CD_MAX_RADIUS = 50
CD_POINTS_RADIUS = 100

LLE_RADIUS = 1
LLE_MIN_STEPS = 1000
LLE_MAX_STEPS = 10000

RQA_RADIUS = 0.001
"""
"""
#  Config 1 CTU

TRAFFIC_FEATURE = INTER_ARRIVAL_TIMES

WINDOW_DIM =  30
SAMP_RATE = 0.01

MIN_INTERECTIONS = 1000
ANOMALY_THRESHOLD = 0.5

AGGREGATE_TD = None
AGGREGATE_ED = None

CD_MIN_RADIUS = 0.001
CD_MAX_RADIUS = 50
CD_POINTS_RADIUS = 100

LLE_RADIUS = 1
LLE_MIN_STEPS = 1000
LLE_MAX_STEPS = 10000

RQA_RADIUS = 0.001
"""
"""
#  Config 1 DARPA

TRAFFIC_FEATURE = INTER_ARRIVAL_TIMES

WINDOW_DIM =  10
SAMP_RATE = 0.001

MIN_INTERECTIONS = 1000
ANOMALY_THRESHOLD = 0.5

AGGREGATE_TD = None
AGGREGATE_ED = None

CD_MIN_RADIUS = 0.001
CD_MAX_RADIUS = 50
CD_POINTS_RADIUS = 100

LLE_RADIUS = 1
LLE_MIN_STEPS = 1000
LLE_MAX_STEPS = 10000

RQA_RADIUS = 0.001
"""
"""
#  Config 2 DARPA

TRAFFIC_FEATURE = INTER_ARRIVAL_TIMES

WINDOW_DIM =  180
SAMP_RATE = 0.1

MIN_INTERECTIONS = 1000
ANOMALY_THRESHOLD = 0.5

AGGREGATE_TD = None
AGGREGATE_ED = None

CD_MIN_RADIUS = 0.001
CD_MAX_RADIUS = 50
CD_POINTS_RADIUS = 100

LLE_RADIUS = 1
LLE_MIN_STEPS = 1000
LLE_MAX_STEPS = 10000

RQA_RADIUS = 0.001
"""
"""
#  Config 1 DARPA 2000

TRAFFIC_FEATURE = INTER_ARRIVAL_TIMES

WINDOW_DIM = 10
SAMP_RATE = None

MIN_INTERECTIONS = 1000
ANOMALY_THRESHOLD = 0.6

AGGREGATE_TD = 1
AGGREGATE_ED = [22]

CD_MIN_RADIUS = 0.001
CD_MAX_RADIUS = 50
CD_POINTS_RADIUS = 100

LLE_RADIUS = 1
LLE_MIN_STEPS = 1000
LLE_MAX_STEPS = 10000

RQA_RADIUS = 0.001
"""