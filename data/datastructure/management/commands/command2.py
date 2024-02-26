# run_both_commands.py

from django.core.management import call_command
from threading import Thread

def function1():
    call_command('command')

def function2():
    call_command('command1')
def function5():
    call_command('command3')
thread1 = Thread(target=function1)
thread2 = Thread(target=function2)
thread5 = Thread(target=function5)

thread1.start() # returns immediately
thread2.start()
thread5.start()
def function3():
    call_command('onehr')
# thread3 = Thread(target=function3)
# thread3.start()
function3()
# thread1 = Thread(target=function1)
# thread2 = Thread(target=function2)

# thread1.start() # returns immediately
# thread2.start()
