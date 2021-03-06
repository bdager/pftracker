"""
Particle Filter class for solving an estimation problem defined 
by a model class.

@author: Bessie Domínguez-Dáger
"""

import numpy as np
from numpy.random import random
from filterpy.monte_carlo import multinomial_resample, stratified_resample, systematic_resample
from pftracker.modules.filter.pfAlgorithms import pfiltering

class ParticleFilter():
    """
    Run a particle filter algorithm for an estimation problem.   

    This class creates particle filter estimates corresponding to a model class.
    This model class contains the calculation way of methods that vary with each 
    model where to apply particle filter estimations. This model methods are:
        - initialization: Create initial particles distribution.
        - prediction: Predict next state of the particles.
        - update: Evaluate predicted particles with an observation model.
        - update_apf: Evaluate predicted particles for second stage weights in
          auxiliary particle filter algorithm.  
        - visualize: Visualize the estimate resulting from particle filter 
          algorithm.
        - saveEstimation: Save particle filter estimates into a .txt file.
        - saveOutputModel: Save the visualization produced by visualize method 
          into a file.
        - get_error: Get the particle filter estimation error.
        - get_estimation: Get all the particle filter estimates.
            
    The ParticleFilter class interface model class with the PF algorithms and
    their methods:              
        - filtering: Runs particle filter algorithm.
        - estimate: Returns the expected particle filter estimation. 
        - resample: Runs resampling step.
           
    Args:
        model : Especific model where to apply the particle filter estimation                   
        algorithm (str): particle filter algorithm to apply
        N (int): Number of particles 
        output (str): Output estimate method 
        resample (str): Resampling method 
        resamplePercent (int): Resampling percent 
        robustPercent (int, optional): Particles percent to use in the robust 
            mean estimation algorithm.
    """
    
    def __init__(self, model, algorithm, N, output, resample, resamplePercent, robustPercent=None): 
        self.model = model
        self.N = N   
        
        # Filter parameters
        self.algorithm = algorithm
        self.arg_output = output    
        if resample != None:
            self.arg_resample = resample
        if resamplePercent != None:
            self.resamplePercent = round(resamplePercent * self.N/100)        
        if robustPercent != None: 
            self.N_robust = round(robustPercent * self.N/100)
        self.estimation = None       
        self.pfiltering = pfiltering(self.N)

    def initialization(self):
        """Create intial particles distribution.""" 
               
        particles = self.model.initialization()       
        return particles
    
    def prediction(self, particles):
        """Predict next state of the particles from time k-1 to k.
        
        Predicts the a priori pdf p(x_{k}|z_{k-1}) that describes
        particles distribution x_{k} using the dynamic model 
        p(x_{k}|x_{k-1}) (state transition model).
            - x_{k}: state vector of particles at time k.
            - x_{k-1}: state vector of  particles at time k-1.
            - z_{k-1}: observations at time k-1.
        
        This function is depedent on the model class.

        Args:
            particles (array): Model specific representation of
                particles x_{k-1}.

        Returns:
            2-element tuple containing
            
            - **particles** (*array*): particles array x_{k} with 
              (state_vector_size, N) dimension. 
            - **uk** (*array*): u_{k} array with (state_vector_size, N) dimension.
              This is a characterization of x_{k}|x_{k-1} (move particles 
              from x_{k-1} to x_{k} without include process noise).
        """
        
        particles, uk = self.model.prediction(particles)
        return particles, uk
    
    def update(self, particles): 
        """Evaluate predicted particles x_{k} with an observation model.
        
        This function is depedent on the model class.
        
        Returns:
            (array) of likelihoods of predicted particles x_{k},
            with (1, N) dimension. This is p(z_{k}|x_{k}).
        """
        
        likelihoods = self.model.update(particles)
        return likelihoods
    
    def update_apf(self, particles):   
        """Evaluate predicted particles x_{k}^{idx} with an observation model.
        
        Evaluate predicted particles x_{k}^{idx} for the second stage 
        weights of auxiliary particle filter algorithm with an 
        observation model. Here idx are the indixes resulting from 
        resampling of the first stage weigths of auxiliary particle 
        filter algorithm.
        
        This function is depedent on the model class.

        Args:
            particles (array): predicted particles array x_{k}^{idx} with 
                (state_vector_size, N) dimension

        Returns:
            (array) of likelihoods of particles x_{k}^{idx},
            with (1, N) dimension. This is p(z_{k}|x_{k}^{idx}).
        """
        
        likelihoods = self.model.update_apf(particles)
        return likelihoods
    
    def filtering(self, pf, particles):
        """Runs particle filter algorithm.
        
        Args:
            pf (ParticleFilter): ParticleFilter class object
            particles (array): particles at time k-1
        
        Returns:
            (array) of particles x_{k} with (state_vector_size,N) dimension 
        """
        
        if self.algorithm == "SIS":
            # Run Sequential Importance Sampling filter
            particles = self.pfiltering.SIS(pf, particles)
            
        elif self.algorithm == "SIR":
            # Run Sequential Importance Sampling filter
            particles = self.pfiltering.SIR(pf, particles)
            
        elif self.algorithm == "G_PF":
            # Run Generic particle filter
            particles = self.pfiltering.G_PF(pf, particles, self.resamplePercent)
            
        elif self.algorithm == "APF":
            # Run Auxilliary particle filter
            particles = self.pfiltering.APF(pf, particles)
            
        return particles
    
    def resample(self, weights):
        """Runs resampling step.
        
        Resampling methods supported: systematic, stratified,
        residual and multinomial.
        
        Args:
            weights (array): particle weigths after update process
            
        Returns:
            (array) of indixes resulting from resampling with (1,N) dimension 
        """        
        def residual_resample(weights):
            """ This was taken from filterpy package and some changes were made.
            
            Performs the residual resampling algorithm used by particle filters.
        
            For more documentation see https://filterpy.readthedocs.org
            """
            N = len(weights)
            indexes = np.zeros(N, 'i')    
        
            # take int(N*w) copies of each weight, which ensures particles with the
            # same weight are drawn uniformly
            num_copies = (np.floor(N*np.asarray(weights))).astype(int)
        #    num_copies = (N*np.asarray(weights)).astype(int)
        #    scaled_weights = N*np.asarray(weights)
            
            k = 0
            for i in range(N):
                # change done here in num_copies[i][0]
                for _ in range(np.array(num_copies[i][0])): # make n copies
                    indexes[k] = i
                    k += 1
        
            # use multinormal resample on the residual to fill up the rest. This
            # maximizes the variance of the samples
            residual = weights - num_copies     # get fractional part
        #    residual = scaled_weights - num_copies
            residual /= sum(residual)           # normalize
            cumulative_sum = np.cumsum(residual)
            cumulative_sum[-1] = 1. # avoid round-off errors: ensures sum is exactly one
            indexes[k:N] = np.searchsorted(cumulative_sum, random(N-k))
        
            return indexes
        
        if self.arg_resample == "systematic":
            indixes = systematic_resample(weights)
        elif self.arg_resample == "stratified":
            indixes = stratified_resample(weights)
        elif self.arg_resample == "residual":
            indixes = residual_resample(weights)
        elif self.arg_resample == "multinomial":
            indixes = multinomial_resample(weights)
        return indixes
           
    def estimate(self, particles, weights): 
        """Returns the expected particle filter estimation.
        
        Args:
            particles: predicted particles x_{k}
            weights: particle weigths after update process
        """
        
        if self.arg_output ==  "weighted_mean":
            # Calculate weighted mean estimate
            self.estimation = np.sum(particles * weights, axis=1)
                    
        elif self.arg_output == "MAP":  
            # Calculate maximum weight
            idx = np.argmax(weights, axis=1)
            self.estimation = particles[:, idx]
            self.estimation = self.estimation.reshape((6,))                 
                    
        elif self.arg_output ==  "robust_mean":  
            # Calculate robust mean estimate 
                                 
            # sort weights in descendent order
            weights_sort = -np.sort(-weights) 
            
            # get index of sorted weights
            idx_sort = np.argsort(-weights) 
            
            # normalize sorted weights
            weights_norm = weights_sort[0, :self.N_robust] / np.sum(weights_sort[0, :self.N_robust])
            
            # sort particles by weight
            particles_sort = particles[:, idx_sort[0, :self.N_robust]]
            
            self.estimation = np.sum(particles_sort * weights_norm, axis=1)
    
    def visualize(self, particles):
        """Visualize the estimate resulting from particle filter algorithm.
        
        This function is depedent on the model class.
        
        Args:
            particles (array): particles array x_{k} with (size_v, N) dimension            
        """
        
        self.model.visualizations(self.estimation, particles)
       
    def saveEstimation(self, file_name):
        """Save particle filter estimates into a .txt file.
        
        This function is depedent on the model class.
        """
        
        self.model.saveEstimation(file_name)
        
    def saveOutputModel(self):
        """Save the visualization produced by visualize method into a file.
        
        This function is depedent on the model class.
        """  
        
        self.model.saveOutputVideo()
        
    def get_error(self, gt_file):
        """Returns the particle filter estimation error.
        
        This function is depedent on the model class.
        
        Args:
            gt_file (str): path to ground truth .txt file  
        """     
        
        return self.model.calc_error(gt_file)
    
    def get_estimation(self):
        """Get all the particle filter estimates."""
        return self.model.getEstimation()
        