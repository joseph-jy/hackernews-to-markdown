# Hacker News Scraper and Markdown Notetaker

## 개요 (Overview)
이 프로젝트는 해커뉴스(news.ycombinator.com)의 특정 게시물에 달린 댓글들을 스크래핑하여 Markdown 형식의 노트로 변환하고 로컬 파일로 저장하는 CLI 도구입니다. 댓글의 계층 구조를 반영하여 적절한 들여쓰기로 가독성을 높였습니다.

## 주요 기능 (Features)
- 해커뉴스 게시물 ID 또는 전체 URL을 통해 댓글 데이터 스크래핑
- 스크래핑된 댓글을 Markdown 형식으로 변환
- 원본 게시물의 제목과 링크를 포함
- 댓글의 계층 구조에 따른 자동 들여쓰기
- 로컬 파일 시스템에 Markdown 노트 저장
- **(선택)** Inference API를 통한 원문 요약 및 댓글 한국어 번역

## 사용법 (Usage)

### 설치 (Installation)

**방법 1: Make 사용 (권장)**
```bash
make install
```

**방법 2: 수동 설치**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 스크립트 실행 (Running the Script)

**방법 1: Make 사용 (권장)**
```bash
make scrape URL="https://news.ycombinator.com/item?id=46918612"
```

**방법 2: 직접 실행**
```bash
venv/bin/python3 hn_scraper.py <HACKER_NEWS_ITEM_ID_OR_URL> -to <OUTPUT_FILE_PATH>
```

**예시:**
```bash
# ID로 실행
venv/bin/python3 hn_scraper.py 46918612 -to ./openciv3.md

# URL로 실행
venv/bin/python3 hn_scraper.py https://news.ycombinator.com/item?id=46918612 -to ./openciv3.md
```

### 요약/번역 기능 설정 (Optional)

Inference API를 설정하면 원문 요약과 댓글 한국어 번역 기능을 사용할 수 있습니다.

1. `.env.example`을 `.env`로 복사:
   ```bash
   cp .env.example .env
   ```

2. `.env` 파일에 실제 API 정보 입력:
   ```
   INFERENCE_API_URL=https://your-api-url/v1/chat/completions
   INFERENCE_API_KEY=your_api_key_here
   INFERENCE_MODEL=your_model_name
   ```

3. 스크립트 실행 시 자동으로 요약 및 번역이 적용됩니다.

**참고:** `.env` 파일이 없거나 설정이 불완전하면 기존처럼 원문 그대로 저장됩니다.

## 코드 구조 (Code Structure)

| 파일 | 설명 |
|------|------|
| `hn_scraper.py` | 핵심 스크래핑 및 Markdown 변환 스크립트 |
| `Makefile` | 간편 실행을 위한 Make 타겟 |
| `.env.example` | 환경 변수 설정 템플릿 |
| `requirements.txt` | Python 의존성 목록 |

## 출력 형식 (Output Format)

### 기본 출력 (Inference API 미설정)
```markdown
# [제목](링크)

## 댓글

- 댓글 1
    - 답글 1
```

### 확장 출력 (Inference API 설정됨)
```markdown
# [제목](링크)

## 요약

원문 요약 내용...

## 댓글

- 번역된 댓글 1
    - 번역된 답글 1
```
