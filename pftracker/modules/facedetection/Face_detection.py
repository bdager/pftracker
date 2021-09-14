"""
Compute one face detection.

@author: Bessie Domínguez-Dáger
"""

import os
import cv2
from imutils.face_utils import rect_to_bb
import numpy as np
import dlib
  

class detect_one_face():
    """One face detection class.
    
    Class used for detecting one face in the first frame of video where
    particle filter algorithm is going to be applied.
    
    Args:
        image (array): image where the face detection is perfomed
    
    Supported Face detectors:
        - 'HaarCascade': Viola and Jones (V&J) detector 
        - 'CaffeModel': Single Shot Detector (SSD) 
        - 'dlib': Histogram of Oriented Gradient (HOG)  
    """    
    def __init__(self, image):  
        # Load the input image
        self.image = image
        self.box = (0,0,0,0)
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
                 
    def detector(self, face_detector): 
        """Run a face detector algortihm on image.
        
        Args:
            face_detector (str): Face detector algorithm to apply
            
        Returns:
            (tuple) with bounding box coordinates resulting from face detection
            on image in the format (startX, startY, endX, endY).
                
        Raises:
            AssertionError: Exception raised if the face detector algorithm
                couldn't detect any face (box iqual to (0, 0, 0, 0).      
        """
        
        if face_detector == "HaarCascade": 
            # Run Viola and Jones (V&J) face detector                      
            self.haarCascade_detector()   
            
        elif face_detector == "CaffeModel":
            # Run Single Shot Detector (SSD) algorithm                        
            self.caffeModel_detector() 
            
        elif face_detector == "dlib":
            # Run Histogram of Oriented Gradient (HOG) face detector
            self.dlib_detector()
        
        # Raise an AssertionError if there's not any face detected
        assert self.box != (0,0,0,0), face_detector + " detector couldn't detect any face"
        return self.box
    
    
    def bb_faces(self, face):
        """
        Returns face bounding box coordinates in the format (startX, startY, endX, endY).
        
        Args:
            faces (tuple): face detection resulting from a detector algorithm 
                in the format (startX, startY, w, h). Where w and h are the 
                weight and height of the face bounding box respectevely.                
        """
        
        (startX, startY, w, h) = face
        endX = startX + w
        endY = startY + h
        self.box = (startX, startY, endX, endY)
            
    def get_cascade_faces_from_model(self, model, minN):
        """Returns a list of face detections from Viola and Jones (V&J) algorithm.
        
        Args:
            model (str): HaarCascade face detector model (frontal, left profile
                or right profile)
            minN (int): Minimum of neighbors needed for retaining each candidate 
                bounding box detected
        """
        # Load face detector model from disk            
        haarcascademodel = os.path.sep.join([self.dir_path, "models", model])
        face_cascade = cv2.CascadeClassifier(haarcascademodel)  
        
        # Obtain multiscale face detections                  
        faces = face_cascade.detectMultiScale(self.gray, scaleFactor=1.2, minNeighbors=minN)
        return faces 
        
    def haarCascade_detector(self): 
        """Run Viola and Jones (V&J) face detector on image.
        
        Returns:
            (tuple) with face bounding box coordinates resulting from detection.
        """
        
        # Convert the input image to grayscale
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Load HaarCascade frontal face detector model from disk
        print("[INFO] loading HaarCascade frontal face detector model...")
        frontal_model = 'haarcascade_frontalface_default.xml'
        
        # Obtain frontal face detections
        frontal_faces = self.get_cascade_faces_from_model(frontal_model, 3)
        
        # Ensure at least one frontal face was detected
        if len(frontal_faces) != 0:
            # Get the bounding box coordinates of the frontal face with the  
            # largest confidence in the format (startX, startY, endX, endY)
            self.bb_faces(frontal_faces[0])   
        else:
            # Load HaarCascade left profile face detector model from disk
            print("[INFO] loading HaarCascade left profile face detector model...")
            left_profile_model = 'haarcascade_profileface.xml'
            
            # Obtain left profile face detections
            left_profile_faces = self.get_cascade_faces_from_model(left_profile_model, 3)
                    
            # Ensure at least one left profile face was detected
            if len(left_profile_faces) != 0:
                # Get the bounding box coordinates of the left profile face with the  
                # largest confidence in the format (startX, startY, endX, endY)
                self.bb_faces(left_profile_faces[0])
            else:
                # Load HaarCascade right profile face detector model from disk
                print("[INFO] loading HaarCascade right profile face detector model...")
                right_profile_model = 'haarcascade_profileface_left2.xml'
                
                # Obtain right profile face detections
                right_profile_faces = self.get_cascade_faces_from_model(right_profile_model, 3)
                
                # Ensure at least one right profile face was detected
                if len(right_profile_faces) != 0:
                    # Get the bounding box coordinates of the right profile face with the  
                    # largest confidence in the format (startX, startY, endX, endY)
                    self.bb_faces(right_profile_faces[0])
                       
    def caffeModel_detector(self, confidence = 0.5):   
        """Run Single Shot Detector (SSD) algorithm for face detection on image.
        
        Args:
            confidence (float, optional): minimum algorithm confidence boundary
                for detection.
        
        Returns:
            (tuple) with face bounding box coordinates resulting from detection.
        """         
                   
        # Load face detector model from disk
        print("[INFO] loading CaffeModel face detector model...")
        protoPath = os.path.sep.join([self.dir_path, "models",
                                      "deploy.prototxt.txt"])  
        modelPath = os.path.sep.join([self.dir_path, "models",
                                "res10_300x300_ssd_iter_140000.caffemodel"])
        net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
        
        # Grab the image dimensions    
        (h, w) = self.image.shape[:2]
        
        # Create an input blob    
        blob = cv2.dnn.blobFromImage(cv2.resize(self.image, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))
     
        # Pass the input blob through the network and obtain face detections 
        net.setInput(blob)
        detections = net.forward()
        
        # Ensure at least one face was detected
        if len(detections) > 0:
            # Get the index of the detection with the largest confidence.
            # The tracking is going to be performaced over the face with the 
            # largest confidence (One Face Tracking).                         
            i = np.argmax(detections[0, 0, :, 2])
     
            # Grab the confidence associated with the largest confidence face 
            confidence_det = detections[0, 0, i, 2]
            
            # Discard weak detections (smaller than the minimum confidence)
            if confidence_det > confidence:                     
                # Compute face bounding box coordinates
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                self.box = (startX, startY, endX, endY)        
                         
    def dlib_detector(self):        
        """Run Histogram of Oriented Gradient (HOG) face detector on image.
        
        Returns:
            (tuple) with face bounding box coordinates resulting from detection.
        """
        
        # Initialize dlib's face detector (HOG-based detector) 
        print("[INFO] loading HOG face detector model...")
        detector = dlib.get_frontal_face_detector()
        
        # Convert the input image to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Obtain face detections
        rects = detector(gray, 2)

        # Ensure at least one face was detected
        if len(rects) != 0:            
            # Get the face detection with the largest confidence
            face = rect_to_bb(rects[0])  
            
            # Get face bounding box coordinates in the format 
            # (startX, startY, endX, endY)
            self.bb_faces(face)
                               
