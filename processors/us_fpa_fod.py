import sqlite3
import psycopg2


# sqlite_conn = sqlite3.connect('data/United States/FPA_FOD_20170508.sqlite')
# c = sqlite_conn.cursor()


postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
cur = postgres_conn.cursor()
cur.execute('SELECT name from fires where name IS NULL')
print(len(cur.fetchall()))
# cur.execute('UPDATE fires SET state = UPPER(state)')

# c.execute('SELECT FIRE_NAME, FIRE_SIZE, date(DISCOVERY_DATE), date(CONT_DATE), STAT_CAUSE_DESCR, STATE, LATITUDE, LONGITUDE FROM fires')
# rows = c.fetchall()

# for row in rows:
#     source = 'FPA-FOD'
#     country = 'USA'
#     cur.execute(""" INSERT INTO fires (source, country, name, size_ac, start_date, end_date, cause, state, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (source, country, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

# cur.close()
# postgres_conn.commit()

# cur.execute( """ CREATE TABLE fires (id SERIAL PRIMARY KEY, source VARCHAR(50), country VARCHAR(50), name VARCHAR(200), size_ac DECIMAL, start_date DATE, end_date DATE, cause VARCHAR(200), state VARCHAR(200), latitude DECIMAL NOT NULL, longitude DECIMAL NOT NULL) """)
# cur.execute( """ DROP TABLE fires """)


