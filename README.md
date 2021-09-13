# Particle Filter Toolbox

> Particle Filter for face tracking in video sequences.

This is a Python framework implemented for 
perfoming face tracking with particle filter algorithms. It cointains 
Sequential Importance Sampling filter, Sequential Importance Resampling 
filter, Generic Particle Filter and Auxiliary Particle Filter algorithms. 
Besides it suports differents options for model specifications and filtering.

For model specifications it provides three state space models and two 
observation models (HSV color- based and Local Binary Patterns (LBP) based). 
Among filtering options it presents diverse resampling and estimation methods.

It also provides three face detector algorithms to be used in the initialization 
step of particle filter algorithms. These detectors are Viola and Jones (VJ), 
Single Shot Detector (SSD) and Histogram of Oriented Gradient (HOG).

Videos for testing face tracking can be loaded from disk or recorded from 
webcam. Resulting videos can be store on disk too. Users can also select 
to save estimation track and plot precision and recall metrics if the 
ground truth of the tested video sequence are available. Besides,  
users can define the number of algorithm runs on the same video sequence.

The idea of this tool is to provide comfortable handling 
and analysis of the particle filter algorithms and their parameters, as 
well as the evaluation of the face tracking for different video inputs. 
In this way, it allows any user, regardless of the level of knowledge on 
the subject, to easily use these tools and quickly compare their results. 


## Installation

**Via PyPI**

The package is hosted on PyPI, so the most easy installation is using pip:

	pip install pftracker

> Note: The pftracker package is dependent on dlib for face dectection with HOG 
classifier. dlib package could be hard to install because it requires cmake and 
other C++ tools dependent on the operation system. The only version of dlib that 
has been previously compiled to a Built Distribution (.whl file), is for Python 
3.6 on Windows 10. So, it is strongly recommend to install a virtual environment with 
this characteristics if you want to avoid the hard dlib installation.

**Via Github**

You also can obtain the code by getting it from the GitHub repository:

https://github.com/bdager/pftracker

For this you can do:

    cd <directory you want to install to>
    git clone http://github.com/bdager/pftracker
    python setup.py install

**Note**

In the GitHub repository there is a file trackUI.py, this file runs the pftracker package 
as a graphical interface. 
Once you have the pftracker installed and the trackUI.py, you can run the graphical interface since
the command prompt, a python virtual environment or shell by:

    [python interpreter] trackUI.py


## Requirements

This graphical interface uses NumPy, OpenCV, PyQt5, imutils,  
dlib, scikit-image, Matplotlib, FilterPy and Python 3.

	
## Example
        
First construct the object and defined input video, filter parameters and 
target model if you want different options than the default ones.

    from pftracker.track import Track
    pf = Track(video="pftracker\input\Aaron_Guiel\Aaron_Guiel5.avi")
     
> *Note: To perform face tracking on webcam video just run: pf = Track()*
	 
Then run the algorithm with the previous definitions and specify 
the number of algorihm iterations and ground truth file is you want to
calculate precision and recall error metrics. Also specify errorFile,
saveTrackFile and saveVideo for saving error, estimates and resulting
video files.
                  
    pf.run(iterations=2, 
            gt="pftracker\input\Aaron_Guiel\Aaron_Guiel5.labeled_faces.txt")
 
Note that if you want to specify a file for saving error you should
provide the ground truth file too.
		
After that you are going to see the face tracking performing over the
selected input video.
        
If you want to plot the precision and recall metrics per frame (and per
iteration in case of you have more than one) and you provided the
ground truth file previously, then you can run:

    pf.plotError()    

See pftracker documentation for more details on http://pftracker.readthedocs.org


## Useful links

Source code:
https://github.com/bdager/pftracker

Documentation:
http://pftracker.readthedocs.org
