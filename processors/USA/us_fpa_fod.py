# Steps to import FPA-FOD fires
#    1. Download FPA-FOD DB from USFS website
#    2. Set sqlite_conn to path of downloaded file and get a cursor
#    3. Connect to postgres fires db and get a cursor
#    4. Select all fires from sqlite file, only grab columns we care about
#    5. Iterate over rows in sqlite cursor object, set source and country, and insert into postgres fires table
#    6. Close and commit changes

import sqlite3
import psycopg2

# Step 2
sqlite_conn = sqlite3.connect('data/United States/FPA_FOD_20170508.sqlite')
c = sqlite_conn.cursor()

# Step 3
postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
cur = postgres_conn.cursor()

# Step 4
c.execute('SELECT FIRE_NAME, FIRE_SIZE, date(DISCOVERY_DATE), date(CONT_DATE), STAT_CAUSE_DESCR, STATE, LATITUDE, LONGITUDE FROM fires WHERE STATE = "{}"'.format('DC'))
rows = c.fetchall()

for row in rows:
    print(row)
# # Step 5
# for row in rows:
#     source = 'FPA-FOD'
#     country = 'USA'
#     cur.execute(""" INSERT INTO fires (source, country, name, size_ac, start_date, end_date, cause, state, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (source, country, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

# # Step 6
# cur.close()
# postgres_conn.commit()

# These are lil' helpers
# def create_fires_table():   
#     cur.execute( """ CREATE TABLE fires (id SERIAL PRIMARY KEY, source VARCHAR(50), country VARCHAR(50), name VARCHAR(200), size_ac DECIMAL, start_date DATE, end_date DATE, cause VARCHAR(200), state VARCHAR(200), latitude DECIMAL NOT NULL, longitude DECIMAL NOT NULL) """)

# c.execute('SELECT DISTINCT(SOURCE_REPORTING_UNIT) FROM fires')
# names = list(map(lambda x: x[0], c.description))
# print(names)
# rows = c.fetchall()
# for row in rows:
#     print(row)


# cur.execute('SELECT SUM(size_ac) from fires;')
# rows = cur.fetchall()
# for row in rows:
#     print(row)
# cur.execute('UPDATE fires SET state = UPPER(state)')

