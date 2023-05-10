# ----------------------------------------------------------------------------------------
# Produced by Zunair Viqar (mzv205@nyu.edu) in May, 2023
# This GUI is generated as part of the Computer Science Capstone Seminar - Spring 2023, at New York University Abu Dhabi
# The Advisors for this were David Melcher, Djellel Difallah, and Osama Abdullah (all from NYU Abu Dhabi)
# For this code to run, make sure to utilize the accompanying Jupyter Notebook for reproduction of the Models utilized
# Primarily, it requires to have FSLEyes installed as a pre-requisite!
# ----------------------------------------------------------------------------------------

# Import the Necessary Libraries
import sys
import os
import shutil
from pathlib import Path
from PyQt5.QtCore import pyqtSlot, Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QTextCursor, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, \
    QHBoxLayout, QGridLayout, QFileDialog, QTextEdit, QLabel, QPlainTextEdit, QFrame, QLineEdit, \
    QGraphicsDropShadowEffect, QComboBox, QSizePolicy


# ----------------------------------------
# PRODUCING THE BASIC STRUCTURE OF THE GUI
class Base(QMainWindow):
    def __init__(self):
        super().__init__()

        style = """
        background-color: #F4F4F2;
        margin-left:10px;
        margin-right:10px;
        """
        self.title = 'MS Longitudinal Analysis'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 750
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create a QLabel for the title
        title = QLabel('Longitudinal Analysis - Multiple Sclerosis')
        font = QFont("Helvetica", 13)
        title.setFont(font)
        title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # Align to the top-center
        title.setStyleSheet(" color:#115270;")
        title.setFixedHeight(15)  # Set a fixed height for the title QLabel

        # Create a QFrame for the horizontal line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("border-color:#115270;");
        line.setFixedHeight(3)  # Set a fixed height for the line to make it visible
        line.setFixedWidth(280)  # Set a fixed width for the line to make it longer

        # Add the title to the QMainWindow
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(QVBoxLayout())
        self.centralWidget().layout().addWidget(title)
        self.centralWidget().layout().addWidget(line, alignment=Qt.AlignHCenter)  # Align the line to the center
        self.centralWidget().layout().addStretch(1)  # Add another stretch to push the table to the bottom
        self.setStyleSheet(style)
        self.setFixedSize(self.width, self.height)
        self.table_widget = ContentArea(self)
        self.centralWidget().layout().addWidget(self.table_widget)
        self.show()


# ------------------------------------------------
# DECLARING FUNCTIONS TO RUN LONGITUDINAL ANALYSIS
def create_directory(folder_path, directory_name):
    path = os.path.join(folder_path, directory_name)
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)


# A function that simply runs all of the FSL or Terminal Commands
def run_command(terminal_command):
    p = os.popen(terminal_command)
    if p:
        return p.read()
    else:
        return "Command Invalid"


# Function to generate new directories, as well as store the paths for the directories to be utilized
def managedirectories(flairTp1, flairTp2):
    current_directory = os.getcwd()
    model_directory = current_directory + '/assets/model'
    locate_training_directory = current_directory + '/assets/model'
    create_directory(locate_training_directory, "Longitudinal_Processing")
    create_directory(locate_training_directory, "Longitudinal_Tests")
    processing_directory = locate_training_directory + "/Longitudinal_Processing"
    testing_directory = locate_training_directory + "/Longitudinal_Tests"
    path = Path(flairTp1)
    timepoint1_directory = path.parent.absolute()
    path = Path(flairTp2)
    timepoint2_directory = path.parent.absolute()
    t1_2_mni = current_directory + '/assets/reference_data/T1_2_MNI152_2mm.cnf'
    mni_directory = current_directory + '/assets/reference_data/MNI152_2mm_brain.nii.gz'
    return model_directory, locate_training_directory, processing_directory, testing_directory, timepoint1_directory, timepoint2_directory, t1_2_mni, mni_directory


# Function to run the brain extraction on the User Input Nifti Images
def run_bet(timepoint1_directory, timepoint2_directory, processing_directory, flairTp1, flairTp2):
    run_command(f"cd {timepoint1_directory} && bet {flairTp1} {processing_directory}/tp1_brain.nii.gz")
    run_command(f"cd {timepoint2_directory} && bet {flairTp2} {processing_directory}/tp2_feature_FLAIR.nii.gz")


