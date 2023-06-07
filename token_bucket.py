import time
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)
redis.flushall()

bucket_capacity = 10
replenish_time = 60
user = "user"
key = f'{user}:123'

initialising_dict ={
    "tokens" : bucket_capacity,
    "last_refill_time" : int(time.time())

}


def is_allowed(key,time):
    if (redis.exists(key)):
        if(time - int((redis.hget(key,"last_refill_time")).decode()) >= 60 ):
            redis.hset(key,"tokens",bucket_capacity)
            redis.hset(key,"last_refill_time",time)
            redis.hincrby(key,"tokens",amount=-1)
            return True
        else:
            if (int((redis.hget(key,"tokens")).decode())>0):
                redis.hincrby(key,"tokens",amount=-1)

                return True
            else:
                return False
    else:
        redis.hmset(key,initialising_dict)
        
        redis.hincrby(key,"tokens",amount=-1)
        return True
    
for _ in range(1,51):
    
    allowed = is_allowed(key,int(time.time()))
    

    if allowed:
        
        print(f"{_}request success")
    else:
        
        print(f"{_}rate limit exceeded")
    time.sleep(2) #time interval between consecutive requests
    


    

