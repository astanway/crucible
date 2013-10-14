import json
import redis
import settings
from os import getcwd
from os.path import dirname, join, realpath

def load():
    __location__ = realpath(join(getcwd(), dirname(__file__)))
    with open(join(__location__, 'data.json'), 'r') as f:
        data = json.loads(f.read())

        print "Connecting to Redis..."
        r = redis.StrictRedis(unix_socket_path=settings.REDIS_SOCKET_PATH)

        r.delete("crucible.unique_metrics")
      
        print "Loading data..."

        for index, series in enumerate(data):
            r.set("crucible." + str(index), json.dumps(series))
            r.sadd("crucible.unique_metrics", "crucible." + str(index))

        print "Loaded."
    
if __name__ == "__main__":
   load()