# For resampling the Timepoint 1 Image onto the Timepoint 2 Image
def resample_images(processing_directory):
    run_command(
        f"cd {processing_directory} && flirt -in tp1_brain.nii.gz -ref tp2_feature_FLAIR.nii.gz -out tp1_feature_FLAIR.nii.gz -omat tp1_feature_FLAIR.mat -interp nearestneighbour -dof 6")


# Run FSL Fast to get the CSF pve file
def run_fsl_fast(locate_training_directory):
    output = run_command(
        f"cd {locate_training_directory} && /usr/local/fsl/bin/fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o {locate_training_directory}/Longitudinal_Processing/ {locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && cp {locate_training_directory}/Longitudinal_Processing/_pve_0.nii.gz {locate_training_directory}/Longitudinal_Processing/tp1_csf_pve.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && /usr/local/fsl/bin/fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o {locate_training_directory}/Longitudinal_Processing/ {locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && cp {locate_training_directory}/Longitudinal_Processing/_pve_0.nii.gz {locate_training_directory}/Longitudinal_Processing/tp2_csf_pve.nii.gz")


# For TimePoint 1
# Obtain the warp_file_MNI2structural
def obtain_files_tp1(locate_training_directory, mni_directory, t1_2_mni):
    output = run_command(
        f"cd {locate_training_directory} && flirt -ref {mni_directory} -in {locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR.nii.gz -omat {locate_training_directory}/Longitudinal_Processing/my_affine_transf.mat")
    output = run_command(
        f"cd {locate_training_directory} && fnirt --in={locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR.nii.gz --aff={locate_training_directory}/Longitudinal_Processing/my_affine_transf.mat --cout={locate_training_directory}/Longitudinal_Processing/my_nonlinear_transf --config={t1_2_mni} --lambda=400,200,150,75,60,45")
    output = run_command(
        f"cd {locate_training_directory} && invwarp -w {locate_training_directory}/Longitudinal_Processing/my_nonlinear_transf -o {locate_training_directory}/Longitudinal_Processing/invwarpvol_new -r {locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && cp {locate_training_directory}/Longitudinal_Processing/invwarpvol_new.nii.gz {locate_training_directory}/Longitudinal_Processing/tp1_warp_file_MNI2structural.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && cp {locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR.nii.gz {locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR_brain.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && make_bianca_mask {locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR.nii.gz {locate_training_directory}/Longitudinal_Processing/tp1_csf_pve.nii.gz {locate_training_directory}/Longitudinal_Processing/tp1_warp_file_MNI2structural.nii.gz 0")
    output = run_command(
        f"cd {locate_training_directory} && distancemap -i {locate_training_directory}/Longitudinal_Processing/tp1_feature_flair_ventmask.nii.gz -m {locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR_brain_mask.nii.gz -o {locate_training_directory}/Longitudinal_Processing/tp1_ventdistmap.nii.gz")


# Generate the Masterfile for BIANCA and runs the BIANCA Algorithm
def generate_bianca_masterfile_tp1(locate_training_directory, model_directory):
    masterfile = f"{locate_training_directory}/Longitudinal_Processing/tp1_masterfile.txt"
    file = open(masterfile, 'w')
    file.write(f"{locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR.nii.gz")
    file.close()
    masterfile = masterfile.replace(" ", "\ ")
    run_command(
        f"cd {model_directory} && bianca --singlefile={masterfile} --loadclassifierdata={model_directory}/mytraining --querysubjectnum=1 --brainmaskfeaturenum=1 -o {locate_training_directory}/Longitudinal_Processing/tp1_BIANCA_LPM.nii.gz -v")


# Moving all the generated files to the 'LongitudinalTests' Folder
def move_files_tp1(locate_training_directory, testing_directory):
    # Storing them appropriately
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR.nii.gz {testing_directory}/tp1_feature_FLAIR.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR_bianca_mask.nii.gz {testing_directory}/tp1_biancamask.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Processing/tp1_feature_FLAIR_brain_mask.nii.gz {testing_directory}/tp1_brainmask.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Processing/tp1_ventdistmap.nii.gz {testing_directory}/tp1_ventdistmap.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Processing/tp1_BIANCA_LPM.nii.gz {testing_directory}/tp1_BIANCA_LPM.nii.gz")


