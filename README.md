## DFLM Video Filter
### About
This software applies image filter on each frame within a video and a filtered video is reconstructed of .ome.tiff 
extension.
### How to use:
The code can be run through [main.py](main.py) and all the dependencies and libraries are included in the conda environment.

The paramaters of the filters (eg. standard deviation and kernal size) can be modified through [settings.json](settings.json).
### Notes:
- A Virtual Environment is needed for running the code.
The environment is located in the [requirements.txt](requirements.txt) file.
- If you face issues due to numpy being incompatible with bioformats, uninstall numpy then reinstall numpy==1.26.4 instead.
- Only .avi video extension have been tested using this code. Data has to be of this extension to be used by the code.
