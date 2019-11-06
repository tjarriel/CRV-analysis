"""
Author:Teresa Jarriel

Use: Takes a time series of singularity index response images as input and produces a Channelized Response Variance (CRV) map, a directionalized Variance map, and a slope map

Notes:
- files must be in .TIF format, it can be case senstitive to .tif vs. .TIF
- when image time series is being used, file names must be in chronological order

"""

import cv2
import numpy as np
from rivamap import singularity_index, georef
import glob, os
from scipy.stats import linregress
from scipy.misc import imsave
from PIL import Image


# User needs to adjust base directory.
# Folder with chronologically ordered singularity index .TIF imagery should appear next to base_dir1
base_dir1 = "/home/engrla/rivamap/SIESD related/PSIs"
psi_images = sorted(glob.glob(base_dir1 + '*/*.TIF'))

#prints files to be used. make sure they are in the order desired
for infile in psi_images:
    print infile
  
#initialize psi_array
I1 = cv2.imread(psi_images[0], cv2.IMREAD_UNCHANGED)
psi_array = np.zeros((len(psi_images), I1.shape[0], I1.shape[1]), dtype='float32')
#load the georeference data here if using Landsat imagery
#gm = georef.loadGeoMetadata('1994_psi_geotagged_WholeDelta_19940118_19940317_LT5.TIF')

# channel response change
for i in range(0, len(psi_images)):
    #prints row out of total to display progress. Can be #'d out if desired
    print(i)
    psi = cv2.imread(psi_images[i], cv2.IMREAD_UNCHANGED)
    psi_array[i,:,:] = psi


print('calculating CRV magnitude...')
CRV = np.var(psi_array, axis=0)
cv2.imwrite("Demo_CRV.TIF", cv2.normalize(CRV, None,0, 255, cv2.NORM_MINMAX))
#optional other file format
#np.save("Demo_CRV.npy", CRV)


print('LINES BEST FIT')
print('calculating size')
[sx,sy,sz]=psi_array.shape
xx=np.arange(sx)
print('swapping axes')
swapped=np.swapaxes(psi_array,0,2)
[xxx,yyy,zzz]=swapped.shape
print('calculating slopes')
slopes=np.zeros((xxx,yyy))
print(xxx)
print(yyy)
for i in range(0,xxx):#should be 0 to xxx for full image
    print(i)
    for j in range(0,yyy): #should be 0 to yyy for full image
        zero_axis=swapped[i,j,:]
        slo=np.polyfit(xx,zero_axis,1)
        slopes[i,j]=slo[0]
swapped_slopes=np.swapaxes(slopes,0,1)

cv2.imwrite("Demo_CRV_slopes.TIF", cv2.normalize(swapped_slopes, None, 0, 255, cv2.NORM_MINMAX))
#optional other file format
#np.save("Demo_CRV_slopes.npy", swapped_slopes)

#determining if the slope is positive or negative based on threshold 
print('generating positive negative map')
[xlen,ylen]=swapped_slopes.shape
print(xlen)
print(ylen)
for i in range (0,xlen):
    for j in range (0,ylen):
        if swapped_slopes[i,j]>.2:
            swapped_slopes[i,j]=1
        elif swapped_slopes[i,j]<-.2:
            swapped_slopes[i,j]=-1
        else:
            swapped_slopes[i,j]=swapped_slopes[i,j]

#multiplying magnitude of CRV by positive or negative one to get directionalized CRV
CRV_directionalized=np.multiply(CRV, swapped_slopes)
cv2.imwrite("Demo_CRV_directionalized.TIF", cv2.normalize(CRV_directionalized, None, 0, 255, cv2.NORM_MINMAX))

#if using Landsat with georeference available, here is the code to save as geoTiff
#georef.saveAsGeoTiff(gm, CRV, os.path.join(base_dir, "Demo_CRV_geotagged.TIF"))
#georef.saveAsGeoTiff(gm, swapped_slopes, os.path.join(base_dir, "Demo_CRV_slopes_geotagged.TIF"))
#georef.saveAsGeoTiff(gm, CRV_directionalized, os.path.join(base_dir, "Demo_CRV_directionalized_geotagged.TIF"))

#printing some simple statistics for each image so 0-255 scale can be converted to real values
CRV_min=np.amin(CRV)
CRV_max=np.amax(CRV)
CRV_mean=np.mean(CRV)
print('CRV minimum is:')
print(CRV_min)
print('CRV maximum is:')
print(CRV_max)
print('CRV mean is:')
print(CRV_mean)

minimum=np.amin(swapped_slopes)
maximum=np.amax(swapped_slopes)
mean=np.mean(swapped_slopes)
print('slope minimum is:')
print(minimum)
print('slope maximum is:')
print(maximum)
print('slope mean is: ')
print(mean)

varianceXslopesign_min=np.amin(CRV_directionalized)
varianceXslopesign_max=np.amax(CRV_directionalized)
varianceXslopesign_mean=np.mean(CRV_directionalized)
print('CRV_directionalized minimum is:')
print(varianceXslopesign_min)
print('CRV_directionalized maximum is:')
print(varianceXslopesign_max)
print('CRV_directionalized mean is:')
print(varianceXslopesign_mean)

print('completed')
