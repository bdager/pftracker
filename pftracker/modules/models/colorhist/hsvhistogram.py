# -*- coding: utf-8 -*-
"""
HSVHistogram creates 3D HSV histogram for an image.

@author: Bessie Domínguez-Dáger
"""

import cv2
import numpy as np

class HSVHistogram:
    """3D HSV histogram calculation.
    
    Args:
        bins (list): number of bins the histogram will use. The list
            contains 3 values corresponding to the number of bins for
            each component of the HSV color space. 
    """
    def __init__(self, bins):
        # store the number of bins the histogram will use
        self.bins = bins
        
        # define number of channels and h, s and v ranges
        self.channels = [0, 1, 2]
        h_range = [0, 180]
        s_range = [0, 256]
        v_range = [0, 256]
        self.ranges = h_range + s_range + v_range  # Concat list          

    def calc_Hist(self, image):
        """
        Returns a 3D histogram for an image in the HSV colorspace.
        
        Args:
            image (array): image from wich to create the HSV histogram
        """
        # convert image from bgr to hsv space
        hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # construct a mask for using all the hue (h) values in the region 
        # of interest and ignoring the weakly (s) or the dim (v) pronounced
        # areas of the bounding box
        mask = cv2.inRange(hsvImage, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        
        # calculate a 3D histogram in the HSV colorspace and normalize it
        # for getting roughly the same histogram for images with the same 
        # content but different scales.
        hsv_hist = cv2.calcHist([hsvImage], self.channels, mask, self.bins, self.ranges)        
        hsv_hist = cv2.normalize(hsv_hist, hsv_hist, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

		  # return 3D histogram as a flattened array
        return hsv_hist.flatten()
    