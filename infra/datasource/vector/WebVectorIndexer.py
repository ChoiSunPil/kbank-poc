# web_faiss_chroma.py
import os
import requests
from bs4 import BeautifulSoup
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

class WebVectorIndexer:
    def __init__(self, url: str, persist_dir: str = "chroma_faiss"):
        self.url = url
        self.persist_dir = persist_dir
        self.embeddings = OpenAIEmbeddings()
        self.vector_db = None
        self.raw_text = ""
        self.documents: list[Document] = []

    def crawl(self):
        print("🌐 웹사이트 크롤링 중...")
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, 'html.parser')
        self.raw_text = soup.get_text(separator='\n', strip=True)

    def prepare_documents(self):
        print("📄 문서로 변환 중...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(self.raw_text)
        self.documents = [
            Document(page_content=chunk, metadata={"source": self.url})
            for chunk in chunks
        ]

    def build_vector_db(self):
        print("🧠 벡터 DB 생성 중...")
        self.vector_db = Chroma.from_documents(
            documents=self.documents,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )

    def search(self, query: str, top_k: int = 3):
        if not self.vector_db:
            raise RuntimeError("❗ 벡터 DB가 준비되지 않았습니다. 먼저 build_vector_db()를 호출하세요.")
        print(f"🔍 검색 중: '{query}'")
        results = self.vector_db.similarity_search(query, k=top_k)
        for i, doc in enumerate(results):
            print(f"\n🔹 결과 {i+1}")
            print(doc.page_content)
            print(f"[출처]: {doc.metadata.get('source')}")