import time
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)
redis.flushall()
user = "user"
key = f'{user}:123'


time_window_sec = 30
capacity = 10

def is_allowed():
    current_time = int(time.time())

    start_time = current_time - time_window_sec
    window = get_current_window(key,start_time)

    if window > capacity:
        return False
    else:
        register_request(str(current_time))
        return True
    
def get_current_window(key,start_time):
    ts_data = redis.hgetall(key)
    if not key:
        return 0
    total_requests = 0
    ls = ts_data.items()
    lst = []
    
    for ts,count in ls:
        lst.append((ts.decode(),count.decode()))
    
    for ts,count in lst:
        if int(ts) > start_time:
            total_requests += int(count)
        else:
            redis.hdel(key,ts)
    
    return total_requests

def register_request(time):
    redis.hincrby(key,time,amount=1)



for _ in range(50):
    #print(int(time.time()))
    allowed = is_allowed()
    

    if allowed:
        
        print(f"{_}request success")
    else:
        
        print(f"{_}rate limit exceeded")
    time.sleep(2) #time interval between consecutive requests


    






