# -*- coding: utf-8 -*-
"""
Running Particle Filter Toolbox.

@author: Bessie Domínguez-Dáger
"""
# import ui files
from pftracker.ui_sources.mainwindow_ui import *
from pftracker.ui_sources.dialog_results_ui import *
from pftracker.ui_sources.dialog_facedetector_ui import *
from pftracker.ui_sources.dialog_error_ui import *

#import PyQt5 packages required for the application
from PyQt5.QtWidgets import QMessageBox, QDialog, QLabel, QFileDialog, QAbstractButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon 
from PyQt5.QtCore import Qt

# import particle filter files
from pftracker.modules.interfacingUI import particle_tracker
from pftracker.modules.metrics import plotE, plotE_average 

# import some required packages
import os
import ctypes
import numpy as np
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT

# specify some paths
execution_path = os.getcwd()
icon_path = os.path.sep.join([execution_path, "pftracker", "ui_sources", 
                              "icons", "PFT.PNG"])
input_path = os.path.sep.join([execution_path, "pftracker", "input"])
output_path = os.path.sep.join([execution_path, "pftracker", "output", 
                                "pf_output.txt"])
output_error_path = os.path.sep.join([execution_path, "pftracker", "output", 
                                      "pf_error.txt"])
outputVideo_path = os.path.sep.join([execution_path, "pftracker", "output", 
                                     "pf_output.avi"])
icon_acept_path = os.path.sep.join([execution_path, "pftracker", "ui_sources", 
                                    "icons", "icons8-checkmark (1).svg"])
icon_run_path = os.path.sep.join([execution_path, "pftracker", "ui_sources", 
                                  "icons", "run_transp.png"])
icon_close_path = os.path.sep.join([execution_path, "pftracker", "ui_sources", 
                                    "icons", "cerrar_t.PNG"])


class Dialog_results(QDialog, Ui_Dialog_results):
    """Class definition for PF tracking results dialog.
    """
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.PB_acept.setIcon(QIcon(icon_acept_path))
        
class Dialog_facedetector(QDialog, Ui_Dialog_detector):
    """Class definition for face detectors dialog.
    """
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)  
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.PB_acept.setIcon(QIcon(icon_acept_path))        

