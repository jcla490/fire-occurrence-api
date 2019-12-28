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
import re

postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
cur = postgres_conn.cursor()

# Grados = Degrees
# Minutos = Minutes
# Segundos = Decimal Seconds

def coord_fixer(latlon_pair):
    coordinate_pair = []
    for coord in latlon_pair:
        coord.lstrip()
        coord = re.split("""[°´¨]""", coord)
        coordinate_pair.append(coord)
    return coordinate_pair

def dms_to_dd(d, m, s):
    dd = float(d) + float(m)/60 + float(s)/3600
    return dd


acres = 0
fires = 0
with open('/Users/joshuaclark/Desktop/repos/fire-occurrence-api/data/Mexico/csvs/Serie_historica_anual_incendios_(2014).csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        SOURCE = 'CONAFOR-FDB'  # good 
        COUNTRY = 'MEXICO'  # good
        coords = row[2]
                # 25°15´15.7¨ - 100°46´58.9¨
        coords.replace(' ', '').strip()
        coords.replace('¨', '')
        lat_long = coords.split('- ')
        coordinate_pair = coord_fixer(lat_long)
        LATITUDE = dms_to_dd(coordinate_pair[0][0], coordinate_pair[0][1], coordinate_pair[0][2])   # yeet
        LONGITUDE = float("-" + str(dms_to_dd(coordinate_pair[1][0], coordinate_pair[1][1], coordinate_pair[1][2])))  #yeet
        try: 
            START_DATE = datetime.datetime.strptime(row[9], '%d/%m/%y').date()  # look good
        except:
            START_DATE = datetime.datetime.strptime(row[9], '%d-%m-%Y').date()  # look good
        try:    
            END_DATE = datetime.datetime.strptime(row[10], '%d/%m/%y').date()  # okay
        except:
            END_DATE = datetime.datetime.strptime(row[10], '%d-%m-%Y').date()  # look good

        FIRE_NAME = row[6]  # just take whatever this says
        STATE = row[4]  #ok
        COUNTRY_ISO = 'MX'
        try:
            SIZE =  float(row[23]) * 2.4710538  #probably
        except ValueError:
            SIZE = float(row[23].replace(',', '')) * 2.4710538 
        CAUSE = row[7] # ye
        if CAUSE.upper() == 'NATURALES':
            CAUSE = 'LIGHTNING'
        elif CAUSE.upper() in ['NINGUNA / NO APLICA', 'DESCONOCIDAS']:
            CAUSE = 'UNKNOWN'
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
            'LONGITUDE': LONGITUDE,
            'COUNTRY_ISO': COUNTRY_ISO,
            'STATE_ISO': None
        }
        # if row_dict['STATE'] == 'Querétaro'.upper():
        #     row_dict['STATE'] == 'QUERETARO'
        # if row_dict['STATE'] == 'Ciudad de México'.upper():
        #     row_dict['STATE'] == 'DISTRITO-FEDERAL'    
        # print(row_dict)

        cur.execute(""" INSERT INTO fires (source, country, name, size_ac, start_date, end_date, cause, state, latitude, longitude, country_iso, state_iso) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (row_dict['SOURCE'], row_dict['COUNTRY'], row_dict['NAME'], row_dict['SIZE_AC'], row_dict['START_DATE'], row_dict['END_DATE'], row_dict['CAUSE'], row_dict['STATE'], row_dict['LATITUDE'], row_dict['LONGITUDE'], row_dict['COUNTRY_ISO'], row_dict['STATE_ISO']))
cur.close()
postgres_conn.commit()        
# print(acres, fires)