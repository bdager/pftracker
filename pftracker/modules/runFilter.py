"""
run_filter class runs a particle filter algorithm with a set of specified
methods and parameters needed for performing the tracking with the graphical
interface.

@author: Bessie Domínguez-Dáger
"""

from imutils.video import FPS 
from pftracker.modules.filter import particlefilter

class run_filter():    
    """
    Run an especific particle filter algorithm for the estimation problem in
    video sequences.
    
    Args:
        model: Object of class describing the especific model where apply the 
            particle filter estimation                   
        algorithm (str): PF algorithm 
        n_particles (int): Number of particles 
        estimateOutput (str): Output estimate method 
        resample (str): Resampling method 
        resamplePercent (int): Resampling percent 
        robustPercent (int): Resampling percent 
        output (str, optional): Path to optional output txt file
    """
        
    def __init__(self, model, algorithm, N, estimate, resample, resamplePercent, 
               robustPercent=None):  
        self.model = model
        self.algorithm = algorithm 
        self.N = N 
        self.estimate = estimate 
        self.resample = resample
        self.resamplePercent = resamplePercent
        self.robustPercent = robustPercent             
        
        ## Initializations
        self.pf = particlefilter(self.model, self.algorithm, self.N,
                                 self.estimate, self.resample, 
                                 self.resamplePercent, self.robustPercent)
        self.particles = self.pf.initialization()           
        
        self.video_closed = ''        
        
    def tracking(self):
        """
        Do the particle filter tracking.
        
        Returns:
            2-element tuple containing
            
            - (*float*): Approximate execution time of the algorithm
              in the face tracking task.
            - (*float*): Approximate number of fps.   
        """
        
        # Start the frames per second throughput estimator
        self.fps = FPS().start() 
        
        # Tracking         
        while True:            
            try:                                        
                self.particles = self.pf.filtering(self.pf, self.particles)        
                self.pf.visualize(self.particles)
            except NameError as error:
                self.video_closed = error
                # if we are viewing a video and we did not grab a frame,
                # then we have reached the end of the video
                break
            else:
                # Save output visualization
                self.pf.saveOutputModel()      
                                 
                # Update the FPS counter
                self.fps.update()       
                
        # Stop the timer 
        self.fps.stop()           
        return self.fps.elapsed(), self.fps.fps(), self.video_closed   

    def save_estimate(self, file_name):
        """
        Save the particle estimation for each frame into a .txt file.
        
        Args:
            file_name (str): path to output .txt file                 
        """
        
        self.pf.saveEstimation(file_name)
    
    def eval_alg(self, gt_file):
        """
        Returns the evaluation (error) of particle filter algorithm results. 
                
        Args:
            gt_file (str): path to ground truth .txt file  
        """
        
        return self.pf.get_error(gt_file)
     
    def get_pf_estimation(self):
        """Get particle filter estimation.""" 
        return self.pf.get_estimation()
    