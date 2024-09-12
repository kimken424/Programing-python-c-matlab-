#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 10:47:51 2023

@author: kensMACbook
"""

from ucl.common import byte_print, decode_version, decode_sn, getVoltage, pretty_print_obj, lib_version,float_to_hex, hex_to_float, encryptCrc, genCrc, byte_print
from ucl.highCmd import highCmd
from ucl.highState_b1 import highState
from ucl.lowCmd import lowCmd
from ucl.unitreeConnection import unitreeConnection, HIGH_WIFI_DEFAULTS, HIGH_WIRED_DEFAULTS
from ucl.enums import MotorModeHigh, GaitType
from ucl.complex_b1 import motorCmd, motorState


#highstate_b1에 있는 바이트에 있는 값 비교함 
with open("./packet/highstate1.bin", "rb") as f:
    data = f.read()
    for b in data:
        print(b)

hstate = highState()
hstate.parseData(data)

head = hex(int.from_bytes(data[0:2], byteorder='little'))
head = hex(int.from_bytes(data[0:2], byteorder='big'))
version = data[12:20]
print(version)
position = [hex_to_float(data[946:950]), hex_to_float(data[950:954]), hex_to_float(data[954:958])]
print(hstate.position())
print(hstate.imu)
data[946]
data[947]
#한 바이트 밀림
hex(data[947])
motorstate=[]
i=0

motorstate.append(hstate.dataToMotorState(data[(i*38)+75:(i*38)+38+75]))
hstate.imu.gyro
hstate.imu.gyroscope
hstate.imu.quaternion