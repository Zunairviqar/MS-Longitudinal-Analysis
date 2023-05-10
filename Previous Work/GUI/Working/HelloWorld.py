import sys
import os
# Importing all the relevant PyQT Libraries to be used
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# Standard Commands --Start--
# Creating an instance of the QApplication which is the underlying of our Graphical User Interface
app = QApplication(sys.argv)

# Outlying the Main Window, also a widget, inside of the Application, could be multiple like Dialog boxes or prompts but I havent explored them yet
window = QWidget()
# Instantiates the MainWindow and exports it to the Screen
window.show()
# Standard Commands --End--

# Sets the Window Title
window.setWindowTitle("Practice GUI")
# The height and width of the Window is defined. There are other ways as well like setGeometry(a,b,c,d)
window.setFixedSize(500, 500)

# This sets the Type of Layout for our application. Q - V - BoxLayout means *V* - Vertical Layout in the form of a Box
# Similarly there is Q*H*Layout for for a Horizontal Box Layout: https://realpython.com/python-pyqt-layout/#building-horizontal-layouts-qhboxlayout
# Alternatively there are Grid Layouts and Form Layouts that can be used for more complex GUI Designs
layout = QVBoxLayout()

# QLabel is a form of a widget. Everything is widget in pyQT and QLabel, as the name suggests, lays out a text box for us
HelloWorld = QLabel("Hello World")

# There are multiple ways to position and style them as can be seen from below. There also ways to position them absolutely on the screen
HelloWorld.setAlignment(Qt.AlignCenter)
HelloWorld.setFont(QFont('Arial', 80))

# Now that we have created a QLabel Widget, we attach that to the layout that we created on line 26
layout.addWidget(HelloWorld)
# Attaching it to the layout allows us to further attach the widget to the main window in an organized manner

# Here we set the layout for the window to the above defined and styled layout (the QVBoxLayout)
window.setLayout(layout)

# This enters a loop for the window and only ends when we close the window!
sys.exit(app.exec_())