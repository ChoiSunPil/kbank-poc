# 🧠 kbank-poc: VectorDB 기반 AI 검색 시스템

> FastAPI, LangChain, HuggingFace, ChromaDB 등을 활용한 임베딩 기반 검색 API 프로젝트

---

## 🔧 프로젝트 환경 구성

### Conda + Poetry에서 Conda + pip 전환 이유
#### apple slicon local pc에서 conda + poetry 사용 시 <br> library import 이슈 발생(ex arm64로 설치해도 x86으로 읽으려고함) <br> 따라서 conda에 있는 라이브러리는 conda-forge 통해서 설치 <br>아닌 경우만 pip 로 설치


### ✅ Conda 환경 설정

이 프로젝트는 [conda-forge](https://conda-forge.org/)를 활용하여 reproducible한 개발 환경을 구성합니다.

#### 1. Conda 환경 생성

```bash
conda env create -f environment.yml
conda activate kbank-poc