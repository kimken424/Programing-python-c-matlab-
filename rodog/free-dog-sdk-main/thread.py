#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 10:17:41 2023

@author: kensMACbook
"""
import sys
import time
import traceback
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from ucl.unitreeConnection import unitreeConnection, HIGH_WIFI_DEFAULTS, HIGH_WIRED_DEFAULTS
from ucl.highCmd import highCmd
from ucl.highState import highState

class Thread1(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.conn = unitreeConnection(HIGH_WIFI_DEFAULTS)
        self.conn.startRecv()
        self.hcmd = highCmd()
        self.hstate = highState()
        # Send empty command to tell the dog the receive port and initialize the connectin
        self.cmd_bytes = self.hcmd.buildCmd(debug=False)
        self.conn.send(self.cmd_bytes)
        time.sleep(0.5) # Some time to collect pakets ;)
        self.data = self.conn.getData()
        self.highstate_imu=[0.0,0.0,0.0]

    def run(self):
        while True:
            time.sleep(0.5)
            data = self.conn.getData()
            for paket in data:
                self.hstate.parseData(paket)
                self.highstate_imu=[self.hstate.imu.quaternion[1],self.hstate.imu.quaternion[2],self.hstate.imu.quaternion[3]]
    
    def value(self):
        self.run()



