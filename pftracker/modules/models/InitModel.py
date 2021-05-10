# -*- coding: utf-8 -*-
"""
Move model creation.

@author: Bessie Domínguez-Dáger
"""

import numpy as np
from pftracker.modules.models import dlg


def createMovModel(estate_var):
    """ 
    Create a dynamic model for propagating particles to the next state.

    Args:
       estate_var (str): State space model
           
    Supported estate_var:
        - 'dynamic_bbox': Self updating bounding box model. 
             In this model the state vector is described by [x, y, Vx, Vy], 
             where (x,y) specify the location of the center of the face 
             window (bounding box) in the image coordinate system and 
             (Vx,Vy) represent the motion velocity. Here the boundig box 
             width is calculated in a self-updating model.
        - '5_variables': Five variables state space model.
             The width of bounding box is inluded in the state space,
             being the state vector define as: [x, y, Vx, Vy, w].
        - '6_variables': Six variables state space model.
             Here the state vector is given by: [x, y, Vx, Vy, w, Vw],
             where Vw is the corresponding rate of width change.
    
    Returns:
        2-element tuple containing
        
        - **dlg_model** (dlg): dlg object class
        - **size_ve** (int): state vector size
    """
    
    if estate_var=="dynamic_bbox":
        # create state transition matrix
        F = [[1, 0, 1, 0],                        
             [0, 1, 0, 1], 
             [0, 0, 1, 0], 
             [0, 0, 0, 1]]
        
        # create noise-system covariance matrix
        sigma_x = 80
        sigma_y = sigma_x
        sigma_vx = 10
        sigma_vy = sigma_vx         
        Sigma = np.diag(np.array([sigma_x, sigma_y, sigma_vx, sigma_vy]))
        
    elif estate_var=="5_variables":
        # create state transition matrix
        F = [[1, 0, 1, 0, 0],          
             [0, 1, 0, 1, 0], 
             [0, 0, 1, 0, 0], 
             [0, 0, 0, 1, 0],             
             [0, 0, 0, 0, 1]]   
        
         # create noise-system covariance matrix
        sigma_x = 80
        sigma_y = sigma_x
        sigma_vx = 10
        sigma_vy = sigma_vx
        sigma_w = 1
        Sigma = np.diag(np.array([sigma_x, sigma_y, sigma_vx, sigma_vy, sigma_w]))
              
    elif estate_var=="6_variables": 
        # create state transition matrix
        F = [[1, 0, 1, 0, 0, 0],          
             [0, 1, 0, 1, 0, 0], 
             [0, 0, 1, 0, 0, 0], 
             [0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 1, 1],
             [0, 0, 0, 0, 0, 1]]   
        
         # create noise-system covariance matrix
        sigma_x = 80
        sigma_y = sigma_x
        sigma_vx = 10
        sigma_vy = sigma_vx
        sigma_w = 1
        sigma_vw = 0.01
        Sigma = np.diag(np.array([sigma_x, sigma_y, sigma_vx, sigma_vy, sigma_w, sigma_vw]))
        
    # create noise-system mean vector 
    size_ve = len(F)                  # state vector size     
    mu = np.zeros(size_ve) 
           
    # create Discrete-time Linear and gaussian model
    dlg_model = dlg(F, mu, Sigma)
    
    return dlg_model, size_ve

