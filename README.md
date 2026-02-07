# Hacker News Scraper and Markdown Notetaker

## 개요 (Overview)
이 프로젝트는 해커뉴스(news.ycombinator.com)의 특정 게시물에 달린 댓글들을 스크래핑하여 Markdown 형식의 노트로 변환하고 로컬 파일로 저장하는 CLI 도구입니다. 댓글의 계층 구조를 반영하여 적절한 들여쓰기로 가독성을 높였습니다.

## 주요 기능 (Features)
- 해커뉴스 게시물 ID 또는 전체 URL을 통해 댓글 데이터 스크래핑
- 스크래핑된 댓글을 Markdown 형식으로 변환
- 원본 게시물의 제목과 링크를 포함
- 댓글의 계층 구조에 따른 자동 들여쓰기
- 로컬 파일 시스템에 Markdown 노트 저장

## 사용법 (Usage)

### 설치 (Installation)

1.  **가상 환경 설정 (Virtual Environment Setup):**
    프로젝트를 위한 격리된 Python 환경을 만듭니다.
    ```bash
    python3 -m venv venv
    ```

2.  **가상 환경 활성화 (Activate Virtual Environment):**
    ```bash
    source venv/bin/activate
    ```

3.  **필수 라이브러리 설치 (Install Dependencies):**
    `requests` (HTTP 요청) 및 `beautifulsoup4` (HTML 파싱) 라이브러리를 설치합니다.
    ```bash
    pip install requests beautifulsoup4
    ```

### 스크립트 실행 (Running the Script)

스크립트는 해커뉴스 게시물의 ID 또는 전체 URL, 그리고 저장할 Markdown 파일 경로를 인자로 받습니다.

```bash
venv/bin/python3 hn_scraper.py <HACKER_NEWS_ITEM_ID_OR_URL> -to <OUTPUT_FILE_PATH>
```

**예시 (Example):**

해커뉴스 ID `46918612`의 댓글을 `openciv3.md` 파일로 저장:

```bash
venv/bin/python3 hn_scraper.py 46918612 -to ./openciv3.md
```

또는 전체 URL을 사용하여 저장:

```bash
venv/bin/python3 hn_scraper.py https://news.ycombinator.com/item?id=46918612 -to ./openciv3.md
```

## 코드 구조 (Code Structure)

-   `hn_scraper.py`: 핵심 스크래핑 및 Markdown 변환 로직을 포함하는 Python 스크립트.

## 변환 구조 예시 (Example Markdown Output)

```markdown
# [OpenCiv3: Open-source, cross-platform reimagining of Civilization III](https://openciv3.org/)

- “Mac will try hard not to let you run this; it will tell you the app is damaged and can’t be opened and helpfully offer to trash it for you. From a terminal you can xattr -cr /path/to/OpenCiv3.app to enable running it.”
How far OSX has come since the days of the “cancel or allow” parody advert.
    - Mac support is the bane of my existence. It doesn't help that none of us core contributors have one, so if anyone is willing to be a lab monkey...
        - I have a Macbook Pro M4 Max, an Apple Developer account, a bit of time, and some enthusiasm. Would love to help!
```
(실제 출력은 더 많은 댓글과 계층 구조를 포함합니다.)