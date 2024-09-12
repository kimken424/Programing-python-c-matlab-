#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 16:03:20 2023

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


class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_position = [-1.0,-2.0]

        self.arm1Y = 0 # 팔 1의 방향
        self.arm1X = 120 # 팔 1의 굽힘
        self.arm1Z = 0

        self.arm2X = 90 # 팔 2의 굽힘        
   
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.planeList = glGenLists(1)
        glNewList(self.planeList, GL_COMPILE)
        # 그리기 코드
        glEndList()

        glEnable(GL_DEPTH_TEST)
        

    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.01, 100)

    def paintGL(self):
        self.camdegree = np.deg2rad(self.arm1Y)
        #gluLookAt(7,7,10, 0,0,0, 0,1,0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(7*math.cos(self.camdegree),7,7*math.sin(self.camdegree), 0,0,0, 0,1,0)
        
        glCallList(self.planeList)
        drawAxes()

        ###  Base: 전후 좌우로 이동 가능

        # 제어를 통해 옮겨간 위치
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(0, 0.5, 0)# 몸통을 평면으로 들어올리는 변환
        glRotatef(self.arm1Z, 0, 0, 1)# 몸통을 회전
        glPushMatrix()
        glScalef(0.5, 0.5, 1)   # 몸통의 크기 변경
        drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ### 팔 1을 그리자
        # 몸통의 반 만큼 올린다 (중심이 관절 위치)
        glTranslatef(0, 0, 0)  
        ### 회전 적용
        #glRotatef(self.arm1Y, 0, 1, 0)
        glRotatef(self.arm1X, 1, 0, 0)
        # 팔의 아래쪽을 관절에 맞추기 (팔의 길이 반 만큼 올리기)
        glTranslatef(0, 2, 0)
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        drawAxes()
        glColor3f(1,1,0)
        drawCube()
        glPopMatrix()

        ### 팔 2를 그리자
        # 부모인 팔 1의 반 만큼 위로 이동
        glTranslatef(0, 1.5, 0)
        # 회전 실시
        glRotatef(self.arm2X, 1, 0, 0)
        # 팔 2의 끝을 관절로 옮김 (팔 2의 반 이동)
        glTranslatef(0, 1.5, 0)
        # 팔 2: 높이가 3인 육면체
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        drawAxes()
        glColor3f(0,1,1)
        drawCube()
        glPopMatrix()
#==================================================================
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(7*math.cos(self.camdegree),7,7*math.sin(self.camdegree), 0,0,0, 0,1,0)
        
        glCallList(self.planeList)
        drawAxes()

        ###  Base: 전후 좌우로 이동 가능

        # 제어를 통해 옮겨간 위치
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(2, 0.5, 0) # 몸통을 평면으로 들어올리는 변환
        glRotatef(self.arm1Z, 0, 0, 1)# 몸통을 회전
        glPushMatrix()
        glScalef(0.5, 0.5, 1)   # 몸통의 크기 변경
        drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ### 팔 1을 그리자
        # 몸통의 반 만큼 올린다 (중심이 관절 위치)
        glTranslatef(0, 0, 0)  
        ### 회전 적용
        #glRotatef(self.arm1Y, 0, 1, 0)
        glRotatef(self.arm1X, 1, 0, 0)
        # 팔의 아래쪽을 관절에 맞추기 (팔의 길이 반 만큼 올리기)
        glTranslatef(0, 2, 0)
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        drawAxes()
        glColor3f(1,1,0)
        drawCube()
        glPopMatrix()
        
        glTranslatef(0, 1.5, 0)
        # 회전 실시
        glRotatef(self.arm2X, 1, 0, 0)
        # 팔 2의 끝을 관절로 옮김 (팔 2의 반 이동)
        glTranslatef(0, 1.5, 0)
        # 팔 2: 높이가 3인 육면체
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        drawAxes()
        glColor3f(0,1,1)
        drawCube()
        glPopMatrix()

