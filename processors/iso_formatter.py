import psycopg2
import csv


countries = []
with open('/Users/joshuaclark/Desktop/repos/fire-occurrence-api/data/ABBREVIATIONS/iso3166-2_country_state_abbrs.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[0]:
            country = {row[0]: {'LONG_NAME': row[3].upper(), 'STATES': []}}
            countries.append(country)


with open('/Users/joshuaclark/Desktop/repos/fire-occurrence-api/data/ABBREVIATIONS/iso3166-2_country_state_abbrs.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[1]:
            split_state = row[1].split('-')
            state_long  = row[3].upper()
            for country in countries:
                if str(split_state[0]) in country:
                    country[str(split_state[0])]['STATES'].append((split_state[1], state_long))


## UPDATING COUNTRIES
def country_update(country, country_iso, countries):
    postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
    cur = postgres_conn.cursor()
    print('gathering fires to process...')
    tup_list = []
    tup_de_dupe = ()
    cur.execute('SELECT * FROM fires')
    for row in cur:
        if row[2] == country:
            for country in countries:
                if country_iso in country:
                    tup_de_dupe = (row[0],  country[country_iso]['LONG_NAME'].replace(r' ','-') )
                    tup_list.append(tup_de_dupe)
    cur.close()
    postgres_conn.commit()

    print('updating rows...')
    postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
    cur = postgres_conn.cursor()
    for record in tup_list:
        cur.execute(""" UPDATE fires SET COUNTRY = %s WHERE ID = %s""", (record[1], record[0]))
    cur.close()
    postgres_conn.commit()
    return print('update complete.')

## UPDATING COUNTRY_ISO
def country_iso_update():
    postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
    cur = postgres_conn.cursor()
    cur.execute(""" UPDATE fires SET COUNTRY_ISO = 'CA' WHERE COUNTRY = 'CANADA' """)
    cur.close()
    postgres_conn.commit()

## UPDATE STATES
tup_list = []
def state_update(country_iso, countries):
    postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
    cur = postgres_conn.cursor()
    cur.execute(""" SELECT id, state FROM fires WHERE country_iso = '{}' """.format(country_iso))
    for row in cur:
        for country in countries:
            if country_iso in country:
                for state_tup in country[country_iso]['STATES']:
                    if row[1].upper() in state_tup[1]:
                        id = row[0]
                        original = row[1]
                        state_iso = state_tup[0]
                        state_long = state_tup[1].replace(r' ','-')
                        record_tup = (id, original, state_iso, state_long)
                        tup_list.append(record_tup)
    cur.close()
    postgres_conn.commit()
    print(len(tup_list))
    print('updating rows...')
    postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
    cur = postgres_conn.cursor()
    for record in tup_list:
        if record[3] == "LIBERTADOR-GENERAL-BERNARDO-O'HIGGINS":
            dummy_higs = "LIBERTADOR-GENERAL-BERNARDO-O''HIGGINS"
            cur.execute(""" UPDATE fires SET STATE = '{}', STATE_ISO = '{}' WHERE ID = '{}' """.format(dummy_higs, record[2], record[0]))
        else:
            cur.execute(""" UPDATE fires SET STATE = '{}', STATE_ISO = '{}' WHERE ID = '{}' """.format(record[3], record[2], record[0]))

    cur.close()
    postgres_conn.commit()
    return print('update complete.')


state_update('CL', countries)
# postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
# cur = postgres_conn.cursor()
# cur.execute('UPDATE fires SET country = UPPER(country)')
# cur.close()
# postgres_conn.commit()