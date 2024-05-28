import os
import collections
import xml.etree.ElementTree as ET


'''
root -> ใช้เพื่อเข้าถึงข้อมูลใน xml file
path_CPF -> path ที่ CPF file ถูกเก็บไว้
''' 
def CPF_dateCheck(root, path_CPF):
    # path_CPF = 'D:\pom\IGSTool_DM\CPFdemo'
   
    dcpf_dict = {}
    image_day = root.find('Dataset_Sources').find('Source_Information').find('Scene_Source').find('IMAGING_DATE').text
    image_time = root.find('Dataset_Sources').find('Source_Information').find('Scene_Source').find('IMAGING_TIME').text
    
    ''' Ex =>>> image_day -> 2021-02-02 / image_time -> 09:24:50.669876  '''
    # print(image_day, image_time)


    # เก็บข้อมูล IMAGING_DATE และ  IMAGING_TIME ของ METADATA.DIM ไว้ใน dcpf_dict
    datetimeCPF = int(image_day.split('-')[0]+image_day.split('-')[1]+image_day.split('-')[2]+image_time.split(':')[0]+image_time.split(':')[1]+image_time.split(':')[2].split('.')[0])
    dcpf_dict[datetimeCPF] = 'ref CPF'
    '''
    image_day -> 20210202092450
    dcpf_dict -> {20210202092450: 'ref CPF'}
    
    '''
    # print(datetimeCPF)
    # print(dcpf_dict)
    # dcpf_list.append(datetimeCPF)

    # for (root_cpf, dirs_cpf, files_cpf) in os.walk(path_CPF, topdown=True):
    #     print(dirs_cpf)
    #     print('===========')

    # for dcpf in os.listdir(path_CPF):

    #  เก็บข้อมูลของ cpf file ที่อยู่ใน path_CPF ในรู้แบบ key=ข้อมูลวันเวลา value=ชื่อ file เพิ่มใน dcpf_dict
    for (_, _, files_cpf) in os.walk(path_CPF, topdown=True):
        for dcpf in files_cpf:
            datecpf = int(dcpf.split('_')[4]+dcpf.split('_')[5].split('.')[0])
            dcpf_dict[datecpf] = dcpf
           
    # เรียงลำดับ key ใน dcpf_dict ใหม่ จะทำให้ วันเวลาของ cpf ที่ต้องใช้อยู่ด้านหน้า วันเวลาของ cpf จาก METADATA.DIM
    dcpf_dict_sorted = collections.OrderedDict(sorted(dcpf_dict.items()))
   

    # dcpf_filename = THEOS_1_20201230_000000_20210101_000000.CPF (ชื่อ ไฟล์ที่ได้จาก cpf)
    dcpf_filename = list(dcpf_dict_sorted.values())[list(dcpf_dict_sorted.keys()).index(datetimeCPF) - 1]
    

    # calibration_filename = CALIBRATION_FILENAME from MATADATA
    calibration_filename = root.find('Data_Strip').find('Sensor_Calibration').find('Calibration').find('CALIBRATION_FILENAME').text

    # print("cal", calibration_filename)

    return dcpf_filename, calibration_filename , dcpf_filename == calibration_filename

# path_metadata = 'D:/MMGS trial/IGSTool_DM/QCDM_directory/UnzipProduct/TH_CAT_200730071347959_1/METADATA.DIM'
# tree = ET.parse(path_metadata)
# root = tree.getroot()
# path_CPF = 'D:/MMGS trial/IGSTool_DM/QCDM_directory/CPFdemo'
# dcpf_filename, calibration_filename , dcpf_filename = CPF_dateCheck(root,path_CPF)
# print(dcpf_filename, calibration_filename , dcpf_filename)


