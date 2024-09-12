from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import *
import pyvista as pv
import stltest as st

import math
import numpy as np

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

class MeshLoader:
    def __init__(self):
        self.nV = 0 # 정점의 개수
        self.nF = 0 # 면의 개수
        self.vertexBuffer = None # 정점 버퍼
        self.idxBuffer = None # 면을 구성하는 정점 인덱스 버퍼

    def loadData(self, filename):
        with open(filename, 'rt') as inputfile:
            self.nV = int(next(inputfile))
            self.vertexBuffer = np.zeros(shape = (self.nV*3, ), dtype=float)
            for i in range(self.nV):
                verts = next(inputfile).split()
                self.vertexBuffer[i*3:i*3+3] = verts
            
            coordMin = self.vertexBuffer.min()
            coordMax = self.vertexBuffer.max()
            scale = max([coordMin, coordMax], key=abs)
            self.vertexBuffer /= scale

            self.nF = int(next(inputfile))
            self.idxBuffer = np.zeros(shape=(self.nF*3, ), dtype=int)
            for i in range(self.nF):
                idx = next(inputfile).split()
                self.idxBuffer[i*3: i*3+3] = idx[1:4]

            print(self.idxBuffer)

    def draw(self):

        glBegin(GL_TRIANGLES)
        for i in range(self.nF):
            verts = self.idxBuffer[i*3: i*3+3]
            glColor3fv(  ( self.vertexBuffer[verts[0]*3 : verts[0]*3 +3] + np.array([1])) / 2.0 )
            glVertex3fv( self.vertexBuffer[verts[0]*3 : verts[0]*3 +3] )
            glColor3fv(  ( self.vertexBuffer[verts[1]*3 : verts[1]*3 +3] + np.array([1])) / 2.0 )
            glVertex3fv( self.vertexBuffer[verts[1]*3 : verts[1]*3 +3] )
            glColor3fv(  ( self.vertexBuffer[verts[2]*3 : verts[2]*3 +3] + np.array([1])) / 2.0 )
            glVertex3fv( self.vertexBuffer[verts[2]*3 : verts[2]*3 +3] )
        glEnd()

        glColor3f(0,0,1)
        for i in range(self.nF):
            verts = self.idxBuffer[i*3: i*3+3]
            glBegin(GL_LINE_LOOP)
            glVertex3fv( self.vertexBuffer[verts[0]*3 : verts[0]*3 +3] )
            glVertex3fv( self.vertexBuffer[verts[1]*3 : verts[1]*3 +3] )
            glVertex3fv( self.vertexBuffer[verts[2]*3 : verts[2]*3 +3] )
            glEnd()

class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)

        self.meshLoader = MeshLoader() # 메시 로더 생성
        self.meshLoader.loadData('./cow.txt')
        self.model1=st.loader()
        self.model1.load_stl(os.path.abspath('')+'/trunk4.STL')
        
        glPointSize(2)


    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.01, 100)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(2,2,2, 0,0,0, 0,1,0)

        drawAxes()
        self.scene=st.draw_scene()
        self.scene.draw()

        #self.meshLoader.draw()


class MyWindow(QMainWindow):
    def __init__(self, title=''):
        QMainWindow.__init__(self)
        self.setWindowTitle(title)
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('메시 읽기')
    window.setFixedSize(1000, 1000)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)