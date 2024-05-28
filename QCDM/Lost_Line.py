from sys import path
# from config import threshold as th
# import xml.etree.ElementTree as ET

def lostLine (root, th):

    lostline_list = []
    try:
    # find number of lost line
        # lostline_num = len(root.find('Data_Strip').find('Sensor_Calibration').find('Calibration').find('Band_Parameters').find('Bad_Line_List'))
        losts = root.find('Data_Strip').find('Sensor_Calibration').find('Calibration').find('Band_Parameters').find('Bad_Line_List')
        lostline_num = len(losts)  
        # print(lostline_num)
        for r in losts:
            # print(r.find('BL_INDEX').text)
            lostline_list.append(r.find('BL_INDEX').text)
    except:
        lostline_num = 0 

    return lostline_list, lostline_num, lostline_num <= th.LostLine_limit


# path = 'D:\pom\TH1_20210122_042918_MS_1A_64088_Scene1_sipros\TH1_20210122_042918_MS_1A_64088_Scene1_W0000'
# path_metadata = path+'/'+"METADATA.DIM"

# tree = ET.parse(path_metadata)
# root = tree.getroot()

# print(lostLine(root))