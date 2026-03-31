from setuptools import setup, find_packages
import os
def parse_requirements(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

install_reqs = parse_requirements("requirements.txt")

setup(
    name="spotify-ai-rec",
    version="0.1.0",
    packages=find_packages(),
    install_requires=install_reqs,  # <-- Tu przekazujemy listę z pliku!
    author="Filip Widera",
    description="AI-powered Spotify recommendation system using RAG and FastAPI",
    python_requires=">=3.9",
)