import logging
from redis import StrictRedis
from time import time, sleep
from threading import Thread
from collections import defaultdict
from multiprocessing import Process, Manager, Lock
from msgpack import Unpacker, unpackb, packb
from os import path, kill, getpid, system
import sys
from math import ceil
import traceback
import operator
import settings

from os import getpid
from os.path import dirname, abspath, isdir

# add the shared settings file to namespace
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings

from algorithms import run_selected_algorithm

class Crucible():
    def __init__(self):
        """
        Initialize the Crucible
        """
        self.redis_conn = StrictRedis(unix_socket_path = settings.REDIS_SOCKET_PATH)
        self.lock = Lock()
        self.anomaly_breakdown = Manager().dict()
        self.anomalous_metrics = Manager().list()

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

        # Make process-specific dicts
        anomaly_breakdown = defaultdict(int)

        # Distill timeseries strings into lists
        for i, metric_name in enumerate(assigned_metrics):

            try:
                raw_series = raw_assigned[i]
                unpacker = Unpacker(use_list = False)
                unpacker.feed(raw_series)
                timeseries = list(unpacker)

                anomalous, ensemble, datapoint = run_selected_algorithm(timeseries, metric_name)

                # If it's anomalous, add it to list
                if anomalous:
                    base_name = metric_name.replace(settings.FULL_NAMESPACE, '', 1)
                    metric = [datapoint, base_name]
                    self.anomalous_metrics.append(metric)

                    # Get the anomaly breakdown - who returned True?
                    for index, value in enumerate(ensemble):
                        if value:
                            algorithm = settings.ALGORITHMS[index]
                            anomaly_breakdown[algorithm] += 1

            # It could have been deleted by the Roomba
            except:
                print traceback.format_exc()

        # Collate process-specific dicts to main dicts
        with self.lock:
            for key, value in anomaly_breakdown.items():
                if key not in self.anomaly_breakdown:
                    self.anomaly_breakdown[key] = value
                else:
        	        self.anomaly_breakdown[key] += value


    def run(self):
        """
        Called when the process intializes.
        """
        now = time()

        # Make sure Redis is up
        try:
            self.redis_conn.ping()
        except:
            print 'crucible can\'t connect to redis at socket path %s' % settings.REDIS_SOCKET_PATH
            sys.exit(1)

        # Discover unique metrics
        unique_metrics = list(self.redis_conn.smembers('crucible.unique_metrics'))

        if len(unique_metrics) == 0:
            print('no metrics in redis. run `sudo python load.py`')
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

        # Log progress
        print('seconds to run    :: %.2f' % (time() - now))
        print('total metrics     :: %d' % len(unique_metrics))
        print('total anomalies   :: %d' % len(self.anomalous_metrics))
        print('anomaly breakdown :: %s' % self.anomaly_breakdown)

        # Reset counters
        self.anomalous_metrics[:] = []
        self.anomaly_breakdown = Manager().dict()


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
