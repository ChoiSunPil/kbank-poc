# 📘 Kbank-ai-poc

---

## 📦 사전 준비 사항

- Python 3.10.x 버전 설치  
- Poetry 설치 (아래 참고)

---

## 💡 Poetry 설치

### 방법 1. pipx 사용 (권장)

```bash
pip install --user pipx
pipx ensurepath
pipx install poetry
```

설치 확인:

```bash
poetry --version
```

### 방법 2. 공식 설치 스크립트

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

---

## 📁 프로젝트 설치

1. 이 레포를 클론합니다:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Poetry가 요구하는 Python 버전 설정 (예: 3.10.4)

```bash
poetry env use /usr/local/bin/python3.10
```

3. 의존성 설치 (가상환경 자동 생성됨)

```bash
poetry install
```

---

## 💻 가상환경 실행

```bash
poetry shell
```

또는 한 번만 실행하고 나올 거면:

```bash
poetry run python main.py
```

---

## ▶️ main.py 실행

```bash
poetry run python main.py
```

가상환경 안이라면 그냥:

```bash
python main.py
```

---

## ✅ 추가 명령어

| 작업 | 명령어 |
|--------|--------|
| 가상환경 위치 확인 | `poetry env info --path` |
| 가상환경 나가기 | `exit` 또는 `Ctrl + D` |
| 특정 명령 실행 | `poetry run <command>` |
| 의존성 업데이트 | `poetry update` |

---

## 🧪 테스트 실행

```bash
poetry run pytest -v
```

---

## 📄 참고 파일

- `pyproject.toml`: 프로젝트 메타 및 의존성 정의
- `poetry.lock`: 설치된 정확한 패키지 버전 잠금 파일

---

## ☕ License

MIT © 2025 Your Name

