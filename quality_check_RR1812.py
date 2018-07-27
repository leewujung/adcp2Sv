
# coding: utf-8

# In[152]:


import numpy as np
import os, sys, glob, re
import matplotlib.pyplot as plt
from pycurrents.adcp.rdiraw import Multiread
import jdcal, datetime


# In[153]:


get_ipython().run_line_magic('matplotlib', 'inline')


# ## Load raw files using Multiread

# In[213]:


pname = '/Volumes/current_cruise/adcp/RR1812/raw/os150/'
fname = glob.glob(pname+'rr2018_203*.raw')
fname


# In[214]:


m = Multiread(pname+'rr2018_203_72000.raw','os')
data = m.read()


# In[215]:


data.pingtype


# In[216]:


m.list_configs()


# In[217]:


data.sysconfig


# In[218]:


data.amp.shape


# In[219]:


data.rVL


# ## Function to convert timestamp

# In[220]:


def dday2timestr(yr,dday):
    ''' 
    Convert dday to str of timestamp
    yr     data.yearbase
    dday   one or more items in a list from data.dday
    '''
    yr1day = jdcal.gcal2jd(yr,1,1)  # get numbers for start of the year
    gcal = [jdcal.jd2gcal(yr1day[0],yr1day[1]+x) for x in np.nditer(dday)]
    td = [datetime.datetime(year=xx[0],month=xx[1],day=xx[2])+datetime.timedelta(days=xx[-1]) for xx in gcal]
    return [x.strftime('%H:%M:%S') for x in td]


# ## Function to plot echogram

# In[221]:


def plot_echogram(val_mtx,ping_num,time_str,depth,fig_sz):
    '''
    Plot echogram for inspection
    Note this is just for plotting, TL compensation is done outside of this function
    Inputs:
       val_mtx   values to be plotted, can be data.amp or with compensation
       ping_num  the ping number to be plotted (slice indexing)
       time_str  use dday2timestr to get trabsmit time
       depth     data.dep
       fig_sz    (fig width, fig height)
    '''
    fig = plt.figure(figsize=fig_sz)
    plt.imshow(val_mtx.T,aspect='auto',interpolation='none',               extent=[0,val_mtx.shape[0],-depth[-1],-depth[0]],               vmin=100, vmax=300)
    plt.xticks(ping_num,time_str)
    plt.xlabel('Time (hr:min:sec)',fontsize='large')
    plt.ylabel('Depth (m)',fontsize='large')
    plt.ylim([-data.dep[-1],0])
    plt.colorbar()
    return fig


# ## Seawater absorption

# In[222]:


import arlpy
r = data.dep/np.cos(m.sysconfig['angle']*np.pi/180)  # convert depth to range [m]
SL = 20*np.log10(r)  # spreading loss
alpha_75k = arlpy.utils.mag2db(arlpy.uwa.absorption(75000,depth=100))      # seawater absorption at 75 kHz
alpha_150k = arlpy.utils.mag2db(arlpy.uwa.absorption(150000,depth=100))     # seawater absorption at 150 kHz
AB_75k = 2*alpha_75k*r/1000
AB_150k = 2*alpha_150k*r/1000


# ## Plot the whole file

# In[223]:


# set up x-axis
ping_jump = int(np.floor(data.dday.shape[0]/8))
ping_num = range(0,data.amp1.shape[0],ping_jump)
time_str = dday2timestr(data.yearbase,data.dday[::ping_jump])

# Plot TL-compensated echogram
fig = plot_echogram(data.amp1+SL-AB_150k,ping_num,time_str,data.dep,(15,4))
# fig.savefig(os.path.join('/Users/wujung/code/adcp2Sv/figs/',os.path.basename(fname[1])[0:-4]),dpi=200)


# ## Plot first 500 pings

# In[224]:


# set up x-axis
ping_jump = 50
ping_num = range(0,500,ping_jump)
time_str = dday2timestr(data.yearbase,data.dday[::ping_jump])

# Plot TL-compensated echogram
fig = plot_echogram(data.amp1[0:500,:]+SL-AB_150k,ping_num,time_str,data.dep,(15,4))
# fig.savefig(os.path.join('/Users/wujung/code/adcp2Sv/figs/',os.path.basename(fname[1])[0:-4])+'_first500ping',dpi=200)

