# run_both_commands.py

from django.core.management import call_command
from threading import Thread

def function1():
    call_command('command')

def function2():
    call_command('command1')

thread1 = Thread(target=function1)
thread2 = Thread(target=function2)

thread1.start() # returns immediately
thread2.start()