# -*- coding: utf-8 -*-
"""
Getting paper results

@author: Bessie Domínguez-Dáger
"""
import os
from pftracker.track import Track
import numpy as np

# set the seed of the random number generator 
np.random.seed(1267)

# get the input data file location
test_file_path = os.path.dirname(os.path.realpath(__file__))
input_path = test_file_path[:test_file_path.rfind('test')] + 'pftracker' + 'input'
Aaron_file = os.path.sep.join([input_path, 'Aaron_Guiel'])

# change the root to Aaron_Guiel5.avi and Aaron_Guiel5.labeled_faces.txt
# files if you have them in another location
input_video = os.path.sep.join([Aaron_file, "Aaron_Guiel5.avi"])
gt_file = os.path.sep.join([Aaron_file, "Aaron_Guiel5.labeled_faces.txt"])


def pf_run(pf_algorithm='G_PF', N = 100, resampling_alg ='systematic',
           face_detector = 'CaffeModel', res_percent = 50,
           estimate_alg = 'weighted_mean', RM_percent = 20, 
           ss ='6_variables', obs_model = 'HSV color-based',
           plot = False):
    
    # create a pftracker object
    pf = Track(video = input_video, n_particles = N, 
               algorithm = pf_algorithm, detector = face_detector,
               resample = resampling_alg, resamplePercent = res_percent, 
               estimate = estimate_alg, robustPercent = RM_percent,
               stateSpace = ss, obsmodel = obs_model)
    
    # perform face tracking based on PF
    pf.run(iterations=40, gt=gt_file)
    
    # plot precision and recall error metrics per frame and iteration
    if plot:
        pf.plotError() 


