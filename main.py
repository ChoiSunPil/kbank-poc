# main.py
from fastapi import FastAPI
from dotenv import load_dotenv

if __name__ == '__main__':

    load_dotenv()
    app = FastAPI(
        title="KBank PoC",
        version="0.1.0",
        description="Kbank Proof-of-Concept API"
    )