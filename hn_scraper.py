import argparse
import requests
from bs4 import BeautifulSoup
import re

def get_hn_url(item_id_or_url):
    if re.match(r'^\d+$', item_id_or_url):
        return f"https://news.ycombinator.com/item?id={item_id_or_url}"
    elif item_id_or_url.startswith("http") and "news.ycombinator.com/item" in item_id_or_url:
        return item_id_or_url
    else:
        raise ValueError("Invalid Hacker News item ID or URL provided.")

def scrape_hacker_news(url):
    response = requests.get(url)
    response.raise_for_status() # Raise an exception for HTTP errors
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_article_info(soup):
    title_tag = soup.select_one('table#hnmain table.fatitem td.title span.titleline a')
    if title_tag:
        title = title_tag.get_text(strip=True)
        link = title_tag['href']
        return f"[{title}]({link})"
    return "No article title found."

def extract_comments(soup):
    comments_data = []
    # Find all comment rows
    comment_rows = soup.select('table.comment-tree tr.athing.comtr')

    for row in comment_rows:
        # Get indentation level
        indent_img = row.select_one('td.ind img')
        indent_level = int(indent_img['width']) // 40 if indent_img else 0

        # Get comment text
        comment_text_div = row.select_one('div.comment div.commtext')
        if comment_text_div:
            # Reconstruct content with paragraphs and code blocks
            comment_paragraphs = []
            for content_element in comment_text_div.children:
                if content_element.name == 'p':
                    # Extract text from paragraph, handling potential nested links
                    paragraph_text = ""
                    for item in content_element.contents:
                        if item.name == 'a' and 'href' in item.attrs:
                            paragraph_text += f"[{item.get_text(strip=True)}]({item['href']})"
                        elif item.name == 'i': # Handle italics tag
                            paragraph_text += item.get_text(strip=True)
                        elif isinstance(item, str): # Handle NavigableString (plain text)
                            paragraph_text += item.strip()
                        else: # Handle other tags by getting their text
                            paragraph_text += item.get_text(strip=True)
                    comment_paragraphs.append(paragraph_text.strip())
                elif content_element.name == 'pre':
                    # For code blocks, preserve formatting within triple backticks
                    code_content = content_element.get_text(strip=False)
                    comment_paragraphs.append(f"""
```
{code_content}
```
""")
                elif content_element.name == 'a' and 'href' in content_element.attrs: # Handle direct links not in <p>
                    comment_paragraphs.append(f"[{content_element.get_text(strip=True)}]({content_element['href']})")
                elif isinstance(content_element, str) and content_element.strip():
                    comment_paragraphs.append(content_element.strip())
            
            comment_content = "\n\n".join(filter(None, comment_paragraphs)).strip()
            
            # Additional cleanup for specific HTML entities or patterns if needed
            comment_content = comment_content.replace('&#x2F;', '/') # Fix HTML entity for slash
            comment_content = comment_content.replace('&quot;', '"') # Fix HTML entity for quotes
            comment_content = comment_content.replace('&#x27;', "'") # Fix HTML entity for apostrophe
            comment_content = comment_content.replace('&#x2D;', "-") # Fix HTML entity for hyphen

            # Remove "reply" links and other non-comment text
            # This is a bit tricky as the structure can vary
            comment_content = re.sub(r'\s*reply\s*', '', comment_content, flags=re.IGNORECASE)
            comment_content = re.sub(r'<u>.*?</u>', '', comment_content) # Remove underline tags

            if comment_content:
                comments_data.append({
                    'indent': indent_level,
                    'text': comment_content
                })
    return comments_data

def convert_to_markdown(article_info, comments_data):
    markdown_output = f"# {article_info}\n\n"
    for comment in comments_data:
        indent_prefix = "    " * comment['indent']
        # Use '-' for the top-level, and '  - ' for nested if user prefers.
        # Given the example, it seems nested are also just indented.
        # Let's stick to simple indentation for now as per example
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

        markdown_content = convert_to_markdown(article_info, comments)

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
