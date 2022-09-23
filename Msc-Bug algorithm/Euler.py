# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 12:00:05 2022

@author: Admin
"""

from math import pi

class EulerAngles:
    def __init__(self, roll=0.0, pitch=0.0, yaw=0.0):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

        self.rad_to_deg = 180.0 / pi
        self.deg_to_rad = 1.0 / self.rad_to_deg
