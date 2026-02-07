import argparse
import os
import requests
from bs4 import BeautifulSoup
import re

# dotenv는 선택적 의존성
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def load_inference_config():
    """환경 변수에서 inference API 설정을 로드합니다."""
    api_url = os.getenv('INFERENCE_API_URL')
    api_key = os.getenv('INFERENCE_API_KEY')
    model = os.getenv('INFERENCE_MODEL')

    if api_url and api_key and model:
        return {
            'url': api_url,
            'key': api_key,
            'model': model
        }
    return None


def call_inference_api(config, prompt, max_tokens=2048):
    """Inference API를 호출합니다."""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config["key"]}'
    }

    payload = {
        'model': config['model'],
        'messages': [
            {'role': 'user', 'content': prompt}
        ],
        'max_tokens': max_tokens,
        'temperature': 0.3
    }

    try:
        response = requests.post(config['url'], headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Inference API 호출 실패: {e}")
        return None


def fetch_article_content(url):
    """원문 URL에서 텍스트 콘텐츠를 가져옵니다."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 스크립트, 스타일 등 불필요한 태그 제거
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()

        # 본문 추출 시도 (일반적인 article 태그 또는 main 태그 우선)
        article = soup.find('article') or soup.find('main') or soup.find('body')

        if article:
            text = article.get_text(separator='\n', strip=True)
            # 너무 긴 경우 잘라냄 (약 8000자)
            return text[:8000]
        return None
    except Exception as e:
        print(f"원문 가져오기 실패: {e}")
        return None


def summarize_article(config, article_url):
    """원문을 요약합니다."""
    content = fetch_article_content(article_url)
    if not content:
        return None

    prompt = f"""다음은 기술 관련 글입니다. 핵심 내용을 3-5문장으로 간결하게 요약해주세요.
요약은 한국어로 작성하고, 기술적 용어는 원문 그대로 유지해주세요.

원문:
{content}"""

    return call_inference_api(config, prompt)


def chunk_comments(comments_data, max_chars=2000):
    """댓글을 적절한 크기의 청크로 분할합니다."""
    chunks = []
    current_chunk = []
    current_size = 0

    for comment in comments_data:
        indent_prefix = "    " * comment['indent']
        comment_line = f"{indent_prefix}- {comment['text']}\n"
        comment_size = len(comment_line)

        if current_size + comment_size > max_chars and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_size = 0

        current_chunk.append(comment)
        current_size += comment_size

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def translate_comments_chunk(config, comments_chunk):
    """댓글 청크를 번역합니다."""
    # 청크를 마크다운 형식으로 변환
    chunk_text = ""
    for comment in comments_chunk:
        indent_prefix = "    " * comment['indent']
        chunk_text += f"{indent_prefix}- {comment['text']}\n"

    prompt = f"""다음 Hacker News 댓글들을 한국어로 번역해주세요.
기술 용어는 원문을 유지하고, 자연스러운 한국어로 번역해주세요.
마크다운 형식(-, 들여쓰기)을 그대로 유지해주세요.
번역된 댓글만 출력하고 다른 설명은 추가하지 마세요.

댓글:
{chunk_text}"""

    return call_inference_api(config, prompt, max_tokens=4096)


def translate_comments(config, comments_data):
    """모든 댓글을 번역합니다."""
    chunks = chunk_comments(comments_data)
    translated_parts = []

    print(f"번역 중... (총 {len(chunks)}개 청크)")

    for i, chunk in enumerate(chunks):
        print(f"  청크 {i+1}/{len(chunks)} 번역 중...")
        translated = translate_comments_chunk(config, chunk)
        if translated:
            translated_parts.append(translated)
        else:
            # 번역 실패 시 원문 유지
            for comment in chunk:
                indent_prefix = "    " * comment['indent']
                translated_parts.append(f"{indent_prefix}- {comment['text']}\n")

    return "\n".join(translated_parts)


def get_hn_url(item_id_or_url):
    if re.match(r'^\d+$', item_id_or_url):
        return f"https://news.ycombinator.com/item?id={item_id_or_url}"
    elif item_id_or_url.startswith("http") and "news.ycombinator.com/item" in item_id_or_url:
        return item_id_or_url
    else:
        raise ValueError("Invalid Hacker News item ID or URL provided.")


def scrape_hacker_news(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def extract_article_info(soup):
    """게시물 제목과 링크를 추출합니다."""
    title_tag = soup.select_one('table#hnmain table.fatitem td.title span.titleline a')
    if title_tag:
        title = title_tag.get_text(strip=True)
        link = title_tag['href']
        return {'title': title, 'link': link, 'markdown': f"[{title}]({link})"}
    return {'title': 'No article title found.', 'link': None, 'markdown': 'No article title found.'}


def extract_comments(soup):
    comments_data = []
    comment_rows = soup.select('table.comment-tree tr.athing.comtr')

    for row in comment_rows:
        indent_img = row.select_one('td.ind img')
        indent_level = int(indent_img['width']) // 40 if indent_img else 0

        comment_text_div = row.select_one('div.comment div.commtext')
        if comment_text_div:
            comment_paragraphs = []
            for content_element in comment_text_div.children:
                if content_element.name == 'p':
                    paragraph_text = ""
                    for item in content_element.contents:
                        if item.name == 'a' and 'href' in item.attrs:
                            paragraph_text += f"[{item.get_text(strip=True)}]({item['href']})"
                        elif item.name == 'i':
                            paragraph_text += item.get_text(strip=True)
                        elif isinstance(item, str):
                            paragraph_text += item.strip()
                        else:
                            paragraph_text += item.get_text(strip=True)
                    comment_paragraphs.append(paragraph_text.strip())
                elif content_element.name == 'pre':
                    code_content = content_element.get_text(strip=False)
                    comment_paragraphs.append(f"""
```
{code_content}
```
""")
                elif content_element.name == 'a' and 'href' in content_element.attrs:
                    comment_paragraphs.append(f"[{content_element.get_text(strip=True)}]({content_element['href']})")
                elif isinstance(content_element, str) and content_element.strip():
                    comment_paragraphs.append(content_element.strip())

            comment_content = "\n\n".join(filter(None, comment_paragraphs)).strip()

            # HTML 엔티티 변환
            comment_content = comment_content.replace('&#x2F;', '/')
            comment_content = comment_content.replace('&quot;', '"')
            comment_content = comment_content.replace('&#x27;', "'")
            comment_content = comment_content.replace('&#x2D;', "-")

            comment_content = re.sub(r'\s*reply\s*', '', comment_content, flags=re.IGNORECASE)
            comment_content = re.sub(r'<u>.*?</u>', '', comment_content)

            if comment_content:
                comments_data.append({
                    'indent': indent_level,
                    'text': comment_content
                })
    return comments_data


def convert_to_markdown(article_info, comments_data, summary=None, translated_comments=None):
    """마크다운 형식으로 변환합니다."""
    markdown_output = f"# {article_info['markdown']}\n\n"

    # 요약이 있으면 추가
    if summary:
        markdown_output += f"## 요약\n\n{summary}\n\n"

    markdown_output += "## 댓글\n\n"

    # 번역된 댓글이 있으면 사용, 없으면 원문 사용
    if translated_comments:
        markdown_output += translated_comments
    else:
        for comment in comments_data:
            indent_prefix = "    " * comment['indent']
            markdown_output += f"{indent_prefix}- {comment['text']}\n"

    return markdown_output


def main():
    parser = argparse.ArgumentParser(description="Scrape Hacker News comments and save as Markdown.")
    parser.add_argument("hn_item", help="Hacker News item ID (e.g., 46918612) or full URL.")
    parser.add_argument("-to", "--output", required=True, help="Output Markdown file path (e.g., ./output.md).")

    args = parser.parse_args()

    try:
        hn_url = get_hn_url(args.hn_item)
        print(f"Scraping Hacker News from: {hn_url}")
        soup = scrape_hacker_news(hn_url)

        article_info = extract_article_info(soup)
        comments = extract_comments(soup)

        # Inference API 설정 확인
        inference_config = load_inference_config()
        summary = None
        translated_comments = None

        if inference_config:
            print("Inference API 설정 감지됨. 요약 및 번역을 수행합니다.")

            # 원문 요약
            if article_info['link'] and article_info['link'].startswith('http'):
                print("원문 요약 중...")
                summary = summarize_article(inference_config, article_info['link'])
                if summary:
                    print("요약 완료!")
                else:
                    print("요약 생성 실패. 요약 없이 진행합니다.")

            # 댓글 번역
            if comments:
                translated_comments = translate_comments(inference_config, comments)
                print("번역 완료!")
        else:
            print("Inference API 설정 없음. 기존 방식으로 진행합니다.")

        markdown_content = convert_to_markdown(article_info, comments, summary, translated_comments)

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Successfully saved comments to {args.output}")

    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Network or HTTP error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
