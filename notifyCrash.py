import os
import Push_notification as psh
import sys


print('enter pid:\n')
pid = int(sys.argv[1])
os.waitpid(pid)


MSG = 'BOT CRASHED OR WAS SHUT OFF'
psh.push(MSG)
