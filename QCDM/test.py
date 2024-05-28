# import cv2
# import sys
# sys.path.append("./config")
from config import manage_config as mcf
# from  
# from config import config as c
from config import path as pth

import shutil
import rootpath
import os.path
from sys import platform


if platform == "linux" or platform == "linux2" or platform == "darwin":
    slash = '/'

elif platform == "win32":
    slash = "{}"
print('================================')

print(pth.path_CPF_demo)

# params = c.config()
config_dict = mcf.Config_from_pg(con_pg = False)
th = mcf.config_nameSpace(config_dict)

print(th.lower_boundary)


path = rootpath.detect()
print(path, slash, "love")
print(os.path.join(path.replace("QCDM",""), "love"))

# dirpath = os.path.replace("QCDM","")
dirpath = rootpath.detect().replace("QCDM","")
qcdmpath = os.path.join(dirpath, "QCDM_directory")

path_productZip = os.path.join(dirpath, "Sample Product")
path_kept_after_QC = os.path.join(qcdmpath, "AfterQCprocess")
path_UnZipProduct = os.path.join(qcdmpath, "UnzipProduct")
path_CPF_demo = os.path.join(qcdmpath, "CPFdemo")
path_Result_QC_json = os.path.join(qcdmpath, "QCResultJSON")
path_databaseini = os.path.join(path, "config", "database.ini")

print("===> ", path_productZip)
print("===> ", path_kept_after_QC)
print("===> ", path_UnZipProduct)
print("===> ", path_CPF_demo)
print("===> ", path_Result_QC_json)
print("===> ", path_databaseini)

ProductName = "TH1_20190618_091213_PAN_1A_W1307"
ProductJsonName = "".join((ProductName,'.json'))
print(ProductJsonName)

print(len([4,5,6]))
rmpath = os.path.join(path_UnZipProduct, "testdir")
print(rmpath)
shutil.rmtree(rmpath)