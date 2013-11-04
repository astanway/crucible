import json
import redis
import settings
from os import getcwd, listdir
from os.path import dirname, join, realpath, isfile

def load():
    print "Connecting to Redis..."
    r = redis.StrictRedis(unix_socket_path=settings.REDIS_SOCKET_PATH)
    r.delete("crucible.unique_metrics")

    print "Loading data..."
    __location__ = realpath(join(getcwd(), dirname(__file__)))
    files = [ f for f in listdir(__location__ + "/timeseries/") if isfile(join(__location__+"/timeseries/",f)) ]
    for index, ts in enumerate(files):
        with open(join(__location__+"/timeseries/" + ts), 'r') as f:
            series = json.loads(f.read())
            r.set("crucible" + str(index), json.dumps(series))
            r.sadd("crucible.unique_metrics", "crucible" + str(index))

    print "Loaded."
    
if __name__ == "__main__":
   load()
