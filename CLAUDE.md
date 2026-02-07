# Hacker News to Markdown

Hacker News 게시물의 댓글을 스크래핑하여 Markdown 파일로 저장하는 CLI 도구.

## 프로젝트 구조

```
.
├── hn_scraper.py    # 핵심 스크래핑 및 Markdown 변환 스크립트
├── Makefile         # 간편 실행을 위한 Make 타겟
├── .env.example     # 환경 변수 설정 템플릿
├── .env             # 실제 환경 변수 (git 제외)
├── requirements.txt # Python 의존성
├── README.md        # 프로젝트 문서
└── .gitignore
```

## 기술 스택

- Python 3
- requests (HTTP 요청)
- BeautifulSoup4 (HTML 파싱)
- python-dotenv (환경 변수 로드)

## 실행 방법

```bash
# 방법 1: Make 사용 (권장)
make install
make scrape URL="https://news.ycombinator.com/item?id=46890814"

# 방법 2: 직접 실행
venv/bin/python3 hn_scraper.py <HN_ID_OR_URL> -to <OUTPUT_PATH>
```

## 주요 함수

| 함수 | 역할 |
|------|------|
| `get_hn_url()` | ID 또는 URL을 HN URL로 변환 |
| `scrape_hacker_news()` | 페이지 HTML 가져오기 |
| `extract_article_info()` | 게시물 제목/링크 추출 |
| `extract_comments()` | 댓글 및 계층 구조 추출 |
| `convert_to_markdown()` | Markdown 형식으로 변환 |
| `load_inference_config()` | .env에서 API 설정 로드 |
| `call_inference_api()` | Inference API 호출 |
| `summarize_article()` | 원문 URL로 요약 생성 |
| `translate_comments()` | 댓글 청크 단위 번역 |
| `chunk_comments()` | 댓글을 적절한 크기로 분할 |

## 환경 변수

| 변수 | 설명 |
|------|------|
| `INFERENCE_API_URL` | Inference API 엔드포인트 |
| `INFERENCE_API_KEY` | API 인증 키 |
| `INFERENCE_MODEL` | 사용할 모델 이름 |

**참고:** 환경 변수가 설정되지 않으면 요약/번역 없이 기존 동작을 유지합니다.

## 개발 규칙

- 한국어 문서 작성 선호
- HTML 엔티티 변환 처리 필요 (`&#x2F;` → `/` 등)
