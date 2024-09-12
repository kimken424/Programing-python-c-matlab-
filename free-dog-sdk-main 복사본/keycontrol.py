#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 12:26:19 2023

@author: kensMACbook
"""

import time
from robmotion import move

class keyinput:
    def __init__(self):
        self.cmdkey=''
        self.n=0
        self.initime=0
        self.ntime=0
        self.m=move()
        
    def run(self,keyinput):
        self.n=0
        self.cmdkey=keyinput
        
        while True:
            time.sleep(0.002)
            if self.n==len(self.cmdkey):
                break
            elif self.cmdkey[self.n]=='w':
                self.pressW()
                self.n +=1
            elif self.cmdkey[self.n]=='a':
                self.pressA()
                self.n +=1
            elif self.cmdkey[self.n]=='s':
                self.pressS()
                self.n +=1
            elif self.cmdkey[self.n]=='d':
                self.pressD()
                self.n +=1
            elif self.cmdkey[self.n]=='q':
                self.pressQ()
                self.n +=1
            elif self.cmdkey[self.n]=='e':
                self.pressE()
                self.n +=1
            elif self.cmdkey[self.n]=='x':
                self.pressX()
                self.n +=1
            else:
                self.n +=1
                
    def pressW(self):
        print('w')
        self.initime=time.time()+2
        while True:
            self.m.forward()
            self.ntime=time.time()
            if self.ntime>=self.initime:
                break
        
    def pressA(self):
        print('a')
        self.initime=time.time()+2
        while True:
            self.m.left()
            self.ntime=time.time()
            if self.ntime>=self.initime:
                break
        
    def pressS(self):
        print('s')
        self.initime=time.time()+2
        while True:
            self.m.back()
            self.ntime=time.time()
            if self.ntime>=self.initime:
                break
        
    def pressD(self):
        print('d')
        self.initime=time.time()+2
        while True:
            self.m.right()
            self.ntime=time.time()
            if self.ntime>=self.initime:
                break
            
    def pressQ(self):
        print('q')
        self.initime=time.time()+2
        while True:
            self.m.turnLeft()
            self.ntime=time.time()
            if self.ntime>=self.initime:
                break
            
    def pressE(self):
        print('e')
        self.initime=time.time()+2
        while True:
            self.m.turnRight()
            self.ntime=time.time()
            if self.ntime>=self.initime:
                break
                
    def pressX(self):
        print('x')
        self.m.forcestand()
            
    
        