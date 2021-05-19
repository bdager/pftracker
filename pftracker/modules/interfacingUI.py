"""
particle_tracker class interfaces all the algorithms and parameters
in the particle filter framework.

@author: Bessie Domínguez-Dáger
"""

import cv2
from imutils.video import VideoStream
import time

from pftracker.modules.models import FaceTracking_2D
from pftracker.modules.models import createMovModel

from pftracker.modules.models import ObsMod
from pftracker.modules.models.colorhist.HSVModel import hsvModel
from pftracker.modules.models.lbp.LBPModel import lbpModel

from pftracker.modules.runFilter import run_filter
   

class particle_tracker(): 
    """Class interfaces particle filter to handle face tracking problem.
    
    This class interfaces particle filter algorithms to work in the 
    face tracking in video sequences task. Video sequences can be recorded
    from computer's webcam or .mp4 or .avi files loaded from disk. 
    
    Args:
       video(str, optional): Path to the input video file 
           (.mp4 or .avi format). Default is the reference
           to the webcam
       algorithm(str): Particle filter algorithm        
       n_particles(int): Number of particles
       detector(str): Face detector algorithm  
       estimate(str): Estimate method 
       resample(str): Resampling method 
       resamplePercent(int): Resampling percent 
       robustPercent(int): Resampling percent         
       obsmodel(str): Observation model
       stateSpace(str): State space model
       
    Supported PF algorithms:
        - 'SIS': Sequential Importance Sampling filter
        - 'SIR': Sequential Importance Resampling filter
        - 'G_PF': Generic particle filter
        - 'APF': Auxilliary particle filter
    
    Supported Face detectors:
        - 'HaarCascade': Viola and Jones (V&J) detector 
        - 'CaffeModel': Single Shot Detector (SSD) 
        - 'dlib': Histogram of Oriented Gradient (HOG) 
    
    Supported estimate methods:    
        - 'weighted_mean': Weighted mean method
        - 'MAP': Maximum weight method
        - 'robust_mean': Robust mean method  
    
    Supported resampling methods:
        - 'systematic': Systematic resampling
        - 'stratified': Stratified resampling
        - 'residual': Residual resampling
        - 'multinomial': Multinomial resampling
    
    Supported observation models: 
        - 'HSV color-based': Color model for weighing the particles  
        - 'LBP-based': Texture model for weighing the particles
                  
    Supported state space models:
        - 'dynamic_bbox': Self updating bounding box model
        - '5_variables': Five variables state space model
        - '6_variables': Six variables state space model       
    """
    
    def __init__(self, video, algorithm, n_particles, detector,
                 estimate, resample, resamplePercent, 
                 robustPercent, obsmodel, stateSpace):            
        self.video = video
        self.algorithm = algorithm 
        self.n_particles = n_particles 
        self.obsmodel = obsmodel
        self.detector = detector
        self.estimate = estimate 
        self.resample = resample
        self.resamplePercent = resamplePercent        
        self.robustPercent = robustPercent        
        self.stateSpace = stateSpace
            
        if self.resample == "Systematic":
            self.resample = "systematic"
        elif self.resample == "Stratified":
            self.resample = "stratified"
        elif self.resample == "Residual":
            self.resample = "residual"
        elif self.resample == "Multinomial":
            self.resample = "multinomial"        
        
        if self.estimate == "Weighted mean":
            self.estimate = "weighted_mean"
        elif self.estimate == "Maximum weight":
            self.estimate = "MAP"
        elif self.estimate == "Robust mean":
            self.estimate = "robust_mean"      
    
        if self.detector == "Viola and Jones (V&J)":
            self.detector = "HaarCascade"
        elif self.detector == "Single Shot Detector (SSD)":
            self.detector = "CaffeModel"
        elif self.detector == "Histogram of Oriented Gradient (HOG)":
            self.detector = "dlib"
        elif self.detector == "Non-Max Suppression":
            self.detector = "nms"  
            
        if self.stateSpace == "[x, y, Vx, Vy] (dynamic bbox)":
           self.stateSpace = "dynamic_bbox" 
        elif self.stateSpace == "[x, y, Vx, Vy, w]":
           self.stateSpace = "5_variables" 
        elif self.stateSpace == "[x, y, Vx, Vy, w, Vw]":
            self.stateSpace = "6_variables"
                        
    def face_tracking(self, saveVideo):
        """
        Run the especified particle filter algorithm for face tracking.
        
        Args:
            saveVideo(str): Path to the output video file. None means
                do not save video
        Returns:
            2-element tuple containing
            
            - **t_elapsed** (*float*): Approximate execution time of the 
              algorithm in the face tracking task.
            - **fps** (*float*): Approximate number of fps.   
            
        Raises:
            AssertionError: Exception raised if the reference to the 
                webcam failed.
            AssertionError: Exception raised if the reference to the 
                input video failed.
        """
        
        # If a video path was not supplied, grab the reference to the webcam    
        if not self.video:
            print("[INFO] starting video stream...")
            v = VideoStream(src=0).start()              
        
        # Otherwise, grab a reference to the video file
        else:
            v = cv2.VideoCapture(self.video)
        
        # Allow the camera or video file to warm up
        time.sleep(2.0)    
        
        # Read first frame
        frame = v.read()
        
        # If the first frame coudn´t be read raise an error to explain it
        # webcam reference
        webcam_error = not(frame is None and self.video is None)
        assert webcam_error, "The reference to the webcam has failed." 
        
        # If the first frame coudn´t be read raise an error to explain it
        # video file reference
        video_file_error = not(frame[1] is None and self.video is not None)
        error_text = ("Incorrect path to the input video file.\n"  +
                      "\t\t\t\tFile " + str(self.video) + " can't be open. "
                      "No such file or directory")
        assert video_file_error, error_text
          
        # Handle the frame from VideoCapture or VideoStream,
        # vide_stream bool variable indicate if we're working 
        # with VideoCapture or VideoStream
        frame, video_stream = (frame[1], False) if self.video else (frame, True)
               
        ## Initializations      
        # Particle motion model: discrete gaussian linear model; 
        # size_ve: state vector size
        movModel, size_ve = createMovModel(self.stateSpace)  
        
        # Observation model initialization ---------------------------                      
        if self.obsmodel == "HSV color-based": 
            # Observation model: HSV histogram
            obsModel = ObsMod(hsvModel, self.n_particles) 
            
        elif self.obsmodel == "LBP-based":
            # Observation model: LBP histogram
            obsModel = ObsMod(lbpModel, self.n_particles)
        #-------------------------------------------------------------
                    
        # 2D-Face model
        faceModel = FaceTracking_2D(movModel, obsModel, self.n_particles, size_ve, 
                                    frame, self.detector, v, video_stream, saveVideo)                                     
        # Initialize run_filter class
        self.run = run_filter(faceModel, self.algorithm, self.n_particles, 
                         self.estimate, self.resample, self.resamplePercent, 
                         self.robustPercent)                                                            
       
        # Run the particle filter algorithm
        t_elapsed, fps, video_closed = self.run.tracking()
        print("[INFO] elapsed time: {:.2f} sec".format(t_elapsed))
        print("[INFO] approx. FPS: {:.2f}".format(fps))
            
        # If we are not using a video file, stop the camera video stream
        if video_stream:
            v.stop()
            
        # Otherwise, release the camera
        else:
            v.release()
            
        # Close all windows
        cv2.destroyAllWindows()    
        
        return t_elapsed, fps, video_closed 
    
    def save_estimation(self, file_name):
        """
        Save the particle estimation for each frame into a .txt file
        
        Args:
            file_name(str): path to output .txt file                 
        """
        
        self.run.save_estimate(file_name)
        
    def eval_pf(self, gt):
        """
        Evaluate particle filter algorithm results. 
        
        This function calculate precision and recall metrics for 
        the resulting tracking.
        
        Args:
            gt(str): path to ground truth .txt file  
            
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
        
        return self.run.eval_alg(gt)
         
    def get_pf_est(self):
        return self.run.get_pf_estimation()