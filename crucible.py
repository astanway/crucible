import logging
from redis import StrictRedis
from time import time
from collections import defaultdict
from multiprocessing import Process, Manager, Lock
from os.path import dirname, abspath
import sys
from math import ceil
import traceback
import settings
import json


# add the shared settings file to namespace
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings

from algorithms import run_algorithms

class Crucible():
    def __init__(self):
        """
        Initialize the Crucible
        """
        self.redis_conn = StrictRedis(unix_socket_path = settings.REDIS_SOCKET_PATH)
        self.lock = Lock()

    def spin_process(self, i, unique_metrics):
        """
        Assign a bunch of metrics for a process to analyze.
        """
        # Discover assigned metrics
        keys_per_processor = int(ceil(float(len(unique_metrics)) / float(settings.CRUCIBLE_PROCESSES)))
        if i == settings.CRUCIBLE_PROCESSES:
            assigned_max = len(unique_metrics)
        else:
            assigned_max = i * keys_per_processor
        assigned_min = assigned_max - keys_per_processor
        assigned_keys = range(assigned_min, assigned_max)

        # Compile assigned metrics
        assigned_metrics = [unique_metrics[index] for index in assigned_keys]

        # Check if this process is unnecessary
        if len(assigned_metrics) == 0:
            return

        # Multi get series
        raw_assigned = self.redis_conn.mget(assigned_metrics)

        # Analyze the mothers
        for i, timeseries_name in enumerate(assigned_metrics):
            timeseries = json.loads(raw_assigned[i])
            run_algorithms(timeseries, timeseries_name)

    def run(self):
        """
        Called when the process intializes.
        """

        # Make sure Redis is up
        try:
            self.redis_conn.ping()
        except:
            print 'crucible can\'t connect to redis at socket path %s' % settings.REDIS_SOCKET_PATH
            sys.exit(1)

        # Discover unique metrics
        unique_metrics = list(self.redis_conn.smembers('crucible.unique_metrics'))

        if len(unique_metrics) == 0:
            print('no data in redis. run `sudo python load.py`')
            sys.exit(1)

        # Spawn processes
        pids = []
        for i in range(1, settings.CRUCIBLE_PROCESSES + 1):
            p = Process(target=self.spin_process, args=(i, unique_metrics))
            pids.append(p)
            p.start()

        # Send wait signal to zombie processes
        for p in pids:
            p.join()


if __name__ == "__main__":
    """
    Start Crucible.
    """

    # Make sure we can run all the algorithms
    try:
        from algorithms import *
        timeseries = map(list, zip(map(float, range(int(time())-86400, int(time())+1)), [1]*86401))
        ensemble = [globals()[algorithm](timeseries) for algorithm in settings.ALGORITHMS]
    except KeyError as e:
        print "Algorithm %s deprecated or not defined; check settings.ALGORITHMS" % e
        sys.exit(1)
    except Exception as e:
        print "Algorithm test run failed."
        traceback.print_exc()
        sys.exit(1)

    crucible = Crucible()
    crucible.run()
