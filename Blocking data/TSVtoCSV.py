import csv

with open('links.tsv','rb') as tsvin, open('links.csv', 'wb') as csvout:
    tsvin = csv.reader(tsvin, delimiter='\t')
    csvout = csv.writer(csvout)
    for row in tsvin:
        csvout.writerow(row)
