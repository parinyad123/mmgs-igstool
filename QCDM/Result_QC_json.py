import cv2

def ResultJSON(name_zip_file, root, LostLine_list, LostLine_num, Lost_status, AngleTrack, Angle_status, incompletedfiles, unopenfiles, complete_status, 
no_data_list, no_data_status, CPFfile, calibration_filename, validation_status, mode_value, mode_status, QC_status, Timer_QC_process, path_imagery):

    each_QC_status_dict = {"QC1LostLine":Lost_status, "QC2IncidenceAngle":Angle_status, "QC3ProductCompletion":complete_status,
    "QC4NoData":no_data_status, "QC5CloudCoverage": True, "QC6CPFCheck": validation_status, "QC7Mode":mode_status, "QC8PointingError": True}

    def QCstatus_check(status): return "PASS" if status == True else "NOT PASS" if status == False else status

    ProductName = str(name_zip_file.split('.')[0])
    SATID = "TH1"

    def ModeImg(root,path_imagery):
        Mode = root.find('Dataset_Sources').find('Source_Information').find('Scene_Source').find('IMAGING_MODE').text
        if Mode == "PAN":
            image = cv2.imread(path_imagery, cv2.IMREAD_UNCHANGED) # อ่านภาพทั้ง 4 bands
            Mode = "PANSHARP" if len(image.shape) == 3 else "PAN"
        return Mode

    # print("Mode = ",Mode)
    Level = root.find('Data_Processing').find('PROCESSING_LEVEL').text
    # print("Level = ",Level)

    dictjson = {
        "ProductName": ProductName,
        "SATID": SATID,
        "Mode": ModeImg(root,path_imagery),
        "Level": Level,
        "Status": QCstatus_check(QC_status),
        "FailedQC": [key for key, value in each_QC_status_dict.items() if (value == False or value == "ERROR")],
        "QCProcessingTime(sec)": Timer_QC_process,
        "QC1LostLine": {
            "QC1Status": QCstatus_check(Lost_status),
            "AmountLostline": LostLine_num,
            "LostlineNo.": LostLine_list
        },
        "QC2IncidenceAngle": {
            "QC2Status": QCstatus_check(Angle_status),
            "VIEWING_ANGLE_ALONG_TRACK": AngleTrack[0],
            "VIEWING_ANGLE_ACROSS_TRACK": AngleTrack[1]
        },
        "QC3ProductCompletion": {
            "QC3Status":QCstatus_check(complete_status),
            "MissingFile": incompletedfiles,
            "ErrorFile": unopenfiles
        },
        "QC4NoData": {
            "QC4Status": QCstatus_check(no_data_status),
            "NoDataPixelPercentage": no_data_list
        },
        "QC5CloudCoverage": {
            "QC5Status":"PASS",
            "CloudCoverPercentage": 9999
        },
        "QC6CPFCheck": {
            "QC6Status": QCstatus_check(validation_status),
            "UsedCPF_from_product": str(calibration_filename),
            "CPF_from_Store": str(CPFfile)
        },
        "QC7Mode": {
            "QC7Status":QCstatus_check(mode_status),
            "Mode": mode_value
        },
        "QC8PointingError": {
            "QC8Status":"PASS",
            "PointingError": 9999
        }
    }

    return dictjson, ProductName