# Steps to import CONAF fires
#   1. Obtain data dump from CONAF information request
#   2. Convert files to proper CSV
#   3. From the main Chile fire statistics webpage, download the summary statistics that show occurrence/area burned from 1985 to present
#   4. Open CSVs in excel and verify the data roughly matches what is shown in the summary statistics (just a sanity check, really)
#   5. Import locale and set time to Spanish due to date formats of start and end dates
#   6. Import proj to convert UTM coordinates to lat longs. Each UTM coord must have a zone!
#   7. Make sure SOURCE = 'CONAF-FDB', COUNTRY = 'CHILE' and COUNTRY_ISO = 'CL' in below dictionary assignments
 
import csv
import datetime
import psycopg2
import locale
from pyproj import Proj, exceptions
from chile_causes import chile_causes

postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
cur = postgres_conn.cursor()
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

with open('data/Chile/20191227_dump/csvs/1997_2002.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    fire_num = 0
    acres = 0
    for row in csv_reader:
        SOURCE = 'CONAF-FDB' 
        COUNTRY = 'CHILE'
        COUNTRY_ISO = 'CL'
        STATE = row[1].upper().strip()
        STATE_ISO = None
        FIRE_NAME = row[5].upper().strip()

        # Lat Long Processing, note that zone should be provided in data. south MUST equal TRUE or bad times will be had
        # try: 
        #     myProj = Proj(proj='utm', ellps='WGS84', zone=row[8], south=True)
        #     LONGITUDE, LATITUDE = myProj(row[6].split(' ')[0], row[7].split(' ')[0], inverse=True)
        # except exceptions.CRSError:
        LONGITUDE, LATITUDE = -0.0, -0.0

        # Cause can only be NATURAL, HUMAN, or UNKNOWN
        CAUSE = row[7].split(' ')[0] 
        if CAUSE in ['NO IDENTIFICADA - Desconocida', 'OTRAS ACTIVIDADES - Otras', '']:
            CAUSE = 'UNKNOWN'
        elif CAUSE == 'OTRAS CAUSAS - Rayos':
            CAUSE = 'NATURAL-LIGHTNING'
        else:
            CAUSE = 'HUMAN'

       # Convert ha to acres
        SIZE =  float(row[19]) * 2.4710538 

        # Dates in locale datetime have format 18-oct-2002 14:51, 18-oct-2002 19:00 or 3/22/18 23:00
        try: 
            START_DATE = datetime.datetime.strptime(row[20], '%d-%b-%Y %H:%M').date() 
        except ValueError: 
            START_DATE = datetime.datetime.strptime(row[20], '%m/%d/%y %H:%M').date() 
        try:
            END_DATE = datetime.datetime.strptime(row[21], '%d-%b-%Y %H:%M').date() 
        except ValueError:  # this accounts for end_date blanks
            try: 
                END_DATE = datetime.datetime.strptime(row[21], '%m/%d/%y %H:%M').date() 
            except: 
                END_DATE = None

        row_dict = {
            'SOURCE': SOURCE,
            'COUNTRY': COUNTRY,
            'NAME': FIRE_NAME,
            'SIZE_AC': SIZE,
            'START_DATE': START_DATE,
            'END_DATE': END_DATE,
            'CAUSE': CAUSE,
            'STATE': STATE,
            'LATITUDE': LATITUDE,
            'LONGITUDE': LONGITUDE,
            'COUNTRY_ISO': COUNTRY_ISO,
            'STATE_ISO': STATE_ISO
        }
        # print(row_dict)
        cur.execute(""" INSERT INTO fires (source, country, name, size_ac, start_date, end_date, cause, state, latitude, longitude, country_iso, state_iso) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (row_dict['SOURCE'], row_dict['COUNTRY'], row_dict['NAME'], row_dict['SIZE_AC'], row_dict['START_DATE'], row_dict['END_DATE'], row_dict['CAUSE'], row_dict['STATE'], row_dict['LATITUDE'], row_dict['LONGITUDE'], row_dict['COUNTRY_ISO'], row_dict['STATE_ISO']))
        acres += row_dict['SIZE_AC']
        fire_num += 1
    print(fire_num, acres)
cur.close()
postgres_conn.commit()   