# For TimePoint 2
def obtain_files_tp2(locate_training_directory, mni_directory, t1_2_mni):
    output = run_command(
        f"cd {locate_training_directory} && flirt -ref {mni_directory} -in {locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR.nii.gz -omat {locate_training_directory}/Longitudinal_Processing/my_affine_transf.mat")
    output = run_command(
        f"cd {locate_training_directory} && fnirt --in={locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR.nii.gz --aff={locate_training_directory}/Longitudinal_Processing/my_affine_transf.mat --cout={locate_training_directory}/Longitudinal_Processing/my_nonlinear_transf --config={t1_2_mni} --lambda=400,200,150,75,60,45")
    output = run_command(
        f"cd {locate_training_directory} && invwarp -w {locate_training_directory}/Longitudinal_Processing/my_nonlinear_transf -o {locate_training_directory}/Longitudinal_Processing/invwarpvol_new -r {locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && cp {locate_training_directory}/Longitudinal_Processing/invwarpvol_new.nii.gz {locate_training_directory}/Longitudinal_Processing/tp2_warp_file_MNI2structural.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && cp {locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR.nii.gz {locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR_brain.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && make_bianca_mask {locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR.nii.gz {locate_training_directory}/Longitudinal_Processing/tp2_csf_pve.nii.gz {locate_training_directory}/Longitudinal_Processing/tp2_warp_file_MNI2structural.nii.gz 0")
    output = run_command(
        f"cd {locate_training_directory} && distancemap -i {locate_training_directory}/Longitudinal_Processing/tp2_feature_flair_ventmask.nii.gz -m {locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR_brain_mask.nii.gz -o {locate_training_directory}/Longitudinal_Processing/tp2_ventdistmap.nii.gz")


def generate_bianca_masterfile_tp2(locate_training_directory, model_directory):
    masterfile = f"{locate_training_directory}/Longitudinal_Processing/tp2_masterfile.txt"
    file = open(masterfile, 'w')
    file.write(f"{locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR.nii.gz")
    file.close()
    masterfile = masterfile.replace(" ", "\ ")
    run_command(
        f"cd {model_directory} && bianca --singlefile={masterfile} --loadclassifierdata={model_directory}/mytraining --querysubjectnum=1 --brainmaskfeaturenum=1 -o {locate_training_directory}/Longitudinal_Processing/tp2_BIANCA_LPM.nii.gz -v")


def move_files_tp2(locate_training_directory, testing_directory):
    # Storing them appropriately
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR.nii.gz {testing_directory}/tp2_feature_FLAIR.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR_bianca_mask.nii.gz {testing_directory}/tp2_biancamask.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Processing/tp2_feature_FLAIR_brain_mask.nii.gz {testing_directory}/tp2_brainmask.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Processing/tp2_ventdistmap.nii.gz {testing_directory}/tp2_ventdistmap.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Processing/tp2_BIANCA_LPM.nii.gz {testing_directory}/tp2_BIANCA_LPM.nii.gz")


# Runs the LOCATE Function using the LongitudinalTests and Testing_imgs_directory
def run_locate(locate_training_directory):
    output = run_command(
        f"/Applications/MATLAB_R2022b.app/bin/matlab -nodisplay -r \"cd('{locate_training_directory}'); LOCATE_testing('Longitudinal_Tests', 'Training_imgs_directory');exit\"")


# Creates the masks for New, Lost, and All Lesions
def masks_analysis(locate_training_directory, testing_directory):
    output = run_command(
        f"cd {testing_directory}/LOCATE_results_directory && fslmaths tp2_BIANCA_LOCATE_binarylesionmap.nii.gz -sub tp1_BIANCA_LOCATE_binarylesionmap.nii.gz {locate_training_directory}/Longitudinal_Tests/new_lesion_mask.nii.gz")
    output = run_command(
        f"cd {testing_directory}/LOCATE_results_directory && fslmaths tp2_BIANCA_LOCATE_binarylesionmap.nii.gz -add tp1_BIANCA_LOCATE_binarylesionmap.nii.gz {locate_training_directory}/Longitudinal_Tests/all_lesion_mask.nii.gz")
    output = run_command(
        f"cd {testing_directory}/LOCATE_results_directory && fslmaths tp1_BIANCA_LOCATE_binarylesionmap.nii.gz -sub tp2_BIANCA_LOCATE_binarylesionmap.nii.gz {locate_training_directory}/Longitudinal_Tests/lost_lesion_mask.nii.gz")

