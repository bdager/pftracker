# -*- coding: utf-8 -*-
"""
Show precision and recall error metrics.

@author: Bessie Domínguez-Dáger
"""

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtWidgets import QSizePolicy


class plotE(FigureCanvas):
    """Plot precision and recall error per frame on the graphical interface.
    
    Args:
        P (array): precision value per frame, array with 
           (1, number_of_frames) dimension  
        R (array): recall value per frame, array with 
           (1, number_of_frames) dimension  
        P_mean (float): precision mean value
        R_mean (float): recall mean value   
    """
    
    def __init__(self, parent, P, R, P_mean, R_mean):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        x = np.arange(0,len(P))
        self.axes.plot(x,P, color='r', label='Precision', lw="1.5")
        self.axes.plot(x,R, color='b', label='Recall')
               
        self.axes.set_xlim([0, len(P)-1])
        self.axes.set_ylim([0, 1.05])
        self.axes.set_xticks([i for i in range(0,len(P)+1, len(P)//10)])
        self.axes.set_xlabel('Number of frames')
        self.axes.set_ylabel('Precision and Recall')
        self.axes.legend()
        self.axes.set_title('Error metrics')
        
        bbox_props = dict(boxstyle='round', fc='white', alpha=0.5, edgecolor='#999999')
        s = 'Medium precision: {:.2f}\nMedium recall: {:.2f}'.format(P_mean, R_mean)
        self.axes.text(len(P)-5, 0.1, s, ha='right', va='center', bbox=bbox_props)
        
        # show the major grid lines with dark grey lines
        self.axes.grid(b=True, which='major')
        
        # show the minor grid lines with very faint and almost transparent 
        # grey lines
        self.axes.minorticks_on()
        self.axes.grid(b=True, which='minor', color ='#999999', alpha=0.2)
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        
        # define the figure widget like expandible
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # notife to the system of the polize actualization
        FigureCanvas.updateGeometry(self)
        
        
class plotE_average(FigureCanvas):
    """Plot precision and recall error per frame on the graphical interface.
    
    Args:
        P (array): precision value per frame, array with 
           (1, number_of_frames) dimension  
        R (array): recall value per frame, array with 
           (1, number_of_frames) dimension  
        P_mean (float): precision mean value
        R_mean (float): recall mean value   
    """
    
    def __init__(self, parent, P, R, P_mean, R_mean):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        x = np.arange(1,len(P)+1)
        
        self.axes.plot(x,P, color='r', label='Precision', lw="1.5")
        self.axes.plot(x,R, color='b', label='Recall')  
                   
        self.axes.set_xlim([1, len(P)])
        self.axes.set_ylim([0, 1.05])
        
#        self.axes.set_xticks([i for i in range(0,len(P)+1, len(P)//10)])
        self.axes.set_xlabel('Number of runs')
        self.axes.set_ylabel('Precision and Recall')
        
        self.axes.legend()
        self.axes.set_title('Error metrics')
        
        bbox_props = dict(boxstyle='round', fc='white', alpha=0.5, 
                          edgecolor='#999999')
        s = 'Medium precision: {:.2f}\nMedium recall: {:.2f}'.format(P_mean, R_mean)
        self.axes.text(len(P)-0.2, 0.1, s, ha='right', va='center', bbox=bbox_props)
        
        # show the major grid lines with dark grey lines
        self.axes.grid(b=True, which='major')
        
        # show the minor grid lines with very faint and almost transparent 
        # grey lines
        self.axes.minorticks_on()
        self.axes.grid(b=True, which='minor', color ='#999999', alpha=0.2)
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        
        # define the figure widget like expandible
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # notife to the system of the polize actualization
        FigureCanvas.updateGeometry(self)
   