# main.py
from fastapi import FastAPI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# FastAPI 인스턴스 생성
app = FastAPI(
    title="KBank PoC",
    version="0.1.0",
    description="Kbank Proof-of-Concept API"
)