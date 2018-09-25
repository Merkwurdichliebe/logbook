"""
This script takes a CSV file exported from an Excel flight logbook
and adds its contents into a sqlite3 database.

It expects this format:
date,planetype,planename,roleonboard,nature,landings,time,notes
e.g.
19/03/2011,DR400-120,F-GKRD,EP,LFPL Local,4,01:04,Some notes

It then populates the 'Vols' table with links to the 'Avions' table.
Only used once to convert my entire Excel worksheet to the sqlite3 format.

(c) 2018 Tal Zana
"""

import csv
import sqlite3 as lite

con = lite.connect('logbook.db')
cur = con.cursor()

# Using 'with', changes are automatically committed.
# Otherwise, we would have to commit them manually. 
with con:
    with open('logbook.csv', mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        for row in csvreader:
            elements = row[0].split('/')
            # print(elements)
            date = elements[2] + '-' + elements[1] + '-' + elements[0]
            cur.execute("SELECT Avion_ID FROM Avions WHERE Immat=?", (row[2],))
            avion_id = cur.fetchone()[0]
            if row[3] == 'P':
                cdb = 1
            else:
                cdb = 0
            
            nature = row[4]

            if row[5] == '':
                atterrissages = 0
            else:
                atterrissages = int(row[5])

            temps = int(row[6][:2]) * 60 + int(row[6][3:])

            notes = row[7]

            # print('{:15} {:10} {:10} {:4} {:20} {:4} {:8} {:20}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            # print('{:15} {:10} {:10} {:5} {:21} {:11} {:11}'.format(date, avion_id, cdb, nature, atterrissages, temps, notes))

            cur.execute("INSERT INTO Vols VALUES(Null, ?, ?, ?, ?, ?, ?, ?)", (date, avion_id, cdb, nature, atterrissages, temps, notes))