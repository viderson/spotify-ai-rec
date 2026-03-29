import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def load_data_to_postgres():
    # 1. Połączenie z bazą w Dockerze (dane z docker-compose.yml)
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="spotify_db",
            user="user",
            password="pass",
            port="5432"
        )
        cur = conn.cursor()
        print("✅ Połączono z bazą danych w Dockerze!")

        # 2. Tworzymy tabelę na piosenki
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id TEXT PRIMARY KEY,
                name TEXT,
                artist TEXT,
                album TEXT,
                description TEXT
            );
        """)

        # 3. Wczytujemy Twoje 25 utworów z JSON-a
        with open('raw_tracks.json', 'r', encoding='utf-8') as f:
            tracks = json.load(f)

        # 4. Wrzucamy dane do bazy
        for t in tracks:
            cur.execute("""
                INSERT INTO tracks (id, name, artist, album, description)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (t['id'], t['name'], t['artist'], t['album'], t['description']))

        conn.commit()
        print(f"🚀 Sukces! Przeniesiono {len(tracks)} utworów z JSON do bazy SQL.")

    except Exception as e:
        print(f"❌ Błąd podczas ładowania danych: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    load_data_to_postgres()