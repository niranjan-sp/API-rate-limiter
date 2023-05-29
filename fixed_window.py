import time
class RateLimiter:
    def __init__(self,rate_limit,window_size):
        self.rate_limit = rate_limit
        self.current_time = int(time.time())
        self.window_size = window_size
        self.requests = []  # a list to record the timestamps at which requests were made
    
    def allow_request(self):
        current_time = int(time.time())

        for req in self.requests: # to remove requests that are outside the current window
            if req < (current_time - self.window_size):
                self.requests.remove(req)

        if len(self.requests) < self.rate_limit:
            self.requests.append(current_time)
            return True
        else:
            return False

limiter = RateLimiter(5,30)

for i in range(40):
    if limiter.allow_request():
        print("API request successful")
    else:
        print("Rate Limit exceded")
    
    time.sleep(2)


