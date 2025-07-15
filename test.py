import math
import statistics
import tifffile as tiff
import cv2
import numpy as np
import json
list = np.zeros(384, dtype=np.uint8)
list[128] = 255
list[129] = 255
list[256] = 255
list[257] = 255
print(list)
tiff.imwrite(
    "black.tiff",
[list for i in range(20)],
)