# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 18:52:58 2023

@author: Sang-Wook Kim
"""
import os, io, sys
import struct

from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import *
import numpy as np
from t0816 복사본import drawR3d

form_class = uic.loadUiType("./detail_ro.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
 
        self.init_ui_value()
        self.init_signal()
    
        self.open_gl = drawR3d(parent=self.frame_gl)
        self.open_gl.resize(861,611)# create class instance, passing in the tab as parent
        #self.open_gl.setMinimumSize(861, 611)                # keep proportions, set to same size as frame
        
        #self.open_gl.paint_rotation = True
        
    def init_ui_value(self):
        self.X11.setRange(0, 360)
        self.X11_2.setRange(0, 360)
        self.X11_3.setRange(0, 360)
        '''self.X12.setRange(0, 360)
        self.X13.setRange(0, 360)
        self.X14.setRange(0, 360)
        self.X22.setRange(0, 360)
        self.X23.setRange(0, 360)
        self.X24.setRange(0, 360)
        self.X32.setRange(0, 360)
        self.X33.setRange(0, 360)
        self.X34.setRange(0, 360)
        self.X42.setRange(0, 360)
        self.X43.setRange(0, 360)
        self.X44.setRange(0, 360)'''


    def init_signal(self):
        self.X11.valueChanged.connect(self.change_X11)
        self.X11_2.valueChanged.connect(self.change_X11_2)
        self.X11_3.valueChanged.connect(self.change_X11_3)
        '''self.X12.valueChanged.connect(self.change_X12)
        self.X13.valueChanged.connect(self.change_X13)
        self.X14.valueChanged.connect(self.change_X14)
        self.X22.valueChanged.connect(self.change_X22)
        self.X23.valueChanged.connect(self.change_X23)
        self.X24.valueChanged.connect(self.change_X24)
        self.X32.valueChanged.connect(self.change_X32)
        self.X33.valueChanged.connect(self.change_X33)
        self.X34.valueChanged.connect(self.change_X34)
        self.X42.valueChanged.connect(self.change_X42)
        self.X43.valueChanged.connect(self.change_X43)
        self.X44.valueChanged.connect(self.change_X44)'''
        

    def change_X11(self):
        angle = self.X11.value()
        print(angle)
        self.open_gl.yaw =angle
        self.open_gl.update()
        
    def change_X11_2(self):
        angle = self.X11_2.value()
        print(angle)
        self.open_gl.roll =angle
        self.open_gl.update()
        
    def change_X11_3(self):
        angle = self.X11_3.value()
        print(angle)
        self.open_gl.pitch =angle
        self.open_gl.update()
'''        
    def change_X12(self):
        angle = self.X12.value()
        print(angle)
        self.open_gl.arm1X1 =angle
        self.open_gl.update()

    def change_X13(self):
         angle = self.X13.value()
         print(angle)
         self.open_gl.arm2X1 =angle
         self.open_gl.update()
         
    def change_X14(self):
        angle = self.X14.value()
        print(angle)
        self.open_gl.shoulder1 =angle
        self.open_gl.update()
        
    def change_X22(self):
        angle = self.X22.value()
        print(angle)
        self.open_gl.arm1X2 =angle
        self.open_gl.update()
        
    def change_X23(self):
        angle = self.X23.value()
        print(angle)
        self.open_gl.arm2X2 =angle
        self.open_gl.update()
        
    def change_X24(self):
        angle = self.X24.value()
        print(angle)
        self.open_gl.shoulder2 =angle
        self.open_gl.update()
        
    def change_X32(self):
        angle = self.X32.value()
        print(angle)
        self.open_gl.arm1X3 =angle
        self.open_gl.update()
        
    def change_X33(self):
        angle = self.X33.value()
        print(angle)
        self.open_gl.arm2X3 =angle
        self.open_gl.update()
        
    def change_X34(self):
        angle = self.X34.value()
        print(angle)
        self.open_gl.shoulder3 =angle
        self.open_gl.update()
        
    def change_X42(self):
        angle = self.X42.value()
        print(angle)
        self.open_gl.arm1X4 =angle
        self.open_gl.update()
        
    def change_X43(self):
        angle = self.X43.value()
        print(angle)
        self.open_gl.arm2X4 =angle
        self.open_gl.update()
        
    def change_X44(self):
        angle = self.X44.value()
        print(angle)
        self.open_gl.shoulder4 =angle
        self.open_gl.update()'''
        
    
         
    
         
     
        
if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    myWindow = WindowClass()
    myWindow.show()
    app.exec_() 