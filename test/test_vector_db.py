import os
import shutil
import pytest
from infra.datasource.vector.WebVectorIndexer import WebVectorIndexer

TEST_URL = "https://velog.io/@nawnoes/Faiss-%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0"
TEST_DB_DIR = "/Users/choisunpil/Desktop/development/2025/kbank-poc/infra/datasource/vector/data"


@pytest.fixture(scope="module")
def indexer():
    # 이전 벡터 DB 디렉토리 제거
    if os.path.exists(TEST_DB_DIR):
        shutil.rmtree(TEST_DB_DIR)

    idx = WebVectorIndexer(url=TEST_URL, persist_dir=TEST_DB_DIR)
    idx.crawl()
    idx.prepare_documents()
    return idx


def test_crawl_success(indexer):
    assert indexer.raw_text is not None
    assert len(indexer.raw_text) > 100  # 최소한의 텍스트는 있어야 함


def test_document_preparation(indexer):
    assert isinstance(indexer.documents, list)
    assert len(indexer.documents) > 0
    assert hasattr(indexer.documents[0], "page_content")


def test_vector_db_build(indexer):
    indexer.build_vector_db()
    assert indexer.vector_db is not None
    assert indexer.vector_db._collection.count() > 0


def test_search(indexer):
    if not indexer.vector_db:
        indexer.build_vector_db()

    query = "faiss 인덱스 저장 방법"
    results = indexer.vector_db.similarity_search(query, k=2)
    print("result" ,results)
    assert len(results) > 0
    for doc in results:
        assert query.split()[0].lower() in doc.page_content.lower()