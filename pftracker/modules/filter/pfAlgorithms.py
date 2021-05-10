# -*- coding: utf-8 -*-
"""
This module implements four particle filter algorithms for solving 
an estimation problem.

All particle filters estimate in a two-stage process: prediction and update. 

@author: Bessie Domínguez-Dáger
"""

import numpy as np
from filterpy.kalman import KalmanFilter

class pfiltering():
    """Particle filter algorithms.
    
    This class contains four particle filter algorithms and the needed 
    methods for running them. 
    
    Supported particle filter algorithms:
        - SIS: Sequential Importance Sampling filter
        - SIR: Sequential Importance Resampling filter
        - G_PF: Generic particle filter
        - APF: Auxilliary particle filter
    
    Args:
        N (int): Number of particles 
    """
    def __init__(self, N):
        self.N = N
        
        # Initialize weights
        self.w = np.ones((1,N)) / N       # weights are uniform at first
        self.i = 0
        
    def neff(self):
        """
        Calculate the number of effective particles.

        Returns:
            (float) number of effective particles
        """
        return 1. / np.sum(np.square(self.w))
     
    def resample_from_index(self, particles, indexes):
        """Returns resampled particles according to indexes.
        
        Args:
            particles (array): predicted particles at time k with 
                (state_vector_size,N) dimension 
            indexes (array): indixes resulting from resampling step
                with (1,N) dimension 
        """
        particles[:, :] = particles[:,indexes]
        self.w[0,:] = self.w[0,indexes]
        self.w.fill(1.0 / len(self.w))
        return particles
    
    def kalman_filter(self, particles_0):
        """Initialize Kalman filter algorithm.
        
        Args:
            particles_0 (array): initial particles distribution with
                (state_vector_size,N) dimension 
        """
        
        self.size = np.size(particles_0, axis=0)
        if self.size==4:
            # Create a Kalman filter object
            # dim_x: Number of state variables for the Kalman filter
            # dim_z: Number of measurement inputs
            self.f = KalmanFilter(dim_x=self.size, dim_z=self.size//2)
            self.f.x = particles_0
            
            # Transition matrix
            self.f.F = np.array([[1, 0, 1, 0],          
                                 [0, 1, 0, 1], 
                                 [0, 0, 1, 0], 
                                 [0, 0, 0, 1]])
            
            # Measurement function
            self.f.H = np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0]])
        elif self.size==5: 
            # Create a Kalman filter object
            self.f = KalmanFilter(dim_x=self.size, dim_z=self.size//2+1)
            self.f.x = particles_0
            
            # Transition matrix
            self.f.F = np.array([[1, 0, 1, 0, 0],           
                                 [0, 1, 0, 1, 0], 
                                 [0, 0, 1, 0, 0], 
                                 [0, 0, 0, 1, 0],
                                 [0, 0, 0, 0, 1]])
            
            # Measurement function
            self.f.H = np.array([[1, 0, 0, 0, 0],
                                 [0, 1, 0, 0, 0],
                                 [0, 0, 0, 0, 1]])
        elif self.size==6:
            # Create a Kalman filter object
            self.f = KalmanFilter(dim_x=self.size, dim_z=self.size//2)
            self.f.x = particles_0
            
            # Transition matrix
            self.f.F = np.array([[1, 0, 1, 0, 0, 0],          
                                 [0, 1, 0, 1, 0, 0], 
                                 [0, 0, 1, 0, 0, 0], 
                                 [0, 0, 0, 1, 0, 0],
                                 [0, 0, 0, 0, 1, 1],
                                 [0, 0, 0, 0, 0, 1]])
            
            # Measurement function
            self.f.H = np.array([[1, 0, 0, 0, 0, 0],
                                 [0, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 1, 0]])
        
        self.f.P *= 1    # Current state covariance matrix
        self.f.R *= 1    # Measurement noise matrix
        self.f.Q *= 1    # Process noise matrix
    
    def calc_uk_with_kf(self, pf, particles):
        """
        Calculate characterization u_{k} of the distribution p(x_{k}|x_{k-1}).
        
        The characterization u_{k} is used in the first stage weigths of
        th APF algorithm and is obtained using a Kalman filter 
        in which the observation comes from the distribution p(x_{k}|x_{k-1}), 
        without include the noise of the dynamic model employed. The 
        magnitude of the noise associated with the distribution 
        p(x_{k}|x_{k-1}) can afect the performance of the APF.
        
        Args:
            pf (particlefilter): particlefilter class object
            particles (array): particles at time k-1 with
                (state_vector_size,N) dimension 
        
        Returns:
            (array) of particles u_{k} with (state_vector_size,N) dimension 
        """
        
        if self.i==0:      
            # initialize Kalmar filter                 
            self.kalman_filter(particles[:,0]) 
            self.i=1
       
        # get predicted particles without include the noise of 
        # the dynamic model
        _, muk = pf.prediction(particles) 
        media = np.sum(muk, axis=1)/self.N

        if self.size==4:
            z = np.array([media[0], media[1]])
        elif self.size==5 or self.size==6:
            z = np.array([media[0], media[1], media[4]])
        
        # one step Kalman Filter prediction
        self.f.predict(F=self.f.F, Q=self.f.Q)
        
        # one step Kalman Filter update
        self.f.update(z, self.f.R, self.f.H)
        
        # create a multivariate gaussian distribution from KF results
        uk = np.random.multivariate_normal(self.f.x, self.f.P, self.N).T
        
        return uk        
        
    def SIS(self, pf, particles):
        """Run Sequential Importance Sampling (SIS) filter.
        
        Args:
            pf (particlefilter): particlefilter class object
            particles (array): particles at time k-1 with
                (state_vector_size,N) dimension 
        
        Returns:
            (array) of particles x_{k} with (state_vector_size,N) dimension 
        """
        
        # prediction step
        particles, _ = pf.prediction(particles) 
        
        # update step
        likelihood  = pf.update(particles)  
        
        # calculate weights
        self.w = self.w * likelihood
        
        # normalize weights
        self.w /= np.sum(self.w)    
         
        # estimate step
        pf.estimate(particles, self.w)

        return particles
        
    def SIR(self, pf, particles):
        """Run Sequential Importance Sampling (SIR) filter.
        
        This filter includes an additional resampling step in each 
        SIS algorithm iteration. Resampling generates a new set
        of particles from the normalized weight, resampling N times 
        from the pdf p(x_{k}|z_{k}). This is done by copying particles 
        with higher weight and discarding low weight particles. This step 
        tries to concentrate particles around state space regions with 
        high importance.
        
        Args:
            pf (particlefilter): particlefilter class object
            particles (array): particles at time k-1 with
                (state_vector_size,N) dimension 
        
        Returns:
            (array) of particles x_{k} with (state_vector_size,N) dimension 
        """
        
        particles = self.SIS(pf, particles)  
        
        # Resample step
        indexes =  pf.resample(self.w.T)
        particles = self.resample_from_index(particles, indexes)
        
        return particles
        
    def G_PF(self, pf, particles, resamplePercent):
        """Run generic particle filter.
        
        This filter includes the resampling step only in some 
        iterations of the SIS algorithm. Resampling is applied 
        when the effective number of particles (N_{eff}^{(k)})
        is below a threshold N_{T}.
        
        Args:
            pf (particlefilter): particlefilter class object
            particles (array): particles at time k-1 with
                (state_vector_size,N) dimension 
        
        Returns:
            (array) of particles x_{k} with (state_vector_size,N) dimension 
        """
        
        particles = self.SIS(pf, particles)
        
        # Resample step
        # Resample if there's too few effective particles
        if self.neff() < resamplePercent:      # If particle cloud degenerate:
            # Resample particles according to self.w
            indexes =  pf.resample(self.w.T)
            particles = self.resample_from_index(particles, indexes)  
                    
        return particles

    def APF(self, pf, particles):#, resamplePercent):
        """Run auxilliary particle filter (APF).
        
        The APF calculates the weights in a two-stage process.
        The first stage weights uses a characterization (u_{k})
        of the distribution p(x_{k}|x_{k-1}) and calculates the 
        weigths of it. Then the algorithm tries to predict which 
        particles are located in regions of high likelihood that 
        constitute the best representation of the set of predicted 
        samples at time k. 
        
        Second stage weights use this information 
        to resample particles (x_{k-1}) at time k-1, propagate them 
        to time k and calculate the likelihoods. Final weights are
        obtained dependent on the actual likelihoods and the likelihood 
        obtained from the characterization u_{k}.
        
        Args:
            pf (particlefilter): particlefilter class object
            particles (array): particles at time k-1 with
                (state_vector_size,N) dimension 
        
        Returns:
            (array) of particles x_{k} with (state_vector_size,N) dimension 
        """        
        
        # calculate u_{k} from p(x_{k}|x_{k-1})
        uk = self.calc_uk_with_kf(pf, particles)
        
        # calculate likelihood for u_{k}, this is p(z_{k}|u_{k})
        likelihood_uk = pf.update(uk)        
                           
        # calculate first stage weights w_{k}^{i} with u_{k}^{i}
        w1 = self.w * likelihood_uk
            
        # normalize weights
        w1 /= np.sum(w1)              
            
        # resample from first stage weights
        indexes =  pf.resample(w1.T)
            
        # get particles x_{k-1}^{idx}  
        particles[:, :] = particles[:, indexes]
            
        # prediction step, move particles from x_{k-1}^{idx} to x_{k}
        particles, _ = pf.prediction(particles)
            
        # update step, p(z_{k}|x_{k}^{idx})
        likelihood_xk  = pf.update_apf(particles)
            
        # calculate second stage weights,
        # w = p(z_{k}|x_{k}^{idx}) / p(z_{k}|u-{k})
        for i in range(self.N):
            if w1[:,i] == 0:
                self.w[:,i] = self.N
            else:
                self.w[:,i] = likelihood_xk[:,i] / likelihood_uk[:,i]      
            
        # normalize weights
        self.w /= np.sum(self.w)    
                      
        # estimate step
        pf.estimate(particles, self.w)
       
        return particles