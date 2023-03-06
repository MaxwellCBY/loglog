import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
from detectfunction import *

# function to plot the area between start line,bp_s and end line,bp_f, 2 plots
def plot_area(whole_p,whole_r,bp_s,bp_f):
    fig,(ax1,ax2) = plt.subplots(2,1, figsize=(24,12),  dpi=360,
                                # SHARE X
                                 sharex=True)
    #1/2 pic
    ax1.scatter(whole_p['Time'], whole_p['Pressure'],
             linestyle = 'solid', color='r',s=1.5)
    for i in np.arange(bp_s['Pressure'].shape[0]):
        ax1.axvline( bp_s['Time'].iloc[i], color = 'green')
    for j in np.arange(bp_f['Pressure'].shape[0]):
        ax1.axvline( bp_f['Time'].iloc[j], color = 'orange')
    for k in np.arange(bp_s['Pressure'].shape[0]):
        ax1.axvspan(bp_s['Time'].iloc[k], bp_f['Time'].iloc[k], alpha=0.2, color='green')
    ax1.set_ylabel('Pressure/psia')
    ax1.set_title('Result of Transient Identification', fontsize=40)
    # xlabel size
    ax1.xaxis.label.set_size(40)
    #ylabel size
    ax1.yaxis.label.set_size(40)
    # x tick size
    ax1.tick_params(axis='x', labelsize=40)
    # y tick size
    ax1.tick_params(axis='y', labelsize=40)

    

    #2/2 pic
    ax2.scatter(whole_r['Time'], whole_r['Rate'],
             linestyle = 'solid', color='b',s=1.5)
    for i in np.arange(bp_s['Pressure'].shape[0]):
        ax2.axvline( bp_s['Time'].iloc[i], color = 'green')
    for j in np.arange(bp_f['Pressure'].shape[0]):
        ax2.axvline( bp_f['Time'].iloc[j], color = 'orange')
    for k in np.arange(bp_s['Pressure'].shape[0]):
        ax2.axvspan(bp_s['Time'].iloc[k], bp_f['Time'].iloc[k], alpha=0.2, color='green')
    ax2.set_xlabel('Time/hr')
    ax2.set_ylabel('Rate/STB/D')
    # xlabel size
    ax2.xaxis.label.set_size(40)
    # ylabel size
    ax2.yaxis.label.set_size(40)
    # xtick size
    ax2.tick_params(axis='x', labelsize=40)
    # ytick size
    ax2.tick_params(axis='y', labelsize=40)
    # font size
    ax2.title.set_size(40)


    fig.subplots_adjust(hspace=0.2)

    fig.show


# function to plot the area between start line,bp_s and end line,bp_f, 1 plot
def plot_areap(whole_p,bp_s,bp_f):
    fig,ax1 = plt.subplots( figsize=(24,8),  dpi=360)

    ax1.scatter(whole_p['Time'], whole_p['Pressure'],
             linestyle = 'solid', color='r',s=1.5)
    for i in np.arange(bp_s['Pressure'].shape[0]):
        ax1.axvline( bp_s['Time'].iloc[i], color = 'green')
    for j in np.arange(bp_f['Pressure'].shape[0]):
        ax1.axvline( bp_f['Time'].iloc[j], color = 'orange')
    for k in np.arange(bp_s['Pressure'].shape[0]):
        ax1.axvspan(bp_s['Time'].iloc[k], bp_f['Time'].iloc[k], alpha=0.2, color='green')
    ax1.set_xlabel('Time/hr')   
    ax1.set_ylabel('Pressure/psia')
    ax1.set_title('Result of Transient Identification', fontsize=40)
    # xlabel size
    ax1.xaxis.label.set_size(40)
    #ylabel size
    ax1.yaxis.label.set_size(40)
    # x tick size
    ax1.tick_params(axis='x', labelsize=40)
    # y tick size
    ax1.tick_params(axis='y', labelsize=40)


    fig.show

