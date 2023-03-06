# necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import find_peaks
from kneebow.rotor import Rotor
import datetime
from datetime import datetime,timedelta

# function to detect the bottom breakpoints, return to PTA_f
def detect_bottombp(df_bhp,p):
   
    # reverse the pressure curve
    df_bhp = df_bhp.copy()
    df_bhp['-Pressure'] = -df_bhp['Pressure']
    df_bhp['order']=df_bhp['Time']-df_bhp['Time'].iloc[0]
    df_bhp['locator']=np.arange(df_bhp.shape[0])

    detect_p = df_bhp.sort_values(by = 'Time',ascending=False,ignore_index=True)
    detect_p['order']=detect_p['order'].iloc[0]-detect_p['order']
    detect_p['peak_locator'] = np.arange(detect_p.shape[0])
    
    # detect the bottom breakpoints using scipy find_peaks()
    # input of scypy find_peaks() should be a numpy array
    X = detect_p['-Pressure'].values

    # p is the prominance
    peaks, _ = find_peaks(X, prominence =p)
    locator_f = peaks

    # put the bottom breakpoints into a dataframe
    PTA_f = pd.DataFrame()
    for i in locator_f:
        PTx = detect_p[ detect_p['peak_locator']== i]
        PTA_f = pd.concat([PTA_f,PTx])
        
    # the bottom breakpoints are the end of shut-in transients, and the start of flowing transients
    label = []
    for i in np.arange(len(locator_f)):
        label += ['flowing']
    PTA_f['label'] = label
    return (PTA_f)

# function to detect the top breakpoints, return to PTA_s
# made on 2022/10/11
def detect_topbp(df_bhp,PTA_f):
    
    df_bhp = df_bhp.copy()
    df_bhp['-Pressure'] = -df_bhp['Pressure']
    df_bhp['order']=df_bhp['Time']-df_bhp['Time'].iloc[0]
    df_bhp['locator']=np.arange(df_bhp.shape[0])

    detect_p = df_bhp.sort_values(by = 'Time',ascending=False,ignore_index=True)
    detect_p['order']=detect_p['order'].iloc[0]-detect_p['order']
    detect_p['peak_locator'] = np.arange(detect_p.shape[0])
    # detect the top breakpoints
    group_s = PTA_f['peak_locator'].values
    group_e = np.append(group_s[1:],(detect_p['peak_locator'].iloc[-1]))

    rotor = Rotor()
    locator_s = []

    for i in np.arange(len(PTA_f)):
        time_left = group_s[i]
        time_right = group_e[i]
        
        # The Shut-in point is excluded.

        detect_period = detect_p.iloc[(time_left+1):time_right]
        # lo is the sequence number for the detection period
        detect_period = detect_period.copy()
        detect_period['lo']= np.arange(len(detect_period))


        peak_lo = detect_period[detect_period['Pressure']==detect_period['Pressure'].max()].head(1)

        if peak_lo['lo'].values[0] > 0:
            rota = detect_period[['Time','Pressure']].iloc[:peak_lo['lo'].values[0]].values
            rotor.fit_rotate(rota)
            

            elbow_idx = rotor.get_elbow_index()
            Peak_pressure = detect_period[detect_period['Time'] == rota[elbow_idx][0]]['Pressure'].values[0]

            if elbow_idx == 0:
                peak = peak_lo['peak_locator'].values[0]
                locator_s += [peak]


            else:
                if Peak_pressure > (peak_lo['Pressure'].values[0]+detect_period['Pressure'].values[0])/2:
                    peak = detect_period[detect_period['Time'] == rota[elbow_idx][0]]['peak_locator'].values[0]
                    locator_s += [peak]

                else:
                    peak = peak_lo['peak_locator'].values[0]
                    locator_s += [peak] 

        else: # (This is quite due to the interval between points are too big, in real case, this can be ignored)
            rota = detect_period[['Time','Pressure']].iloc[:peak_lo['lo'].values[0]+1].values
            rotor.fit_rotate(rota)
            elbow_idx = rotor.get_elbow_index()

            if elbow_idx == 0:
                peak = peak_lo['peak_locator'].values[0]
                locator_s += [peak]

            else:
                peak = detect_period[detect_period['Time'] == rota[elbow_idx][0]]['peak_locator'].values[0]
                locator_s += [peak]
            

    PTA_s = pd.DataFrame()
        
    for j in locator_s:
        PTx = detect_p[ detect_p['peak_locator']== j]
        PTA_s = pd.concat([PTA_s,PTx])

    label = []
    for i in np.arange(len(locator_s)):
        label += ['shutin']
    PTA_s['label'] = label
    return(PTA_s)

