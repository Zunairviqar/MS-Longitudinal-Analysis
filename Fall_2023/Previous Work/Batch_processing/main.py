from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from fsl.wrappers import bet
import os
from fsl.wrappers.fslmaths import fslmaths



def bet(self):
    bet(self.TP_1_Flair, self.TP_1_Flair_Brain)
    bet(self.TP_1_T1, self.TP_1_T1_Brain)


def bet_2(self):
    bet(self.TP_2_FLAIR, self.TP_2_Flair_Brain)
    bet(self.TP_2_T1, self.TP_2_T1_Brain)


def resample_flair(self):
    x = os.system(
        f"flirt -in {self.TP_1_Flair_Brain} -ref {self.sample_brain} -out {self.resampled_FLAIR_TP1} -applyxfm")


def register_tp2_to_tp1(self):
    x = os.system(
        f"flirt -in {self.TP_2_Flair_Brain} -ref {self.resampled_FLAIR_TP1} -out {self.registered_FLAIR_TP2} -omat {self.registered_FLAIR_TP2_mat} {self.registration_parameters}")


def register_to_MNI(self):
    x = os.system(
        f"flirt -in {self.resampled_FLAIR_TP1} -ref {self.MNI_Brain} -out {self.resampled_FLAIR_TP1_To_MNI} -omat {self.resampled_FLAIR_TP1_To_MNI_mat} {self.registration_parameters}")


def register_to_MNI_2(self):
    x = os.system(
        f"flirt -in {self.registered_FLAIR_TP2} -ref {self.MNI_Brain} -out {self.registered_FLAIR_TP2_To_MNI} -omat {self.registered_FLAIR_TP2_To_MNI_mat} {self.registration_parameters}")


def register_t1_to_flair(self):
    x = os.system(
        f"flirt -in {self.TP_1_T1_Brain} -ref {self.resampled_FLAIR_TP1} -out {self.TP_1_T1_Brain_To_Resampled_FLAIR} -omat {self.TP_1_T1_Brain_To_Resampled_FLAIR_mat} {self.registration_parameters}")


def register_t1_to_flair_2(self):
    x = os.system(
        f"flirt -in {self.TP_2_T1_Brain} -ref {self.registered_FLAIR_TP2} -out {self.TP_2_T1_Brain_To_Registered_FLAIR} -omat {self.TP_2_T1_Brain_To_Registered_FLAIR_mat} {self.registration_parameters}")


def generate_masterfile(self):
    file = open(self.TP_1_Masterfile, 'w')
    file.write(self.resampled_FLAIR_TP1 + ' ')
    file.write(self.TP_1_T1_Brain_To_Resampled_FLAIR + ' ')
    file.write(self.resampled_FLAIR_TP1_To_MNI_mat + ' ')
    file.write(self.FLAIR_Lesion_Mask + ' ')


def generate_masterfile_2(self):
    file = open(self.TP_2_Masterfile, 'w')
    file.write(self.registered_FLAIR_TP2 + ' ')
    file.write(self.TP_2_T1_Brain_To_Registered_FLAIR + ' ')
    file.write(self.registered_FLAIR_TP2_To_MNI_mat + ' ')
    file.write(self.FLAIR_Lesion_Mask_2 + ' ')


def run_bianca(self):
    x = os.system(
        f"bianca --singlefile={self.TP_1_Masterfile} --loadclassifierdata={self.Classifer} --querysubjectnum=1 --brainmaskfeaturenum=1 --featuresubset=1,2 --matfeaturenum=3 -o {self.Bianca_output} -v")


def run_bianca_2(self):
    x = os.system(
        f"bianca --singlefile={self.TP_2_Masterfile} --loadclassifierdata={self.Classifer} --querysubjectnum=1 --brainmaskfeaturenum=1 --featuresubset=1,2 --matfeaturenum=3 -o {self.Bianca_output_2} -v")


def bianca_binary(self):
    fslmaths(self.Bianca_output).thr(0.9).bin().run(self.Bianca_output_bin)


def bianca_binary_2(self):
    fslmaths(self.Bianca_output_2).thr(0.9).bin().run(self.Bianca_output_bin_2)


def bianca_open(self):
    x = os.system(f"fslmaths {self.Bianca_output_bin} -kernel box 2 -ero -dilM {self.Bianca_output_bin_ero_dilM}")


def bianca_open_2(self):
    x = os.system(
        f"fslmaths {self.Bianca_output_bin_2} -kernel box 2 -ero -dilM {self.Bianca_output_bin_ero_dilM_2}")


def run_all_bianca(self):
    self.bet()
    self.resample_flair()
    self.register_to_MNI()
    self.register_t1_to_flair()
    self.generate_masterfile()
    self.run_bianca()
    self.bianca_binary()
    self.bianca_open()


def run_all_bianca_2(self):
    self.bet_2()
    self.register_tp2_to_tp1()
    self.register_to_MNI_2()
    self.register_t1_to_flair_2()
    self.generate_masterfile_2()
    self.run_bianca_2()
    self.bianca_binary_2()
    self.bianca_open_2()


def subtract_lesions(self):
    x = os.system(
        f"fslmaths {self.Bianca_output_bin_ero_dilM_2} -sub {self.Bianca_output_bin_ero_dilM} New_lesion_mask.nii.gz")


def lost_lesions(self):
    x = os.system(
        f"fslmaths {self.Bianca_output_bin_ero_dilM} -sub {self.Bianca_output_bin_ero_dilM_2} Old_lesion_mask.nii.gz")


def total_lesions(self):
    x = os.system(
        f"fslmaths {self.Bianca_output_bin_ero_dilM_2} -add {self.Bianca_output_bin_ero_dilM} Total_lesion_mask.nii.gz")
