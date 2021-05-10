# -*- coding: utf-8 -*-
"""
Evaluate results of 2D face tracking based on particle filter algorithm. 

@author: Bessie Domínguez-Dáger
"""
import numpy as np
from pftracker.modules.metrics.PrecRecall import calc_PrecRecall

def error(det_tuple, gt_file):
    """2D face tracking evaluation.
    
    This function reads ground truth annotations of bounding box from .txt 
    files and then calculates precision and recall error metrics between 
    detections that have been obtained from particle filter estimation and 
    ground truth annotations.
    
    Ground truth annotations shoud be in the format: 
        - x,y,w,h
        
    where (x, y) are the center bounding box coordinates and (w, h) are the 
    bounding box width and height respectively.
    
    Besides, it is possible to read annotations from the 'YouTube Dataset'
    format:
        - name, [ignore], x, y, w, h, [ignore], [ignore]
    
    This dataset was used for testing the framework and is available at 
    www.cs.tau.ac.il/˜wolf/ytfaces
    
    Args:
        det_tuple(tuple): tuple with particle filter estimation results                     
        gt_file(str): .txt file directory of ground truth annotations 
    
    Returns:
         6-element tuple containing
            
         - **P** (*array*): precision value per frame, array with 
           (1, number_of_frames) dimension  
         - **R** (*array*): recall value per frame, array with 
           (1, number_of_frames) dimension  
         - **P_mean** (*float*): precision mean value
         - **R_mean** (*float*): recall mean value  
         - **P_std** (*float*): precision standard deviation value
         - **R_std** (*float*): recall standard deviation value
    """

    det = np.zeros((len(det_tuple), 4)).astype(int)
    det_temp = np.zeros((len(det_tuple), 4))
    for j in range(len(det_tuple)): 
        det_temp[j] = det_tuple[j]
        det[j, 0:2] = det_temp[j, 0:2] - det_temp[j, 2:]//2 
        det[j, 2:] = det_temp[j, 0:2] + det_temp[j, 2:]//2   
    
    gtFile = open(gt_file)
    gt_list = gtFile.readlines()
    gt = np.zeros((len(det_tuple), 4)).astype(int)
    gt_temp = np.zeros((len(det_tuple), 4)).astype(int)
    for i in range(len(det_tuple)):
        if len(gt_list[i].split(",")) > 4:
            gt_temp[i] = gt_list[i].split(",")[2:-2]
        elif len(gt_list[i].split(",")) == 4:
            gt_temp[i]= gt_list[i].split(",")
        gt[i, 0:2] = gt_temp[i, 0:2] - gt_temp[i, 2:]//2
        gt[i, 2:] = gt_temp[i, 0:2] + gt_temp[i, 2:]//2    
    gtFile.close()   
    
    # compute precision and recall metrics
    P, R = calc_PrecRecall(det, gt)
    
    P = P.astype(float)
    R = R.astype(float)
    
    # precision and recall average
    P_mean = np.sum(P)/len(P)
    R_mean = np.sum(R)/len(R)
    
    # precision and recall standard deviation
    P_std = np.std(P, dtype=np.float64)
    R_std = np.std(R, dtype=np.float64)

    return P, R, P_mean, R_mean, P_std, R_std
    
