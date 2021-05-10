# -*- coding: utf-8 -*-
"""
hsvModel class defines an HSV model for calculating the likelihoods of 
particles at actual time k.

@author: Bessie Domínguez-Dáger
"""
import numpy as np
from pftracker.modules.models.colorhist.hsvhistogram import HSVHistogram
import cv2

class hsvModel():
    """HSV color-based model.
    
    It defines an HSV model for calculating the likelihoods of particles 
    at actual time k.
    
    Args:
        hist_ref (array): reference HSV histogram
        hsvHistCalc (HSVHistogram): image descriptor (3D HSV histogram)
        N (int): number of particles
        l (int, optional): lambda Bhattacharyya distance coefficient       
    """
    
    def __init__(self, roi, N, l=20):        
        self.hsvHistCalc = HSVHistogram([8, 8, 4])
        self.hist_ref = self.hsvHistCalc.calc_Hist(roi)
        self.N = N          
        self.l = l
        self.distances = np.zeros((1, self.N))
        
    def calcLikelihood(self, image, particles, s):
        """Calculate the likelihood of each particle.
        
        This function calcultes the distance between the reference histogram 
        and the histograms obtained for the actual set of particles at time k.
        To do this it is used the Bhattacharyya distance metric.
        
        Args:
            image (array): frame at time k
            particles (array): particles at time k
            s (int): bounding box width
            
        Returns:
            (array) of likelihoods p(z_{k}|x_{k}) with (1,N) dimension
        """
  
        s=s//2
        
        # loop over the particles
        for iPart in range(self.N):
            # set the boundaries of bounding box of each particle on image
            minY = np.around(np.max((particles[1,iPart]-s, 1))).astype(int)
            maxY = np.around(np.min((particles[1,iPart]+s, image.shape[0]))).astype(int)
            minX = np.around(np.max((particles[0,iPart]-s, 1))).astype(int)
            maxX = np.around(np.min((particles[0,iPart]+s, image.shape[1]))).astype(int)
          
            HSVhist = self.hsvHistCalc.calc_Hist(image[minY:maxY, minX:maxX, :])
                
            # calculate histograms distance by Bhattacharyya distance
            dBhattacharyya = cv2.compareHist(self.hist_ref, HSVhist, method = cv2.HISTCMP_BHATTACHARYYA)
            self.distances[0, iPart] = dBhattacharyya
    
        # calculate the likelihood  
        likelihood = np.exp(-self.l*self.distances**2)
        
        return likelihood
        