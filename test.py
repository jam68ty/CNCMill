# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:37:51 2021

@author: 張嘉真
"""
import numpy as np
import pandas as pd 
import os
import glob

path = './d' 
files = glob.glob(path + "/*.csv")

li = []

for filename in files:
    df = pd.read_csv(filename)
    for col in df.columns:
        
    #li.append(df)

#df = pd.concat(li)