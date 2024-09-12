#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 23:58:21 2023

@author: kensMACbook
"""
import sys
import time
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib import pyplot as plt
import numpy as np
import pyqtgraph as pg
from keycontrol import keyinput      
from myunitree_value import myunitree
#from ken_openGL import PyQtOpenGL
from robot3dmodel_3 import robot3d

class Tread1(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        while True:
            time.sleep(0.2)
            self.parent.sendCmd()
            self.parent.openglset()
        
a=keyinput()
form_class = uic.loadUiType("roui.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        self.num1=0
        super().__init__()
        self.setupUi(self)
        self.key=''
        self.isungb1 = myunitree()
        #버튼에 기능을 연결하는 코드
        self.btn_q.clicked.connect(self.buttonQ)
        self.btn_w.clicked.connect(self.buttonW)
        self.btn_e.clicked.connect(self.buttonE)
        self.btn_a.clicked.connect(self.buttonA)
        self.btn_s.clicked.connect(self.buttonS)
        self.btn_d.clicked.connect(self.buttonD)
        self.btn_z.clicked.connect(self.buttonZ)
        self.btn_x.clicked.connect(self.buttonX)
        self.btn_c.clicked.connect(self.buttonC)
        self.btn_ok.clicked.connect(self.buttonOK)
        self.btn_cancel.clicked.connect(self.buttonCancel)
        #opengl 관련
        self.open_gl = robot3d(parent=self.frame_gl)   # create class instance, passing in the tab as parent
        self.open_gl.setMinimumSize(441, 411)                # keep proportions, set to same size as frame

        #self.open_gl.paint_rotation = True

        
    def buttonQ(self):
        self.key=self.key+'q'
        self.command.setText(self.key)
        
        
    def buttonW(self):
        self.key=self.key+'w'
        self.command.setText(self.key)
        
    def buttonE(self):
        self.key=self.key+'e'
        self.command.setText(self.key)
        
    def buttonA(self):
        self.key=self.key+'a'
        self.command.setText(self.key)
        
    def buttonS(self):
        self.key=self.key+'s'
        self.command.setText(self.key)
        
    def buttonD(self):
        self.key=self.key+'d'
        self.command.setText(self.key)
        
    def buttonZ(self):
        self.key=self.key+'z'
        self.command.setText(self.key)
    
    def buttonX(self):
        self.key=self.key+'x'
        self.command.setText(self.key)
    
    def buttonC(self):
        self.key=self.key+'c'
        self.command.setText(self.key)
    
    def buttonOK(self):
        b=Tread1(self)
        b.start()
        self.isungb1.connect()
        a.run(self.key)
        self.key=''
        self.command.setText(self.key)

    def buttonCancel(self):
        self.key=''
        self.command.setText(self.key)

    def sendCmd(self):
        self.isungb1.sendCmd()
        self.Xvalue.setText(str(np.rad2deg(self.isungb1.motorQ[0])))
        self.Yvalue.setText(str(np.rad2deg(self.isungb1.motorQ[1])))
        self.Xvalue_2.setText(str(np.rad2deg(self.isungb1.motorQ[2])))
        self.Zvalue.setText(str(np.rad2deg(self.isungb1.hstateRPY[2])))
        
    def openglset(self):
        self.open_gl.robotRPY3d([self.isungb1.hstateRPY[0],self.isungb1.hstateRPY[1],self.isungb1.hstateRPY[2]])
        self.open_gl.robotMotor3d([self.isungb1.motorQ[0],self.isungb1.motorQ[1],self.isungb1.motorQ[2],self.isungb1.motorQ[3],self.isungb1.motorQ[4],self.isungb1.motorQ[5],self.isungb1.motorQ[6],self.isungb1.motorQ[7],self.isungb1.motorQ[8],self.isungb1.motorQ[9],self.isungb1.motorQ[10],self.isungb1.motorQ[11]])
        self.open_gl.update()
        for i in range(20):
            print(np.rad2deg(self.isungb1.motorQ[i]))
        
    
    
    
if __name__ == "__main__" :

    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()
    

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

    
        