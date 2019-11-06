"""
Author:Teresa Jarriel

Use: Takes a time series of singularity index response images as input and produces a sliding window plot depicting how the CRV is changing over time
Notes:
- files must be in .TIF format, it can be case senstitive to .tif vs. .TIF
- when image time series is being used, file names must be in chronological order

"""

import cv2
import numpy as np
from numpy import *
from rivamap import singularity_index, georef
import glob, os
import matplotlib.pyplot as plt

#this code calculates CRV sliding window time series for multiple window sizes from 15 to 60 in 5 image increments. If only one window size is desired, change range
for x in range(15,60,5):
    # User needs to adjust base directory.
    # Folder with chronologically ordered singularity index .TIF imagery should appear next to base_dir
    base_dir = '/home/engrla/rivamap/SIESD related/SlidingWindow/demo_PSIs'
    psi_images = sorted(glob.glob(base_dir + '*/*.TIF'))
    
    step_size=x
    number_sections=(len(psi_images)-step_size)+1
    print ('number of singularity index images: ')
    print(len(psi_images))
    print ('number of windows: ')
    print(number_sections)
    print ('step size: ')
    print(x)

    #initialize psi_array
    I1 = cv2.imread(psi_images[0], cv2.IMREAD_UNCHANGED)
    psi_array = np.zeros((step_size, I1.shape[0], I1.shape[1]), dtype='float32')

    averages=[]

    xval=list(range(0,number_sections))

    for i in range(0,number_sections,1):
        for j in range(i,i+step_size):
            psi = cv2.imread(psi_images[j], cv2.IMREAD_UNCHANGED)
            psi_array[j-i,:,:] = psi
        channel_var=np.var(psi_array,axis=0)
        avg=np.mean(channel_var)
        print('window '+str(i))
        averages.append(avg)
        psi_array = np.zeros((step_size, I1.shape[0], I1.shape[1]), dtype='float32')
        
    plt.scatter(xval,averages)    
    plt.xlabel('window number')
    plt.ylabel('average CRV for window images')
    plt.savefig(os.path.join("demo_slidingwindow_"+str(x)+".TIF"))
    plt.savefig(os.path.join("demo_slidingwindow_"+str(x)+".eps"), format='eps')
    plt.close('all')

print('completed')
