"""
This module implements top-level of pftracker module. 

@author: Bessie Domínguez-Dáger
"""

import numpy as np
from pftracker.modules.metrics.plotErrorTrack import plotE, plotE_average
from pftracker.modules.interfacingUI import ParticleTracker

class Track():
    """
    Track class provides top-level of pftracker module for user
    handeling. Here are defined all the particle filter parameters
    and target model specifications for perfoming the task of face
    traking in video sequences.     
      
    Methods:
        run(iterations, gt, errorFile, saveTrackFile, saveVideo): Perform the 
            face tracking based on particle filter.
        plotError(): Plot precision and recall error metrics.
            
    Args:
       video(str, optional): Path to the input video file 
           (.mp4 or .avi format). Default is the reference
           to the webcam (None)
       algorithm(str, optional): Particle filter algorithm. Default
           is 'G_PF'        
       n_particles(int, optional): Number of particles. Default is 100
       detector(str, optional): Face detector algorithm. Default is
           'CaffeModel'
       estimate(str, optional): Estimate method. Default is 'weighted_mean'
       resample(str, optional): Resampling method. Default is 'systematic'
       resamplePercent(int, optional): Resampling percent. Default is 50
       robustPercent(int, optional): Resampling percent. Default is 20
       obsmodel(str, optional): Observation model. Default is 'HSV color-based'
       stateSpace(str, optional): State space model. Default is 'dynamic_bbox'
                  
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

    Raises:
        AssertionError: Exception raised if the path to the input video file 
            does not contain .mp4 or .avi extension.
            
    Example:
        
        First construct the object and defined input video, filter parameters and 
        target model if you want different options than the default ones.
    
        .. code::
    
            from pftracker.track import Track
            pf = Track(video="pftracker\input\Aaron_Guiel\Aaron_Guiel5.avi")
        
        Then run the algorithm with the previous definitions and specify 
        the number of algorihm iterations and ground truth file is you want to
        calculate precision and recall error metrics. Also specify errorFile,
        saveTrackFile and saveVideo for saving error, estimates and resulting
        video files.
        
        .. code::
            
            pf.run(iterations=2, 
                   gt="pftracker\input\Aaron_Guiel\Aaron_Guiel5.labeled_faces.txt")
        
        Note that if you want to specify a file for saving error you should
        provide the ground truth file too.
        
        After that you are going to see the face tracking performing over the
        selected input video.
        
        If you want to plot the precision and recall metrics per frame (and per
        iteration in case of you have more than one) and you provided the
        ground truth file previously, then you can run:
        
        .. code::
            
            pf.plotError()    
    """
    def __init__(self, video=None, 
                 algorithm="G_PF", n_particles=100, 
                 detector="CaffeModel", estimate="weighted_mean", 
                 resample="systematic", resamplePercent=50, 
                 robustPercent=20, obsmodel="HSV color-based", 
                 stateSpace="dynamic_bbox"):                 
        # handling input format error type
        if video != None:
            error_text = ("Path to the input video file should contain "
                          ".mp4 or .avi extension at the end.\n"
                          "\t\t\t\tExample: Track(video=\"pftracker\input"
                          "\Aaron_Guiel\Aaron_Guiel5.avi\")") 
            avi_file = "avi" == video.split(".")[-1] 
            mp4_file = "mp4" == video.split(".")[-1]  
            assert (avi_file or mp4_file), error_text
            
        # Input Video
        self.video = video
        
        # Filter parameters
        self.algorithm = algorithm 
        self.n_particles = n_particles         
        self.detector = detector
        self.estimate = estimate        
        self.resample = resample
        self.resamplePercent = resamplePercent        
        self.robustPercent = robustPercent   
        
        # Target model parameters
        self.obsmodel = obsmodel
        self.stateSpace = stateSpace

        
    def run(self, iterations=10, gt=None, errorFile=None, 
            saveTrackFile=None, saveVideo=None): 
        """
        Perform the face tracking based on particle filter.
        
        Args:
            iterations(int, optional): Number of algorithm iterations. 
                Default is 10. 
                If the input video is the reference to the webcam then
                the video is recorded just once and therefore the algorithm
                iterations are always equal to 1.
            gt(str, optional): Path to the ground truth file. Without this
                file is not posible to calculate precision and recall error
                metrics. Default is None
            errorFile(str, optional): Path to a .txt file for saving precision,
                recall and F1-score error metrics. Default is None (do not save
                error).
                
                **Example**
                
                .. code::
                    
                    pf.run(errorFile="pftracker\output\pf_error.txt")
                    
                In case of the number of iterations is greater than 1, the
                errors of each tracking iteration are saved in the same
                .txt file separated by a blank line. Besides, average precision, 
                recall, elapsed time and fps per iteration are going to be 
                saved at the end of the file.
                Note that if you want to save the error file you should
                provide the ground truth file too.
            saveTrackFile(str, optional): Path to the estimate .txt file.
                Default is None (do not save estimates).
                
                **Example**
                
                .. code::
                    
                    pf.run(saveTrackFile="pftracker\output\pf_estimates.txt")
                    
                In case of the number of iterations is greater than 1, all the
                estimates of each tracking iteration are saved in the same
                .txt file separated by a blank line.
            saveVideo(str, optional): Path to the output video file.                                
                Default is None (do not save video).
                Always the output file is a .avi format, so please specify 
                this format when write the path. 
                
                **Example**
                
                .. code::
                    
                    pf.run(saveVideo="pftracker\output\pf_output.avi")
                    
                In case of the number of iterations is greater than 1 and you
                want to save all the resulting videos from tracking, you just
                have to specify one name for a video file as explain before 
                and the number of the iteration is going to be added 
                automatically to that name.
                
                **Example**                
                
                If you run the command:
                            
                .. code::    
                            
                    pf.run(2, saveVideo="pftracker\output\pf_output.avi")
                        
                The resulting video file names are:
                    
                pf_output0001.avi
                
                pf_output0002.avi 
            
        Raises:
            AssertionError: Exception raised if the path to the ground truth  
                file does not contain the .txt extension.
            AssertionError: Exception raised if the path to the error   
                file does not contain the .txt extension.
            AssertionError: Exception raised if the path to the estimates  
                file does not contain the .txt extension.
            AssertionError: Exception raised if the path to the output video  
                file does not contain .avi extension.
        """
        i = iterations
        self.ii = iterations
        t, fps = 0, 0
        self.P, self.R, self.P_mean, self.R_mean = 0,0,0,0        
        P_std_perFrame, R_std_perFrame, F1Score_std_perFrame = 0.0, 0.0, 0.0
        self.P_array = np.zeros((i,1))
        self.R_array = np.zeros((i,1))
        P_std_array = np.zeros((i,1))
        R_std_array = np.zeros((i,1))
        F1Score_std_array = np.zeros((i,1))
        t_array = np.zeros((i,1))
        fps_array = np.zeros((i,1))