# Stores all the useful files in the user inputted output folder
def store_files(locate_training_directory, outputFolderPath):
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Tests/tp1_feature_FLAIR.nii.gz {outputFolderPath}/tp1_feature_FLAIR.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Tests/tp2_feature_FLAIR.nii.gz {outputFolderPath}/tp2_feature_FLAIR.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Tests/all_lesion_mask.nii.gz {outputFolderPath}/all_lesion_mask_on_tp2.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Tests/lost_lesion_mask.nii.gz {outputFolderPath}/lost_lesion_mask_on_tp2.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Tests/new_lesion_mask.nii.gz {outputFolderPath}/new_lesion_mask_on_tp2.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Tests/LOCATE_results_directory/tp1_BIANCA_LOCATE_binarylesionmap.nii.gz {outputFolderPath}/tp1_lesion_mask.nii.gz")
    output = run_command(
        f"cd {locate_training_directory} && mv {locate_training_directory}/Longitudinal_Tests/LOCATE_results_directory/tp2_BIANCA_LOCATE_binarylesionmap.nii.gz {outputFolderPath}/tp2_lesion_mask.nii.gz")


# Removes all the intermediary files
def remove_intermediary(locate_training_directory):
    shutil.rmtree(f"{locate_training_directory}/Longitudinal_Processing")
    shutil.rmtree(f"{locate_training_directory}/Longitudinal_Tests")


# Changes the color of the 'Open in FSLEyes' button
def openFslButton(outputFolderPath):
    if os.path.exists(f"{outputFolderPath}/tp1_lesion_mask.nii.gz") and os.path.exists(
            f"{outputFolderPath}/tp2_lesion_mask.nii.gz"):
        return True


# Opens all the files in FSLEyes
def openFslEyes(outputFolderPath):
    output = run_command(
        f"fsleyes {outputFolderPath}/new_lesion_mask_on_tp2.nii.gz {outputFolderPath}/lost_lesion_mask_on_tp2.nii.gz {outputFolderPath}/all_lesion_mask_on_tp2.nii.gz {outputFolderPath}/tp1_feature_FLAIR.nii.gz {outputFolderPath}/tp1_lesion_mask.nii.gz -dr 0 1 -cm red-yellow {outputFolderPath}/tp2_feature_FLAIR.nii.gz {outputFolderPath}/tp2_lesion_mask.nii.gz -dr 0 1 -cm blue-lightblue &")
# ------------------------------------------------


