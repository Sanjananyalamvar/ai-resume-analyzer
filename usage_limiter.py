import time
from collections import deque
class DailyCounter:
    def __init__(self): self.events=deque()
    def count(self):
        now=time.time()
        while self.events and now-self.events[0]>=86400: self.events.popleft()
        return len(self.events)
    def add(self): self.events.append(time.time())
def check_and_record(session_state,counter,session_limit,daily_limit,cooldown_seconds,prefix='ai'):
    now=time.time(); sk=f'_{prefix}_events'; ck=f'_{prefix}_last'
    events=session_state.setdefault(sk,[]); events[:]=[t for t in events if now-t<86400]
    last=session_state.get(ck,0)
    if len(events)>=session_limit: return False,'Session usage limit reached. Please try again later.'
    if counter.count()>=daily_limit: return False,'The shared daily usage limit has been reached. Try again tomorrow.'
    if now-last<cooldown_seconds: return False,f'Please wait {int(cooldown_seconds-(now-last))+1} seconds before trying again.'
    events.append(now); session_state[ck]=now; counter.add(); return True,None
def refund(session_state,counter,prefix='ai'):
    events=session_state.get(f'_{prefix}_events',[])
    if events: events.pop()
    if counter.events: counter.events.pop()
