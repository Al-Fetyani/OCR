import cv2
from PyQt5.QtWidgets import QApplication, QFileDialog, QRubberBand
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import pytesseract
import os
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
import glob
import subprocess
import numpy as np
from PIL import ImageGrab
from pynput import keyboard

language_path = 'C:\\Program Files\\Tesseract-OCR\\tessdata\\'
language_path_list = glob.glob(language_path + '*.traineddata')
language_list = [os.path.splitext(os.path.basename(path))[0] for path in language_path_list]

class APP(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi("gui.ui", self)
        self.image = None

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        self.pushButton.clicked.connect(self.open_image)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.ui.label_2.setMouseTracking(True)
        self.ui.label_2.installEventFilter(self)
        self.ui.label_2.setAlignment(Qt.AlignCenter)

        self.language = 'eng'
        self.comboBox.addItems(language_list)
        self.comboBox.currentIndexChanged['QString'].connect(self.language_change)
        self.comboBox.setCurrentIndex(language_list.index(self.language))
    def on_press(key):
        if key == keyboard.Key.esc:
            return False
        try:
            k = key.char 
        except:
            k = key.name 
        if k == "f1":  
            return False  
    def language_change(self, value):
        self.language = value
    
    def open_image(self):
        self.textEdit.clear()
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        if filename:
            self.image = cv2.imread(filename)
            self.display_image()
            self.perform_ocr()
    def real_time(self):
        subprocess.run(['python', 'shot.py'])
        with open('screenshot_coordinates.txt', 'r') as f:
            coordinates = f.read().split(',')
        coordinates = [int(coord) for coord in coordinates]
        self.image = ImageGrab.grab(bbox=(coordinates[0], coordinates[1], coordinates[2], coordinates[3]))
        self.display_image()
        self.perform_ocr()

    def display_image(self):
        if self.image is not None:
            frame = cv2.cvtColor(np.array(self.image), cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            self.ui.label_2.setPixmap(QPixmap.fromImage(image))
        else:
            QtWidgets.QMessageBox.information(self, "Error", "Error loading image")

    def perform_ocr(self):
        text = pytesseract.image_to_string(np.array(self.image), lang=self.language)
        self.textEdit.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = APP()
    window.show()
    sys.exit(app.exec_())
