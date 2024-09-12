#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 16:03:09 2023

@author: kensMACbook
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
csv_test = pd.read_csv('1frame.csv', header=None)

plt.pcolor(csv_test, cmap = 'jet')

plt.colorbar()
plt.clim(0,3000)
theta_x = np.arange(38, -38, -0.475)
theta_y = np.arange(16,-16,-0.54)
X=np.cos(np.deg2rad(theta_x))
Y=np.sin(np.deg2rad(theta_x))
Z=np.sin(np.deg2rad(theta_y))
K=np.cos(np.deg2rad(theta_y))
#depth=csv_test.to_numpy()
depth=np.transpose(csv_test)
Kco=np.repeat(K,160)
#Kco=Kco.reshape((60,160))
Kco=np.transpose(Kco.reshape((60,160)))
Xco=np.repeat(X,60)
Xco=Xco.reshape((160,60))
RXco=Kco*Xco*depth
Yco=np.repeat(Y,60)
Yco=Yco.reshape((160,60))
RYco=Kco*Yco*depth
Zco=np.repeat(Z,160)
#Zco=Zco.reshape((60,160))
RZco=np.transpose(Zco.reshape((60,160))
RZco = RZco*depth
