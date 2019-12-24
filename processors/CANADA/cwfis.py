# Steps to import CWFIS fires
#   1. Download .txt file from CWFIS Datamart
#   2. Add to GIS as xy file and ensure projected to provided coordinate system (see metadata)
#   3. Add new fields for 'state', 'name', 'cause', and 'size_ac'
#   4. Calculate a field in 'size_ac' that is a conversion of the provided size field (hectares)
#   5. Calculate a field in 'cause' that calls H and H-PB values as HUMAN, L is LIGHTNING, and n/a or U is UNKNOWN
#   6. Calculate a field in 'name' where BC and YT fires are given names that are in the 'MORE_INFO' column and the remaining fires have their default name
#   7. Calculate a field in 'state' which is the two-letter abbreviation of the state provided by the SOURCE column. For PC (Parks Canada) fires, label the state as 'PC'
#   8. Definition query for only 'PC' state fires. Import a shapefile of Canadian provinces and territories from Census. Intersect these fires with this layer
#   9. Use the results of the intersection to populate the state column with the proper provinces and territories
#   10. Merge these fires with the rest of the fires to get a complete dataset. Remove fires that have 'PC' as the state.
#   11. Remove any fires without a start (report date) date.
#   12. Check to make sure dates seem logical.
#   13. Check to make sure locations seem logical. Search longitude for positive values and flip the sign to negative. 
#   12. Export from GIS as a JSON to use below. 

# Note these date formats
#   REP_DATE is m/d/YYYY no 0 padding
#   OUT_DATE is YYYY-mm-dd HH:MM:SS when it exists

import csv
import psycopg2
import datetime

postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
cur = postgres_conn.cursor()
with open('data/Canada/canada_fires_2019.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        source = 'CWFIS-NFDB'
        country = 'CANADA'
        row['REP_DATE'] = datetime.datetime.strptime(row['REP_DATE'], '%m/%d/%Y %H:%M:%S').date()
        if row['OUT_DATE']:
            row['OUT_DATE'] = datetime.datetime.strptime(row['OUT_DATE'], '%Y-%m-%d %H:%M:%S').date()
        else:
            row['OUT_DATE'] = None
        # print((source, country, row['name'], row['size_ac'], row['REP_DATE'], row['OUT_DATE'], row['cause_type'], row['state'], row['LATITUDE'], row['LONGITUDE']))
        cur.execute(""" INSERT INTO fires (source, country, name, size_ac, start_date, end_date, cause, state, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (source, country, row['name'], row['size_ac'], row['REP_DATE'], row['OUT_DATE'], row['cause_type'], row['state'], row['LATITUDE'], row['LONGITUDE']))
cur.close()
postgres_conn.commit()
