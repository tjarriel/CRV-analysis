"""
Author: The base for this code was originally written by Leo Isikdogan (http://www.isikdogan.com/) and was edited further by Teresa Jarriel

Use: Creates singularity index response maps from pre-processed imager where water features have been emphasized using RGB_to_GrayscaleWaterEmphasized matlab code provided.

Notes:
- files must be in .TIF format, it can be case senstitive to .tif vs. .TIF
- when image time series is being used, file names must be in chronological order
- to adjust threshold for centerline delineation (to make more or fewer channels appear) go to delineate.py thresholdCenterlines function and adjust input thresholds

"""

import cv2
from rivamap import singularity_index, delineate, preprocess, georef, visualization
import glob, os
import numpy as np

# User needs to adjust base directory.
# Folder with water emphasized .TIF imagery should appear next to base_dir1
print("compiling directory 1")
base_dir1 = "/home/engrla/rivamap/SIESD related/demoImages"
Gray_images = sorted(glob.glob(base_dir1 + '*/*.TIF'))

for i in range(0, len(Gray_images)):
    print ('working on image ' + str(i+1) + ' out of ' + str(len(Gray_images))) 
    I1 = cv2.imread(Gray_images[i], cv2.IMREAD_GRAYSCALE)
    # Create the filters that are needed to compute the singularity index
    filters = singularity_index.SingularityIndexFilters()

    # Compute the modified multiscale singularity index
    psi, widthMap, orient = singularity_index.applyMMSI(I1, filters)

    # Extract channel centerlines
    nms = delineate.extractCenterlines(orient, psi)
    centerlines = delineate.thresholdCenterlines(nms)

    # Generate a raster map of the extracted channels
    raster = visualization.generateRasterMap(centerlines, orient, widthMap)

    inputFile=Gray_images[i]
    filename_w_ext = os.path.basename(inputFile)

    # Save the images that are created at the intermediate steps
    cv2.imwrite(os.path.join(filename_w_ext+"_MNDWI"), cv2.normalize(I1, None, 0, 255, cv2.NORM_MINMAX))
    cv2.imwrite(os.path.join(filename_w_ext+"_PSI.TIF"), cv2.normalize(psi, None, 0, 255, cv2.NORM_MINMAX))
    cv2.imwrite(os.path.join(filename_w_ext+"_Centerlines.TIF"), centerlines.astype(int)*255)
    cv2.imwrite(os.path.join(filename_w_ext+"_RasterMap"),cv2.normalize(raster, None, 0, 255, cv2.NORM_MINMAX))
    #optional other file format
    #np.save(os.path.join(filename_w_ext+"_PSI.npy"), psi)

    print i

print('completed')
