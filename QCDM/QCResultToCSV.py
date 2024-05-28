import json
import glob
import os
import operator
from pandas import DataFrame
import pandas as pd
from config import path as pth

path = pth.path_Result_QC_json
list_of_QCresult = glob.glob(path+'*')
# list_of_QCresult = glob.glob('D:\MMGS trial\IGSTool_DM\QCDM\QCResultsJSON\*')
columnsName = ['ProductName', 'SATID', 'Mode', 'Level', 'Status', 'FailedQC','QCProcessingTime(sec)', 'QC1Status', 'NumberLostline', 'QC2Status', 'ViewingAngleAlongTrack', 'ViewingAngleAcrossTrack', 'QC3Status', 'MissingFile', 'ErrorFile', 'QC4Status', 'NoDataPercentage', 'QC5Status', 'CloudCoverPercentage', 'QC6Status', 'UsedCPF', 'QC7Status', 'Mode', 'QC8Status', 'PointingError']

df = pd.DataFrame(columns=columnsName)
appended_df = []
for i in list_of_QCresult:
    #      data = json.load(open(i))
    data = json.load(open(i))
    key_list = list(data)
    j = 7
    subdata = {}
    while j < 15:
        subdata.update(data[key_list[j]])
        j += 1
    data_to_fill = list(range(22))
    data_to_fill[0:7] = list(data.values())[0:7]
    data_to_fill[7:] = list(subdata.values())
    tempdf = pd.DataFrame([data_to_fill], columns=columnsName)
    appended_df.append(tempdf)

maindf = pd.concat(appended_df)
print(maindf)
maindf.to_csv('QCTestResult.csv', index=False)