class Dialog_plotError(QDialog, Ui_Dialog_error):
    """Class definition for tracking error dialog.
    """
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)  
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)
        self.close_event = False
    
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """Main class containing the main window of the graphical interface.
    
    This class cointains all the methods needed for running the graphical
    interface since the main window. Here particle filter parameters and
    models definitions are offered for testing face tracking in video 
    sequences.
    
    Supported options:
        - filter algorithms (SIS, SIS, GPF, APF),
        - number of particles,
        - resampling algorithms (multinomial, systemactic, stratified, residual),
        - resampling percent,
        - estimation algorithms (weighted mean, maximum weight, robust mean),
        - robust mean percent,
        - state space defintions,
        - observation models (HSV color-based, LBP-based)
        - input video (from webcam or disk)
        - save estimation
    
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)      # method for generating the interface
        self.setWindowIcon(QIcon(icon_path))
        self.PB_aceptar.setIcon(QIcon(icon_run_path))
        self.PB_cancelar.setIcon(QIcon(icon_close_path))
        self.pushButton_gtSearch.clicked.connect(self.openGtFile)
        self.PB_aceptar.clicked.connect(self.run)
        self.comboBox_filtro.currentIndexChanged.connect(self.enableResample_fromAlgorithm)
        self.comboBox_salida.currentIndexChanged.connect(self.RobustOutput)
        self.pushButton_signal.clicked.connect(self.OpenFileSignal)
        self.PB_cancelar.clicked.connect(self.close) 
        self.checkBox_save.clicked.connect(self.getEstPath)
        self.checkBox_save_error.clicked.connect(self.getErrorPath)
        
        self.dialog_results = Dialog_results()
        self.dialog_results.PB_error.clicked.connect(self.showError) 
        
        self.dialog_face = Dialog_facedetector()
        self.dialog_face.checkBox_save.clicked.connect(self.saveOutVideo)
        self.dialog_face.PB_acept.clicked.connect(self.facedetector)
        
        self.dialog_error = Dialog_plotError()
        
        self.outputName = None
        self.outputErrorPath = None
        self.outVideoName = None
        self.fileNameSignal = None
        self.nameSignal = "webcam"    
        self.detector = '' 
        self.gtFileName = ''
            
    def get_algorithm(self):
        """Get particle filter algorithm."""      
        self.algorithm = self.comboBox_filtro.currentText()
                 
    def get_n_particles(self):
        """Get number of particles."""
        self.n_particles = self.spinBox_NoParticulas.value()
       
    def get_estimate(self):
        """ Get estimation's algorithm for output."""
        self.estimate = self.comboBox_salida.currentText()
    
    def get_resample(self):
        """Get resample algorithm if the particle filter algorithm is not SIS."""
        if self.algorithm == "SIS":
            self.resample = None
        else:
            self.resample = self.comboBox_Tresample.currentText()  
      
    def get_resamplePercent(self):
        """Get resample percent if the particle filter algorithm is G_PF""" 
        if self.algorithm == "G_PF":            
            self.resamplePercent = self.spinBox_resample.value()  
        else:
            self.resamplePercent = None
            
    def get_robustPercent(self):
        """Get robust percent of particles for robust mean estimation algorithm."""
        if self.spinBox_salida.isEnabled():
            self.robustPercent = self.spinBox_salida.value()
        else:
            self.robustPercent = None
                
    def get_stateSpace(self):
        """Get particle filter algorithm."""
        self.stateSpace = self.comboBox_ee.currentText()
           
    def get_obsModel(self):
        """Get particle filter algorithm."""
        self.obsModel = self.comboBox_obsmodel.currentText()
        
    def run(self): 
        """Get the all selected filter and model parameters and then call
        the face detector dialog.
        """
        # Get filter parameters
        self.get_algorithm()
        self.get_estimate()
        self.get_resample()
        self.get_resamplePercent()
        self.get_robustPercent()
        self.get_n_particles()
        self.get_obsModel()
        self.get_stateSpace()

        if self.lineEdit_signal.text() == "" :  
            textError = ("Empty field: Input video.\nPlease select Record " 
                         "video from Webcam or load a video file from disk.")
            self.showMessage("Empty field", textError, QMessageBox.Critical,
                             QMessageBox.Ok, QMessageBox.Ok)
        else:
            # Run particle filter tracking
            if self.dialog_face.checkBox_save.isChecked():
                self.dialog_face.checkBox_save.setChecked(False)
            self.openFaceDialog()

    
    def openFaceDialog(self): 
        """Open face detector dialog."""
        if self.fileNameSignal == None:
            self.label_process.setText("Starting video stream...") 
        else:
            self.label_process.setText("Reading video file...") 
        self.dialog_face.exec_()
        if not self.label_process.text == '':
            self.label_process.setText('') 

        
    def facedetector(self):   
        """Get face detector algortihm and close face detector dialog."""                     
        if self.dialog_face.radioButton_viola.isChecked():
            self.detector = self.dialog_face.radioButton_viola.text()     
        elif self.dialog_face.radioButton_SSD.isChecked():
            self.detector = self.dialog_face.radioButton_SSD.text()            
        elif self.dialog_face.radioButton_HOG.isChecked():
            self.detector = self.dialog_face.radioButton_HOG.text()
   
        self.dialog_results.label_detector.setText(self.detector)       
        self.dialog_face.close()
        self.label_process.setText('')  
        self.run2DFfilter()
        
    def run2DFfilter(self): 
        """Run face tracking based on particle filter."""
        i = self.spinBox_runs.value()
        self.ii = self.spinBox_runs.value()
        t, fps = 0, 0
        self.P, self.R, self.P_mean, self.R_mean = 0,0,0,0
        P_std_perFrame, R_std_perFrame = 0.0, 0.0
        self.P_array = np.zeros((i,1))
        self.R_array = np.zeros((i,1))
        P_std_array = np.zeros((i,1))
        R_std_array = np.zeros((i,1))
        t_array = np.zeros((i,1))
        fps_array = np.zeros((i,1))
        self.idx = 0
        
        self.pf = particle_tracker(video= self.fileNameSignal, 
                                   algorithm = self.algorithm,
                                   n_particles = self.n_particles,
                                   estimate = self.estimate, 
                                   resample = self.resample, 
                                   resamplePercent = self.resamplePercent, 
                                   robustPercent = self.robustPercent, 
                                   detector = self.detector,                                   
                                   obsmodel = self.obsModel,
                                   stateSpace = self.stateSpace) 
        
        # if the input video is the reference to the webcam, call pf just       
        # once with that reference, if it´s not call pf depending on the
        # number of algorithm runs
        
        # Perform face tracking on webcam video
        if self.fileNameSignal == None:
            self.t_elapsed, self.fps = self.pf.face_tracking(self.outVideoName) 
            
            # Save pf estimates
            if self.outputName is not None:
                 self.pf.save_estimation(self.outputName)
                 
        # Perform face tracking on video file                
        else:                
            if self.outputName is not None:
                # Open .txt estimates file                  
                est_output = open(self.outputName,"w")
                
            if self.outputErrorPath is not None:
                # Open .txt error file                  
                error_output = open(self.outputErrorPath,"w")
                
            if self.outVideoName is not None and self.ii != 1:                
                self.outVideoName = self.outVideoName.split(".avi")[:-1][0]
            else:
                video_output = self.outVideoName
                
            while (i > 0):
                print ("Run: {}".format(self.idx+1))
                
                if self.outVideoName is not None and self.ii != 1:
                    video_output = self.outVideoName + "{}.avi".format(str(self.idx+1).zfill(4)) 
                    
                try:
                    t_elapsed_i, fps_i =  self.pf.face_tracking(video_output)                      
                    
                except AssertionError as faceDetect_error:    
                    print(faceDetect_error.args[0])
                    text_error = (self.detector + " could not detect any face, "
                                  "please try with another face detector algorithm.")
                    self.showMessage("Error message", text_error, QMessageBox.Critical,
                                         QMessageBox.Ok, QMessageBox.Ok)   
        
                else:  
                    # get the number of video frames at the first run
                    if self.idx == 0:
                        first_track = self.pf.get_pf_est()
                        
                    # if the video window is closed, break the loop. With this
                    # intention compare the number of frames at the first run
                    # with the current one
                    track = self.pf.get_pf_est()                    
                    if len(first_track) != len(track):
                        break
                                            
                    t += t_elapsed_i
                    fps += fps_i
                    t_array[self.idx] = t_elapsed_i
                    fps_array[self.idx] = fps_i
                                        
                    if self.gtFileName != '':
                        # Evaluate particle filter algorithm performance
                        P_i, R_i, P_mean_i, R_mean_i, P_std_i, R_std_i = self.pf.eval_pf(self.gtFileName)
                        
                        self.P += P_i
                        self.R += R_i
                            
                        self.P_array[self.idx] = P_mean_i
                        self.R_array[self.idx] = R_mean_i
                        P_std_array[self.idx] = P_std_i
                        R_std_array[self.idx] = R_std_i
                            
                        P_std_perFrame += P_std_i
                        R_std_perFrame += R_std_i
                        
                        print("[INFO] approx. precision: {:.2f} +- {:.2f}".format(P_mean_i, P_std_i))
                        print("[INFO] approx. recall: {:.2f} +- {:.2f}".format(R_mean_i, R_std_i))
                        
                        if self.outputErrorPath is not None:
                            # Write tracking error as P R          
                            for pt in zip(P_i, R_i):            
                                error_output.write("%.2f %.2f \n" % pt)         
                            error_output.write("\n")
                
                    if self.outputName is not None:
                        track = self.pf.get_pf_est()
                        # Write track points as x, y, w, w          
                        for pt in track:            
                            est_output.write("%.2f %.2f %.2f %.2f \n" % pt) 
                        est_output.write("\n")
                    
                    i -= 1
                    self.idx += 1
            
            if self.gtFileName != '' and self.outputErrorPath != None:
                error_output.write("Average precision, recall, elapsed time and "
                             "fps per iteration:\n")
                for pt in zip(self.P_array, P_std_array, self.R_array, R_std_array, t_array, fps_array):            
                    error_output.write("%.2f+-%.2f %.2f+-%.2f %.2f %.2f \n" % pt)     
            
            if self.outputErrorPath != None:
                # Close output file
                error_output.close()
