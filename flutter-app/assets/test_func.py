#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 22:34:14 2021

@author: amirmoradi
"""
from scipy import signal
import numpy as np

def hassan():
    sos = signal.butter(N=30,
            Wn=np.array([10, 20]) / (4000 / 2),
            btype='bandpass',
            analog=False,
            output='sos')
    return sos

def amir():
    b = hassan()
    return b