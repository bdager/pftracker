# -*- coding: utf-8 -*-
"""
Module containing observation models.

@author: Bessie Domínguez-Dáger
"""

  
class ObsMod():
    """Observation Model base class.
    
    Args:
        bins (list): number of bins of the HSV histogram. The list
            contains 3 values corresponding to the number of bins for
            each component of the HSV color space (h, s and v) 
        N (int): number of particles 
        
    """
    
    def __init__(self, model, N):
        self.N = N          # N: number of particles            
        
        # Initialize the image descriptor -- a 3D HSV histogram
        self.model = model
                                                                                                    
    def calcHist_ref(self, first_frame, bounding_box):
        """Calculate reference histogram.
        
        first_frame (array): first frame of the video sequences
        bounding_box (array): face bounding box for the first frame
        """
        
        # set up the ROI where calculate the histogram
        x1,y1,x2,y2 = bounding_box
        roi = first_frame[y1:y2, x1:x2]
        
        # Initialize the especific observation model
        self.model = self.model(roi, self.N)       
       
    def calcDistance(self, image, particles, s):   
        """Calculate the likelihood of each particle.
        
        Args:
            image (array): frame at time k
            particles (array): particles at time k
            s (int): bounding box width
            
        Returns:
            (array) of likelihoods p(z_{k}|x_{k}) with (1,N) dimension
        """  
                                  
        likelihood = self.model.calcLikelihood(image, particles, s)
        return likelihood
    