# from pandas.core.frame import DataFrame
from types import SimpleNamespace as sn
import psycopg2
import pandas as pd
from config import pgconfig



def Config_from_pg(con_pg):

    if con_pg == True:
        params = pgconfig.pgconfig()
        try:
            con = psycopg2.connect(user=params['user'],
                                            password=params['password'],
                                            host=params['host'],
                                            port=params['port'],
                                            database=params['database'])

            cur = con.cursor()
            # print("Sucess connect")
            # print(cur)
            
        except:
            print("Cannot Connect to config database")


            # sql = "select * from config_qc c where id = 1"
        sql = "select * from config_qc where generate_time = (select max(generate_time) from config_qc)"
        # print(sql)
        # print(cur)
        # cur.execute(sql)

      

        # rows = cur.fetchall()
        # for row in rows:
           
        #     print(row)

        dfsql = pd.read_sql(sql, con)
        # print(dfsql.to_string(index=False))
        # print("angle_limit = ",(dfsql['angle_limit']).to_string(index=False))
        # print("generate_time = ", dfsql['generate_time'][0])
        # print("column = ", dfsql.columns)

        con.commit()
        cur.close()
        con.close()

        config_dict = {
    
            #  QC 01 --->  Lost line
            "PerformQC01_LostLine": dfsql['performqc01_lostline'][0],
            "LostLine_limit": dfsql['lostline_limit'][0],

            #  QC 02 ---> Incidence Angle
            "PerformQC02_IncidenceAngle": dfsql['performqc02_incidenceangle'][0],
            "Angle_limit": dfsql['angle_limit'][0],

            #  QC03 --->  Product completion
            "PerformQC03_ProductCompletion": dfsql['performqc03_productcompletion'][0],

            # QC 04.2 ---> No data value in Image
            "PerformQC04_NoData": dfsql['performqc04_nodata'][0],
            "NumberOfBandtopass_NoData": dfsql['numberofbandtopass_nodata'][0],
            "error_no_data": dfsql['error_no_data'][0],

            # QC 05 --> Cloud Coverage
            "PerformQC05_CloudCover": dfsql['performqc05_cloudcover'][0],
            "max_cloud_percent": dfsql['max_cloud_percent'][0],

            # QC 06 ---> CPF validation
            "PerformQC06_CPFcheck": dfsql['performqc06_cpfcheck'][0],

            # QC 07 --> Mode
            "PerformQC07_Mode": dfsql['performqc07_mode'][0],
            "NumberOfBandtopass_Mode": dfsql['numberofbandtopass_mode'][0],
            "lower_boundary": dfsql['lower_boundary'][0],
            "upper_boundary": dfsql['upper_boundary'][0],

            # QC08 --> Pointing Error
            "PerformQC08_PointingError": dfsql['performqc08_pointingerror'][0]
            }

    else:
        config_dict = {
    
            #  QC 01 --->  Lost line
            "PerformQC01_LostLine": True,
            "LostLine_limit": 8,

            #  QC 02 ---> Incidence Angle
            "PerformQC02_IncidenceAngle": True,
            "Angle_limit": 40,

            #  QC03 --->  Product completion
            "PerformQC03_ProductCompletion": True,

            # QC 04.2 ---> No data value in Image
            "PerformQC04_NoData": True,
            "NumberOfBandtopass_NoData": 4,
            "error_no_data": 5,

            # QC 05 --> Cloud Coverage
            "PerformQC05_CloudCover": False,
            "max_cloud_percent": 50,

            # QC 06 ---> CPF validation
            "PerformQC06_CPFcheck": True,

            # QC 07 --> Mode
            "PerformQC07_Mode": True,
            "NumberOfBandtopass_Mode": 3,
            "lower_boundary": 50,
            "upper_boundary": 200,

            # QC08 --> Pointing Error
            "PerformQC08_PointingError": False
            }
    return config_dict


# print(Config_from_pg(con_pg = True))
# cf = Config_from_pg()

# print("config = ", cf['PerformQC08_PointingError'])
# print("totol = " , cf)

def config_nameSpace(con_pg):
    config_dict = Config_from_pg(con_pg)
    th = sn(**config_dict)
    return th
