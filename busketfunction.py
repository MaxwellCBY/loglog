import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from plotfunction import *

# save the identified curve
def save_curve(PTA,TI,df_bhp):
    # incert PTs to the first row of TI
    TIse = pd.concat([PTA.iloc[0:1],TI],axis=0)
    # incert PTe to the last row of TI
    TIse = pd.concat([TIse,PTA.iloc[-1:]],axis=0)

    # separate df_bhp according to TIse's points
    split_l = []
    split_r = []
    for i in np.arange(len(TIse)-1):
        split_l.append(TIse['Time'].iloc[i])
        split_r.append(TIse['Time'].iloc[i+1])

    for i in np.arange(len(split_l)):
        time_left = split_l[i]
        time_right = split_r[i]
        #time_left keep 1 decimal
        tl = time_left.round(1)
        #time_right keep 1 decimal
        tr = time_right.round(1)

        pp = df_bhp[(df_bhp['Time']>=time_left)
                        &
                        (df_bhp['Time']<=time_right)]

        pp = pp[['Time','Pressure']].copy()   
        
        if pp['Pressure'].iloc[0] < pp['Pressure'].iloc[-1]:
            label = '1' # 1 means flowing
            pp['label'] = label
            pp['label'] = pp['label'].astype(int)


            files_save_path = "TI_curve/Flowing_curve" 

            if not os.path.exists(files_save_path):
                os.makedirs(files_save_path)

            fig, ax = plt.subplots(figsize=(10, 10),dpi = 120)
            ax.scatter(pp['Time'],pp['Pressure'],color = 'black',s = 10)
            # without axis
            ax.axis('off')
            # save the figure
            fig.savefig(os.path.join(files_save_path,'curve_Flowing_%d_%d.png'%(tl,tr)),facecolor='white')
            plt.close()
    

        else:
        
            label = '0' # 0 means shutin
            pp['label'] = label 
            pp['label'] = pp['label'].astype(int) 

        # save pp to csv
            files_save_path = "TI_curve/Shutin_data" 
            if not os.path.exists(files_save_path):
                os.makedirs(files_save_path)

            fig, ax = plt.subplots(figsize=(10, 10),dpi = 120)
            ax.scatter(pp['Time'],pp['Pressure'],color = 'black',s = 10)
            # without axis
            ax.axis('off')
            # save the figure
            fig.savefig(os.path.join(files_save_path,'curve_Shutin_%d_%d.png'%(tl,tr)),facecolor='white')
            plt.close()


# save the identified data
def save_data(PTA,TI,df_bhp):
    # incert PTs to the first row of TI
    TIse = pd.concat([PTA.iloc[0:1],TI],axis=0)
    # incert PTe to the last row of TI
    TIse = pd.concat([TIse,PTA.iloc[-1:]],axis=0)

    # separate df_bhp according to TIse's points
    split_l = []
    split_r = []
    for i in np.arange(len(TIse)-1):
        split_l.append(TIse['Time'].iloc[i])
        split_r.append(TIse['Time'].iloc[i+1])

    for i in np.arange(len(split_l)):
        time_left = split_l[i]
        time_right = split_r[i]
        #time_left keep 1 decimal
        tl = time_left.round(1)
        #time_right keep 1 decimal
        tr = time_right.round(1)

        pp = df_bhp[(df_bhp['Time']>=time_left)
                        &
                        (df_bhp['Time']<=time_right)]

        pp = pp[['Time','Pressure']].copy()   
        
        if pp['Pressure'].iloc[0] < pp['Pressure'].iloc[-1]:
            label = '1' # 1 means flowing
            pp['label'] = label
            pp['label'] = pp['label'].astype(int)


            files_save_path = "TI_data/Flowing_data" 

            if not os.path.exists(files_save_path):
                os.makedirs(files_save_path)

            pp.to_csv(os.path.join(files_save_path,'data_Flowing_%d_%d.csv'%(tl,tr)),index=False)

        else:
        
            label = '0' # 0 means shutin
            pp['label'] = label 
            pp['label'] = pp['label'].astype(int) 

        # save pp to csv
            files_save_path = "TI_data/Shutin_data" 
            if not os.path.exists(files_save_path):
                os.makedirs(files_save_path)
            pp.to_csv(os.path.join(files_save_path,'data_Shutin_%d_%d.csv'%(tl,tr)),index=False)


