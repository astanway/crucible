# The path for the Redis unix socket
REDIS_SOCKET_PATH='/tmp/redis.sock'

# This is the location the Skyline agent will write the anomalies file to disk. 
# It needs to be in a location accessible to the webapp.
ANOMALY_DUMP = 'webapp/static/dump/anomalies.json'

# This is the number of processes that the Skyline analyzer will spawn.
# Analysis is a very CPU-intensive procedure. You will see optimal results
# if you set ANALYZER_PROCESSES to several less than the total number of
# CPUs on your box. Be sure to leave some CPU room for the Horizon workers, 
# and for Redis.
CRUCIBLE_PROCESSES = 3

# These are the algorithms that the Analyzer will run. To add a new algorithm,
# you must both define the algorithm in algorithms.py and add its name here.
ALGORITHMS = [
                'first_hour_average',
                'mean_subtraction_cumulation',
                'stddev_from_average',
                'stddev_from_moving_average',
                'least_squares',
                'grubbs',
                'histogram_bins',
                'median_absolute_deviation',
                'ks_test',
             ]

# This is the number of algorithms that must return True before a metric is
# classified as anomalous.
CONSENSUS = 6

# This is to enable second order anomalies. This is an experimental feature, so
# it's turned off by default.
ENABLE_SECOND_ORDER = False

"""
Webapp settings
"""

# The IP address for the webapp
WEBAPP_IP = '127.0.0.1'

# The port for the webapp
WEBAPP_PORT = 1500

