from configparser import ConfigParser
import os 
from config import path as p

# print(path.path_databaseini)

def pgconfig(filename=p.path_databaseini, section='postgresql'):
    if not os.path.exists(filename):
        print("Not found ", filename)

    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

