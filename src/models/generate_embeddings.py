import psycopg2
from sentence_transformers import SentenceTransformer
from src.utils.logger import get_logger

logger = get_logger(__name__)

def generate_embedding():
    model = SentenceTransformer('all-MiniLm-L6-v2')
    logger.info(f"Model downloading: all-MiniLm-L6-v2")

    conn = psycopg2.connect(
        host = 'localhost',
        database = 'spotify_db',
        user = 'user',
        password = "pass",
        port = "5432"
    )
    cur = conn.cursor()

    cur.execute("SELECT id, name, artist, album, release_date, description FROM tracks WHERE embedding is NULL;")
    rows = cur.fetchall()

    if not rows:
        logger.info("All tracks are already inicialed")
        return
    logger.info(f"Starting to generate vectors for {len(rows)} tracks ...")
    for id, name, artists, album, release_date, description in rows:
        text_to_process = f"{name} from album: {album} by {artists} made in {release_date}. {description}"
        embedding = model.encode(text_to_process).tolist()

        cur.execute(
            "UPDATE tracks SET embedding = %s WHERE id = %s",
            (embedding, id)
        )
        logger.info(f"vector was generated for: {name} track")
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Embeddings added to db")
if __name__ == '__main__':
    generate_embedding()