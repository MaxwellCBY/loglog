# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 16:31:57 2022

@author: 2925582
"""


# necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
# read file using numpy to read txt file
pressure = np.loadtxt('Data/Pressure.txt')
rate = np.loadtxt('Data/Rate.txt')

#bp file is manually detected breakpoints
bp = np.loadtxt('Data/Processed_Rate.txt')

p_data = pd.DataFrame(pressure,columns = ['p_time','pressure'])

r_data = pd.DataFrame(rate,columns = ['r_time','rate'])

bp_data = pd.DataFrame(bp,columns = ['bp_time','bp_rate'])

# select the time period for PTA analysis
time_left = p_data['p_time'].values.min()
time_right = p_data['p_time'].values.max()

# Select the PTA data from the raw data 

Pressure = p_data[(p_data['p_time']>time_left)
                  &
                  (p_data['p_time']<time_right)]

Rate = r_data[(r_data['r_time']>time_left)
                  &
                  (r_data['r_time']<time_right)]

#BP is breaking points data set
BP = bp_data[(bp_data['bp_time']>time_left)
                  &
                  (bp_data['bp_time']<time_right)]

#Using difference to select the transient
Pressure['dp'] = Pressure['pressure'].diff()
Rate['dr']=Rate['rate'].diff()
BP['dbp']=BP['bp_rate'].diff()

Rate['locator']=np.arange(Rate.shape[0])
Rate.head()

PTA = Rate[Rate['dr']>15000]


# set the font size
plt.rcParams.update({'font.size': 16})

    
BP_shutin = PTA['locator'].values
BP_flow = PTA['locator'].values-1
interval= 0.4

for i in BP_shutin:
    t_shutin =  Rate['r_time'][Rate['locator'] ==i].values[0]
    BP_t = Pressure[(Pressure['p_time']>=(t_shutin-interval))
                            &
                    (Pressure['p_time']<=(t_shutin+interval))]
    
    BP_t = BP_t[['p_time','pressure']]
    delta_pressure = BP_t['pressure'].diff()
    delta_time= BP_t['p_time'].diff()
    BP_t['derivative'] = delta_pressure/delta_time
    plt.rcParams.update({'font.size': 8})
    
    figure,(ax1,ax2) = plt.subplots(2,1, figsize=(5,6),
                                    dpi=100,
                                    # 共享x轴
                                    sharex=True)
 
    ax1.scatter(BP_t['p_time'],BP_t['pressure'],linestyle = 'solid', color='red')
    ax1.set_ylabel('Pressure/psia')
    ax1.set_title('BP_%d points overview' %i)
    ax2.scatter(BP_t['p_time'],BP_t['derivative'],linestyle = 'solid', color='k')
    ax2.set_xlabel('Time/hr')
    ax2.set_ylabel('derivative')
    # 调整子图形之间的纵向距离
    figure.subplots_adjust(hspace=0.1) 
#    plt.savefig('BP_shutin/derivate%d.jpg'%i) 
    
    
 
    
    
