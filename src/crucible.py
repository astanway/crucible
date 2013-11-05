import logging
from time import time
from multiprocessing import Process
import os
from os.path import dirname, join, abspath, isfile
from sys import exit
import traceback
from settings import ALGORITHMS
import json
import shutil
from os import getcwd, listdir, makedirs

from algorithms import run_algorithms

class Crucible():

    def run(self):
        """
        Called when the process intializes.
        """
        __data__ = abspath(join(dirname( __file__ ), '..', 'data'))
        files = [ f for f in listdir(__data__) 
                    if isfile(join(__data__,f)) ]

        # Spawn processes
        pids = []
        for index, ts_name in enumerate(files):
            if ts_name == ".DS_Store":
            	continue

            __data__ = abspath(join(dirname( __file__ ), '..', 'data'))
            with open(join(__data__ + "/" + ts_name), 'r') as f:
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
    
    __results__ = abspath(join(dirname( __file__ ), '..', 'results'))

    try:
        shutil.rmtree(__results__)
        makedirs(__results__)
    except:
        makedirs(__results__)

    crucible = Crucible()
    crucible.run()
