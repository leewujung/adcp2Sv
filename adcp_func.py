#!/Users/wujung/anaconda/envs/py27/bin/python
'''
Functions to load and plot ADCP data as echogram
'''

import numpy as np
import os, sys, glob, re
import matplotlib.pyplot as plt
from pycurrents.adcp.rdiraw import Multiread
import datetime
import arlpy   # ARL underwater acoustics toolbox
from mpl_toolkits.axes_grid1 import make_axes_locatable


#import numpy as np
#import os, sys, glob, re
#import matplotlib.pyplot as plt
#import jdcal, datetime
#import arlpy   # ARL underwater acoustics toolbox
#from mpl_toolkits.axes_grid1 import make_axes_locatable
#from pycurrents.adcp.rdiraw import Multiread
#import adcp_func


def load_raw_files(filename):
    '''
    Load the latest files
    Input:
       pname   path where data files are
       nf      number of latest files to load
    '''
    # get frequency info
    tmp = os.path.basename(os.path.dirname(filename[0]))
    freq = int(re.split('os*',tmp)[1])*1000  # get ADCP frequency [Hz]
    
    print 'Loading files... (os'+str(freq/1000)+')'
    for f in filename:  # print files that are being loaded
        print '  '+os.path.basename(f) 
    m = Multiread(filename,'os')  # read the latest nf files
    data = m.read()
    
    # get attenuation and spreading loss
    r = data.dep/np.cos(m.sysconfig['angle']*np.pi/180)  # convert depth to range [m]
    alpha = arlpy.utils.mag2db(arlpy.uwa.absorption(freq,depth=100))  # seawater absorption [dB/km]
    
    # prep output: note both absorption and spreading loss are negative
    param = dict([('freq',freq),\
                  ('range',r),\
                  ('alpha',alpha),\
                  ('absorption',2*alpha*r/1000),\
                  ('spreading_loss',-20*np.log10(r))])
    return m,data,param
    

def get_ping_time(data,ping_num):
    return [str(data.rVL['Second'][x])+':'+str(data.rVL['Second'][x])+':'+str(data.rVL['Second'][x]) for x in ping_num]
    

#def dday2timestr(yr,dday):
#    ''' 
#    Convert dday to str of timestamp
#    yr     data.yearbase
#    dday   one or more items in a list from data.dday
#    '''
#    yr1day = jdcal.gcal2jd(yr,1,1)  # get numbers for start of the year
#    gcal = [jdcal.jd2gcal(yr1day[0],yr1day[1]+x) for x in np.nditer(dday)]
#    td = [datetime.datetime(year=xx[0],month=xx[1],day=xx[2])+datetime.timedelta(days=xx[-1]) for xx in gcal]
#    return [x.strftime('%H:%M:%S') for x in td]


def plot_echogram_ax(ax,val_mtx,ping_num,time_str,depth,caxis):
    '''
    Plot echogram on a particular axis
    Note this is just for plotting, TL compensation is done outside of this function
    Inputs:
       ax        the axis to plot on
       val_mtx   values to be plotted, can be data.amp or with compensation
       ping_num  the ping number to be plotted (slice indexing)
       time_str  use dday2timestr to get trabsmit time
       depth     data.dep
    '''
    im = ax.imshow(val_mtx.T,aspect='auto',interpolation='none',\
               extent=[0,val_mtx.shape[0],-depth[-1],-depth[0]],\
               vmin=caxis[0], vmax=caxis[1])
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="1%", pad=0.05)
    cbar = plt.colorbar(im,cax=cax)
    #cbar.ax.tick_params(labelsize=14)
    ax.set_xticks(ping_num)
    ax.set_xticklabels(time_str)
    ax.set_xlabel('Time (hr:min:sec)',fontsize='large')
    ax.set_ylabel('Depth (m)',fontsize='large')
    ax.set_ylim([-depth[-1],0])


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
    plt.imshow(val_mtx.T,aspect='auto',interpolation='none',\
               extent=[0,val_mtx.shape[0],-depth[-1],-depth[0]],\
               vmin=100, vmax=300)
    plt.xticks(ping_num,time_str)
    plt.xlabel('Time (hr:min:sec)',fontsize='large')
    plt.ylabel('Depth (m)',fontsize='large')
    plt.ylim([-data.dep[-1],0])
    plt.colorbar()
    return fig


