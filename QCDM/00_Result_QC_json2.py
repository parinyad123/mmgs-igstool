def ResultJSON(name_zip_file, root, LostLine, Lost_status, AngleTrack, Angle_status, incompletedfiles, unopenfiles, complete_status, 
no_data_list, no_data_status, CPFfile, calibration_filename, validation_status, mode_value, mode_status, QC_status, Timer_QC_process):

    each_QC_status_dict = {"QC1LostLine":Lost_status, "QC2IncidenceAngle":Angle_status, "QC3ProductCompletion":complete_status,
    "QC4NoData":no_data_status, "QC5CloudCoverage": True, "QC6CPFCheck": True, "QC7Mode":mode_status, "QC8PointingError": True}

    # def QCstatus_check(status):
    #     return "PASS" if status == True else "NOT PASS"

    def QCstatus_check(status):
        if status == True:
            return "PASS"
        elif status == False:
            return "NOT PASS "
        else:
            return "ERROR"

    ProductName = str(name_zip_file.split('.')[0])
    SATID = "TH1"
    Mode = root.find('Dataset_Sources').find('Source_Information').find('Scene_Source').find('IMAGING_MODE').text
    # print("Mode = ",Mode)
    Level = root.find('Data_Processing').find('PROCESSING_LEVEL').text
    # print("Level = ",Level)

    dictjson = {
        "ProductName": ProductName,
        "SATID": SATID,
        "Mode": Mode,
        "Level": Level,
        "Status": QCstatus_check(QC_status),
        "FailedQC": [key for key, value in each_QC_status_dict.items() if value == False],
        "QCProcessingTime(sec)": Timer_QC_process,
        "QC1LostLine": {
            "QC1Status": QCstatus_check(Lost_status),
            "NumberLostline": LostLine
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
            "UsedCPF": str(calibration_filename)
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