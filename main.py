import javabridge, bioformats as bf            # frame access
import cv2                           # filtering + re-encode
import tifffile as tiff
import numpy as np
from pathlib import Path
from tkinter import filedialog
from filters import *

filePath = filedialog.askopenfilename()
FPS  = 60                                      # fallback if metadata absent

# --- spin up the Bio-Formats JVM ----------
javabridge.start_vm(class_path=bf.JARS)
rdr = bf.ImageReader(filePath)

frame_count = rdr.rdr.getImageCount()
w, h = rdr.rdr.getSizeX(), rdr.rdr.getSizeY()

# --- set up AVI writer --------------------
fourcc = cv2.VideoWriter_fourcc(*"DIVX")

#Asking user for filter
choice = input("Please Choose a filter number: \n1) Lowered Gaussian\n2) Averaging Filter\n ..... ")
if choice == "1":
    filter = lg_filter()
    filterName = "LoweredGaussian"
elif choice == "2":
    filter = avg_filter()
    filterName = "AveragingFilter"

# --- streaming loop (no huge RAM spike) ---
frames = []
for t in range(frame_count):
    frame = rdr.read(t=t, z=0, c=0, rescale=False)      # NumPy array
    filtered = cv2.filter2D(frame, -1, filter)  # avg_filter or lg_filter()
    frames.append(filtered)

stack = np.stack(frames)

tiff.imwrite(
    Path(filePath).stem+"_"+filterName+".ome.tiff",
    stack,
    photometric='minisblack',
    metadata={'axes': 'TYX'},  # T: time, YX: spatial
    ome=True
)

# video.release()
javabridge.kill_vm()
input("Filtered Video Created.")