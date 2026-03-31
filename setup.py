from setuptools import setup, find_packages

setup(
    name="spotify-ai-rec",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "spotipy",
        "pandas",
        "psycopg2-binary",
        "pgvector",
        "python-dotenv",
        "langchain",
        "fastapi",
        "uvicorn",
        "streamlit"
    ],
    author="Filip Widera",
    description="AI-powered Spotify recommendation system using RAG and FastAPI",
    python_requires=">=3.9",
)