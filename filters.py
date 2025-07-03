import math
import numpy as np
import json

with open("settings.json") as f:
    data = json.load(f)
    lg_sd = data["Lowered Gaussian"]["Standard Deviation"]
    avg_kernal = data["Averaging Filter"]["Kernal"]
f.close()

# Lowered Gaussian Filter
def lg_filter(sd=lg_sd):
    total = 0
    k_size = 1 + 2*math.ceil(3*sd)
    a = 1/(2*math.pi*sd*sd)
    g_filter = np.zeros([k_size, k_size])
    for i in range(k_size):
        for j in range(k_size):
            g_filter[i, j] = a*math.e**(-((i-int(k_size/2))**2+(j-int(k_size/2))**2)/(2*sd**2))
            total += g_filter[i, j]
    b = total/(k_size*k_size)
    lg_filter = g_filter - b
    return lg_filter

# Average filter
def avg_filter(kernal=avg_kernal):
    avg_filter = np.zeros([kernal, kernal])
    for i in range(kernal):
        for j in range(kernal):
            avg_filter[i][j] = 1/(kernal*kernal)