# add label to the time series data, eg, 1 means flowing, 0 means shutin
def data_addlabel(PTA,TI,df_bhp):
    # incert PTs to the first row of TI
    TIse = pd.concat([PTA.iloc[0:1],TI],axis=0)
    # incert PTe to the last row of TI
    TIse = pd.concat([TIse,PTA.iloc[-1:]],axis=0)
    # separate df_bhp according to TIse's points
    split_l = []
    split_r = []
    for i in np.arange(len(TIse)-1):
        split_l.append(TIse['Time'].iloc[i])
        split_r.append(TIse['Time'].iloc[i+1])

    # create a new dataframe to store the data
    ti_label = pd.DataFrame()

    for i in np.arange(len(split_l)):
        time_left = split_l[i]
        time_right = split_r[i]

        pp = df_bhp[(df_bhp['Time']>=time_left)
                        &
                        (df_bhp['Time']<=time_right)]

        pp = pp[['Time','Pressure']].copy()   
        
        if pp['Pressure'].iloc[0] < pp['Pressure'].iloc[-1]:
            label = '1' # 1 means flowing

            pp['label'] = label
            pp['label'] = pp['label'].astype(int)
            # append pp to ti_label
            ti_label = pd.concat([ti_label,pp],axis=0)

        else:
        
            label = '0' # 0 means shutin
            pp['label'] = label 
            pp['label'] = pp['label'].astype(int) 

           # append pp to ti_label
            ti_label = pd.concat([ti_label,pp],axis=0)
    # keep only unique values in ti_label['Time']
    ti_label = ti_label.drop_duplicates(subset='Time',keep='first')
    return(ti_label)

# function to adjust A1,2,5,20 raw data to be usable with TPMR method
def adjust_A1(df_bhpraw):

    pd.options.mode.chained_assignment = None
    df_bhpraw['Time'] = df_bhpraw.index

    df_bhpraw = df_bhpraw.copy() # use the copy for the following
    df_bhpraw1 = df_bhpraw[['Time','DHP']]
    # times the 'DHP' value by 14.5038 to convert to psi
    df_bhpraw1['DHP'] = df_bhpraw1['DHP']*14.5038
    
    df_rateraw1 = df_bhpraw[['Time','RAT']]
    # change df_bhpraw1 name of columns
    df_bhpraw1.columns = ['Time','Pressure']
    df_rateraw1.columns = ['Time','Rate']

    # delete rows of df_bhpraw1 before df_bhpraw1['Pressure'] first NaN value

    df_rateraw1 = df_rateraw1.loc[df_bhpraw1['Pressure'].first_valid_index():]
    df_bhpraw1 = df_bhpraw1.loc[df_bhpraw1['Pressure'].first_valid_index():]

    time_start = df_bhpraw1['Time'].head(1).astype(str).iloc[0]
    time_end = df_bhpraw1['Time'].tail(1).astype(str).iloc[0]

    df_bhp = df_bhpraw1[(df_bhpraw1['Time'] > time_start) & (df_bhpraw1['Time'] < time_end)]
    df_rate = df_rateraw1[(df_rateraw1['Time'] > time_start) & (df_rateraw1['Time'] < time_end)]


    # delete row of df_bhp == 0
    df_bhp = df_bhp[df_bhp['Pressure'] != 0]
    # select row of df_rate['Time'] start from df_bhp['Time'].iloc[0]
    df_rate = df_rate[df_rate['Time'] >= df_bhp['Time'].iloc[0]]

    df_bhp = df_bhp.dropna()
    df_rate = df_rate.dropna()

    # change time to accumulated time
    df_bhp = df_bhp.copy()
    ts = df_bhp['Time']-df_bhp['Time'].iloc[0]
    df_bhp['hr'] = ts / timedelta(hours = 1)
    df_bhp = df_bhp[['hr','Pressure']]
    df_bhp = df_bhp.rename(columns={'hr':'Time'})
    df_bhp.reset_index(drop = True,inplace = True)

    # change time to accumulated time

    df_rate = df_rate.copy()
    ts = df_rate['Time']-df_rate['Time'].iloc[0]
    df_rate['hr'] = ts / timedelta(hours = 1)
    df_rate = df_rate[['hr','Rate']]
    df_rate = df_rate.rename(columns={'hr':'Time'})
    df_rate.reset_index(drop = True,inplace = True)
    return(df_bhp,df_rate)


# adjust the 
def adjust_C5(pressure):

    # change the index to column
    pressure['Time'] = pressure.index

    # choose the columns 'TIMESTEP' and 'q' of interest
    df_bhp = pressure[['Time','BHP']]
    df_bhp.columns = ['Time','Pressure']
    df_bhp = df_bhp.copy()

    df_rate = pressure[['Time','q']]
    # change column name
    df_rate.columns = ['Time','Rate']

    return df_bhp, df_rate



