#!/usr/bin/python
import csv
from random import randint
import random
import re
import unicodedata
import string

def sanitise_name(name):
	name_parts = name.split(' ')
	safe_name = ''

	for name_part in name_parts:
		safe_name = safe_name + remove_accents(name_part) + ' '

	return safe_name.rstrip()

def remove_accents(data):
	return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()

print 'DROP TABLE IF EXISTS moma2'
print 'CREATE TABLE moma2(title VARCHAR(800), artist VARCHAR(100), artist_bio VARCHAR(1000), year INTEGER,'\
        + ' medium VARCHAR(1500), dimensions VARCHAR(2500), credit_line VARCHAR(700), moma_number VARCHAR(20),'\
        + ' classification VARCHAR(100), department VARCHAR(100), date_acquired DATE, curator_approved VARCHAR(1),'\
        + ' object_id  INTEGER, url VARCHAR(200));'

data = []
yoko_count = 0

random.seed()

ind = [randint(0,123919) for p in range(0,10000)] #big buncha random nos

with open('/home/hannah/teaching/270/assignment/Artworks.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

    header = True

    num_rows = 0

    for row in spamreader:
        if header:
            header = False
        else:

            row_vals = []

            for i in range(0, len(row)):
                if (len(row[i])>0):
                    row_vals.append(row[i].decode('ascii', 'ignore'))
                else:
                    row_vals.append("NULL")

            if ',' in row_vals[1]:
                continue

            row_vals[3] = [int(s) for s in row_vals[3].split() if s.isdigit()]

            if len(str(row_vals[3])) == 6:
                if "Yoko Ono" in row_vals[1]: # big up the yoko, man
                    if yoko_count < 10:
                        data.append(row_vals)
                        yoko_count += 1
                elif len(data) < 5000:
                    if num_rows in ind:
                        data.append(row_vals)

            num_rows += 1



for item in data:
    query = 'INSERT INTO moma2 VALUES(\'' + (item[0].replace("'","''")) + '\','+\
            '\'' + (item[1].replace("'","''")) + '\','+\
            '\'' + (item[2].replace("'","''")) + '\','+\
              str(item[3][0]) + ','+\
             '\'' + (item[4].replace("'","''")) + '\','+\
             '\'' + (item[5].replace('\"', 'in').replace('\'','ft')) + '\','+\
             '\'' + (item[6].replace("'","''")) + '\','+\
             '\'' + (item[7].replace("'","''")) + '\','+\
             '\'' + (item[8].replace("'","''")) + '\','+\
             '\'' + (item[9].replace("'","''")) + '\','+\
             '\'' + (item[10].replace("'","''")) + '\','+\
             '\'' + (item[11].replace("'","''")) + '\','+\
             '\'' + (item[12].replace("'","''")) + '\','+\
             '\'' + (item[13].replace("'","''")) + '\');'


    print(query.replace('\'NULL\'','NULL')) #hacky hack hack
