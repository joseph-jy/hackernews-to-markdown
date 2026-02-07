.PHONY: scrape install

# 의존성 설치
install:
	@python3 -m venv venv
	@venv/bin/pip install -r requirements.txt

# Hacker News 스크래핑
# 사용법: make scrape URL="https://news.ycombinator.com/item?id=46890814"
scrape:
	@venv/bin/python3 hn_scraper.py $(URL) -to ./output.md