# function to plot the break points in pressure and rate 2 plots
def plot_bp(whole_p,whole_r,bp_f,bp_s):
    fig,(ax1,ax2) = plt.subplots(2,1, figsize=(24,12),  sharex=True          )
    #1/2 pic 
    ax1.scatter(whole_p['Time'], whole_p['Pressure'],  linestyle = 'solid', color='r',s=1.5)
    ax1.scatter(bp_f['Time'],bp_f['Pressure'],
             color ='black',s=55,marker = '^')
    ax1.scatter(bp_s['Time'],bp_s['Pressure'],
             color ='black',s=55,marker = 'v')
    ax1.set_ylabel('Pressure/psia')
    ax1.set_title('Result of Transient Identification')

    #2/2 pic
    ax2.scatter(whole_r['Time'], whole_r['Rate'],
             linestyle = 'solid', color='b',s=1.5)
    for i in np.arange(bp_f['Pressure'].shape[0]):
        ax2.axvline( bp_f['Time'].iloc[i], color = 'green')
    for j in np.arange(bp_s['Pressure'].shape[0]):
        ax2.axvline( bp_s['Time'].iloc[j], color = 'orange')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Rate/STB/D')

    fig.subplots_adjust(hspace=0.2) 

    fig.show

# function to plot the break points in pressure 1 plot
def plot_bpp(whole_p,bp_f,bp_s):
    fig,ax1 = plt.subplots(figsize=(24,12),  dpi=120  )
    ax1.scatter(whole_p['Time'], whole_p['Pressure'],  linestyle = 'solid', color='r',s=1.5)
    ax1.scatter(bp_f['Time'],bp_f['Pressure'],
             color ='black',s=55,marker = '^')
    ax1.scatter(bp_s['Time'],bp_s['Pressure'],
             color ='black',s=55,marker = 'v')
    ax1.set_xlabel('Time/hr')
    ax1.set_ylabel('Pressure/psia')
    ax1.set_title('Result of Transient Identification')

    fig.show

# function to plot the bottom break points in pressure 1 plot
def plot_bpb(whole_p,bp_f):
    fig,ax1 = plt.subplots(figsize=(24,12),  dpi=120  )
    ax1.scatter(whole_p['Time'], whole_p['Pressure'],  linestyle = 'solid', color='r',s=1.5)
    ax1.scatter(bp_f['Time'],bp_f['Pressure'],
             color ='black',s=55,marker = '^')
    ax1.set_xlabel('Time/hr')
    ax1.set_ylabel('Pressure/psia')
    ax1.set_title('Result of Transient Identification_Bottom Breakpoints')

    fig.show

# plot 1 plot with 2 y axis
def plot_2y(x_p,y_p,x_r,y_r):
#draw the period
    plt.figure(figsize=(12,9),dpi = 100)
    
    plt.scatter(x_p,y_p, linestyle = 'solid', color='red', label = 'Pressure',s=3)
    plt.legend(loc=1)                 # Legend on the topleft
    y_min =y_p.values.min()-50
    y_max =y_p.values.max()+150
    plt.ylim(y_min,y_max)

    plt.xlabel('Time/hr')
    plt.ylabel('Pressure/psia')
# rignt y-axis
    ax2 = plt.twinx()
    ax2.scatter(x_r,y_r,linestyle = 'solid', color='b',s=3, label='Rate')
    ax2.set_ylabel('Rate/STB/D')      

    y2_min =-22000
    y2_max = 1000
    plt.ylim(y2_min,y2_max)   
    plt.legend(loc=4)                 # Legend on the bottomleft 

# zoom in plot with both df_bhp and df_rate, n is the number of bp in each zoom-in pic.

def plot_zoombp(df_bhp,df_rate,PTA,TI,n):
    
    T_s = TI[TI['label']=='shutin']
    T_f = TI[TI['label']=='flowing']
    
    sep_l = np.arange(0,len(PTA['locator'].values),n)
    sep_r = np.append(sep_l[1:],(len(PTA['locator'].values)-1))

    for i in np.arange(len(sep_l)):
        time_left = PTA['Time'].iloc[sep_l[i]]
        time_right = PTA['Time'].iloc[sep_r[i]]

        Pressure = df_bhp[(df_bhp['Time']>=time_left)
                        &
                        (df_bhp['Time']<=time_right)]

        Rate = df_rate[(df_rate['Time']>=time_left)
                        &
                        (df_rate['Time']<=time_right)]

        P_f = T_f[(T_f['Time']>=time_left)
                        &
                        (T_f['Time']<=time_right)]

        P_s = T_s[(T_s['Time']>=time_left)
                        &
                        (T_s['Time']<=time_right)]
        plot_bp(Pressure,Rate,P_f,P_s)

