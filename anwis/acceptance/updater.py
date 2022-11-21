from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

from acceptance.service import update_leftovers


def start():
    scheduler = BackgroundScheduler()
    trigger = OrTrigger([CronTrigger(minute=25)])
    scheduler.add_job(update_leftovers, trigger)
    scheduler.start()
