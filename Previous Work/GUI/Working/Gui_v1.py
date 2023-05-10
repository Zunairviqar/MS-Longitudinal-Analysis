import sys
import os

from fsl.wrappers import bet

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QPushButton, QVBoxLayout, QFileDialog, QLabel, QTextEdit


# you can copy and run this code

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        self.file_path = None
        self.TP_1_Flair = ''
        self.TP_1_T1 = ''

        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Multiple Sclerosis Tool")
        self.setFixedSize(500, 500)

        file_btn = QPushButton("Choose File for Flair Timepoint 1")
        self.myTextBox = QTextEdit()
        self.myTextBox.setFixedHeight(40)
        verify_1 = QLabel("Please verify the file path")
        verify_1.setAlignment(Qt.AlignRight)

        file_btn_2 = QPushButton("Choose File for T1 Timepoint 1")
        self.myTextBox_2 = QTextEdit()
        self.myTextBox_2.setFixedHeight(40)
        verify_2 = QLabel("Please verify the file path")
        verify_2.setAlignment(Qt.AlignRight)

        bet_btn = QPushButton("Run Brain Extraction")
        resample_Flair = QPushButton("Resample the FLAIR Image to Testing Data")
        register_FLAIR = QPushButton("Register the Resampled Brain to MNI Space")
        register_T1 = QPushButton("Register the T1 Image onto the Resampled Flair Image")
        Create_MF = QPushButton("Create a Master file with the Generated Data for BIANCA")
        BIANCA = QPushButton("Run the BIANCA Algorithm")
        Binary_mask = QPushButton("Create a Binary Mask from the BIANCA Output")
        Ero_Dil = QPushButton("Refine the Binary Mask")


        layout = QVBoxLayout()
        layout.addWidget(file_btn)
        layout.addWidget(self.myTextBox)
        layout.addWidget(verify_1)

        layout.addWidget(file_btn_2)
        layout.addWidget(self.myTextBox_2)
        layout.addWidget(verify_2)

        layout.addWidget(bet_btn)
        layout.addWidget(resample_Flair)
        layout.addWidget(register_FLAIR)

        layout.addWidget(register_T1)
        layout.addWidget(Create_MF)
        layout.addWidget(BIANCA)
        layout.addWidget(Binary_mask)
        layout.addWidget(Ero_Dil)



        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        file_btn.clicked.connect(self.open_1)  # connect clicked to self.open()
        file_btn_2.clicked.connect(self.open_2)  # connect clicked to self.open()
        bet_btn.clicked.connect(self.bet)

        self.show()

    def open_1(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.myTextBox.setText(path[0])
            self.TP_1_Flair = path[0]

    def open_2(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.myTextBox_2.setText(path[0])
            self.TP_1_T1 = path[0]


    def bet(self):
        bet(self.TP_1_Flair, 'FLAIR_TP1_Test_Brain')
        bet(self.TP_1_T1, 'data/TP_1/T1_TP1_Test_Brain')
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
