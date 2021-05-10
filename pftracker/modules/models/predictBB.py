# -*- coding: utf-8 -*-
"""
The boundig box is calculated in a self-updating model.

@author: Bessie Domínguez-Dáger
"""
import numpy as np

def self_updating_bbox(center, bbox, dl, particles, N):
    """Self updating bounding box model.
    
    Args:
        center (list): 2-elements list of particle filter estimation 
            (x,y coordinates of bounding box center)
        bbox (int): bounding box width at previos time
        dl (float): average distance from the previous frame to the target center
        particles (array): particles array x_{k} with (size_v, N) dimension
        N (int): number of particles
        
    Returns:
         2-element tuple containing
            
         - **bbox_new** (*int*): new bounding box width prediction
        - **d** (*float*): average distance between the particles and 
          the target center
        
    """
    
    # average distance between the particles and the target center
    d = (1/N) * np.sum(np.sqrt(np.sum(np.square(center-particles[:,1:2]))))
    
    # calculate the new bounding box
    bbox_new = np.around(bbox*d/dl).astype(int)
    
    return bbox_new, d
    