# function to plot the shut-in transient in pressure and rate 2 plots
def plot_zoomarea(df_bhp,df_rate,PTA,TI,n):
    
    T_s = TI[TI['label']=='shutin']
    T_f = TI[TI['label']=='flowing']
    
    sep_l = np.arange(0,len(PTA['locator'].values),n)
    sep_r = np.append(sep_l[1:],(len(PTA['locator'].values)-1))
    for i in np.arange(len(sep_l)):
        time_left = PTA['Time'].iloc[sep_l[i]]
        time_right = PTA['Time'].iloc[sep_r[i]]

        Pressure = df_bhp[(df_bhp['Time']>=time_left)
                        &
                        (df_bhp['Time']<=time_right)]

        Rate = df_rate[(df_rate['Time']>=time_left)
                        &
                        (df_rate['Time']<=time_right)]


        P_f = T_f[(T_f['Time']>=time_left)
                        &
                        (T_f['Time']<=time_right)]

        P_s = T_s[(T_s['Time']>=time_left)
                        &
                        (T_s['Time']<=time_right)]
                        
        # judge the start of P_f should be after P_s
    
        if (P_s.empty == False) & (P_f.empty == False):
            if len(P_s) >1:
                if len(P_s) > len(P_f):
                    P_s = P_s.iloc[:-1]
                    plot_area(Pressure,Rate,P_s,P_f) 
                elif len(P_s) == len(P_f) : 
                    
                    if P_s['Time'].iloc[0] > P_f['Time'].iloc[0]:
                        P_f = P_f.iloc[1:]
                        P_s = P_s.iloc[:-1]
                        plot_area(Pressure,Rate,P_s,P_f)
                    else:
                        plot_area(Pressure,Rate,P_s,P_f)   
                
                else:
                    P_f = P_f.iloc[1:]
                    plot_area(Pressure,Rate,P_s,P_f) 
            else :
                if P_s['Time'].iloc[0] < P_f['Time'].iloc[0]:
                    plot_area(Pressure,Rate,P_s,P_f)
                else:
                    pass
        else:
            pass


def plot_zoombp(df_bhp,df_rate,PTA,TI,n):
    
    T_s = TI[TI['label']=='shutin']
    T_f = TI[TI['label']=='flowing']
    
    sep_l = np.arange(0,len(PTA['locator'].values),n)
    sep_r = np.append(sep_l[1:],(len(PTA['locator'].values)-1))

    for i in np.arange(len(sep_l)):
        time_left = PTA['Time'].iloc[sep_l[i]]
        time_right = PTA['Time'].iloc[sep_r[i]]

        Pressure = df_bhp[(df_bhp['Time']>=time_left)
                        &
                        (df_bhp['Time']<=time_right)]

        Rate = df_rate[(df_rate['Time']>=time_left)
                        &
                        (df_rate['Time']<=time_right)]

        P_f = T_f[(T_f['Time']>=time_left)
                        &
                        (T_f['Time']<=time_right)]

        P_s = T_s[(T_s['Time']>=time_left)
                        &
                        (T_s['Time']<=time_right)]
        plot_bp(Pressure,Rate,P_f,P_s)

