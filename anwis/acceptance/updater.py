from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

from acceptance.service import update_leftovers, update_photos_from_wb

def start():
    scheduler = BackgroundScheduler()
    trigger = OrTrigger([CronTrigger(minute=25)])
    scheduler.add_job(update_leftovers, trigger)
    scheduler.add_job(update_photos_from_wb, trigger)
    scheduler.start()
