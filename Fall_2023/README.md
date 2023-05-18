# MS-Longitudinal-Analysis
This repository is for the Longitudinal Analysis of MRI Scans of patients with Multiple Sclerosis, and is intended to be the Computer Science Capstone Seminar for Fall 2022 &amp; Spring 2023 at NYU Abu Dhabi.

In our experimentation and analysis, we make use of BIANCA (https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/BIANCA), and LOCATE (https://git.fmrib.ox.ac.uk/vaanathi/LOCATE-BIANCA/-/tree/master) and automate the training, testing and then expand it over Longitudinal Analysis.

As part of this project, there are two primary files:
-  /Longitudinal_Analysis_Multiple_Sclerosis_FinalVersion_Spring_2023.ipynb
-  /GUI/ms_gui.py

Both the files compliment each other. The Jupyter Notebook can be read through for details on how the Analysis is working, and for training of the models with detailed guidelines on preparing the data and automating the training. 

Then, these models are stored and copied, automatically by the Jupyter Notebook at /GUI/assets/model which is then utilized by the Graphical User Interface to allow for a User Friendly Utilization of the models, and to obtain masks for New, Old and All Multiple Sclerosis Lesions for any patient.

A Sample Prepared Dataset for the training can be found here: https://drive.google.com/drive/folders/19SavtEGMwiEvUtkAUeG8ie2xrSm18Hcv?usp=share_link. If you want to test this project yourself, you will have to install FSL, MATLAB, PyQT5, and other related packages/tools.

The advisors for the project were David Melcher, Djellel Difallah and Osama Abdullah.

If you have queries regarding the project, feel free to contact mzv205@nyu.edu!

