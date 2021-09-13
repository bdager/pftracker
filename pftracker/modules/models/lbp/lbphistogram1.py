"""
Local Binary Patterns (LBP) histogram on image.

Take it from pyimagesearch..........
"""

# import the necessary packages
import cv2
#from skimage import color 
from skimage.feature import local_binary_pattern
import numpy as np

class LBPHistogram:
    """
    LBP histogram calculation.
    
    Args:
        numPoints (int):number of sampling points
        radius (int): radius from  the center pixel
    """
    def __init__(self, numPoints, radius):
        # store the number of points and radius
        self.numPoints = numPoints
        self.radius = radius 

    def calc_Hist(self, image, eps=1e-7):
        """
        Returns the LBP histogram of an image.
        
        Args:
            image (array): image from wich to create the LBP histogram
            eps (float, optional): minimum for avoiding histogram non defined
               calculation (division by zero)
        """
        # convert the image to gray scale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#        gray_image = color.rgb2gray(image)
        
        # compute the LBP representation of the image         
        lbp = local_binary_pattern(gray_image, self.numPoints,
              self.radius, method="uniform")
        
        #v1
        # build the LBP histogram
#        (hist, _) = np.histogram(lbp.ravel(),
#                    bins=np.arange(0, self.numPoints + 3),
#                    range=(0, self.numPoints + 2))
        #v2
#        n_bins = int(lbp.max() + 1)
#        (hist, _) = np.histogram(lbp.ravel(), bins=n_bins,
#                    range=(0, n_bins))
        
          # normalize the histogram
#        hist = hist.astype("float")
#        hist /= (hist.sum() + eps)   
          
        #v3
#        lbp = local_binary_pattern(gray_image, 8, 8, method='uniform')
        img_ku = lbp.astype(np.uint8)
        hist = cv2.calcHist([img_ku],[0],None,[256],[0,256])
        hist = cv2.normalize(hist,hist).flatten()
#        hist = cv2.normalize(hist, hist, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        return hist