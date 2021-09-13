# -*- coding: utf-8 -*-
"""
Precision and Recall metrics calculation.

@author: Bessie Domínguez-Dáger
"""

import numpy as np

def calc_PrecRecall(det, gt):
    """
    Compute Precision, Recall and F1-score metrics for rectangular bounding boxes.
     
    Args:
        det (array): detection vector bounding box [startX startY endX endY]
        gt (array): ground truth vector bounding box [startX startY endX endY]
       
    Returns:
         3-element tuple containing
            
         - **precision** (*array*): precision value per frame, array with 
           (1, number_of_frames) dimension  
         - **recall** (*array*): recall value per frame, array with 
           (1, number_of_frames) dimension  
         - **F1Score** (*array*): F-1-score metric per frame, array with 
           (1, number_of_frames) dimension  
    """
    
    # initialize an array for saving gt and det intersected region 
    # of each particle
    inters = np.zeros(gt.shape)        
    
    # get the maximum value of starX and starY betwen det and gt
    inters[:,:2] = np.amax((det[:,:2], gt[:,:2]),0)
    
    # get the minimum value of endX and endY betwen det and gt
    inters[:,2:] = np.amin((det[:,2:], gt[:,2:]),0)

    # get width and height of intersected region
    inters[:,2:] = inters[:,2:] - inters[:,:2]
    
    # discard regions that are not intersected
    inters[inters < 0] = 0
    
    # calculate intersected region area
    TPArea =  inters[:,2] * inters[:,3]

    # do a copy of gt and det arrays and calculate weight and
    # height of both bounding boxes
    wh_gt= gt[:, 2:] - gt[:, 0:2]  
    wh_det = det[:, 2:] - det[:, :2] 

    # precision metric -----> TP/(TP+FP)
    # A(gt intersect det) / A(det) 
    detArea =  wh_det[:,0] * wh_det[:,1]
    precision = TPArea / detArea

    # recall metric ------> TP/(TP+FN)
    # A(gt intersect det) / A(gt)
    gtArea =  wh_gt[:,0] * wh_gt[:,1]
    recall = TPArea / gtArea
    
    # for comparing precision/recall values      
    eps = 1e-7
    F1Score = 2 * precision*recall / (precision+recall+eps)

    return precision, recall, F1Score