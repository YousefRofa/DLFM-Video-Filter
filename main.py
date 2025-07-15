from pathlib import Path
import tifffile as tiff
from filters import *
from tkinter import filedialog

filePath = filedialog.askopenfilename()
cap = cv2.VideoCapture(filePath)

frames = []
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    else:
        h = frame.shape[0]
        w = frame.shape[1]
        gray = cv2.cvtColor(frame.astype("uint16"), cv2.COLOR_BGR2GRAY)
        lg_filtered = cv2.filter2D(gray, -1, lg_filter())  # avg_filter or lg_filter()
        avg_filtered = cv2.filter2D(gray, -1, avg_filter())
        diff_avg_1, diff_avg_2 = diff_avg_filter()
        diff_avg_filtered = np.subtract(cv2.filter2D(gray.astype("int16"), -1, diff_avg_1), cv2.filter2D(gray.astype('int16'), -1, diff_avg_2))
        diff_gauss_1, diff_gauss_2 = diff_gauss_filter()
        diff_gauss_filtered = np.subtract(cv2.filter2D(gray.astype("int16"), -1, diff_gauss_1), cv2.filter2D(gray.astype("int16"), -1, diff_gauss_2))
        median_filtered = median_filter(gray)
        filtered_total =[]
        TopNames = cv2.cvtColor(tiff.imread("TopNames.tif"), cv2.COLOR_BGR2GRAY)
        BottomNames = cv2.cvtColor(tiff.imread("BottomNames.tif"), cv2.COLOR_BGR2GRAY)
        for i in TopNames:
            filtered_total.append(i)
        for i in range(len(lg_filtered)):
            filtered_total.append(np.concatenate((gray[i], lg_filtered[i], avg_filtered[i])))
        for i in BottomNames:
            filtered_total.append(i)
        for i in range(len(diff_avg_filtered)):
            filtered_total.append(np.concatenate((diff_avg_filtered[i], median_filtered[i], diff_gauss_filtered[i])))
        frames.append(filtered_total)
cap.release()
cv2.destroyAllWindows()
stack = np.stack(frames)

tiff.imwrite(
    Path(filePath).stem+"_FILTERS"+".ome.tiff",
    stack,
    photometric='minisblack',
    metadata={'axes': 'TYX'},# T: time, YX: spatial
    ome=True
)

# video.release()
input("Filtered Video Created.")