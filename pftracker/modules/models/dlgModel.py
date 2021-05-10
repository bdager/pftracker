# -*- coding: utf-8 -*-
"""
Discrete-time Linear and gaussian system equation.

@author: Bessie Domínguez-Dáger
"""

import numpy as np

class dlg():
    """
    Propagate particles from time k-1 to k using a Discrete-time Linear 
    and gaussian model in the prediction step of particle filters.
    
    Args:
        F (array): State transition matrix with (state_vector_size,
          state_vector_size) dimension  
        muW (array): Noise-system mean vector with (state_vector_size,1)
            dimension
        SigmaW (array): Noise-system covariance matrix with (state_vector_size,
          state_vector_size) dimension            
    """
    
    def __init__(self, F, muW, SigmaW):                    
        self.F = F                    # State transition matrix 
        self.muW = muW                # noise-system mean vector
        self.SigmaW = SigmaW          # noise-system covariance matrix                      
        
    def move_particles(self, xk_1, N):     
        """Move particles from time k-1 to time k.
        
        Args:
            xk_1 (array): particles in the previous state, with 
                (state_vector_size,N) dimension. 
            N (int): number of samples
            
        Returns:
            2-element tuple containing
            
            - **xk** (*array*): particles in the actual state with 
              (state_vector_size,N) dimension. 
            - **muk** (*array*): characterization of x_{k}|x_{k-1} 
              where particles are moved particles from x_{k-1} to x_{k} 
              without include the process noise.
        """
        
        noise = np.random.multivariate_normal(self.muW, self.SigmaW, N).T
        muk = np.dot(self.F, xk_1)
        xk = muk + noise            # xk: particles in the actual state
        return xk, muk
        