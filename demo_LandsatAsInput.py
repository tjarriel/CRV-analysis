"""
Author: The base for this code was originally written by Leo Isikdogan (http://www.isikdogan.com/) and was edited further by Teresa Jarriel

Use: Creates singularity index response maps from Landsat imagery (using bands 3 and 6 of Landst 8, bands 2 and 5 for Landsat 5 and 7).

Notes:
- files must be in .tif format, it can be case senstitive to .tif vs. .TIF
- when image time series is being used, file names must be in chronological order
- tif files must have georeference
- to adjust threshold for centerline delineation (to make more or fewer channels appear) go to delineate.py thresholdCenterlines function and adjust input thresholds
"""

import cv2
import numpy as np
from rivamap import singularity_index, delineate, preprocess, georef, visualization
import glob, os

# User needs to adjust base directories.
# Folder with band 3 (or band 2) imagery should appear next to base_dir1
# Folder with band 6 (or band 5) imagery should appear next to base_dir2

print("compiling directory 1")
base_dir1 = "/home/engrla/rivamap/GBMD related/GBMD_images_new/B3s_part"
B3s = sorted(glob.glob(base_dir1 + '*/*.tif'))
print("compiling directory 2")
base_dir2 = "/home/engrla/rivamap/GBMD related/GBMD_images_new/B6s_part"
B6s = sorted(glob.glob(base_dir2 + '*/*.tif'))

#prints names of files being used
for infile in B3s:
    print infile
for infile in B6s:
    print infile

# channel response change
for i in range(0, len(B3s)):
    print(i)
    filters = singularity_index.SingularityIndexFilters()
    B3 = cv2.imread(B3s[i], cv2.IMREAD_UNCHANGED)
    B6 = cv2.imread(B6s[i], cv2.IMREAD_UNCHANGED)
    I1 = preprocess.mndwi(B3, B6)
    psi, widthMap, orient = singularity_index.applyMMSI(I1, filters, togglePolarity = False)
    nms = delineate.extractCenterlines(orient, psi)    
    centerlines = delineate.thresholdCenterlines(nms)
    
    print("creating files")
    gm = georef.loadGeoMetadata(B3s[i])
    base = os.path.basename(B3s[i])
    georef.exportCSVfile(centerlines, widthMap, gm, str(base)+ "_geo_points.csv")

    psi=preprocess.contrastStretch(psi)
    psi=preprocess.double2im(psi,'uint16')
    georef.saveAsGeoTiff(gm,psi, str(base) + "_geo_psi.TIF")
    
    mndwi=preprocess.contrastStretch(I1)
    mndwi=preprocess.double2im(mndwi,'uint16')
    georef.saveAsGeoTiff(gm,mndwi, str(base) + "_geo_mndwi.TIF")
    #optional other file format
    #cv2.imwrite("MNDWI.TIF", cv2.normalize(I1, None, 0, 255, cv2.NORM_MINMAX))

    centerlines=preprocess.contrastStretch(centerlines)
    centerlines=preprocess.double2im(centerlines,'uint16')
    georef.saveAsGeoTiff(gm,centerlines, str(base) + "_geo_centerlines.TIF")
    #optional other file format
    #cv2.imwrite("centerlines.TIF", centerlines.astype(int)*255)
print('completed')
