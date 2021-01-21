import os
import Push_notification as psh


print('enter pid:\n')
pid = int(input())
os.waitpid(pid)

MSG = 'BOT CRASHED OR WAS SHUT OFF'
psh.push(MSG)
