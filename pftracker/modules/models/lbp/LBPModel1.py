# -*- coding: utf-8 -*-
"""
lbpModel class defines a LBP model for calculating the likelihoods of 
particles at actual time k.

@author: Bessie Domínguez-Dáger
"""

import cv2
from pftracker.modules.models.lbp.lbphistogram1 import LBPHistogram
import numpy as np


class lbpModel():
    """LBP-based model.
    
    Args:
        hist_ref (array): reference LBP histogram
        lbpHistCalc (HSVHistogram): image descriptor (LBP histogram)
        N (int): number of particles
    """
    def __init__(self, roi, N):           
        self.lbpHistCalc = LBPHistogram(numPoints=8, radius=8) #24,8; 8,4;
        self.hist_ref = self.lbpHistCalc.calc_Hist(roi)
        self.N = N
        self.distances = np.zeros((1, self.N))
        
    def calcLikelihood(self, image, particles, s):    
        """Calculate the likelihood of each particle.
        
        This function calcultes the distance between the reference histogram 
        and the histograms obtained for the actual set of particles at time k.
        To do this it is used the Alternative CHI Square distance metric.
        
        Args:
            image (array): frame at time k
            particles (array): particles at time k
            
        Returns:
            (array) of likelihoods p(z_{k}|x_{k}) with (1,N) dimension
        """
          
        # Results are better with a fixed scale between 10 and 40,
        # a bigger number of pixels will take more execution time
        s=20 
#        s=25
        
        # loop over the particles
        for iPart in range(self.N):
            # set the boundaries of bounding box of each particle on image
            minY = np.around(np.max((particles[1,iPart]-s, 1))).astype(int)
            maxY = np.around(np.min((particles[1,iPart]+s, image.shape[0]))).astype(int)
            minX = np.around(np.max((particles[0,iPart]-s, 1))).astype(int)
            maxX = np.around(np.min((particles[0,iPart]+s, image.shape[1]))).astype(int)
  
            roi = image[minY:maxY, minX:maxX, :]
            LBPhist = self.lbpHistCalc.calc_Hist(roi)
            
            #v1
            # calculate Alternative CHI Square distance (use especifically for 
            # LBP histograms comparison)
#            chi_square = np.sum((self.hist_ref - LBPhist)**2 / (self.hist_ref + LBPhist))
#            chi_square = 2 * np.sum((self.hist_ref - LBPhist)**2 / (self.hist_ref + LBPhist))
#            chi_square = 0.5 * np.sum((self.hist_ref - LBPhist)**2 / (self.hist_ref + LBPhist + 1e-10))
#            self.distances[0, iPart] = chi_square
            
            #v2
#            divergence=self.kullback_leibler_divergence(LBPhist, self.hist_ref)
#            self.distances[0, iPart] = divergence
            
            #v3
            chi_square = cv2.compareHist(self.hist_ref, LBPhist, method = cv2.HISTCMP_CHISQR)
            self.distances[0, iPart] = chi_square
            
        # calculate the likelihood  
#        sigma = 0.06   # 0.01; 0.05; 0.06; 0.08
#        sigma = 0.06
#        sigma = 0.01
#        sigma = 0.008
#        likelihood = np.exp(-self.distances**2/(2*sigma**2))
#        likelihood = 1/np.sqrt(2*np.pi*sigma**2) * np.exp(-self.distances**2/(2*sigma**2))
        self.l=35
        likelihood = np.exp(-self.l*self.distances**2)
        
        return likelihood
    
    def kullback_leibler_divergence(self, p, q):
        p = np.asarray(p)
        q = np.asarray(q)
        filt = np.logical_and(p != 0, q != 0)
        return np.sum(p[filt] * np.log2(p[filt] / q[filt]))
        