# new function to detect the top breakpoints, return to PTA_s
# made on 2023/02/11
def newdetect_topbp(df_bhp,PTA_f):
    # reverse the pressure curve
    df_bhp = df_bhp.copy()
    df_bhp['-Pressure'] = -df_bhp['Pressure']
    df_bhp['order']=df_bhp['Time']-df_bhp['Time'].iloc[0]
    df_bhp['locator']=np.arange(df_bhp.shape[0])

    detect_p = df_bhp.sort_values(by = 'Time',ascending=False,ignore_index=True)
    detect_p['order']=detect_p['order'].iloc[0]-detect_p['order']
    detect_p['peak_locator'] = np.arange(detect_p.shape[0])

    # detect the top breakpoints
    group_s = PTA_f['peak_locator'].values
    group_e = np.append(group_s[1:],(detect_p['peak_locator'].iloc[-1]))

    rotor = Rotor()
    locator_s = []

    for i in np.arange(len(PTA_f)):
        time_left = group_s[i]
        time_right = group_e[i]
        
        # The Shut-in point is excluded.
        detect_period = detect_p.iloc[(time_left+1):time_right]

        # lo is the sequence number for the detection period
        detect_period = detect_period.copy()
        detect_period['lo']= np.arange(len(detect_period))

        # find the maximum pressure point in the detection period 
        peak_lo = detect_period[detect_period['Pressure']==detect_period['Pressure'].max()].head(1)

        # the target pressure is to avoid the noise, there is space for improvement here
        Target_pressure = (peak_lo['Pressure'].values[0]+detect_period['Pressure'].values[0])/2

        # this judge is the basic condition for detecting the top breakpoints, 
        # to judge if there are points in the detection period
        
        if peak_lo['lo'].values[0] > 0:
            
            # select the data from the bottom break point to the peak point, and rotate it from the bottom break point
            rota = detect_period.iloc[:peak_lo['lo'].values[0]]
            rota_rotate = rota[['Time','Pressure']].values
            rotor.fit_rotate(rota_rotate)
            elbow_idx = rotor.get_elbow_index()
            
            # the pressure where the peak point is
            Peak_pressure = detect_period[detect_period['Time'] == rota_rotate[elbow_idx][0]]['Pressure'].values[0]
            
            # Judge 1 !!!
            # elbow_idx == 0 means that there is no elbow point in the detection period, 
            # the peak point is the top break point
            if elbow_idx == 0:
                peak = peak_lo['peak_locator'].values[0]
                locator_s += [peak]
            
            # elbow_idx != 0 means that there is elbow point in the detection period,
            else:
                # Judge 2 !!!
                # the target pressure separate the detect period into 2 parts, 
                # the first part is from the peak point to the target pressure, 
                # in this part, the elbow point is the top break point.

                if Peak_pressure > Target_pressure:
                    peak = detect_period[detect_period['Time'] == rota_rotate[elbow_idx][0]]['peak_locator'].values[0]
                    locator_s += [peak]
                
                # Judge 3 !!!
                # the second part is from the target pressure to the bottom break point,
                # in this part, the new peak point is replaced by the target pressure,
                # and then, check the elbow point again.

                else:
                    # select the new peak point, which is the clostest to the target pressure
                    rota = rota.copy()
                    rota['diff'] = abs(rota['Pressure']-Target_pressure)
                    new_dpeak = rota.sort_values(by = 'diff',ascending=True)

                    # select the second row of the new_detect dataframe as a dataframe
                    new_dpeak = new_dpeak.iloc[1:2]

                    # select detect_period from the time of the bottom break point to the time of the new_detect
                    rota_new = rota[['Time','Pressure']]
                    rota_new = rota_new[rota_new['Time']>=new_dpeak['Time'].values[0]].values

                    # another rotation from the new peak point, which is the clostest to the target pressure
                    # from the bottom break point to the new peak point
                    rotor.fit_rotate(rota_new)
                    elbow_idx_new = rotor.get_elbow_index()

                    # the pressure where the new peak point is
                    Peak_pressure_new = detect_period[detect_period['Time'] == rota_new[elbow_idx_new][0]]['Pressure'].values[0]
                    
                    # Judge 4 !!!
                    # elbow_idx_new == 0 means that there is no elbow point in the detection period,
                    # the new peak point is the top break point
                    if elbow_idx_new == 0:
                        peak = new_dpeak['peak_locator'].values[0]
                        locator_s += [peak]
                    
                    # elbow_idx_new != 0 means that there is elbow point in the detection period,
                    # the elbow point is the true top break point
                    else:
                        peak = detect_period[detect_period['Time'] == rota_new[elbow_idx_new][0]]['peak_locator'].values[0]
                        locator_s += [peak] 

        else: # (This is quite due to the interval between points are too big, in real case, this can be ignored)
            rota = detect_period[['Time','Pressure']].iloc[:peak_lo['lo'].values[0]+1].values
            rotor.fit_rotate(rota)
            elbow_idx = rotor.get_elbow_index()

            if elbow_idx == 0:
                peak = peak_lo['peak_locator'].values[0]
                locator_s += [peak]

            else:
                peak = detect_period[detect_period['Time'] == rota[elbow_idx][0]]['peak_locator'].values[0]
                locator_s += [peak]
            
    

    
    PTA_s = pd.DataFrame()
    for j in locator_s:
        PTx = detect_p[ detect_p['peak_locator']== j]
        PTA_s = pd.concat([PTA_s,PTx])

    label = []
    for i in np.arange(len(locator_s)):
        label += ['shutin']
    PTA_s['label'] = label
    return(PTA_s)

