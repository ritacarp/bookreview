from apscheduler.schedulers.blocking import BlockingScheduler
from app.tasks.tasks import example
 
sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='fri', hour=16)
def scheduled_job():
    print('1) Example job is run friday at 4pm.')
    example(60)
    print('2) Example job finished.')

sched.start()