# function to adjust B8B raw data to be usable with TPMR method
# raw data has 2 inputs: df_bhpraw and df_rateraw
def adjust_B8B_raw (df_bhpraw,df_rateraw):
    # copy the dataframes
    df_bhpraw = df_bhpraw.copy()
    df_rateraw = df_rateraw.copy()
    # rename the columns
    df_bhpraw.columns = ['Time','Pressure']
    df_rateraw.columns = ['Time','Rate']

    # select the data from timestamp'2010-03-21'
    df_bhp = df_bhpraw[df_bhpraw['Time']>'2010-03-21']
    df_rate = df_rateraw[df_rateraw['Time']>'2010-03-21']
    # select df_bhp to the end timestamp of df_rate
    df_bhp = df_bhp[df_bhp['Time']<df_rate['Time'].iloc[-1]]

    # check nan values if necessary !!!
    # df_bhp.isna().sum()
    # df_rate.isna().sum()

    # reset the index
    df_bhp = df_bhp.reset_index(drop=True)
    df_rate = df_rate.reset_index(drop=True)

    # change time to accumulated time
    df_bhp = df_bhp.copy()
    ts = df_bhp['Time']-df_bhp['Time'].iloc[0]
    df_bhp['hr'] = ts / timedelta(hours = 1)
    df_bhp = df_bhp[['hr','Pressure']]
    df_bhp = df_bhp.rename(columns={'hr':'Time'})
    df_bhp.reset_index(drop = True,inplace = True)

    # change time to accumulated time

    df_rate = df_rate.copy()
    ts = df_rate['Time']-df_rate['Time'].iloc[0]
    df_rate['hr'] = ts / timedelta(hours = 1)
    df_rate = df_rate[['hr','Rate']]
    df_rate = df_rate.rename(columns={'hr':'Time'})
    df_rate.reset_index(drop = True,inplace = True)

    return df_bhp,df_rate

# function to adjust B8B resampled data to be usable with TPMR method
# resampled data has 1 input: df_input
def adjust_B8B_resample (df_input):
    # copy the dataframes
    df_b = df_input.copy()
    # put index to a column
    df_b['Time'] = df_b.index
    # change index to int
    df_b.index = np.arange(len(df_b))
    # rename BHP to Pressure
    df_b = df_b.rename(columns={'BHP':'Pressure'})
    # rename WIR to Rate
    df_b = df_b.rename(columns={'WIR':'Rate'})
    # select df_bhpraw Time and Pressure
    df_bhpraw = df_b[['Time','Pressure']]
    # select df_rateraw Time and Rate
    df_rateraw = df_b[['Time','Rate']]

    # select the data from timestamp'2010-03-21'
    df_bhp = df_bhpraw[df_bhpraw['Time']>'2010-03-21']
    df_rate = df_rateraw[df_rateraw['Time']>'2010-03-21']
    # select df_bhp to the end timestamp of df_rate
    df_bhp = df_bhp[df_bhp['Time']<df_rate['Time'].iloc[-1]]

    # check nan values if necessary !!!
    # df_bhp.isna().sum()
    # df_rate.isna().sum()

    # delete the nan values
    df_bhp = df_bhp.dropna()
    df_rate = df_rate.dropna()

    # reset the index
    df_bhp = df_bhp.reset_index(drop=True)
    df_rate = df_rate.reset_index(drop=True)

    # change time to accumulated time
    df_bhp = df_bhp.copy()
    ts = df_bhp['Time']-df_bhp['Time'].iloc[0]
    df_bhp['hr'] = ts / timedelta(hours = 1)
    df_bhp = df_bhp[['hr','Pressure']]
    df_bhp = df_bhp.rename(columns={'hr':'Time'})
    df_bhp.reset_index(drop = True,inplace = True)

    # change time to accumulated time

    df_rate = df_rate.copy()
    ts = df_rate['Time']-df_rate['Time'].iloc[0]
    df_rate['hr'] = ts / timedelta(hours = 1)
    df_rate = df_rate[['hr','Rate']]
    df_rate = df_rate.rename(columns={'hr':'Time'})
    df_rate.reset_index(drop = True,inplace = True)

    return df_bhp,df_rate


def info_input(df_bhp):
    # check how long in years
    timed = df_bhp['Time'].max() - df_bhp['Time'].min()
    # change timed to years
    timed = timed/24/365
    # keep 2 decimal places
    timed = round(timed,2)
    print('The input data is', timed, 'years')
    print('The input data contains', df_bhp.shape[0], 'points')
        
