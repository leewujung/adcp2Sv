#!/Users/wujung/anaconda/envs/py27/bin/python
'''
Test writing  random things to text file
'''

import datetime, os, glob

pname = '/Users/wujung/code/adcp2Sv/figs/'
fname = glob.glob(pname+'*.txt')

for x in fname[-5:]:
        print x
        
print 'No problem!'