# --------------------------------------------
# DESIGN, LAYOUT AND FUNCTION CALLS OF THE GUI
class ContentArea(QWidget):
    def __init__(self, parent):
        # self.create_directories() // Function that creates the directories for the Output Files to be stored
        def basiclayout():
            super(QWidget, self).__init__(parent)
            self.layout = QVBoxLayout(self)
            style = """
            background-color: #EEECEC;
            padding-top:10px;
            padding-left:20px;
            """
            self.setStyleSheet(style)
            # Add tabs
            self.mainWindow = QWidget()

            self.mainWindow.layout = QVBoxLayout(self)

        basiclayout()
        self.tp1_selected = False
        self.tp2_selected = False
        self.folder_selected = False
        self.analysis_complete = False

        # Function for Opening the 'File Selector' and then choosing the image for TimePoint 1
        def open_tp1(event):
            file_filter = "NIFTI files (*.nii.gz)"
            path = QFileDialog.getOpenFileName(self, 'Open a file', '', file_filter)
            if path != ('', ''):
                print("File path : " + path[0])
                tp1_text_box.setText(path[0])  # Shows the path in the Text Box for Timepoint 1
                tp1_file_name.setText(path[0].split("/")[-1])  # Splits the File Path to get the file name
                self.flairTp1 = path[0]
                self.tp1_selected = True
                if self.tp1_selected & self.tp2_selected & self.folder_selected:
                    run_analysis.setStyleSheet(button_available)

        # Function for Opening the 'File Selector' and then choosing the image for TimePoint 2
        def open_tp2(event):
            file_filter = "NIFTI files (*.nii.gz)"
            path2 = QFileDialog.getOpenFileName(self, 'Open a file', '', file_filter)
            if path2 != ('', ''):
                print("File path : " + path2[0])
                tp2_text_box.setText(path2[0])  # Shows the path in the Text Box for Timepoint 1
                tp2_file_name.setText(path2[0].split("/")[-1])  # Splits the File Path to get the file name
                self.flairTp2 = path2[0]
                self.tp2_selected = True
                if self.tp1_selected & self.tp2_selected & self.folder_selected:
                    run_analysis.setStyleSheet(button_available)

        # Function for Opening the 'File Selector' and then choosing the output folder
        def open_output(event):
            path2 = QFileDialog.getExistingDirectory(self, 'Open a folder', '')
            if path2 != ('', ''):
                print("File path : " + path2)
                output_text_box.setText(path2)  # Shows the path in the Text Box for Timepoint 1
                output_file_name.setText(path2.split("/")[-1])  # Splits the File Path to get the file name
                self.outputFolderPath = path2
                self.folder_selected = True
                if self.tp1_selected & self.tp2_selected & self.folder_selected:
                    run_analysis.setStyleSheet(button_available)

        def showOnScreen(input):
            print(input)
            outputScreen.insertPlainText(input)
            outputScreen.insertPlainText("\n")
            QApplication.processEvents()

        def on_run_analysis_clicked():
            if self.tp1_selected & self.tp2_selected & self.folder_selected:
                print("Can Run")
                model_directory, locate_training_directory, processing_directory, testing_directory, timepoint1_directory, timepoint2_directory, t1_2_mni, mni_directory = managedirectories(
                    self.flairTp1, self.flairTp2)
                showOnScreen("-> running brain extraction...")
                # run_bet(timepoint1_directory, timepoint2_directory,processing_directory, self.flairTp1, self.flairTp2)
                showOnScreen("-> brain extraction complete!")
                showOnScreen("-> resampling both timepoints...")
                # resample_images(processing_directory)
                showOnScreen("-> resampling complete...!")
                showOnScreen("-> running fsl fast...")
                # run_fsl_fast(locate_training_directory)
                showOnScreen("-> fsl fast complete...!")
                showOnScreen("-> obtaining other intermediary files...!")
                # obtain_files_tp1(locate_training_directory, mni_directory, t1_2_mni)
                # generate_bianca_masterfile_tp1(locate_training_directory, model_directory)
                # move_files_tp1(locate_training_directory, testing_directory)
                # obtain_files_tp2(locate_training_directory, mni_directory, t1_2_mni)
                # generate_bianca_masterfile_tp2(locate_training_directory, model_directory)
                # move_files_tp2(locate_training_directory, testing_directory)
                showOnScreen("-> files obtained!")
                showOnScreen("-> Running LOCATE...")
                # run_locate(locate_training_directory)
                showOnScreen("-> LOCATE complete!")
                # run_analysis(locate_training_directory, testing_directory)
                showOnScreen("-> Storing Data in Output Folder")
                # store_files(locate_training_directory, self.outputFolderPath)
                remove_intermediary(locate_training_directory)
                showOnScreen("-> Longitudinal Analysis Complete! Please check your files in the output folder.")
                self.analysis_complete = openFslButton(self.outputFolderPath)
                if self.analysis_complete:
                    open_fsl.setStyleSheet(button_available)
            else:
                print("Please select all three paths!")

        def on_open_fsl_clicked():
            if self.analysis_complete:
                openFslEyes(self.outputFolderPath)
            else:
                print("Please Run Longitudinal Analysis first")

        # -----------------------------------------------
        # BASIC CODE THAT APPLIES OVERALL
        # Create a QGraphicsDropShadowEffect and set its properties
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 50))  # Set the color to black
        shadow.setBlurRadius(15)  # Set the blur radius
        shadow.setOffset(0, 0)  # Set the offset

        button_available = """
        QPushButton {
            background-color: #3E8AAC;
            color: #FFFFFF;
            text-align: center;
            padding: 0 10px;
            margin-top: 10px;
            margin-left: 100px;
            margin-right: 100px;
            margin-bottom: 10px;
            border-radius: 5px;
            padding-top: 5px;
            padding-bottom: 5px;
        }
        QPushButton:hover {
            background-color: #5FB2D3;
        }
        """

        button_not_available = """
        QPushButton {
            background-color: #90A3AB;
            color: #FFFFFF;
            text-align: center;
            padding: 0 10px;
            margin-top: 10px;
            margin-left: 100px;
            margin-right: 100px;
            margin-bottom: 10px;
            border-radius: 5px;
            padding-top: 5px;
            padding-bottom: 5px;
        }
        """

        # -----------------------------------------------
        # CODE STARTS FOR THE FIRST BLOCK - TIME-POINT 1
        # The first text label for choosing timepoint 1
        biglabel = QLabel("Choose Flair File for Time-point 1")
        font = QFont("Helvetica", 14)
        biglabel.setFont(font)
        biglabel.setStyleSheet(" color:#696767;")

        # A Horizontal Layout for the DropDown Image and the TextBox
        h_layout1 = QHBoxLayout()
        h_layout1.setContentsMargins(4, 10, 20, 0)

        # Adds an Image to the Screen with the specified size
        select_tp1 = QLabel()
        pixmap = QPixmap("assets/images/down")
        max_size = QSize(45, 45)
        scaled_pixmap = pixmap.scaled(max_size, aspectRatioMode=Qt.KeepAspectRatio)
        select_tp1.setPixmap(scaled_pixmap)
        select_tp1.setStyleSheet("padding-top: -5px;")
        select_tp1.setAlignment(Qt.AlignVCenter)  # Set the vertical alignment to center

        # Create the QTextEdit for the text box and place it next to the image
        tp1_text_box = QTextEdit()
        tp1_text_box.setReadOnly(True)  # set the readOnly property to True
        tp1_text_box.setFixedHeight(40)  # Set a fixed height for the line to make it visible
        tp1_text_box.setStyleSheet(
            "background-color: white; border: 1px solid white; border-radius: 5px; padding-top:-8px;")
        tp1_text_box.setAlignment(Qt.AlignVCenter)
        tp1_text_box.setGraphicsEffect(shadow)

        # A Second Horizontal Layout for the folder, file name, and text
        h_layout2 = QHBoxLayout()
        h_layout2.setContentsMargins(3, -5, 20, 0)

        # Adds the folder image to the screen
        folder_image = QLabel()
        pixmap = QPixmap("assets/images/folder.png")
        max_size = QSize(23, 23)
        scaled_pixmap = pixmap.scaled(max_size, aspectRatioMode=Qt.KeepAspectRatio)
        folder_image.setPixmap(scaled_pixmap)
        folder_image.setStyleSheet("padding-top: 0px;padding-left:23px;")
        folder_image.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # Spacing between the folder and the file name
        h_layout2.addSpacing(1)
        # Adds the file name (blue colored) on the GUI
        tp1_file_name = QLabel("No File Selected")
        font = QFont("Helvetica", 10)
        tp1_file_name.setFont(font)
        tp1_file_name.setStyleSheet("color:#115270;padding-top:-5px;padding-left:-40px;")
        tp1_file_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # Label to verify the file paths in text
        verify_label = QLabel("Verify the File Path & Name")
        verify_label.setFont(font)
        verify_label.setStyleSheet("color:#888888;padding-top: -10px;")
        verify_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        verify_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Adds all of the produced widgets and layouts to the mainWindow
        self.mainWindow.layout.addWidget(biglabel)
        self.mainWindow.layout.addLayout(h_layout1)
        self.mainWindow.layout.addLayout(h_layout2)
        h_layout1.addWidget(select_tp1)
        h_layout1.addWidget(tp1_text_box)
        h_layout2.addWidget(folder_image)
        h_layout2.addWidget(tp1_file_name)
        h_layout2.addWidget(verify_label)

        # For appropriate alignment of the second horizontal layout
        h_layout2.setStretchFactor(folder_image, 0)  # Set stretch factor to 0
        h_layout2.setStretchFactor(tp1_file_name, 1)  # Set stretch factor to 1
        h_layout2.setStretchFactor(verify_label, 0)  # Set stretch factor to 0

        # Mapping the open_tp1 function to the Drop Down Image
        select_tp1.mousePressEvent = open_tp1
        # CODE ENDS FOR THE FIRST BLOCK - TIME-POINT 1
        # -----------------------------------------------

        # -----------------------------------------------
        # CODE STARTS FOR THE SECOND BLOCK - TIME-POINT 2
        biglabel2 = QLabel("Choose Flair File for Time-point 2")
        font = QFont("Helvetica", 14)
        biglabel2.setFont(font)
        biglabel2.setStyleSheet(" color:#696767;padding-top:15px;")

        # A Horizontal Layout for the DropDown Image and the TextBox
        h_layout1 = QHBoxLayout()
        h_layout1.setContentsMargins(4, 10, 20, 0)

        # Adds an Image to the Screen with the specified size
        select_tp2 = QLabel()
        pixmap = QPixmap("assets/images/down")
        max_size = QSize(45, 45)
        scaled_pixmap = pixmap.scaled(max_size, aspectRatioMode=Qt.KeepAspectRatio)
        select_tp2.setPixmap(scaled_pixmap)
        select_tp2.setStyleSheet("padding-top: -5px;")
        select_tp2.setAlignment(Qt.AlignVCenter)  # Set the vertical alignment to center

        # Create the QTextEdit for the text box and place it next to the image
        tp2_text_box = QTextEdit()
        tp2_text_box.setReadOnly(True)  # set the readOnly property to True
        tp2_text_box.setFixedHeight(40)  # Set a fixed height for the line to make it visible
        tp2_text_box.setStyleSheet(
            "background-color: white; border: 1px solid white; border-radius: 5px; padding-top:-8px;")
        tp2_text_box.setAlignment(Qt.AlignVCenter)
        tp2_text_box.setGraphicsEffect(shadow)

        # A Second Horizontal Layout for the folder, file name, and text
        h_layout2 = QHBoxLayout()
        h_layout2.setContentsMargins(3, -5, 20, 0)

        # Adds the folder image to the screen
        folder_image = QLabel()
        pixmap = QPixmap("assets/images/folder.png")
        max_size = QSize(23, 23)
        scaled_pixmap = pixmap.scaled(max_size, aspectRatioMode=Qt.KeepAspectRatio)
        folder_image.setPixmap(scaled_pixmap)
        folder_image.setStyleSheet("padding-top: 0px;padding-left:23px;")
        folder_image.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # Spacing between the folder and the file name
        h_layout2.addSpacing(1)
        # Adds the file name (blue colored) on the GUI
        tp2_file_name = QLabel("No File Selected")
        font = QFont("Helvetica", 10)
        tp2_file_name.setFont(font)
        tp2_file_name.setStyleSheet("color:#115270;padding-top:-5px;padding-left:-40px;")
        tp2_file_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # Label to verify the file paths in text
        verify_label = QLabel("Verify the File Path & Name")
        verify_label.setFont(font)
        verify_label.setStyleSheet("color:#888888;padding-top: -10px;")
        verify_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        verify_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.mainWindow.layout.addWidget(biglabel2)
        self.mainWindow.layout.addLayout(h_layout1)
        self.mainWindow.layout.addLayout(h_layout2)
        h_layout1.addWidget(select_tp2)
        h_layout1.addWidget(tp2_text_box)
        h_layout2.addWidget(folder_image)
        h_layout2.addWidget(tp2_file_name)
        h_layout2.addWidget(verify_label)

        # For appropriate alignment of the second horizontal layout
        h_layout2.setStretchFactor(folder_image, 0)  # Set stretch factor to 0
        h_layout2.setStretchFactor(tp2_file_name, 1)  # Set stretch factor to 1
        h_layout2.setStretchFactor(verify_label, 0)  # Set stretch factor to 0

        # Mapping the open_tp1 function to the Second Drop Down Image
        select_tp2.mousePressEvent = open_tp2
        # CODE ENDS FOR THE SECOND BLOCK - TIME-POINT 2
        # -----------------------------------------------

        # -----------------------------------------------
        # CODE STARTS FOR THE THIRD BLOCK - OUTPUT FOLDER
        biglabel3 = QLabel("Where do you want to store the results?")
        font = QFont("Helvetica", 14)
        biglabel3.setFont(font)
        biglabel3.setStyleSheet(" color:#696767;padding-top:15px;")

        # A Horizontal Layout for the DropDown Image and the TextBox
        h_layout1 = QHBoxLayout()
        h_layout1.setContentsMargins(4, 10, 20, 0)

        # Adds an Image to the Screen with the specified size
        select_output = QLabel()
        pixmap = QPixmap("assets/images/down")
        max_size = QSize(45, 45)
        scaled_pixmap = pixmap.scaled(max_size, aspectRatioMode=Qt.KeepAspectRatio)
        select_output.setPixmap(scaled_pixmap)
        select_output.setStyleSheet("padding-top: -5px;")
        select_output.setAlignment(Qt.AlignVCenter)  # Set the vertical alignment to center

        # Create the QTextEdit for the text box and place it next to the image
        output_text_box = QTextEdit()
        output_text_box.setReadOnly(True)  # set the readOnly property to True
        output_text_box.setFixedHeight(40)  # Set a fixed height for the line to make it visible
        output_text_box.setStyleSheet(
            "background-color: white; border: 1px solid white; border-radius: 5px; padding-top:-8px;")
        output_text_box.setAlignment(Qt.AlignVCenter)
        output_text_box.setGraphicsEffect(shadow)

        # A Second Horizontal Layout for the folder, file name, and text
        h_layout2 = QHBoxLayout()
        h_layout2.setContentsMargins(3, -5, 20, 0)

        # Adds the folder image to the screen
        folder_image = QLabel()
        pixmap = QPixmap("assets/images/folder.png")
        max_size = QSize(23, 23)
        scaled_pixmap = pixmap.scaled(max_size, aspectRatioMode=Qt.KeepAspectRatio)
        folder_image.setPixmap(scaled_pixmap)
        folder_image.setStyleSheet("padding-top: 0px;padding-left:23px;")
        folder_image.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # Spacing between the folder and the file name
        h_layout2.addSpacing(1)
        # Adds the file name (blue colored) on the GUI
        output_file_name = QLabel("No File Selected")
        font = QFont("Helvetica", 10)
        output_file_name.setFont(font)
        output_file_name.setStyleSheet("color:#115270;padding-top:-5px;padding-left:-40px;")
        output_file_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # Label to verify the file paths in text
        verify_label = QLabel("Verify the File Path & Name")
        verify_label.setFont(font)
        verify_label.setStyleSheet("color:#888888;padding-top: -10px;")
        verify_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        verify_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.mainWindow.layout.addWidget(biglabel3)
        self.mainWindow.layout.addLayout(h_layout1)
        self.mainWindow.layout.addLayout(h_layout2)
        h_layout1.addWidget(select_output)
        h_layout1.addWidget(output_text_box)
        h_layout2.addWidget(folder_image)
        h_layout2.addWidget(output_file_name)
        h_layout2.addWidget(verify_label)

        # For appropriate alignment of the second horizontal layout
        h_layout2.setStretchFactor(folder_image, 0)  # Set stretch factor to 0
        h_layout2.setStretchFactor(output_file_name, 1)  # Set stretch factor to 1
        h_layout2.setStretchFactor(verify_label, 0)  # Set stretch factor to 0

        # Mapping the open_tp1 function to the Second Drop Down Image
        select_output.mousePressEvent = open_output
        # CODE ENDS FOR THE THIRD BLOCK - OUTPUT FOLDER
        # -----------------------------------------------

        # -----------------------------------------------
        # CODE STARTS FOR THE FOURTH BLOCK - RUN ANALYSIS
        run_analysis = QPushButton("Run Longitudinal Analysis")
        run_analysis.setStyleSheet(button_not_available)
        run_analysis.setGraphicsEffect(shadow)
        # Add the button to the layout
        self.mainWindow.layout.addWidget(run_analysis)
        run_analysis.clicked.connect(on_run_analysis_clicked)
        # CODE ENDS FOR THE FOURTH BLOCK - RUN ANALYSIS
        # -----------------------------------------------

        # -----------------------------------------------
        # CODE STARTS FOR THE FIFTH BLOCK - OUTPUT SCREEN
        outputScreen = QPlainTextEdit()
        font = QFont("Helvetica", 10)
        outputScreen.setFont(font)
        outputScreen.setStyleSheet("color: #75BB5D; background-color: rgb(0,0,0);")
        outputScreen.setReadOnly(True)  # set the readOnly property to True
        self.mainWindow.layout.addWidget(outputScreen, 7)
        # CODE ENDS FOR THE FIFTH BLOCK - OUTPUT SCREEN
        # -----------------------------------------------

        # -----------------------------------------------
        # CODE STARTS FOR THE SIXTH BLOCK - OPEN FSLEYES
        open_fsl = QPushButton("Open Results in FSLEyes")
        open_fsl.setStyleSheet(button_not_available)
        open_fsl.setGraphicsEffect(shadow)
        self.mainWindow.layout.addWidget(open_fsl)
        open_fsl.clicked.connect(on_open_fsl_clicked)
        # CODE ENDS FOR THE SIXTH BLOCK - OPEN FSLEYES
        # -----------------------------------------------

        # For displaying everything!
        self.mainWindow.setLayout(self.mainWindow.layout)
        self.layout.addWidget(self.mainWindow)
        self.setLayout(self.layout)


# --------------------------------
# DISPLAYING THE GUI ON THE SCREEN
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Base()
    sys.exit(app.exec_())
