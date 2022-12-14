from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

from .services import update_leftovers


def start():
    scheduler = BackgroundScheduler()
    trigger = OrTrigger([CronTrigger(hour=20, minute=35)])
    scheduler.add_job(update_leftovers, trigger)
    scheduler.start()