#            
            if self.outputName is not None:
                # Close output file
                est_output.close()
            
            if self.ii == 1:
                self.t_elapsed, self.fps = t_elapsed_i, fps_i
                if self.gtFileName != '':
                    self.P_mean = P_mean_i
                    self.R_mean = R_mean_i
            else:            
                t /= self.idx
                fps /= self.idx
                
                self.t_elapsed, self.fps = t, fps
                
                print("\nTotal of full runs: {}".format(self.idx))
                print("Average time (sec): {:.2f}".format(t))
                print("Average fps: {:.2f}".format(fps))
                
                if self.gtFileName != '':
                    #precision and recall per iteration
                    self.P /= self.idx
                    self.R /= self.idx
                    
                    # precision and recall standard deviation
                    P_std = np.std(self.P_array, dtype=np.float64)
                    R_std = np.std(self.R_array, dtype=np.float64)
                    
                    # precision and recall standard deviation
                    P_std_perFrame /= self.idx
                    R_std_perFrame /= self.idx
                    
                    self.P_mean = sum(self.P)/len(self.P)
                    self.R_mean = sum(self.R)/len(self.R)       
                
                    print("Average precision +- std per frame/iteration: "
                          "{:.2f} +- {:.2f}/{:.3f}"
                          .format(self.P_mean, P_std_perFrame, P_std))
                    print("Average recall +- std per frame/iteration: "
                          "{:.2f} +- {:.2f}/{:.3f}"
                          .format(self.R_mean, R_std_perFrame, R_std))
                    
        self.t_elapsed = "{:.2f} seconds".format(self.t_elapsed)
        self.fps = "{:.2f}".format(self.fps)    
        
        # open results dialog
        self.openResultsDialog()
            
             
    def openResultsDialog(self):
        """Open results dialog."""
        self.dialog_results.label_TFiltro.setText(self.comboBox_filtro.currentText())        
        self.dialog_results.label_TSalida.setText(self.comboBox_salida.currentText())
        self.dialog_results.label_NoParticulas.setText(self.spinBox_NoParticulas.text())
        self.dialog_results.label_t.setText(self.t_elapsed)
        self.dialog_results.label_fps.setText(self.fps)
        self.dialog_results.label_Modelo.setText("2D Face Tracking")
        self.dialog_results.label_ee.setText(self.comboBox_ee.currentText())
        self.dialog_results.label_obsmodel.setText(self.comboBox_obsmodel.currentText())
        self.dialog_results.label_resultRuns.setText(str(self.idx))
        
        if self.dialog_results.label_resAlgorithm.isEnabled():
            self.dialog_results.label_resAlgorithm.setText(self.comboBox_Tresample.currentText())
        if self.dialog_results.label_resPercent.isEnabled():
            self.dialog_results.label_resPercent.setText(self.spinBox_resample.text())
        if self.dialog_results.label_robustMean.isEnabled():
            self.dialog_results.label_robustMean.setText(self.spinBox_salida.text())
        
        self.dialog_results.PB_acept.clicked.connect(self.dialog_results.close)
        self.dialog_results.exec_()


    def enableResample_fromAlgorithm(self):
        """
        Method to enable or disable resampling options in relation
        to the PF algorithm.
        """
        def enableResample(enable1, enable2):        
            self.label_Tresample.setEnabled(enable1)
            self.comboBox_Tresample.setEnabled(enable1)
            self.label_resample.setEnabled(enable2)
            self.spinBox_resample.setEnabled(enable2)
            self.dialog_results.label_resAlgorithm1.setEnabled(enable1)
            self.dialog_results.label_resAlgorithm.setEnabled(enable1)
            self.dialog_results.label_resPercent1.setEnabled(enable2)
            self.dialog_results.label_resPercent.setEnabled(enable2)
            
        self.get_algorithm()
        if self.algorithm == "SIS": 
            enableResample(False, False)            
        elif self.algorithm == "SIR":
            enableResample(True, False)  
        elif self.algorithm == "G_PF": 
            enableResample(True, True)
        elif self.algorithm == "APF":
            enableResample(True, False)
            
            
    def RobustOutput(self):
        """Method to enable or disable Robust Mean percent options."""
        def enableRobustOutput(enable):
            self.label_salida.setEnabled(enable)
            self.spinBox_salida.setEnabled(enable)
            self.dialog_results.label_robustMean1.setEnabled(enable)
            self.dialog_results.label_robustMean.setEnabled(enable)
            
        index = self.comboBox_salida.currentIndex()
        if index == 2:
            enableRobustOutput(True)
        else:
            enableRobustOutput(False)
            
            
    def OpenFileSignal(self):    
        """Open a window for selecting an input video file."""
        def openFile():
            fileNameSignal = QFileDialog.getOpenFileName(self, "Open file",
                             input_path, "Video (*.mp4 *.avi);;Text files (*.txt)")          
            if fileNameSignal[0] != '':
                self.fileNameSignal = fileNameSignal[0]                            
                self.nameSignal = self.fileNameSignal.split('/')[-1:][0]
        
        def enable_runs_gt(enable):
            self.label_gt.setEnabled(enable)
            self.lineEdit_gt.setEnabled(enable)
            self.pushButton_gtSearch.setEnabled(enable)
            self.label_runs.setEnabled(enable)
            self.spinBox_runs.setEnabled(enable)
        
        # 2D Face Tracking options for recording video or open video file 
        if self.nameSignal != "webcam":
            # Show webcam option for recording video
            result = self.showMessage("Record video...", "Record Webcam video?", 
                                 QMessageBox.Question, QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.Yes)
            if result == QMessageBox.Yes :
                self.nameSignal = "webcam"
                self.fileNameSignal = None
            else: 
                openFile()
        else:
            openFile()
            
        self.lineEdit_signal.setText(self.nameSignal)
        
        if self.fileNameSignal is not None:
            enable_runs_gt(True)
        else:
            enable_runs_gt(False)
           
    
    def openGtFile(self):
        """Open window for selecting ground truth file on disk."""
        gtFileName = QFileDialog.getOpenFileName(self, "Select annotations file",
                             input_path, "Text files (*.txt)")                  
        if gtFileName[0] != '':
            self.gtFileName = gtFileName[0]                            
            nameGt = self.gtFileName.split('/')[-1:][0]
            self.lineEdit_gt.setText(nameGt)
            self.checkBox_save_error.setEnabled(True)
            self.dialog_results.PB_error.setEnabled(True)
            
            
    def getEstPath(self):
        """Select a path to save estimates.
        
        Open a window for selecting the name of the file (.txt file wich will
        contain the particle estimation track per each frame of every 
        iteration) and where to store it on disk.
        """
        if self.checkBox_save.isChecked():
            fileName = QFileDialog.getSaveFileName(self, "Save file",
                           output_path, "Text files (*.txt)")
            self.outputName = fileName[0]
        else:
            self.outputName = None
            
            
    def getErrorPath(self):
        """Select a path to save error.
        
        Open a window for selecting the name of the file (.txt file wich will
        contain the algortihm erro per each frame and iteration) and where to 
        store it on disk.
        """
        if self.checkBox_save_error.isChecked():
            errorFileName = QFileDialog.getSaveFileName(self, "Save error file",
                           output_error_path, "Text files (*.txt)")
            self.outputErrorPath = errorFileName[0]
        else:
            self.outputErrorPath = None        
     
        
    def showError(self):
        """Plot precision and recall error metrics per frame."""
        def show(qmc):
            # instantiate a navigation toolbar from matplotlib package for  
            # the plot and widget
            ntb = NavigationToolbar2QT(qmc, self.dialog_error.widget)
            
            # package the plot and navigation toolbar within the vertical layout
            self.dialog_error.verticalLayout_chart.addWidget(qmc)
            self.dialog_error.verticalLayout_chart.addWidget(ntb)
    
            if not self.dialog_error.exec():
                self.dialog_error.verticalLayout_chart.removeWidget(qmc)
                self.dialog_error.verticalLayout_chart.removeWidget(ntb)
                
        # initialize the plot with the widget parent and precision 
        # and recall metrics 
        qmc1 = plotE(self.dialog_error.widget, self.P, self.R, self.P_mean, 
                    self.R_mean)        
        show(qmc1)
            
        if self.idx != 1:
            qmc2 = plotE_average(self.dialog_error.widget, self.P_array, 
                                     self.R_array, self.P_mean, self.R_mean)
            show(qmc2)            
            
    
    def saveOutVideo(self):
        """Save the resulting video.
        
        Open a window for selecting the name of the video resulting from
        the tracking based on PF algorithm and where to store it on disk.
        """
        if self.dialog_face.checkBox_save.isChecked():
            fileName = QFileDialog.getSaveFileName(self, "Save video file",
                           outputVideo_path, "Video (*.avi)")
            self.outVideoName = fileName[0]
        else:
            self.outVideoName = None
            
      
    def showMessage(self, wTitle, Text, Box, Buttons, dButtons):   
        mb = QMessageBox()
        mb.setWindowTitle(wTitle)
        mb.setWindowIcon(QIcon(icon_path))
        mb.setText(Text)
        mb.setIcon(Box)
        mb.setStandardButtons(Buttons)
        mb.setDefaultButton(dButtons)
        ret = mb.exec_()
        return ret
    
    
    def closeEvent(self, event):  
        """Show message for being sure to close the graphical interface. 
        """
        result = self.showMessage("Exit...", "Are you sure do you want to close the interface?", 
                    QMessageBox.Question, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if result == QMessageBox.Yes :
            event.accept()
        else: event.ignore()   
                
                 
if __name__ == "__main__": 
    app = QtWidgets.QApplication([])
    
    # it's necessary to use a Windows call from python to explicity tell to
    # Windows what is the correct AppUserModelIDfor this process and in this
    # way get the actual taskbar icon for the application and not the python icon 
    myappid = 'mycompany.myproduct.subproduct.version' # this is an arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    window = MainWindow()
    window.show()
    app.exec_()   
