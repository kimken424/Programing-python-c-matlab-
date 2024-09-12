#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 23:03:04 2023

@author: kensMACbook
"""

from ucl.common import byte_print, decode_version, decode_sn, getVoltage, pretty_print_obj, lib_version
from ucl.highCmd import highCmd
from ucl.highState import highState
from ucl.lowCmd import lowCmd
from ucl.unitreeConnection import unitreeConnection, HIGH_WIFI_DEFAULTS, HIGH_WIRED_DEFAULTS
from ucl.enums import MotorModeHigh, GaitType
from ucl.complex import motorCmd
import time
import math
import numpy as np

class move:
    def __init__(self):
        self.conn = unitreeConnection(HIGH_WIFI_DEFAULTS)
        self.conn.startRecv()
        self.hcmd = highCmd()
        self.hstate = highState()
        # Send empty command to tell the dog the receive port and initialize the connectin
        self.cmd_bytes = self.hcmd.buildCmd(debug=False)
        self.conn.send(self.cmd_bytes)
        time.sleep(0.5) # Some time to collect pakets ;)
        self.data = self.conn.getData()
        
        
    def forward(self):
        self.hcmd.mode = MotorModeHigh.VEL_WALK
        self.hcmd.velocity = [0.3, 0]
        self.cmd_bytes = self.hcmd.buildCmd(debug=False)
        self.conn.send(self.cmd_bytes)
        
    def back(self):
        self.hcmd.mode = MotorModeHigh.VEL_WALK
        self.hcmd.velocity = [-0.3, 0]
        self.cmd_bytes = self.hcmd.buildCmd(debug=False)
        self.conn.send(self.cmd_bytes)
    
    def right(self):
        self.hcmd.mode = MotorModeHigh.VEL_WALK
        self.hcmd.velocity = [0, -0.15]
        self.cmd_bytes = self.hcmd.buildCmd(debug=False)
        self.conn.send(self.cmd_bytes)
        
    def left(self):
        self.hcmd.mode = MotorModeHigh.VEL_WALK
        self.hcmd.velocity = [0, 0.15]
        self.cmd_bytes = self.hcmd.buildCmd(debug=False)
        self.conn.send(self.cmd_bytes)
        
    def turnRight(self):
        self.hcmd.mode = MotorModeHigh.VEL_WALK
        self.hcmd.yawSpeed = np.deg2rad(-30)
        self.cmd_bytes = self.hcmd.buildCmd(debug=False)
        self.conn.send(self.cmd_bytes)
    
    def turnLeft(self):
        self.hcmd.mode = MotorModeHigh.VEL_WALK
        self.hcmd.yawSpeed = np.deg2rad(30)
        self.cmd_bytes = self.hcmd.buildCmd(debug=False)
        self.conn.send(self.cmd_bytes)
     
    def forcestand(self):
        self.hcmd.mode = MotorModeHigh.FORCE_STAND