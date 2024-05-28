import cv2
import numpy as np
from threading import Thread
import queue

# from config import threshold as th

que = queue.Queue()

def storeInQueue(f):
    def wrapper(*args):
        que.put(f(*args))
    return wrapper
@storeInQueue



def Mode_and_Nodata(img, bandNo):

    # Calculate No data
    nodata = (np.count_nonzero(img==1) / np.count_nonzero(img))*100


    # Calculate Mode 
    unique, counts = np.unique(img, return_counts=True)

    if unique[0] == 0:
        unique = unique[1:]
        counts = counts[1:]

    uniq = list(unique)
    count = list(counts)

    for i in range(len(count)):
        if count[i] == np.max(count):
            # ModeList.append(uniq[i])
            mode = np.int32(uniq[i]).item() # ใส่ item() เพื่อเปลี่ยน np.int ให้เป็น int เพราะถ้าเป็น np.int จะสร้าง json ไม่ได้
  
    return nodata, mode, bandNo
    # return nodata, Mode, NodataList, ModeList

def Mode_and_Nodata_multithread(path, th):

    image = cv2.imread(path, cv2.IMREAD_UNCHANGED) # อ่านภาพทั้ง 4 bands
    print("image = ", image) 
    imgs = cv2.split(image) # เก็บข้อมูลแต่ละ band ใน list imgs
    print("imgs =", imgs)
    # ทำการคำนวณ Mode และ Nodata โดยเรียกใช้ function Mode_and_Nodata
    threads = [Thread(target=Mode_and_Nodata, args=(img, bandNo, )) for bandNo, img in enumerate(imgs)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    # result = que.get()

    resultList = []

    while not que.empty():
        result = que.get() # เก็บผลการคำนวณ Mode และ Nodata ไว้ใน result
        resultList.append(result)
    
         # แยกเก็บ ค่า Nodata และ Mode ที่ได้จาก result เก็บใน list
        # Percentage_NoData_list.append(float((result[0])[0]))
        # mode_eachband.append(int((result[1])[0]))
    
    indexResult = [indexRes[2] for indexRes in resultList ]

    sortBandResult = [resultList[indexResult.index(i)] for i in range(len(resultList))]
 
    Percentage_NoData_list = [noData[0] for noData in sortBandResult]
    mode_eachband = [Mode[1] for Mode in sortBandResult]
    bool_Percentage_NoData_list = [True if noData < th.error_no_data else False for noData in Percentage_NoData_list]
    bool_mode_eachband = [True if th.lower_boundary < m < th.upper_boundary else False for m in mode_eachband]

    # Pass by minimum no. of band

    # return Percentage_NoData_list, True if sum(bool_Percentage_NoData_list) >= th.NumberOfBandtopass_NoData else False if len(bool_Percentage_NoData_list) > 1 else bool_Percentage_NoData_list[0], mode_eachband, True if sum(bool_mode_eachband) >= th.NumberOfBandtopass_Mode else False if len(bool_mode_eachband) > 1 else bool_mode_eachband[0]
    
    # Pass by r,g,b
    
    return Percentage_NoData_list, True if sum(bool_Percentage_NoData_list[:3]) >= th.NumberOfBandtopass_NoData else False if len(bool_Percentage_NoData_list) > 1 else bool_Percentage_NoData_list[0], mode_eachband, True if sum(bool_mode_eachband[:3]) >= th.NumberOfBandtopass_Mode else False if len(bool_mode_eachband) > 1 else bool_mode_eachband[0]
        

# path = 'D:\pom\TH_CAT_21020208295419_1_1P_GOBI_20210202\TH_CAT_21020208295419_1/IMAGERY.TIF' # PAN
# path = 'D:\pom\TH_CAT_21020307054506_1_1M_LIBYA1_20210202\TH_CAT_21020307054506_1/IMAGERY.TIF' # MS


# print(Mode_and_Nodata_multithread(path))