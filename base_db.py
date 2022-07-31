import sqlite3


BASE_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/'
API_KEY = '2dc3504289e7ccdd7ef3952c0b9ab8190052dd5e'
language = 'ru'
conn = sqlite3.connect('carbis_db.db')
cur = conn.cursor()
cur.execute('''
            CREATE TABLE IF NOT EXISTS secret_data(
            id INTEGER PRIMARY KEY,
            URL TEXT NOT NULL,
            API_KEY TEXT NOT NULL,
            language VARCHAR NOT NULL);
            ''')
insert_query=('''
            INSERT INTO secret_data(id, URL, API_KEY, language) VALUES (?,?,?,?)
                ''')
insert = (1, BASE_URL, API_KEY, language)
cur.execute(insert_query, insert)
conn.commit()
conn.close()