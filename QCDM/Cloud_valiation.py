import psycopg2
import pandas as pd
from config import db_config as con

def CloudVal(directory_name):
    con = psycopg2.connect(user=con.user,
                                    password=con.password,
                                    host=con.host,
                                    port=con.port,
                                    database=con.database)
    
    cur = con.cursor()


    sql = "select cloud_coverage from theos1_scene where id = (select sceneid from theos1_production where productname = \'{}\')".format(directory_name)

    cur.execute(sql)
    cloud_value = float(pd.read_sql(sql, con)['cloud_coverage'][0])
    # print(cloud_vulue)
    # print(type(cloud_vulue['cloud_coverage'][0]))

    # print(type(((cur.fetchall())[0])[0]))


    con.commit()
    cur.close()
    con.close()
    return cloud_value, cloud_value<15