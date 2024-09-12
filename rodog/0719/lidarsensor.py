#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 22:58:04 2023

@author: kensMACbook
"""
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import *
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


'''plt.pcolor(csv_test, cmap = 'jet')
plt.colorbar()
plt.clim(0,3000)
plt.colorbar
plt.colorbar()
plt.clim(0,30000)
plt.clim(0,15000)
plt.clim(0,6000)
3
plt.clim(0,3000)
76/160
32/60
import numpy as np'''
csv_test = pd.read_csv('1frame.csv', header=None)
theta_x = np.arange(38, -38, -0.475)
theta_y = np.arange(16,-16,-0.54)
X=np.cos(np.deg2rad(theta_x))
Y=np.sin(np.deg2rad(theta_x))
Z=np.sin(np.deg2rad(theta_y))
K=np.cos(np.deg2rad(theta_y))
#depth=csv_test.to_numpy()
depth=np.transpose(csv_test)
Kco=np.repeat(K,160)
Kco=Kco.reshape((60,160))
Kco=np.transpose(Kco)
Xco=np.repeat(X,60)
Xco=Xco.reshape((160,60))
RXco=Kco*Xco*depth
#Xv=Kco*Xco
Yco=np.repeat(Y,60)
Yco=Yco.reshape((160,60))
RYco=Kco*Yco*depth
#Yv=Kco*Yco
Zco=np.repeat(Z,160)
Zco=Zco.reshape((60,160))
RZco=np.transpose(Zco)
#Zv=RZco
RZco = RZco*depth
#R=(np.sqrt(Xv*Xv+Yv*Yv+Zv*Zv))

def drawPlane():
    n, w = 100, 500
    # n: 체스판 한면의 정점수, w: 체스판 한면의 길이
   
    d = w / (n-1) # 인접한 두 정점 사이의 간격

    #  체스판 그리기
    glColor3f(0.3,0.5,0)
    glBegin(GL_QUADS)
    for i in range(n):
        for j in range(n):
            if (i+j)%2 == 0:
                startX = -w/2 + i*d
                startZ = -w/2 + j*d
                glVertex3f(startX, 0, startZ)
                glVertex3f(startX, 0, startZ+d)
                glVertex3f(startX+d, 0, startZ+d)
                glVertex3f(startX+d, 0, startZ)
    glEnd()

def drawAxes():
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(1,0,0)
    glColor3f(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,1,0)
    glColor3f(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1)
    glEnd()

def drawCube():
    v0 = [-0.5, 0.5, 0.5]
    v1 = [ 0.5, 0.5, 0.5]
    v2 = [ 0.5, 0.5,-0.5]
    v3 = [-0.5, 0.5,-0.5]
    v4 = [-0.5,-0.5, 0.5]
    v5 = [ 0.5,-0.5, 0.5]
    v6 = [ 0.5,-0.5,-0.5]
    v7 = [-0.5,-0.5,-0.5]
    glBegin(GL_LINES)
    glVertex3fv(v0); glVertex3fv(v1)
    glVertex3fv(v1); glVertex3fv(v2)
    glVertex3fv(v2); glVertex3fv(v3)
    glVertex3fv(v3); glVertex3fv(v0)
    glVertex3fv(v4); glVertex3fv(v5)
    glVertex3fv(v5); glVertex3fv(v6)
    glVertex3fv(v6); glVertex3fv(v7)
    glVertex3fv(v7); glVertex3fv(v4)
    glVertex3fv(v0); glVertex3fv(v4)
    glVertex3fv(v1); glVertex3fv(v5)
    glVertex3fv(v2); glVertex3fv(v6)
    glVertex3fv(v3); glVertex3fv(v7)    
    glEnd()
    drawAxes()
    
def drawpoint():
    v0 = [0.0, 0.0, 0.0]
    glPointSize(1)
    glBegin(GL_POINTS)
    glColor3f(1,1,1)
    glVertex3fv(v0)   
    
    glEnd()
    


class MyGLWidget1(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_position = [0.0,0.0]
   
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.planeList = glGenLists(1)
        glNewList(self.planeList, GL_COMPILE)
        # 그리기 코드
        #drawPlane()
        glEndList()

        glEnable(GL_DEPTH_TEST)


    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.01, 100)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for j in range(60):
            for i in range(160):
                
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                gluLookAt(-10,0,0, 0,0,0, 0,0,1)
                glRotatef(self.base_position[1]*100, 0, 1, 0)
                glRotatef(self.base_position[0]*100, 0, 0, 1)
        
                glCallList(self.planeList)
                drawAxes()
    
            ###  Base: 전후 좌우로 이동 가능
    
            # 제어를 통해 옮겨간 위치
            
                 # 몸통을 평면으로 들어올리는 변환
                glTranslatef(RXco[j][i]*0.01, RYco[j][i]*0.01, RZco[j][i]*0.01)
                glPushMatrix()
                glScalef(0.2, 0.2, 0.2)   # 몸통의 크기 변경
                #drawAxes()    
                glColor3f(1,1,1)        
                drawpoint()
                glPopMatrix()
        #glOrtho(-50, 50, -50, 50, -50.0, 50.0)
        
        
class MyGLWidget2(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_position = [0.0,0.0]
   
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.planeList = glGenLists(1)
        glNewList(self.planeList, GL_COMPILE)
        # 그리기 코드
        #drawPlane()
        glEndList()

        glEnable(GL_DEPTH_TEST)


    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.01, 100)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(-25,0,0, 0,0,0, 0,0,1)
        glRotatef(self.base_position[1]*100, 0, 1, 0)
        glRotatef(self.base_position[0]*100, 0, 0, 1)

        glCallList(self.planeList)
        drawAxes()
        
        count=0
        for j in range(0,59):
            #glBegin(GL_TRIANGLE_STRIP)
            glBegin(GL_LINES)
            for i in range(320):
                c=j
                if i%2==1:
                    glColor3f(1,1,1)
                    c+=1
                    glVertex3f(RXco[c][(i-1)/2]*0.01, RYco[c][(i-1)/2]*0.01, RZco[c][(i-1)/2]*0.01)
                else:
                    glColor3f(1,1,1)
                    glVertex3f(RXco[j][i/2]*0.01, RYco[j][i/2]*0.01, RZco[j][i/2]*0.01)
            glEnd()
                
class MyGLWidget3(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_position = [0.0,0.0]
   
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.planeList = glGenLists(1)
        glNewList(self.planeList, GL_COMPILE)
        # 그리기 코드
        #drawPlane()
        glEndList()

        glEnable(GL_DEPTH_TEST)


    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.01, 100)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(-30,0,0, 0,0,0, 0,0,1)
        glRotatef(self.base_position[1]*100, 0, 1, 0)
        glRotatef(self.base_position[0]*100, 0, 0, 1)

        glCallList(self.planeList)
        drawAxes()
        
        count=0
        for j in range(0,59):
            glBegin(GL_TRIANGLE_STRIP)
            #glBegin(GL_LINES)
            for i in range(320):
                c=j
                if i%2==1:
                    glColor3f(0,0,1)
                    c+=1
                    glVertex3f(RXco[c][(i-1)/2]*0.01, RYco[c][(i-1)/2]*0.01, RZco[c][(i-1)/2]*0.01)
                else:
                    glColor3f(0,1,0)
                    glVertex3f(RXco[j][i/2]*0.01, RYco[j][i/2]*0.01, RZco[j][i/2]*0.01)
            glEnd()
                       
                
                
    



class MyWindow(QMainWindow):
    def __init__(self, title=''):
        QMainWindow.__init__(self)
        self.setWindowTitle(title)
        self.glWidget = MyGLWidget2()
        self.setCentralWidget(self.glWidget)

    def keyPressEvent(self, e):
       
        step = 0.1

        if e.key() == Qt.Key.Key_W:
            self.glWidget.base_position[1] -= step
        elif e.key() == Qt.Key.Key_S:
            self.glWidget.base_position[1] += step
        elif e.key() == Qt.Key.Key_A:
            self.glWidget.base_position[0] -= step
        elif e.key() == Qt.Key.Key_D:
            self.glWidget.base_position[0] += step
       
        self.glWidget.update()

def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('변환의 이해')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)