from apscheduler.scheduler import Scheduler
from realtimeTask import runRealtimeTask
from taskDebug import taskDebug

sched = Scheduler()

@sched.interval_schedule(minutes=5)
def timed_job():
    tic = time.clock()
    runRealtimeTask() 
    toc = time.clock()
    taskDebug('--- RealtimeTask done ['+ str(toc-tic) + ' seconds] ---')

sched.start()

while True:
    pass