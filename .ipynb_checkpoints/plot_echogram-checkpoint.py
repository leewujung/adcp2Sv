#!/Users/wujung/anaconda/envs/py27/bin/python
'''
Plot ADCP echogram for the latest files
'''
import numpy as np
import os, sys, glob, re
import matplotlib.pyplot as plt
#from pycurrents.adcp.rdiraw import Multiread
import datetime
import arlpy   # ARL underwater acoustics toolbox
from mpl_toolkits.axes_grid1 import make_axes_locatable

sys.path.append('/Users/wujung/adcpcode/programs')
from pycurrents.adcp.rdiraw import Multiread
import adcp_func


#import numpy as np
#import os, sys, glob, re
#import matplotlib.pyplot as plt
#import jdcal,datetime
#import arlpy   # ARL underwater acoustics toolbox
#from mpl_toolkits.axes_grid1 import make_axes_locatable



# Set up paths and params
pname_75 = '/Volumes/wjlee_apl_2/2017_cruises/ADCP_RR1713/raw/os75/'
pname_150 = '/Volumes/wjlee_apl_2/2017_cruises/ADCP_RR1713/raw/os150/'
nf = 5   # load the latest 5 files
fname_75 = glob.glob(pname_75+'*.raw')
fname_150 = glob.glob(pname_150+'*.raw')

m_75,data_75,param_75 = adcp_func.load_raw_files(fname_75[-nf:])
m_150,data_150,param_150 = adcp_func.load_raw_files(fname_150[-nf:])

# set up x-axis
ping_jump_150 = int(np.floor(data_150.dday.shape[0]/8))
ping_num_150 = range(0,data_150.amp1.shape[0],ping_jump_150)
time_str_150 = adcp_func.get_ping_time(data_150,ping_num_150)
#time_str_150 = adcp_func.dday2timestr(data_150.yearbase,data_150.dday[::ping_jump_150])

ping_jump_75 = int(np.floor(data_75.dday.shape[0]/8))
ping_num_75 = range(0,data_75.amp1.shape[0],ping_jump_75)
time_str_75 = adcp_func.get_ping_time(data_75,ping_num_75)
#time_str_75 = adcp_func.dday2timestr(data_75.yearbase,data_75.dday[::ping_jump_75])

# Plot
print 'Plotting...'
fig = plt.figure(figsize=(12,7))
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)
plt.subplots_adjust(hspace=0.25)
adcp_func.plot_echogram_ax(ax1,data_75.amp1-param_75['absorption']-2*param_75['spreading_loss'],\
                 ping_num_75,time_str_75,data_75.dep,[125,300])
adcp_func.plot_echogram_ax(ax2,data_150.amp1-param_150['absorption']-2*param_150['spreading_loss'],\
                 ping_num_150,time_str_150,data_150.dep,[125,300])
ax1.set_title('75 kHz')
ax1.set_xlabel('')
ax2.set_title('150 kHz')
ax1.set_ylim([-250,0])
ax2.set_ylim([-250,0])

# Save figure
now_datetime = datetime.datetime.now()
now_str =  now_datetime.strftime("%Y-%m-%d-%H-%M-%S")
fig.savefig(os.path.join('/Users/wujung/code/adcp2Sv/figs/'+now_str),dpi=200)

