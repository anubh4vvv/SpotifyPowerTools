import os

from dotenv import load_dotenv

from services.app_paths import env_file_candidates


for env_file in env_file_candidates():

    if env_file.exists():
        load_dotenv(
            dotenv_path=env_file,
            override=False
        )


CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")