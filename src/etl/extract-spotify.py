import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
from dotenv import load_dotenv
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv() # Ładuje dane z pliku .env

def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope="playlist-read-private"
    ))

def fetch_playlist_data(playlist_id):
    sp = get_spotify_client()
    logger.info(f"Initialize data download from spotyfy for playlist: {playlist_id}")
    try:
        results = sp.playlist_items(playlist_id)
        tracks = results.get('items', [])
    except Exception as e:
        logger.error(f"Error connect to API: {e}") 
    enriched_data = []

    for i, entry in enumerate(tracks):
        track_data = entry.get('item')
        if not track_data: continue
        track_id = track_data.get('id')
        if not track_id: continue
        try:
            data = {
                'id': track_id,
                'name': track_data.get('name'),
                'artist': track_data['artists'][0]['name'] if track_data.get('artists') else 'Unknown',
                'album': track_data.get('album', {}).get('name', 'Unknown'),
                'release_date': track_data.get('album', {}).get('release_date'),
                'popularity': track_data.get('popularity'),
                'description': f"Song '{track_data.get('name')}' by {track_data['artists'][0]['name']} from the album {track_data.get('album', {}).get('name', 'Unknown')}."
            }
            
            enriched_data.append(data)
        except Exception as e:
            logger.warning(f"Error with track {i}: {e}")
    output_path = "raw_tracks.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_data, f, indent=4, ensure_ascii=False)
    logger.info(f"Succesfull data transfer {len(enriched_data)} tracks to {output_path}")
if __name__ == "__main__":
    # Przykład: ID playlisty "Top 50 - Polska" (znajdziesz w linku do playlisty)
    POLAND_TOP_50_ID = '6LJLPCTvZn0IOojFgQZa6y'
    fetch_playlist_data(POLAND_TOP_50_ID)
    