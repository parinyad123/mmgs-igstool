# from operator import truediv
from Lost_Line import lostLine
from Incidence_Angle import find_AngleTrack
from CPFdate import CPF_dateCheck
from ProductCompletionV02 import Product_Completed
from Result_QC_json import ResultJSON
from Nodata_Mode import Mode_and_Nodata_multithread
# from config import threshold as th

# from config import path as pth
from config import manage_config as mcf

import xml.etree.ElementTree as ET
import shutil
import os
import zipfile
import json
import time
import rootpath

# ================== Constant =======================
error = {"status": "ERROR", "value": -1}
skip = {"status": "SKIP", "value": -2}


# ===================Config Management===============================

# config_dict = mcf.Config_from_pg(con_pg = True)
# th = mcf.config_nameSpace(config_dict)

# 'True' is config from database but if not 'False'
th = mcf.config_nameSpace(con_pg=False)

# ================== Path Management ==========================
# 1. ทำการเช็ดว่า path ใน path.py มีค่าหรือไม่ โดยใช้ try/except
# 2. check directory ไม่มี จะทำการสร้าง
path = rootpath.detect()
dirpath = path.replace("QCDM","")
qcdmpath = os.path.join(dirpath, "QCDM_directory")

path_productZip = os.path.join(dirpath, "Sample Product")
path_kept_after_QC = os.path.join(qcdmpath, "AfterQCprocess")
path_UnZipProduct = os.path.join(qcdmpath, "UnzipProduct")
path_CPF_demo = os.path.join(qcdmpath, "CPFdemo")
path_Result_QC_json = os.path.join(qcdmpath, "QCResultJSON")
path_databaseini = os.path.join(path, "config", "database.ini")

path_kept_after_QC_pass = os.path.join(path_kept_after_QC, "Pass")
path_kept_after_QC_notpass = os.path.join(path_kept_after_QC, "NotPass")
path_kept_after_QC_error = os.path.join(path_kept_after_QC, "Error")

# ------------------------------------------------------------

#  Path สำหรับเก็บ Zip Product จาก Sippos
try:
    # path_productZip = pth.path_productZip
    path_productZip = path_productZip
except:
    print('Please, specify a directory for keeping unziped product path in config/path.py')

if not os.path.exists(path_productZip):
    print("Not found a Directory for keeping CPF files follow ", path_productZip)
    # os.makedirs(path_productZip)
    # print("Directory ", path_productZip, " Created")
# else:
#     print("Directory ", path_productZip, " already exists")
# ----------------------------------------------------------------------
# print(str(os.listdir(path_productZip)))
# name_zip_frist = str(os.listdir(path_productZip)[0])

# print(name_zip_frist)
# path_first_product = path_productZip + name_zip_frist
# ----------------------------------------------------------------------
# path สำหรับเก็บ directory หลังจากสิ้นสุด QC
try:
    # path_kept_after_QC = pth.path_kept_after_QC
    path_kept_after_QC = path_kept_after_QC
except:
    print('Please, specify a directory for keeping after QC product in config/path.py')

if not os.path.exists(path_kept_after_QC):
    os.makedirs(path_kept_after_QC)
    print("Directory ", path_kept_after_QC, " Created")
# else:
#     print("Directory ", path_kept_after_QC, " already exists")
if not os.path.exists(path_kept_after_QC_pass):
    os.makedirs(path_kept_after_QC_pass)
    print("Directory ", path_kept_after_QC_pass, " Created")

if not os.path.exists(path_kept_after_QC_notpass):
    os.makedirs(path_kept_after_QC_notpass)
    print("Directory ", path_kept_after_QC_notpass, " Created")

if not os.path.exists(path_kept_after_QC_error):
    os.makedirs(path_kept_after_QC_error)
    print("Directory ", path_kept_after_QC_error, " Created")

# Path สำหรับเก็บ Product Unzip
try:
    # path_UnZipProduct = pth.path_UnZipProduct
    path_UnZipProduct = path_UnZipProduct
except:
    print('Please, specify a directory for keeping unzip product in config/path.py')

if not os.path.exists(path_UnZipProduct):
    os.makedirs(path_UnZipProduct)
    print("Directory ", path_UnZipProduct, " Created")
# else:
#     print("Directory ", path_UnZipProduct, " already exists")

# path CPF demo
try:
    # path_CPF_demo = pth.path_CPF_demo
    path_CPF_demo = path_CPF_demo
except:
    print('Please, specify a directory for keeping CPF in config/path.py')

if not os.path.exists(path_CPF_demo):
    print("Not found a Directory for keeping CPF files follow ", path_CPF_demo)
    # os.makedirs(path_CPF_demo)
    # print("Directory ", path_CPF_demo, " Created")
# else:
#     print("Directory ", path_CPF_demo, " already exists")

# path สำหรับ เก็บ result QC json
try:
    # path_Result_QC_json = pth.path_Result_QC_json
    path_Result_QC_json = path_Result_QC_json
except:
    print('Please, specify a directory for keeping json result in config/path.py')

