import numpy as np


def shutindata(df_bhp,df_rate,T_s,T_f):
    # make a list to store dataframes for shutin plot
    df_bhp_list = []
    df_rate_list = []
    # the length of the list is the number of shut-in transient
    for i in range(len(T_s)):
        df_bhp_list.append(df_bhp[(df_bhp['Time']>=T_s['Time'].iloc[i]) & (df_bhp['Time']<=T_f['Time'].iloc[i])])
        # reset the index of the dataframe
        df_bhp_list[i].reset_index(drop=True,inplace=True)
        df_rate_list.append(df_rate[(df_rate['Time']>=T_s['Time'].iloc[i]) & (df_rate['Time']<=T_f['Time'].iloc[i])])
        df_rate_list[i].reset_index(drop=True,inplace=True)
    return df_bhp_list,df_rate_list

def loglogdata (df_bhp,df_rate,T_f):
    # make a list to store dataframes for loglog plot
    df_bhp_list_log = []
    df_rate_list_log = []
    # the length of the list is the number of shut-in transient
    for i in range(len(T_f)):
        # the start time is alwayes the start of df_bhp['Time'].iloc[0]
        # the end time is the value of T_f['Time'].iloc[i]
        df_bhp_list_log.append(df_bhp[(df_bhp['Time']>=df_bhp['Time'].iloc[0]) & (df_bhp['Time']<=T_f['Time'].iloc[i])])
        df_rate_list_log.append(df_rate[(df_rate['Time']>=df_bhp['Time'].iloc[0]) & (df_rate['Time']<=T_f['Time'].iloc[i])])
    return df_bhp_list_log,df_rate_list_log

def calculate_shutin_length (T_f,T_s):
    # claculate the length of the shut-in transient, and store it in a list
    shutin_length = []
    for i in range(len(T_f)):
        shutin_length.append(T_f['Time'].iloc[i] - T_s['Time'].iloc[i])
    return shutin_length

# calculate the rate before shut-in
def calculate_rate_median (df_rate,T_f,T_s,shutin_length):
    # make a new list to store the data from (T_s.Time.iloc[0]-shutin_length[0]) to T_s.Time.iloc[0]
    df_rate_list_new = []
    # make a list to store the median value of the rate
    median_rate_list = []
    for i in range(len(T_f)):
        df_rate_list_new.append(df_rate[(df_rate['Time']>=T_s['Time'].iloc[i]-shutin_length[i]) & (df_rate['Time']<=T_s['Time'].iloc[i])])
        # calculate the median value of the rate
        median_rate = df_rate_list_new[i]['Rate'].median()
        median_rate_list.append(median_rate)
    return median_rate_list

def calculate_rate_last (df_rate,T_f,T_s,shutin_length):
    # make a new list to store the data from (T_s.Time.iloc[0]-shutin_length[0]) to T_s.Time.iloc[0]
    df_rate_list_new = []
    # make a list to store the median value of the rate
    last_rate_list = []
    for i in range(len(T_f)):
        df_rate_list_new.append(df_rate[(df_rate['Time']>=T_s['Time'].iloc[i]-shutin_length[i]) & (df_rate['Time']<=T_s['Time'].iloc[i])])
        # calculate the last value of the rate
        last_rate = df_rate_list_new[i]['Rate'].iloc[-1]
        last_rate_list.append(last_rate)
    return last_rate_list

def bourdet_der(median_rate_list,df_bhp_list,i,T_s,ratio_qr):
# the reference rate is regarded as the median value of the rate
    qr = median_rate_list[i]*ratio_qr
    
# the rate value before shut-in
    qn = median_rate_list[i]
# the superposition of the two parts

# the second part is the part before shut-in
    pro1 = -(qr-0)/qn*np.log10(df_bhp_list[i].Time.values[1:] - 0)

# the first part is the part before shut-in
    bui1 = -(0-qr)/qn*np.log10(df_bhp_list[i].Time.values[1:]-T_s.Time.iloc[i])

# the superposition time is the sum of the two parts 
    t_s = pro1 + bui1

# the pressure value from the beginning of shutin to the end of shutin
    p = df_bhp_list[i].Pressure.values[1:]
# the bourdet derivative includes 3 points, t0, t1, t2, p0, p1, p2
# t0 is the point before t1, t2 is the point after t1
    t0 = t_s[0:-2]
    t1 = t_s[1:-1]
    t2 = t_s[2:]
# p0 is the point before p1, p2 is the point after p1
    p0 = p[0:-2]
    p1 = p[1:-1]
    p2 = p[2:]

# the derivative is calculated by the formula
    x1 = t1-t0
    x2 = t2-t1
# absolute value of p1-p0 is needed
    pp1 = np.abs(p1-p0)
    pp2 = np.abs(p2-p1)
# the derivative is calculated by the formula
    der = (pp1/x1*x2 + pp2/x2*x1)/(x1+x2)
    der = der/np.log(10)
# remove the last der, because it is always not accurate
    der = der[0:-1]
# the time for loglog plot
    ttt = df_bhp_list[i].Time.values[1:]-df_bhp_list[i].Time.values[0]
# note the shape of der should be the same as ttt_der
    ttt_der = ttt[1:-2] 
# the pressure difference
    ppp = np.abs(df_bhp_list[i].Pressure.values-df_bhp_list[i].Pressure.values[0])
    ppp = ppp[1:]
# ttt_der is the time for derivative
# der is the derivative
# ttt is the time for pressure difference
# ppp is the pressure difference
    return ttt_der,der,ttt,ppp