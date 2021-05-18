# -*- coding: utf-8 -*-
"""
Model definition for 2D face tracking on video sequences.

@author: Bessie Domínguez-Dáger
"""

import os
import cv2
import numpy as np
from pftracker.modules.facedetection import detect_one_face
from pftracker.modules.metrics.eval_2DFace import error
from pftracker.modules.models.predictBB import self_updating_bbox


class FaceTracking_2D():
    """ Model for 2D face tracking based on particle filter. 
    
    This class describes a face tracking on video sequences model
    created for applying particle filter algorithms. Here are defined 
    the main characteristics and behavior of the target model.
    
    Args:
        movModel (createMovModel): Dynamic model 
        obsModel (ObsModels): Observation model
        N (int): Number of particles 
        size_v (int): State vector size
        detector (str): Face detector algorithm  
        v (VideoCapture or VideoStream): reference to the webcam 
            (VideoCapture object) or .mp4 or .avi video file
            (VideoStream object)
        video_stream (bool): This variable indicates if we're working 
            with VideoCapture or VideoStream
        saveVideo (str, optional): Path to the output video file.
            Default is None
    """ 
    
    def __init__(self, movModel, obsModel, N, size_v, first_frame, detector, v, video_stream, 
                 saveVideo=None):
        self.movModel = movModel
        self.obsModel = obsModel
        self.N = N
        self.size_v = size_v      # state vector size
        self.frame = first_frame  # just at the first moment for initialization
        self.detector = detector  # face detector
        self.video = v
        
        # vide_stream bool variable indicates if we're working 
        # with VideoCapture or VideoStream
        self.video_stream = video_stream        
        
        # variables related to particles and weights
        self.upthreshold = np.array([[self.frame.shape[1],self.frame.shape[0]]]).T-1
        self.estimate = np.zeros((self.size_v, 1))        
        
        # variables used for saving estimated output particle
        self.frameCounter = 0
        self.execution_path = os.getcwd()  # get the current working directory
        
        # variable for saving output video with the tracking implementation
        self.writer = None
        self.saveVideo = saveVideo
               
    def initialization(self):   
        """Create intial particles distribution.
        
        Sample particles from initial distribution, init particles in x and y 
        at bounding box center position resulting from face detector algorithm.  
        
        Returns:
            (array) with (size_v, N) dimension, particles at first time                
        """            
        
        # detect face in first frame
        startX,startY,endX,endY = detect_one_face(self.frame).detector(self.detector)   

        # Calculate reference histogram
        self.obsModel.calcHist_ref(self.frame, (startX, startY, endX, endY))  
            
        w = endX - startX     # bounding box width 
        h = endY - startY     # bounding box height 
        
        self.bbox = w
        
        # Initial position on the face bounding box center
        xy_init_pos = np.array([startX + w//2, startY + h//2])         
                        
        # Init particles to initial position          
        # -- particles: [x, y, Vx, Vy,...] = [0, 0, 0, 0,...]
        self.particles_0 = np.zeros((self.N, self.size_v))  

        # -- initial position x, y          
        particles_0_xy = np.ones((self.N, 2), int) * xy_init_pos    
        
        # -- particles = [x, y, 0, 0,...] 
        self.particles_0[:, :2] = particles_0_xy                   
        
        if self.size_v!=4:
            # w = bounding box width from face detection at first
            # -- particles = [x, y, 0, 0, w, 0]             
            self.particles_0[:, 4:5] = np.ones((self.N, 1), int) * w       
                                                                                                                                               
        self.track = ((self.particles_0.T[0,0], self.particles_0.T[1,0], 
                      self.bbox, self.bbox),)
                                                           
        return self.particles_0.T                                                           
    
    
    def prediction(self, particles):      
        """ 
        Propagate particles from time k-1 to k using a dynamic model.
        
        Args:
            particles (array): Model specific representation
                of all particles, with (size_v, N) dimension.
           
        Returns:
            2-element tuple containing
            
            - **particles** (*array*): predicted particles array x_{k} with 
              (size_v, N) dimension. 
            - **uk** (*array*): u_{k} array with (size_v, N) dimension. This is a 
              characterization of x_{k}|x_{k-1} (move particles from x_{k-1} 
              to x_{k} without include process noise).
        """
        
        particles, uk = self.movModel.move_particles(particles, self.N)
        
        # Clip out-of-bounds particles        
        particles[:2, :] = np.round(np.clip(particles[:2, :], np.zeros((2, self.N)), 
                                   self.upthreshold))
        particles[-1:, :] = np.round(particles[-1:, :])

        return particles, uk
    

    def update(self, particles):  
        """
        Evaluate predicted particles x_{k}.

        Args:
            particles (array): predicted particles array x_{k} with
                (size_v, N) dimension

        Returns:
            (array) of likelihoods p(z_{k}|x_{k}) with (1,N) dimension
         """
         
        # grab the current frame
        self.frame = self.video.read()
            
        # handle the frame from VideoCapture or VideoStream
        self.frame = self.frame[1] if not self.video_stream else self.frame
            
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if self.frame is None:
            self.close_e()        
        
        self.likelihood = self.obsModel.calcDistance(self.frame, particles, self.bbox)          
            
        return self.likelihood 
    
    def update_apf(self, particles):  
        """Evaluate predicted particles x_{k}^{idx}.
        
        Evaluate predicted particles x_{k}^{idx} for the second stage 
        weights of auxiliary particle filter algorithm. Here idx are
        the indixes resulting from resampling of the first stage 
        weigths of auxiliary particle filter algorithm.

        Args:
            particles (array): predicted particles array x_{k}^{idx} with 
                (size_v, N) dimension

        Returns:
            (array) of likelihoods p(z_{k}|x_{k}^{idx}) with (1,N) dimension
         """     
         
        self.likelihood = self.obsModel.calcDistance(self.frame, particles, self.bbox)          
            
        return self.likelihood
             
        
    def visualizations(self, estimate, particles):   
        """
        Visualization function for particles, resulting estimation and bounding box.
        
        This function visualize the set of particles, the resulting estimation
        and the bounding box in each iteration of the particle filter algorithm,
        showing all these in each frame of the analyzed video
        
        Args:
            estimate (array): estimated particle filter tracking result array
                with (size_v, 1) dimension
            particles (array): particles array x_{k} with (size_v, N) dimension
        """
                         
        # plot particles as points on image
        def draw_circle(image, center, radius, color):
            cv2.circle(image, (center[0], center[1]), radius, color, -1)
        
        # plot estimate as a cross on image
        def draw_cross(image, center, color, d):
            cv2.line(image, (center[0] - d, center[1] - d), 
                     (center[0] + d, center[1] + d), color, 1, cv2.LINE_AA, 0)
            cv2.line(image, (center[0] + d, center[1] - d), 
                     (center[0] - d, center[1] + d), color, 1, cv2.LINE_AA, 0) 
        
        # draw face bounding box on image
        def draw_rectangle(image, center, s, color):
            s=s//2     
            
            startY = np.max((center[1]-s, 1))
            endY = np.min((center[1]+s, image.shape[0]))
            startX = np.max((center[0]-s, 1))
            endX = np.min((center[0]+s, image.shape[1]))
            
            cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
        
        # call draw_circle, draw_cross and draw_rectangle functions on image
        def showing():
            for i in range (self.N):
                draw_circle(self.frame, particles.T[i].astype(int), 1, (0, 0, 255))  
            
            # draw the estimate output particle as a cross
            draw_cross(self.frame,(estimate[0].astype(int), estimate[1].astype(int)),
                                  (0, 255, 0), 3)
            
            # draw the face bounding box determine by the estimate output particle
            draw_rectangle(self.frame, (estimate[0].astype(int), estimate[1].astype(int)),
                          self.bbox, (0, 255, 0)) 
            
            cv2.imshow('2D Face Tracking', self.frame)

            if cv2.waitKey(30) & 0xFF == 27 or cv2.getWindowProperty('2D Face Tracking', cv2.WND_PROP_VISIBLE) < 1:
                self.close_e()
  
        self.frameCounter +=1  
        
        if self.size_v==4: 
            showing()
            center = [estimate[0], estimate[1]] 
            if self.frameCounter==1:
               self.d = 1 
               _, self.d = self_updating_bbox(center, self.bbox, self.d, particles, self.N)
            else:
                self.bbox, self.d = self_updating_bbox(center, self.bbox, self.d, particles, self.N)           
        else:
            self.bbox = estimate[4].astype(int)
            showing()
        
        self.track += ((estimate[0], estimate[1], self.bbox, self.bbox),)
                  
        # comment/uncomment for saving the 2, 50, 100 and 130 frames 
#        if self.frameCounter==2 or self.frameCounter==50 or self.frameCounter==100 or self.frameCounter==130:
#            p = os.path.sep.join([self.execution_path, "output", "{}.png".format(
#                    str(self.frameCounter).zfill(5))])
#            cv2.imwrite(p, self.frame)
   
    
    def getEstimation(self):
        """Get particle filter estimation."""
        return self.track

        
    def saveEstimation(self, file_name):
        """
        Save the particle estimation for each frame into a .txt file
        
        Args:
            file_name (str): path to output .txt file                 
        """
        
        # Open output file
#        output_name = os.path.join(self.execution_path, file_name)
        output = open(file_name,"w")
           
        # Write track points as x, y, w, w          
        for pt in self.track:            
            output.write("%.2f %.2f %.2f %.2f \n" % pt) 

        # Close output file
        output.close()              
                
              
    def saveOutputVideo(self):
        """Save output visualization into a .avi video file."""
        
        # if we are supposed to be writing a video to disk, initialize
        # the writer
        if self.saveVideo is not None and self.writer is None:           
            fourcc = cv2.VideoWriter_fourcc(*"MJPG") 
            # Uncomment the next line for running the PF_tracking.py code
#            path = os.path.sep.join([self.execution_path, self.saveVideo])
            path = self.saveVideo
            self.writer = cv2.VideoWriter(path, fourcc, 30,
                    (self.frame.shape[1], self.frame.shape[0]), True)
        
        # check to see if we should write the frame to disk
        if self.writer is not None:
            self.writer.write(self.frame) 

    def calc_error(self, gt_file):
        """
        Evaluate particle filter algorithm results. 
        
        This function calculate precision and recall metrics for 
        the resulting face tracking.
        
        Args:
            gt (str): path to ground truth .txt file  
            
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
        
        det_tuple = self.track
        P, R, P_mean, R_mean, P_std, R_std = error(det_tuple, gt_file)
        return P, R, P_mean, R_mean, P_std, R_std
                       
            
    def close_e(self): 
        """Close video file if it has reached to the end or if the window 
        of the video has been closed.

        """
        # check if it's necessary to release the video writer pointer
        if self.writer is not None:
            self.writer.release()
            
        raise NameError("video closed")