#        self.F1Score = 0.0
        self.F1Score_array = np.zeros((i,1))
        self.idx = 0
        self.plot = True
        
        pf = ParticleTracker(video = self.video, algorithm = self.algorithm,
                              n_particles = self.n_particles, detector = self.detector,
                              estimate = self.estimate, resample = self.resample, 
                              resamplePercent = self.resamplePercent, 
                              robustPercent = self.robustPercent, 
                              obsmodel = self.obsmodel, stateSpace = self.stateSpace)
        
        if gt != None:
            error_text = ("Path to the ground truth file should contain the "
                          ".txt extension at the end.\n"
                          "\tExample: pf.run(gt=\"pftracker\input\Aaron_Guiel"
                          "\Aaron_Guiel5.labeled_faces.txt\")")                              
            assert "txt" == gt.split(".")[-1], error_text
        
        if errorFile != None:
            error_text = ("Path to the error file should contain the "
                          ".txt extension at the end.\n"
                          "\tExample: pf.run(errorFile=\"pftracker\output"
                          "\pf_error.txt\")")                              
            assert "txt" == errorFile.split(".")[-1], error_text
            
        if saveTrackFile != None:
            error_text = ("Path to the estimates file should contain the "
                          ".txt extension at the end.\n"
                          "\tExample: pf.run(saveTrackFile=\"pftracker"
                          "\output\pf_estimates.txt\")")                              
            assert "txt" == saveTrackFile.split(".")[-1], error_text
         
        if saveVideo != None:
            error_text = ("Path to the output video file should contain "
                          "the .avi extension at the end.\n"
                          "\tExample: pf.run(saveVideo=\"pftracker"
                          "\output\pf_output.txt\")")                              
            assert "avi" == saveVideo.split(".")[-1], error_text
        
        # If the input video is the reference to the webcam, call pf just       
        # once with that reference, if it´s not call pf depending on the
        # number of algorithm runs
        
        # Perform face tracking on webcam video        
        if self.video == None: 
            pf.face_tracking(saveVideo)  

            # Save pf estimates
            if saveTrackFile != None:
                pf.save_estimation(saveTrackFile)
                
        # Perform face tracking on video file     
        else: 
            if errorFile != None:
                # Open .txt error file
                error_text = ("Path to the error file should contain the "
                              ".txt extension at the end.\n"
                              "\tExample: pf_tracker(saveVideo=\"pftracker"
                              "\output\pf_error.txt\")")                              
                assert "txt" == errorFile.split(".")[-1], error_text                    
                error_output = open(errorFile,"w")
                
            if saveTrackFile != None:
                est_output = open(saveTrackFile,"w")
            
            if saveVideo != None and self.ii != 1:
                saveVideo = saveVideo.split(".avi")[:-1][0]
            else:
                video_output = saveVideo
            
            while (i > 0):
                print ("Run: {}".format(self.idx+1))
                
                if saveVideo != None and self.ii != 1:
                    video_output = saveVideo + "{}.avi".format(str(self.idx+1).zfill(4))

                t_i, fps_i, video_closed = pf.face_tracking(video_output)   
            
                # if the video window is closed, break the loop
                if video_closed.args[0] == "video closed":             
                    break
                    
                t += t_i
                fps += fps_i
                t_array[self.idx] = t_i
                fps_array[self.idx] = fps_i
                                        
                if gt != None:
                    # Evaluate particle filter algorithm performance
                    P_i, R_i,P_mean_i,R_mean_i,P_std_i,R_std_i, F1Score_i, F1Score_std_i = pf.eval_pf(gt)
                    
                    # sum precision and recall of each frame per iteration
                    self.P += P_i
                    self.R += R_i             
                    
                    # save mean precision and recall per iteration in two arrays
                    self.P_array[self.idx] = P_mean_i
                    self.R_array[self.idx] = R_mean_i
                    
                    # save precision and recall standard deviation per 
                    # iteration in two arrays
                    P_std_array[self.idx] = P_std_i
                    R_std_array[self.idx] = R_std_i
                    
                    # save F1-score and its standard deviation per iteration 
                    # in two arrays
                    self.F1Score_array[self.idx] = F1Score_i
                    F1Score_std_array[self.idx] = F1Score_std_i                    
                    
                    # save mean precision, recall and F1-score per frame 
                    P_std_perFrame += P_std_i
                    R_std_perFrame += R_std_i
                    F1Score_std_perFrame += F1Score_std_i
                    
                    print("[INFO] approx. precision: {:.2f} +- {:.2f}"
                          .format(P_mean_i, P_std_i))
                    print("[INFO] approx. recall: {:.2f} +- {:.2f}"
                          .format(R_mean_i, R_std_i))
                    print("[INFO] approx. F1-score: {:.2f} +- {:.2f}"
                          .format(F1Score_i, F1Score_std_i))
                    
                    if errorFile != None:
                        # Write tracking error as P R          
                        for pt in zip(P_i, R_i):            
                            error_output.write("%.2f %.2f\n" % pt)         
                        error_output.write("\n")
                    
                if saveTrackFile != None:
                    track = pf.get_pf_est()
                    # Write track points as x, y, w, w          
                    for pt in track:            
                        est_output.write("%.2f %.2f %.2f %.2f\n" % pt) 
                    est_output.write("\n")
                
                i -= 1
                self.idx += 1
            
            if gt != None and errorFile != None:
                error_output.write("Average precision, recall, F1-score, "
                             "elapsed time and fps per iteration:\n")
                for pt in zip(self.P_array, P_std_array, self.R_array, 
                              R_std_array, self.F1Score_array, 
                              F1Score_std_array, t_array, fps_array):            
                    error_output.write("%.2f+-%.2f %.2f+-%.2f %.2f+-%.2f %.2f %.2f\n" % pt)                  
            
            if errorFile != None:
                # Close output file
                error_output.close()
            
            if saveTrackFile != None:
                # Close output file
                est_output.close()
            
            if self.ii == 1 or self.idx == 0:
                if gt != None and self.idx == 1:
                    self.P_mean = P_mean_i
                    self.R_mean = R_mean_i
                elif self.idx == 0: 
                    self.plot = False
            else:
                t /= self.idx
                fps /= self.idx
                
                print("\nTotal of full runs: {}".format(self.idx))
                print("Average time (sec): {:.2f}".format(t))
                print("Average fps: {:.2f}".format(fps))
                
                if gt != None:
                    # mean precision and recall per frame 
                    self.P /= self.idx
                    self.R /= self.idx                  
                    
                    # precision and recall standard deviation per frame
                    P_std_perFrame /= self.idx
                    R_std_perFrame /= self.idx
                    
                    F1Score_std_perFrame /= self.idx
                    
                    # precision and recall standard deviation per iteration
                    P_std = np.std(self.P_array, dtype=np.float64)
                    R_std = np.std(self.R_array, dtype=np.float64)
                    
                    # mean precision and recall of the total number of iterations
                    self.P_mean = sum(self.P)/len(self.P)
                    self.R_mean = sum(self.R)/len(self.R)   
    
                    F1Score_mean = sum(self.F1Score_array)/len(self.F1Score_array)
                    F1Score_std = np.std(self.F1Score_array, dtype=np.float64)
                                    
                    print("Average precision +- std per frame/iteration: "
                          "{:.2f} +- {:.2f}/{:.2f}"
                          .format(self.P_mean, P_std_perFrame, P_std))
                    print("Average recall +- std per frame/iteration: "
                          "{:.2f} +- {:.2f}/{:.2f}"
                          .format(self.R_mean, R_std_perFrame, R_std))
                    print("Average F1-score: +- std per frame/iteration: "
                          "{:.2f} +- {:.2f}/{:.2f}"
                          .format(F1Score_mean[0], F1Score_std_perFrame, F1Score_std))
                    

    def plotError(self):
        """Plot precision and recall error metrics.
        
        This method plots precision and recall per frame if a ground truth file
        was provided. If the number of algorithm runs if bigger than one, then
        precision and recall are plotted per particle filter algorithm run too.
        """
        if not self.plot:
            print("It´s not possible to plot the error because the pf "
                  "algorithm has to perform a full run at list once")
        else:
            try:
                # plot error
                plotE(self.P, self.R, self.P_mean, self.R_mean)
                if self.idx != 1:
                    plotE_average(self.P_array, self.R_array, self.P_mean, self.R_mean)
            except TypeError:
                print("There is no ground truth file provided for ploting "
                      "precision and recall error metrics.")
        