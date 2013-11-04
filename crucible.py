import logging
from time import time
from multiprocessing import Process
from os.path import dirname, join, realpath, isfile, exists
from sys import exit
import traceback
from settings import ALGORITHMS
import json
from os import getcwd, listdir, makedirs

from algorithms import run_algorithms

class Crucible():

    def run(self):
        """
        Called when the process intializes.
        """
        __location__ = realpath(join(getcwd(), dirname(__file__)))
        files = [ f for f in listdir(__location__ + "/data/") 
                    if isfile(join(__location__ + "/data/",f)) ]

        # Spawn processes
        pids = []
        for index, ts_name in enumerate(files):
            with open(join(__location__ + "/data/" + ts_name), 'r') as f:
                timeseries = json.loads(f.read())
                p = Process(target=run_algorithms, args=(timeseries, ts_name))
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
        ensemble = [globals()[algorithm](timeseries) for algorithm in ALGORITHMS]
    except KeyError as e:
        print "Algorithm %s deprecated or not defined; check settings.ALGORITHMS" % e
        exit(1)
    except Exception as e:
        print "Algorithm test run failed."
        traceback.print_exc()
        exit(1)
    
    __results__ = realpath(join(getcwd(), dirname(__file__))) + "/results/"
    if not exists(__results__):
        makedirs(__results__)

    crucible = Crucible()
    crucible.run()
