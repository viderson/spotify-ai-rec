import json
import psycopg2
import os
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)
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
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        logger.info("Succesfull conection to db")
        cur.execute("DROP TABLE IF EXISTS tracks CASCADE;") # Dodaj to przed CREATE TABLE
        logger.info("Previous table has been dropped")
        # 2. Tworzymy tabelę na piosenki
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id TEXT PRIMARY KEY,
                name TEXT,
                artist TEXT,
                album TEXT,
                release_date DATE,
                description TEXT,
                embedding vector(384)
            );
        """)

        # 3. Wczytujemy Twoje 25 utworów z JSON-a
        with open('raw_tracks.json', 'r', encoding='utf-8') as f:
            tracks = json.load(f) 

        # 4. Wrzucamy dane do bazy
        for t in tracks:
            cur.execute("""
                INSERT INTO tracks (id, name, artist, album, release_date, description)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (t['id'], t['name'], t['artist'], t['album'], t['release_date'], t['description']))
        
        conn.commit()
        logger.info(f"Succes! db has been loaded with {len(tracks)} tracks")

    except Exception as e:
        logger.error(f"Connection to db failed because: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    load_data_to_postgres()