from django.core.management.base import BaseCommand
# from schedule import every, run_pending
import schedule
import time
from datastructure.views import get1hrdata,get1hrdatac,get4hrdata,get4hrdatac,get24hrdata,get24hrdatac

class Command(BaseCommand):
    help = 'Execute an hourly task'

    

    def handle(self, *args, **options):
        self.job()
        time.sleep(60)
        self.job1()
        time.sleep(60)
        self.job2()
        time.sleep(60)
        # Schedule the job to run every hour
        schedule.every(1).hours.do(self.job)
        schedule.every(4).hours.do(self.job1)
        schedule.every(24).hours.do(self.job2)
        while True:
            # Run any pending scheduled tasks
            schedule.run_pending()
            
            # Sleep for a short duration (e.g., 1 minute) before the next iteration
            
    
    def job(self):
        get1hrdata()
        get1hrdatac()

    def job1(self):
        get4hrdata()
        get4hrdatac()

    def job2(self):
        get24hrdata()
        get24hrdatac()
        
    
