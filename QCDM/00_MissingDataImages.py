import cv2
import numpy as np

def find_missing_pixels(img_file):
    nodata_eachband = []
    ratio_nodata = 0.00002
    img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
    # print(img.shape)
    # calculate to find amount of 0 values
    if (img.ndim == 2):
        row, col = img.shape
        elem_num = row*col
        missing_pixels_num = np.count_nonzero(img==0)
        nodata_eachband.append(missing_pixels_num/elem_num)
    elif (img.ndim == 3):
        row, col,_  = img.shape
        elem_num = row*col
        # print('size = ', elem_num)
        for i in range(4):
            missing_pixels_num = np.count_nonzero(img[:,:,i]==0)
            nodata_eachband.append(missing_pixels_num/elem_num)
    else:
        nodata_eachband=[1]
    #     print('Error Band of image')

    
    return nodata_eachband, np.any(np.array(nodata_eachband) < ratio_nodata)

    # missing_pixels_num = np.count_nonzero(np.isnan(img))
    # missing_pixels_num = np.count_nonzero(img==0)
    # print('missing data = ',missing_pixels_num)
    # nonmissing_pixels_num = np.count_nonzero(~np.isnan(img))
    # nonmissing_pixels_num = np.count_nonzero(img!=0)
    # print('Missing pixels = ',missing_pixels_num,'Non missing', img_pixels_num)
    # print(missing_pixels_num + nonmissing_pixels_num)
    # return missing_pixels_num/elem_num
    # return missing_pixels_num/(missing_pixels_num + nonmissing_pixels_num)