#  function to detect all the breakpoints, reutrn in PTA
def detect_PTA(df_bhp,PTA_f,PTA_s):

    df_bhp = df_bhp.copy()
    df_bhp['-Pressure'] = -df_bhp['Pressure']
    df_bhp['order']=df_bhp['Time']-df_bhp['Time'].iloc[0]
    df_bhp['locator']=np.arange(df_bhp.shape[0])

    detect_p = df_bhp.sort_values(by = 'Time',ascending=False,ignore_index=True)
    detect_p['order']=detect_p['order'].iloc[0]-detect_p['order']
    detect_p['peak_locator'] = np.arange(detect_p.shape[0])

    PTA= pd.concat([PTA_f,PTA_s])

    PTe = detect_p.iloc[:1]
    PTs = detect_p.iloc[-1:]
    PTe = PTe.copy()
    PTs = PTs.copy()
    PTs['label']=['start']
    PTe['label']=['end']

    PTA= pd.concat([PTA,PTs])
    PTA= pd.concat([PTA,PTe])

    PTA = PTA.sort_values("Time",ascending = True)
    
    return(PTA)

# function to detect the shut-in transient longer than the interval
def detect_TI(PTA_f,PTA_s, interval):
    
    TI = pd.DataFrame()
    # calculte the maximum duration between PTA_f['Time'] and PTA_s['Time']
    max_duration = max(PTA_f['Time'].values - PTA_s['Time'].values)
    
    # if the maximum duration is smaller than the interval, then return the dataframe
    # print the warning message "The interval is too big"
    if max_duration < interval:
        print("The interval is too big,the dataframe is empty")
        return(TI)
    else:
        for i in np.arange(len(PTA_f)):
            if PTA_f['Time'].iloc[i] - PTA_s['Time'].iloc[i] > interval:
        
                TI = pd.concat([TI,PTA_s.iloc[[i]]])
                TI = pd.concat([TI,PTA_f.iloc[[i]]])
                # sort the dataframe by time
                TI = TI.sort_values(by = 'Time',ascending = True)
        return(TI)


# print the shut-in detection results
def detect_result(TI,interval):
    if TI.empty:
        print('There is no shut-in transient that longer than %d hours.'% (interval))
    else:
        T_s = TI[TI['label']=='shutin']
        T_f = TI[TI['label']=='flowing']
        DT = pd.DataFrame()
        DT['Length'] = T_f['Time'].values - T_s['Time'].values
        print('There are %d shut-in transients that longer than %d hours.'% (T_s.shape[0],interval))
        print('The longest identified shut-in transient is %d hours.'% (DT.max()[0]))
        print('The shortest identified shut-in transient is %d hours.'% (DT.min()[0]))

def calc_derivative(time, pressure, factor_L):

#Bourdet logarithmic pressure derivative
        
#Parameters
#----------
#time: time array (k,)
#pressure: bhp array (k,) 
#factor_L: smoothing factor (float)
        
#Returns
#-------
#deriv_pressure: bourdet derivative (m,)
           
    n_points = len(time)
    deriv_pressure = []
    i = 0
    while i < n_points:
        t1 = time[i]
        p1 = pressure[i]
        # encontrar o ti-1
        j = i
        while j > 0:
            if time[j] < t1 / np.exp(factor_L):
                break
            j -= 1
        # encontrar o ti+1
        k = i
        while k < n_points-1:
            if time[k] > t1 * np.exp(factor_L):
                break
            k += 1

        p0, p2 = pressure[j], pressure[k]
        t0, t2 = time[j], time[k]
        log_t0 = np.log(t0) if t0 != 0 else 0
        log_t1 = np.log(t1) if t1 != 0 else 0
        log_t2 = np.log(t2) if t2 != 0 else 0
        w1 = log_t1 - log_t0
        w2 = log_t2 - log_t1
        m1 = (p1-p0)/w1 if w1 > 0 else 0
        m2 = (p2-p1)/w2 if w2 > 0 else 0
        tdpdt = m1*w2/(w1+w2) + m2*w1/(w1+w2)
        deriv_pressure.append(tdpdt)
        i+=1
    return np.array(deriv_pressure)