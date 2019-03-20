import sqlite3
import pandas as pd
import os
import csv

'''
Input= Filename of the csv dataset without .csv extension
Output= Returns the filename of the database
'''
def csv_to_sqlite(filename):
    df = pd.read_csv('files/'+filename+'.csv')
    dirName = 'database/'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")
    else:
        print("Directory ", dirName, " already exists")
    sqlite_file = dirName+'staging.db'
    conn = sqlite3.connect(sqlite_file)
    df.to_sql('staging', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    return sqlite_file

'''
Input= The indicator code as in the World Bank Data Set, the list of columns that are to be retrieved,filename
Output= The directory in which the file is saved

Note: The filneame is not a required field and is set to 'staging.csv' by default

The function allows the user to execute the select query on the staging database
'''
def select_query(indicator_code, column_list, filename = 'staging.csv'):
    dirName = 'files/csv/'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")
    else:
        print("Directory ", dirName, " already exists")

    column_str=''
    for id, column in enumerate(column_list):
        if id!=len(column_list)-1:
            column_str += '`'+str(column)+'`' + ', '
        else:
            column_str += '`'+str(column)+'`'

    with open('files/csv/'+filename, 'w+') as write_file:
        conn = sqlite3.connect('database/staging.db')
        cursor = conn.cursor()
        select_query = 'select '+column_str+' from staging where `Indicator Code`=? order by `Country Name`'
        param_code_tuple=(indicator_code, )
        data = cursor.execute(select_query, param_code_tuple)
        names = [description[0] for description in data.description]
        writer = csv.writer(write_file)
        writer.writerow(names)
        writer.writerows(data)
        conn.commit()
        conn.close()

'''
Input= The SQL query to be executed, filename
Output= The directory in which the file is saved

Note: The filneame is not a required field and is set to 'staging.csv' by default

The function allows the user to execute any SQL query on the staging database
'''
def exec_query(query, filename = 'staging.csv'):
    dirName = 'files/csv/'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")
    else:
        print("Directory ", dirName, " already exists")

    with open('files/csv/'+filename, 'w+') as write_file:
        conn = sqlite3.connect('database/staging.db')
        cursor = conn.cursor()
        select_query = query
        data = cursor.execute(select_query)
        return list(data)
        names = [description[0] for description in data.description]
        writer = csv.writer(write_file)
        writer.writerow(names)
        writer.writerows(data)
        conn.commit()
        conn.close()

'''
To return the column 
'''