# zoomin plot area only pressure curve
def plot_zoomareap(df_bhp,PTA,TI,n):
    
    T_s = TI[TI['label']=='shutin']
    T_f = TI[TI['label']=='flowing']
    
    sep_l = np.arange(0,len(PTA['locator'].values),n)
    sep_r = np.append(sep_l[1:],(len(PTA['locator'].values)-1))
    for i in np.arange(len(sep_l)):
        time_left = PTA['Time'].iloc[sep_l[i]]
        time_right = PTA['Time'].iloc[sep_r[i]]

        Pressure = df_bhp[(df_bhp['Time']>=time_left)
                        &
                        (df_bhp['Time']<=time_right)]


        P_f = T_f[(T_f['Time']>=time_left)
                        &
                        (T_f['Time']<=time_right)]

        P_s = T_s[(T_s['Time']>=time_left)
                        &
                        (T_s['Time']<=time_right)]
                        
        # judge the start of P_f should be after P_s
    
        if (P_s.empty == False) & (P_f.empty == False):
            if len(P_s) >1:
                if len(P_s) > len(P_f):
                    P_s = P_s.iloc[:-1]
                    plot_areap(Pressure,P_s,P_f) 
                elif len(P_s) == len(P_f) : 
                    
                    if P_s['Time'].iloc[0] > P_f['Time'].iloc[0]:
                        P_f = P_f.iloc[1:]
                        P_s = P_s.iloc[:-1]
                        plot_areap(Pressure,P_s,P_f)
                    else:
                        plot_areap(Pressure,P_s,P_f)   
                
                else:
                    P_f = P_f.iloc[1:]
                    plot_areap(Pressure,P_s,P_f) 
            else :
                if P_s['Time'].iloc[0] < P_f['Time'].iloc[0]:
                    plot_areap(Pressure,P_s,P_f)
                else:
                    pass
        else:
            pass

def breakpoo(dd):
    # plot the zoom-in break point
    group_s = PTA_f['peak_locator'].values
    group_e = np.append(group_s[1:],(detect_p['peak_locator'].iloc[-1]))

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
        peak_right = peak_lo['lo']-5
        pressure_right = detect_period.iloc[peak_right.values[0]:peak_lo['lo'].values[0]]['Pressure'].mean()
        if (peak_lo['Pressure'].values - pressure_right)<10:
            # data from start to max
            rota = detect_period[['Time','Pressure']].iloc[:peak_lo['lo'].values[0]].values
            rotor.fit_rotate(rota)
            elbow_idx = rotor.get_elbow_index()
                
            fig = plt.subplots(1,1, figsize=(24,12),  dpi=120  )
            rotor.plot_elbow()
            plt.xlabel('Time/hr')
            plt.ylabel('Pressure/psia')
            
            peak = detect_period[detect_period['Time'] == rota[elbow_idx][0]]['peak_locator'].values[0]
            locator_s += [peak]
            

        else:
            
            fig,(ax) = plt.subplots(1,1, figsize=(24,12),  dpi=80  )

            ax.scatter(detect_period['Time'],detect_period['Pressure'])
            plt.axvline(peak_lo['Time'].values,color = 'black')
            plt.xlabel('Time/hr')
            plt.ylabel('Pressure/psia')
            peak = peak_lo['peak_locator'].values[0]
            locator_s += [peak]
        
#loglog plot
def loglogplot(df_loglog):
    fig, ax = plt.subplots(figsize=[24,12])
    #make a color list
    color = cm.rainbow(np.linspace(0, 1, len(df_loglog)))
    for i ,c  in zip(np.arange(len(df_loglog)),color):
        df_der = df_loglog[i]
       
        ax.scatter(df_der['dt'], df_der['dp'], s=35, marker = "x", label= 'Shut-in %d'%(i+1), color = c)
        ax.scatter(df_der['dt'], df_der['der'], s=35, marker = "o", color = c)
    
        # Label plot axes
        ax.set_xlabel(r'Elapsed Time ', fontsize=40)
        ax.set_ylabel(r'Pressure' + '\n' + r'Pressure Derivative', fontsize=40)

        # Label the plot title
        ax.set_title('log-log plot', fontsize=40)

        # Adjust log axes style and limits
    
        ax.set_xscale('log')
        ax.set_yscale('log')

        # adjust x label size
        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=20)
        # adjust x ticks size
        ax.tick_params(axis='x', which='major', labelsize=20)
        ax.tick_params(axis='y', which='major', labelsize=20)

        ax.legend(loc='best', fontsize=20)

        ax.grid(which='major', axis='both', alpha=1, color='k')
        ax.grid(which='minor', axis='both', linestyle=':', alpha=1, color='grey')
    
    return fig
