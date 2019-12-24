# Steps to import CONAFOR fires
#   1. Download from agency at https://datos.gob.mx/busca/dataset/incendios-forestales
#   2. Convert file to proper CSV
#   3. In EXCEL, perform data cleaning, specially check for weird incomplete rows, lat/lon sign errors, date errors, crazy sizes, mispelled causes and states
#   4. If CAUSE is not NATURALES, then its HUMAN. These years have amazingly detailed cause info..fix that below
#   5. Use DMS to DD converted to get the right lat/lon format
#   6. Convert the dates to a date object
#   7. Convert size to acres while accounting for commas on big boy fires


import csv
import datetime
import psycopg2
postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
cur = postgres_conn.cursor()

# Grados = Degrees
# Minutos = Minutes
# Segundos = Decimal Seconds

def dms_to_dd(d, m, s):
    dd = float(d) + float(m)/60 + float(s)/3600
    return dd


acres = 0
fires = 0
with open('data/Mexico/csvs/Serie_historica_anual_incendios_(2017).csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        
        SOURCE = 'CONAFOR-FDB'  # good 
        COUNTRY = 'MEXICO'  # good
        LATITUDE = dms_to_dd(row[2], row[3], row[4])   # yeet
        LONGITUDE = float("-" + str(dms_to_dd(row[5], row[6], row[7])))  #yeet
        START_DATE = datetime.datetime.strptime(row[14], '%m/%d/%y').date()  # look good
        END_DATE = datetime.datetime.strptime(row[15], '%m/%d/%y').date()  # okay
        FIRE_NAME = row[11]  # just take whatever this says
        STATE = row[9]  #ok
        try:
            SIZE =  float(row[28]) * 2.4710538  #probably
        except ValueError:
            SIZE = float(row[28].replace(',', '')) * 2.4710538 
        CAUSE = row[12] # ye
        if CAUSE.upper() == 'NATURALES':
            CAUSE = 'LIGHTNING'
        else:
            CAUSE = 'HUMAN'

        row_dict = {
            'SOURCE': SOURCE,
            'COUNTRY': COUNTRY,
            'NAME': FIRE_NAME.upper(),
            'SIZE_AC': SIZE,
            'START_DATE': START_DATE,
            'END_DATE': END_DATE,
            'CAUSE': CAUSE,
            'STATE': STATE.upper(),
            'LATITUDE': LATITUDE,
            'LONGITUDE': LONGITUDE
        }
        acres += row_dict['SIZE_AC']
        if row_dict['STATE'] == 'Querétaro'.upper():
            fires += 1
    print(fires)
        # cur.execute(""" INSERT INTO fires (source, country, name, size_ac, start_date, end_date, cause, state, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (row_dict['SOURCE'], row_dict['COUNTRY'], row_dict['NAME'], row_dict['SIZE_AC'], row_dict['START_DATE'], row_dict['END_DATE'], row_dict['CAUSE'], row_dict['STATE'], row_dict['LATITUDE'], row_dict['LONGITUDE']))
cur.close()
postgres_conn.commit()        
print(acres, fires)