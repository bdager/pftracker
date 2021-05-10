# -*- coding: utf-8 -*-
"""
Show precision and recall error metrics. This script presents two functions:
plotE() and plotE_average(), both are called by pf_tracking_average.py
for generating particle filter tracking results on the paper.

@author: Bessie Domínguez-Dáger
"""
import numpy as np
import matplotlib.pyplot as plt

def plotE(P, R, P_mean, R_mean):
    """Plot precision and recall error per frame.
    
    Args:
        P (array): precision value per frame, array with 
           (1, number_of_frames) dimension  
        R (array): recall value per frame, array with 
           (1, number_of_frames) dimension  
        P_mean (float): precision mean value
        R_mean (float): recall mean value   
    """
    
    params = {'figure.figsize': (11,4.5), 'legend.fontsize': 14, 'font.size': 14,
              'xtick.labelsize': 12, 'ytick.labelsize': 12}
    plt.rcParams.update(params)
    
    x = np.arange(0,len(P))
    plt.plot(x, P, color='r', label='Precision')
    plt.plot(x, R, color='b', label='Recall')
    
    plt.ylim(ymin=0)
    plt.xlim(xmin=0, xmax=len(P)-1)
    plt.xlabel('Number of frames')
    plt.ylabel('Precision and Recall')
    plt.title('Error metrics', fontsize = 15)
    plt.legend()
    
    bbox_props = dict(boxstyle='round', fc='white', alpha=0.5, edgecolor='#999999')
    s = 'Medium precision: {:.2f}\nMedium recall: {:.2f}'.format(P_mean, R_mean)
    plt.text(len(P)-5, 0.1, s, ha='right', va='center', bbox=bbox_props)
    
    # show the major grid lines with dark grey lines
    plt.grid(b=True, which='major')
    
    # show the minor grid lines with very faint and almost transparent 
    # grey lines
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color ='#999999', linestyle='-', alpha=0.2)
        
    plt.show()
    
    
def plotE_average(P, R, P_mean, R_mean):
    """Plot precision and recall error per particle filter algorithm run.
    
    Args:
        P (array): precision value per frame, array with 
           (1, number_of_frames) dimension  
        R (array): recall value per frame, array with 
           (1, number_of_frames) dimension  
        P_mean (float): precision mean value
        R_mean (float): recall mean value   
    """
   

    params = {'figure.figsize': (11,4.5), 'legend.fontsize': 14, 'font.size': 14,
              'xtick.labelsize': 12, 'ytick.labelsize': 12}
    plt.rcParams.update(params)
    
    x = np.arange(1,len(P)+1)
    plt.plot(x, P, color='r', label='Precision', marker = "^", 
                       markersize="6", markeredgewidth="1", markerfacecolor="white",
                       markeredgecolor="red")
    plt.plot(x, R, color='b', label='Recall', marker = "s",
                       markersize="6", markeredgewidth="1", markerfacecolor="white",
                       markeredgecolor="blue")
    
    plt.ylim(ymin=0, ymax=1.05)
    plt.xlim(xmin=1, xmax=len(P))
    plt.xlabel('Number of tests')
    plt.ylabel('Precision and Recall')
    plt.title('Error metrics', fontsize = 15)
    plt.legend()
    
    bbox_props = dict(boxstyle='round', fc='white', alpha=0.5, edgecolor='#999999')
    s = 'Medium precision: {:.2f}\nMedium recall: {:.2f}'.format(P_mean, R_mean)
    plt.text(len(P)-0.2, 0.1, s, ha='right', va='center', bbox=bbox_props)
    
    # show the major grid lines with dark grey lines
    plt.grid(b=True, which='major')
    
    # show the minor grid lines with very faint and almost transparent 
    # grey lines
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color ='#999999', linestyle='-', alpha=0.2)
        
    plt.show()    