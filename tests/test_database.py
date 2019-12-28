import psycopg2
import pytest

class TestDatabase():
    postgres_conn = psycopg2.connect(database="fires", user="postgres", password="OvenT0aster!")
    cur = postgres_conn.cursor()

    # TEST EVERY RECORD HAS A SOURCE
    def test_source(self):
        self.cur.execute(""" SELECT DISTINCT source FROM fires """)
        for row in self.cur:
            assert None not in row

    # TEST EVERY RECORD HAS A COUNTRY
    def test_country(self):
        self.cur.execute(""" SELECT DISTINCT country FROM fires """)
        for row in self.cur:
            assert None not in row

    # TEST EVERY RECORD HAS A COUNTRY_ISO
    def test_country_iso(self):
        self.cur.execute(""" SELECT DISTINCT country_iso FROM fires """)
        for row in self.cur:
            assert None not in row

    # TEST EVERY RECORD HAS A STATE
    def test_state(self):
        self.cur.execute(""" SELECT DISTINCT state FROM fires """)
        for row in self.cur:
            assert None not in row

    # TEST EVERY RECORD HAS A STATE_ISO
    def test_state_iso(self):
        self.cur.execute(""" SELECT DISTINCT state_iso FROM fires """)
        for row in self.cur:
            assert None not in row

    # TEST EACH RECORD HAS A SIZE
    def test_size_ac(self):
        self.cur.execute(""" SELECT size_ac FROM fires """)
        for row in self.cur:
            assert None not in row

    # TEST EACH SIZE IS >= 0
    def test_size_ac_num(self):
        self.cur.execute(""" SELECT size_ac FROM fires """)
        for row in self.cur:
            assert row[0] >= 0

    # TEST EACH RECORD HAS A CAUSE
    def test_cause(self):
        self.cur.execute(""" SELECT cause FROM fires """)
        for row in self.cur:
            assert None not in row

    # TEST EACH RECORD HAS A CAUSE THAT IS HUMAN, LIGHTNING, OR UNKNOWN
    def test_cause_name(self):
        self.cur.execute(""" SELECT cause FROM fires """)
        for row in self.cur:
            assert row[0] in ['HUMAN', 'LIGHTNING', 'UNKNOWN']

    # TEST EVERY RECORD HAS A START DATE
    def test_start(self):
        self.cur.execute(""" SELECT start_date FROM fires """)
        for row in self.cur:
            assert None not in row

    # TEST EVERY RECORD HAS A START DATE THAT IS EARLIER THAN THE END DATE, IF THERE IS ONE
    def test_start_end(self):
        self.cur.execute(""" SELECT start_date, end_date FROM fires """)
        for row in self.cur:
            if row[1] != None:
                assert row[0] <= row[1]

    def close(self):
        self.cur.close()
        self.postgres_conn.commit() 







