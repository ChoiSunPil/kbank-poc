# test_web_vector_indexer.py

import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import deque
import re
import pytest
from infra.datasource.vector.KbankWebVectorIndexer import KbankWebVectorIndexer


PERSIST_DIR = "/Users/choisunpil/Desktop/development/2025/kbank-poc/infra/datasource/vector/data"
@pytest.fixture
def indexer():

    indexer = KbankWebVectorIndexer(
        url="https://www.kbanknow.com",  # 테스트용으로 적절한 URL로 교체!
        persist_dir=PERSIST_DIR
    )
    yield indexer

def test_search(indexer):
    indexer.crawl("/ib20/mnu/PBKMAN000000")
    indexer.build_vector_db()
    assert indexer.vector_db is not None, "벡터 DB 생성 실패"
    results = indexer.vector_db.similarity_search("플러스 박스 금리", k=1)

    print(results)
    assert isinstance(results, list), "결과 타입이 리스트가 아님"
    if results:
        assert hasattr(results[0], "page_content"), "page_content 없음"


def test_crawling():
    base_url = "https://www.kbanknow.com"
    base_path ="/ib20/mnu/PBKMAN000000"
    print("🌐 하위 페이지 포함 전체 크롤링 중...")
    queue = deque([base_url + base_path])
    count = 0
    visited = set()
    def convert_go_menu(js_call: str) -> str:
        match = re.search(r"goMenu\('(\w+)'\)", js_call)
        if match:
            menu_id = match.group(1)
            return f"/ib20/mnu/{menu_id}"
        return None

    while queue and count < 50:
        current_url = queue.popleft()
        if current_url in visited:
            continue

        count += 1
        print(current_url)
        pattern = re.compile(r"goMenu\(['\"]([^'\"]+)['\"]\)")

        codes = set()

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            res = requests.get(current_url, headers=headers, timeout=10)
            visited.add(current_url)
            # 링크 추출 및 큐에 추가
            pattern = re.compile(r"goMenu\(['\"]([^'\"]+)['\"]\)")
            matches = pattern.findall(res.text)

            print("🎯 추출된 메뉴 코드:", matches)
            print("!23")

        except Exception as e:
            print(f"⚠️ 실패: {current_url} | 이유: {e}")