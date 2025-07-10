import rawpy
import os
import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import tifffile as tiff
from tqdm import tqdm                  # progress bar
import numpy as np
# filePath = filedialog.askopenfilename()
from tkinter import filedialog


# filePath = filedialog.askopenfilename()
filePath = "data.avi"
cap = cv2.VideoCapture(filePath)

frames = []
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    else:
        frames.append(frame)

cap.release()
cv2.destroyAllWindows()

stack = np.stack(frames)

tiff.imwrite(
    Path(filePath).stem+"_"+".ome.tiff",
    stack,
    photometric='minisblack', # T: time, YX: spatial
    ome=True
)

# video.release()
input("Filtered Video Created.")