def get_results():
    ##---------------------------------------------------------------
    ## SIS 
    # Sequential Importance Sampling filter results
    
    # Parameters:
    # face detector: SSD,
    # number of particles: 100,
    # estimation algorithm: weighted mean,
    # state space dimension: 6 variables,
    # observation model: HSV color-based
    
    print("SIS results:\n"
          "Parameters:\n"
          "\tface detector: SSD,\n"
          "\tnumber of particles: 100,\n"
          "\testimation algorithm: weighted mean,\n"
          "\tstate space dimension: 6 variables,\n"
          "\tobservation model: HSV color-based)\n")
        
    pf_run(pf_algorithm = 'SIS')
    
    #-----------------------------------------------------------------
    ## SIR 
    # Sequential Importance Resampling filter results
    
    # Parameters
    # face detector: SSD,
    # number of particles: 100,
    # resampling algorithm: systematic,
    # estimation algorithm: weighted mean,
    # state space dimension: 6 variables,
    # observation model: HSV color-based
    
    print("\nSIR results:\n"
          "Parameters:\n"
          "\tface detector: SSD,\n"
          "\tnumber of particles: 100,\n"
          "\tresampling algorithm: systematic,\n"
          "\testimation algorithm: weighted mean,\n"
          "\tstate space dimension: 6 variables,\n"
          "\tobservation model: HSV color-based)\n")
        
    pf_run(pf_algorithm = 'SIR', plot = True)
    
    #-----------------------------------------------------------------
    ## GPF 
    # Generic Particle Filter results
    
    # Parameters
    # face detector: SSD,
    # number of particles: 100,
    # resampling algorithm: systematic,
    # resampling percent: 50,
    # estimation algorithm: weighted mean,
    # state space dimension: 6 variables,
    # observation model: HSV color-based
    
    print("\nGPF results:\n"
          "Parameters:\n"
          "\tface detector: SSD,\n"
          "\tnumber of particles: 100,\n"
          "\tresampling algorithm: systematic,\n"
          "\tresampling percent: 50,\n"
          "\testimation algorithm: weighted mean,\n"
          "\tstate space dimension: 6 variables,\n"
          "\tobservation model: HSV color-based)\n")
        
    pf_run(plot = True)
    
    #-----------------------------------------------------------------
    ## GPF with different parameters
    #-----------------------------------------------------------------
    # Resampling algorithm
    #-----------------------------------------------------------------
    # Stratified resampling    

    print("\nGPF with different parameters:\n"
          "\tresampling algorithm: stratified\n")
    
    pf_run(resampling_alg = 'stratified')
    
    #-----------------------------------------------------------------
    # Residual resampling

    print("\nGPF with different parameters:\n"
          "\tresampling algorithm: residual\n")
    
    pf_run(resampling_alg = 'residual')
    
    #-----------------------------------------------------------------
    # Multinomial resampling 
    
    print("\nGPF with different parameters:\n"
          "\tresampling algorithm: multinomial\n")
    
    pf_run(resampling_alg = 'multinomial')
    
    #-----------------------------------------------------------------
    # Resampling percent
    #-----------------------------------------------------------------
    # Resampling percent = 25 
    
    print("\nGPF with different parameters:\n"
          "\tresampling percent: 25 \n")
    
    pf_run(res_percent = 25)
    
    #-----------------------------------------------------------------
    # Resampling percent = 75 
    
    print("\nGPF with different parameters:\n"
          "\tresampling percent: 75 \n")
    
    pf_run(res_percent = 75)
    
    #-----------------------------------------------------------------
    # Estimation algorithm
    #-----------------------------------------------------------------
    # Maximum weight method   
    
    print("\nGPF with different parameters:\n"
          "\testimation algorithm: maximum weight\n")
    
    pf_run(estimate_alg = 'MAP')
    
    #-----------------------------------------------------------------
    # Robust mean method with 20 %
    
    print("\nGPF with different parameters:\n"
          "\testimation algorithm: Robust mean with 20 %\n")
    
    pf_run(estimate_alg = 'robust_mean')
    
    #-----------------------------------------------------------------
    # Robust mean method with 50 %
    
    print("\nGPF with different parameters:\n"
          "\testimation algorithm: Robust mean with 50 %\n")
    
    pf_run(estimate_alg = 'robust_mean', RM_percent = 50)
    
    #-----------------------------------------------------------------
    # Robust mean method with 70 %
    
    print("\nGPF with different parameters:\n"
          "\testimation algorithm: Robust mean with 70 %\n")
    
    pf_run(estimate_alg = 'robust_mean', RM_percent = 70)
    
    #-----------------------------------------------------------------
    # Number of particles
    #-----------------------------------------------------------------
    # Number of particles = 50  
    
    print("\nGPF with different parameters:\n"
          "\tnumber of particles: 50\n")
    
    pf_run(N = 50)
    
    #-----------------------------------------------------------------
    # Number of particles = 200      
    
    print("\nGPF with different parameters:\n"
          "\tnumber of particles: 200\n")
    
    pf_run(N = 200)
    
    #-----------------------------------------------------------------
    # Number of particles = 300  
    
    print("\nGPF with different parameters:\n"
          "\tnumber of particles: 300\n")
    
    pf_run(N = 300)
    
    #-----------------------------------------------------------------
    # Number of particles = 400  
    
    print("\nGPF with different parameters:\n"
          "\tnumber of particles: 400\n")
    
    pf_run(N = 400)
    
    #-----------------------------------------------------------------
    # Number of particles = 500  
    
    print("\nGPF with different parameters:\n"
          "\tnumber of particles: 500\n")
    
    pf_run(N = 500)
    
    #-----------------------------------------------------------------
    # Dynamic model
    #-----------------------------------------------------------------
    # Self updating bounding box model
    
    print("\nGPF with different parameters:\n"
          "\tstate space dimension: 4 variables with self updating bounding box\n")
    
    pf_run(ss = 'dynamic_bbox', plot = True)
    
    #-----------------------------------------------------------------
    # Five variables model
    
    print("\nGPF with different parameters:\n"
          "\tstate space dimension: 5 variables\n")
    
    pf_run(ss = '5_variables')
    
    #-----------------------------------------------------------------
    # LBP-based observation model
    #-----------------------------------------------------------------
    
    print("\nGPF with different parameters:\n"
          "\tobservation model: LBP-based\n")
    
    pf_run(obs_model = 'LBP-based')
    
    #-----------------------------------------------------------------
    # Face detector
    #-----------------------------------------------------------------
    # Viola and Jones (V&J) detector 
    
    print("\nGPF with different parameters:\n"
          "\tface detector: Viola and Jones (V&J)\n")
    
    pf_run(face_detector = 'HaarCascade')
    
    #-----------------------------------------------------------------
    # Histogram of Oriented Gradient (HOG) 
    
    print("\nGPF with different parameters:\n"
          "\tface detector: Histogram of Oriented Gradient (HOG)\n")
    
    pf_run(face_detector = 'dlib')
    
    #-----------------------------------------------------------------
    ## APF
    # Auxiliary Particle Filter results
    
    # Parameters
    # face detector: SSD,
    # number of particles: 100,
    # resampling algorithm: systematic,
    # estimation algorithm: weighted mean,
    # state space dimension: 6 variables,
    # observation model: HSV color-based
    
    print("\nAPF results:\n"
          "Parameters:\n"
          "\tface detector: SSD,\n"
          "\tnumber of particles: 100,\n"
          "\tresampling algorithm: systematic,\n"
          "\testimation algorithm: weighted mean,\n"
          "\tstate space dimension: 6 variables,\n"
          "\tobservation model: HSV color-based)\n")
    
    pf_run(pf_algorithm = 'APF', plot = True)    
    #-----------------------------------------------------------------

if __name__ == '__main__':
    get_results()