#==================================================================
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(7*math.cos(self.camdegree),7,7*math.sin(self.camdegree), 0,0,0, 0,1,0)
        
        glCallList(self.planeList)
        drawAxes()

        ###  Base: 전후 좌우로 이동 가능

        # 제어를 통해 옮겨간 위치
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(2, 0.5, 4) # 몸통을 평면으로 들어올리는 변환
        glRotatef(self.arm1Z, 0, 0, 1)# 몸통을 회전
        glPushMatrix()
        glScalef(0.5, 0.5, 1)   # 몸통의 크기 변경
        drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ### 팔 1을 그리자
        # 몸통의 반 만큼 올린다 (중심이 관절 위치)
        glTranslatef(0, 0, 0)  
        ### 회전 적용
        #glRotatef(self.arm1Y, 0, 1, 0)
        glRotatef(self.arm1X, 1, 0, 0)
        # 팔의 아래쪽을 관절에 맞추기 (팔의 길이 반 만큼 올리기)
        glTranslatef(0, 2, 0)
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        drawAxes()
        glColor3f(1,1,0)
        drawCube()
        glPopMatrix()
        
        glTranslatef(0, 1.5, 0)
        # 회전 실시
        glRotatef(self.arm2X, 1, 0, 0)
        # 팔 2의 끝을 관절로 옮김 (팔 2의 반 이동)
        glTranslatef(0, 1.5, 0)
        # 팔 2: 높이가 3인 육면체
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        drawAxes()
        glColor3f(0,1,1)
        drawCube()
        glPopMatrix()
        
#==================================================================
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(7*math.cos(self.camdegree),7,7*math.sin(self.camdegree), 0,0,0, 0,1,0)
        
        glCallList(self.planeList)
        drawAxes()

        ###  Base: 전후 좌우로 이동 가능

        # 제어를 통해 옮겨간 위치
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(0, 0.5, 4) # 몸통을 평면으로 들어올리는 변환
        glRotatef(self.arm1Z, 0, 0, 1)# 몸통을 회전
        glPushMatrix()
        glScalef(0.5, 0.5, 1)   # 몸통의 크기 변경
        drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ### 팔 1을 그리자
        # 몸통의 반 만큼 올린다 (중심이 관절 위치)
        glTranslatef(0, 0, 0)  
        ### 회전 적용
        #glRotatef(self.arm1Y, 0, 1, 0)
        glRotatef(self.arm1X, 1, 0, 0)
        # 팔의 아래쪽을 관절에 맞추기 (팔의 길이 반 만큼 올리기)
        glTranslatef(0, 2, 0)
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        drawAxes()
        glColor3f(1,1,0)
        drawCube()
        glPopMatrix()
        
        ### 팔 2를 그리자
        # 부모인 팔 1의 반 만큼 위로 이동
        glTranslatef(0, 1.5, 0)
        # 회전 실시
        glRotatef(self.arm2X, 1, 0, 0)
        # 팔 2의 끝을 관절로 옮김 (팔 2의 반 이동)
        glTranslatef(0, 1.5, 0)
        # 팔 2: 높이가 3인 육면체
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        drawAxes()
        glColor3f(0,1,1)
        drawCube()
        glPopMatrix()

#==================================================================
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(7*math.cos(self.camdegree),7,7*math.sin(self.camdegree), 0,0,0, 0,1,0)

        glCallList(self.planeList)
        drawAxes()

        ###  Base: 전후 좌우로 이동 가능

        # 제어를 통해 옮겨간 위치
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(1, 0.5, 2) # 몸통을 평면으로 들어올리는 변환
        #glRotatef(self.arm1Z, 0, 0, 1)# 몸통을 회전
        glPushMatrix()
        glScalef(2, 2, 5)   # 몸통의 크기 변경
        drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        
        
class MyWindow(QMainWindow):
    def __init__(self, title=''):
        QMainWindow.__init__(self)
        self.setWindowTitle(title)
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

    def keyPressEvent(self, e):
       
        step = 0.1
        angle_step = 1

        if e.key() == Qt.Key.Key_W:
            self.glWidget.base_position[1] -= step
        elif e.key() == Qt.Key.Key_S:
            self.glWidget.base_position[1] += step
        elif e.key() == Qt.Key.Key_A:
            self.glWidget.base_position[0] -= step
        elif e.key() == Qt.Key.Key_D:
            self.glWidget.base_position[0] += step
        elif e.key() == Qt.Key.Key_Q:
            self.glWidget.arm1Y += angle_step
        elif e.key() == Qt.Key.Key_E:
            self.glWidget.arm1Y -= angle_step
        elif e.key() == Qt.Key.Key_1:
            self.glWidget.arm1X += angle_step
        elif e.key() == Qt.Key.Key_2:
            self.glWidget.arm1X -= angle_step
        elif e.key() == Qt.Key.Key_3:
            self.glWidget.arm2X += angle_step
        elif e.key() == Qt.Key.Key_4:
            self.glWidget.arm2X -= angle_step
       
        self.glWidget.update()

def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('변환의 이해')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)