import math
import statistics

import cv2
import numpy as np
import json

with open("settings.json") as f:
    data = json.load(f)
    lg_sd = data["Lowered Gaussian"]["Standard Deviation"]
    avg_kernal = data["Averaging Filter"]["Kernal"]
    diff_avg_kernal1 = data["Difference in Average Filter"]["Kernal1"]
    diff_avg_kernal2 = data["Difference in Average Filter"]["Kernal2"]
    diff_gauss_sd1 = data["Difference in Gaussian Filter"]["Standard Deviation1"]
    diff_gauss_sd2 = data["Difference in Gaussian Filter"]["Standard Deviation2"]
    median_kernal = data["Median Filter"]["Kernal"]
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

# Difference in Gaussian Filter
def diff_gauss_filter(sd1 =diff_gauss_sd1, sd2 =diff_gauss_sd2):
    k_size1 = 1 + 2*math.ceil(3*sd1)
    k_size2 = 1 + 2*math.ceil(3*sd2)
    a1 = 1/(2*math.pi*sd1*sd1)
    a2 = 1/(2*math.pi*sd2*sd2)
    gauss_filter1 = np.zeros([k_size1, k_size1])
    gauss_filter2 = np.zeros([k_size2, k_size2])
    for i in range(k_size1):
        for j in range(k_size1):
            gauss_filter1[i, j] = a1*math.e**(-((i-int(k_size1/2))**2+(j-int(k_size1/2))**2)/(2*sd1**2))
    for i in range(k_size2):
        for j in range(k_size2):
            gauss_filter2[i, j] = a2 * math.e ** (
                        -((i - int(k_size2 / 2)) ** 2 + (j - int(k_size2 / 2)) ** 2) / (2 * sd2 ** 2))
    return gauss_filter1, gauss_filter2

# Average Filter
def avg_filter(kernal=avg_kernal):
    avg_filter = np.zeros([kernal, kernal])
    for i in range(kernal):
        for j in range(kernal):
            avg_filter[i][j] = 1/(kernal*kernal)
    return avg_filter

# Difference in Average Filter
def diff_avg_filter(kernal1 =diff_avg_kernal1, kernal2 =diff_avg_kernal2):
    filter1 = np.zeros([kernal1, kernal1])
    filter2 = np.zeros([kernal2, kernal2])
    for i in range(kernal1):
        for j in range(kernal1):
            filter1[i][j] = 1/(kernal1*kernal1)
    for i in range(kernal2):
        for j in range(kernal2):
            filter2[i][j] = 1/(kernal2*kernal2)
    return filter1, filter2

# Median Filter
def median_filter(image, kernal=median_kernal):
    # Due to computation time, we will use opencv's version of a median filter. But here is the written code
    # -----------------------------------------------------------
    # filtered_image = np.zeros([image.shape[0], image.shape[1]])
    # for i in range(image.shape[0]):
    #     for j in range(image.shape[1]):
    #         median_filter_list = []
    #         for k in range(-int(kernal/2), int(kernal/2)+1):
    #             for l in range(-int(kernal/2), int(kernal/2)+1):
    #                 try:
    #                     median_filter_list.append(image[i+k][j+l])
    #                 except:
    #                     pass
    #         filtered_image[i][j] = statistics.median(median_filter_list)
    # return filtered_image
    return cv2.medianBlur(image, kernal)