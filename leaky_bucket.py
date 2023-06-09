import time
import redis
import threading

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

redis.flushall()
bucket_capacity = 10
key = "user:123"

leak_rate = 10/60

def background_task(key):
    while(redis.llen(key) != 0):
        redis.rpop(key)
        time.sleep(1/leak_rate)
        #print(redis.llen(key))
        if(redis.llen(key) == 0):
            break
        
    #print("before delete")
    #time.sleep(1/leak_rate)
    redis.delete(key)

    #print("after delete")



#background_thread.start()
background_thread = threading.Thread(target=background_task , args=(key,))


def is_allowed(key,request_id):
    if redis.exists(key):
        if redis.llen(key) < bucket_capacity :
            redis.lpush(key,request_id)
            return True
        else:
            return False
    else:
        redis.lpush(key,request_id)
        

        print(background_thread.is_alive())
        background_thread.start()
        return True





for i in range(50):
    request = f"Request {i+1}"
    allowed = is_allowed(key,request)

    if allowed:
        print(f"{request} success")
    else:
        print(f"{request} failed")

    time.sleep(1) # time between two requests







