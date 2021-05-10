About the toolbox
=================

Introduction
************

This is a graphical interface based on a Python framework implemented for perfoming face tracking with particle filter algorithms. It cointains Sequential Importance Sampling filter, Sequential Importance Resampling filter, Generic Particle Filter and Auxiliary Particle Filter algorithms. Besides it suports differents options for model specifications and filtering.

For model specifications it provides three state space models and two observation models (HSV color- based and Local Binary Patterns (LBP) based). Among filtering options it presents diverse resampling and estimation methods.

It also provide three face detector algorithms to be used in the initialization step of particle filter algorithms. These detectors are Viola and Jones (V&J), Single Shot Detector (SSD) and Histogram of Oriented Gradient (HOG).

Videos for testing face tracking can be loaded from disk or recorded from webcam. Resulting videos can be store on disk too. Users can also select to save estimation track and plot precision and recall metrics if the ground truth of the tested video sequence are available.

The idea of this graphical interface is to provide comfortable handling and analysis of the particle filter algorithms and their parameters, as well as the evaluation of the face tracking for different video inputs. In this way, it allows any user, regardless of the level of knowledge on the subject, to easily use these tools and quickly compare their results. 


Usage
*****

You can get the code by getting it from the GitHub repository:

https://github.com/bdager/pftraker-master/pftracker

Once you have it, for running the graphical interface, since the command prompt or a python 
virtual enviroment or shell run:

::

    [python interpreter] particleUI.py
	

Main window of the graphical interface:

.. image:: _static/Captura2.png




