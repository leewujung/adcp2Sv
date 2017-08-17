#!/Users/wujung/anaconda/envs/py27/bin/python
'''
Test writing  random things to text file
'''

import datetime, sys

now_datetime =  datetime.datetime.now()
now_str =  now_datetime.strftime("%Y-%m-%d-%H-%M-%S")

with open('/Users/wujung/code/adcp2Sv/figs/'+now_str+'.txt', mode='a') as file:
    file.write('Printed string recorded at %s.\n' % 
               datetime.datetime.now())
