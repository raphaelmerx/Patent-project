# find tables that contain patent_id

import MySQLdb
import csv
import time

begin = time.time()


db = MySQLdb.connect(host="patent.czb2hytpd5lf.us-west-1.rds.amazonaws.com", # your host, usually localhost
                     user="uspto", # your username
                      passwd="ferrisbueller", # your password
                      db="uspto") # name of the data base

# a DictCursor returns dictionaries instead of tuples
cur = db.cursor() 
# cur = db.cursor()

# a dictCursor returns columns in a different order than a tupleCursor
def getColumns(query):
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    columns = ()
    row = cur.fetchone()
    for key in row:
        columns = columns +(key,)
    return columns

def printCsv(query):
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    # get the columns
    columns = ()
    row = cur.fetchone()
    for key in row:
        columns = columns +(key,)
    # begin the csv part
    CSVfile = open('temp.csv','wb')
    wrtr = csv.writer(CSVfile, delimiter=',', quotechar='"')
    # write the column names in csv
    wrtr.writerow(columns)
    # write the first line of data, stored in row
    csvLine=()
    for key in row:
        csvLine = csvLine + (row[key],)
    wrtr.writerow(csvLine)
    # then write the other lines
    for row in cur.fetchall():
        csvLine = ()
        for key in row:
            csvLine = csvLine + (row[key],)
        wrtr.writerow(csvLine)
    # close the CSV
    CSVfile.close()

printCsv("select patent_id,citation_id from uspatentcitation where patent_id!='' and date between '2005-01-01' and '2010-01-01' limit 0,10000")
# query select * from uspatentcitation where patent_id!='';
# 2 columns, patent_id and citation_id

end = time.time()
print end-begin



