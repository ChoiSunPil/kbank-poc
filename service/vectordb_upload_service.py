
from infra.datasource.vector.KbankWebVectorIndexer import KbankWebVectorIndexer
def update_vectordb(file):
    try:
        indexer = KbankWebVectorIndexer()
        indexer.file_to_vector(file)
        return "업로드 완료"
    except Exception as e:
        return f"❌ 처리 실패: {str(e)}"