if not os.path.exists(path_Result_QC_json):
    os.makedirs(path_Result_QC_json)
    print("Directory ", path_Result_QC_json, " Created")
# else:
#     print("Directory ", path_Result_QC_json, " already exists")
# ------------------------------------------------------------


# ---------------- Strat for loop process ---------------------

# print("list = ", os.listdir(path_productZip))

for name_zip_file in os.listdir(path_productZip): # os.listdir จะทำการสร้าง list รายชื่อของ zipped product ที่อยู่ใน path_productZip

    # ================== Start Timer ==================== (นับเวลาที่ใช้สำหรับการ process)
    start_milli_sec = int(round(time.time() * 1000))

    # สร้าง path เพื่อเรียก zipped product 
    # path_first_product = path_productZip + name_zip_file
    path_first_product = os.path.join(path_productZip, name_zip_file)
    # ทำการ Unzip Product เข้าไปเก็บไว้ใน path_UnZipProduct
    with zipfile.ZipFile(path_first_product,"r") as zip_ref:
        zip_ref.extractall(path_UnZipProduct)

    # path ข้อมูล metadata และ  imagery ใน directory
    for paths, dirs, files in os.walk(path_UnZipProduct): # os.walk ทำการไล่ดู files และ directory ข้างใน path_UnZipProduct ไปทีละชั้น
        for file in files:

            # ถ้าเจอ file ชื่อ METADATA.DIM และ IMAGERY.TIF ให้ทำการสร้าง path เพื่อใช้เข้าถึง file
            if 'METADATA.DIM' == file: 
                # path_metadata = paths + '/METADATA.DIM'
                path_metadata = os.path.join(paths, "METADATA.DIM")

            elif 'IMAGERY.TIF' == file:
                # path_imagery = paths + '/IMAGERY.TIF'
                path_imagery = os.path.join(paths, "IMAGERY.TIF")


    # =============================================================

    # root for Metadata management
    # สร้าง root เพื่อเข้าถึงข้อมูลใน METADATA.DIM
    tree = ET.parse(path_metadata)
    root = tree.getroot()

    #  QC 01 --->  Lost line 
    # print('------------------------- QC 01 -----------------------------------------')
    if th.PerformQC01_LostLine == True:
        try:
            LostLine_list, LostLine_num, Lost_status = lostLine(root,th) 
        # print(LostLine, Lost_status)
        except:
            print('Lost line QC is Error')
            LostLine_list = error['value']
            LostLine_num = error['value']
            Lost_status = error['status']
    else: LostLine_list = skip['value']; LostLine_num = skip['value']; Lost_status = skip['status']

    #  QC 02 ---> Incidence Angle
    # print('------------------------- QC 02 -----------------------------------------') 
    if th.PerformQC02_IncidenceAngle == True:
        try:
            AngleTrack, Angle_status = find_AngleTrack(root,th)
        # print(AngleTrack, Angle_status)
        except:
            print('Angle track QC is Error')
            AngleTrack = [error['value'], error['value']]
            Angle_status = error['status']
    else: AngleTrack = [skip['value'], skip['value']]; Angle_status = skip['status']
    #  QC03 --->  Product completion
    # print('------------------------- QC 03.1 -----------------------------------------')
    if th.PerformQC03_ProductCompletion == True:
        try:
            incompletedfiles, unopenfiles, complete_status = Product_Completed(path_UnZipProduct)
        # print(incompletedfiles, unopenfiles, complete_status)
        except:
            print('Product completed QC is Error')
            incompletedfiles = [error['value']]
            unopenfiles = [error['value']]
            complete_status = error['status']
    else: incompletedfiles = [skip['value']]; unopenfiles = [skip['value']]; complete_status = skip['status']
    #  QC 04.2 ---> No data value in Image
    # print('------------------------- QC 04.1 -----------------------------------------')
    # try:
    #     no_data_list, no_data_status = no_Data_image(path_imagery)
  
    # except:
    #     print('No data image QC is Error')
    #     no_data_list = 9999
    #     no_data_status = "Error"



    #  QC 05 ---> Cloud coverage
    # print('------------------------- QC 05 -----------------------------------------')
    # cloud_volue, cloud_status = CloudVal(name_unzip_frist)
    # # cloud_volue, cloud_status = CloudVal(address_01)
    # print(cloud_volue, cloud_status)


    #  QC 06 ---> CPF validation
    # print('------------------------- QC 06 -----------------------------------------')
    if th.PerformQC06_CPFcheck == True:
        try:
            CPFfile, calibration_filename, validation_status =  CPF_dateCheck(root, path_CPF_demo)
        # print(CPFfile, calibration_filename, validation_status) 
        except:
            print('CPF data check QC is Error')
            CPFfile = error['value']
            calibration_filename = error['value']
            validation_status = error['status']
    else: CPFfile = skip['value']; calibration_filename = skip['value']; validation_status = skip['status']

    # QC 07 ---> Pointing
    # print('------------------------- QC 07 -----------------------------------------')
    # file sequence 
    # file_name = root.find('Data_Strip').find('Data_Strip_Identification').find('FILE_NAME').text

    # igpst = root.find('Data_Strip').find('Data_Strip_Identification').find('IGPST').text
    # print('sequence = ',file_name)

    # igpst = igpst.split(' ')[0].split('-')
    # igpst = igpst[0]+igpst[1]+igpst[2]
    # print(igpst)
    # print(igpst[0]+igpst[1]+igpst[2])
    # print(igpst.split(' ')[0].split('-'))


    # QC 10 ---> Mode
    # print('------------------------- QC 10 -----------------------------------------')
    # try:
    #     mode_value, mode_status = Mode(path_imagery)
    # except:
    #     print('Calculate mode QC is Error')
    #     mode_value = 9999 
    #     mode_status = "Error"
  


    # QC 4 and 10 ---> No data and Mode
    # print('------------------------- QC 4 and 10 -----------------------------------')
    if th.PerformQC04_NoData == True or th.PerformQC07_Mode == True:
        try:
            no_data_list, no_data_status, mode_value, mode_status = Mode_and_Nodata_multithread(path_imagery, th)
            # print("QC No data: ", no_data_list)
            # print("QC Mode: ", mode_value)
        except:
            print('No data image QC and Calculate mode QC is Error')
            no_data_list = error['value']
            no_data_status = error['status']
            mode_value = error['value']
            mode_status = error['status']
        
    if th.PerformQC04_NoData == False:
        no_data_list = skip['value']; no_data_status = skip['status']
    if th.PerformQC07_Mode == False:
        mode_value = skip['value']; mode_status = skip['status']

    # print('------------------------- QC Finish -----------------------------------')

    # print(path_UnZipProduct)
    # Check QC ทุก critiria ผ่านหรือไม่
    try:
        # QC_status = Lost_status and Angle_status and complete_status and no_data_status and mode_status and validation_status
        # QC status for move zip product
        QC_status_list = [Lost_status, Angle_status, complete_status, no_data_status, mode_status, validation_status]
        QC_status = True

        # เปลี่ยน SKIP status ให้เป็น True
        # for i in range(len(QC_status_list)):
        #     if QC_status_list[i] == "SKIP":
        #         QC_status_list[i] = True
        
        # # print("QC = ", QC_status_list)
        # for ii in QC_status_list:
        #     if ii == "ERROR":
        #         QC_status = "ERROR"
        #         break
        #     else:
        #         QC_status= QC_status and ii
        
        for i in QC_status_list:
            if i == "ERROR":
                QC_status = "ERROR"
                break
            else:
                if i == "SKIP":
                    i = True
                QC_status = i and QC_status
    
            
    except:
        print('QC status is Error')

    try:
        if QC_status == True:
            # path_move = path_kept_after_QC + '/Pass/'
            path_move = path_kept_after_QC_pass
        elif QC_status == False:
            # path_move = path_kept_after_QC + '/NotPass/'
            path_move =  path_kept_after_QC_notpass
        elif QC_status == "ERROR": 
            # path_move = path_kept_after_QC + '/Error/'
            path_move = path_kept_after_QC_error
    except:
        print('Not found path for keeping product after QC process')

    # ทำการย้าย zipped product ไปตาม path ที่ขึ้นอยู่กับ QC_status
    shutil.move(path_first_product, path_move, copy_function = shutil.copytree)

    # ================== End Timer ====================
    end_milli_sec = int(round(time.time() * 1000))

    Timer_QC_process = (end_milli_sec - start_milli_sec)/1000
    # print(Timer_QC_process, "sec")

    # ===============  Result Format JSON =========================
    try:
        dict_json, ProductName = ResultJSON(name_zip_file, root, LostLine_list, LostLine_num, Lost_status, AngleTrack, Angle_status, incompletedfiles, unopenfiles, complete_status, 
        no_data_list, no_data_status, CPFfile, calibration_filename, validation_status, mode_value, mode_status, QC_status, Timer_QC_process, path_imagery)
        
    except:
        print('Cannot build JSON format')

    try:
        ProductJsonName = "".join((ProductName,'.json'))
        path_ProductJsonName = os.path.join(path_Result_QC_json, ProductJsonName)
        # print("path_ProductJsonName ==> ",path_ProductJsonName)
        with open(path_ProductJsonName, "w") as outfile:
            json.dump(dict_json, outfile)
    except:
        print('Cannot write JSON file')
        

    # ============= remove all files and directory in path_UnZipProduct ==========================


    # import time
    # time.sleep(10)

    # ลบ files และ directory ทั้งหมด ใน UnZipProduct directory
    try:
        for file in os.listdir(path_UnZipProduct):
            path_rm = os.path.join(path_UnZipProduct, file) 
            
        #     try:
        #         shutil.rmtree(path_rm)
        #     except OSError:
        #         os.remove(path_rm)
            try:
                shutil.rmtree(path_rm)
            except OSError:
                os.remove(path_rm)
    except:
        print('Cannot remove unzip product')

    print('Success-----------', Timer_QC_process)




    # # shutil.rmtree(path_first_product)

    # shutil.move(path_move+name_zip_frist, path_productZip, copy_function = shutil.copytree)

