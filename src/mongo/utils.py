import re
import requests
from bs4 import BeautifulSoup

def extract_data_from_url(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title of the page
    title = soup.title.string if soup.title else "No title found"
    title = re.sub(r'\s*-\s*Freedium$', '', title).strip()

    # Initialize containers for content, images, and code blocks
    article_content = ""
    images = []
    code_blocks = []

    # Find content between the markers "< Go to the original" and "Reporting a Problem"
    start_marker = "< Go to the original"
    end_marker = "Reporting a Problem"

    page_text = soup.get_text()
    start_index = page_text.find(start_marker)
    end_index = page_text.find(end_marker)

    if start_index != -1 and end_index != -1:
        article_content = page_text[start_index + len(start_marker):end_index].strip()

    # Extract content, images, and code blocks using BeautifulSoup
    for tag in soup.find_all(True):  # Find all tags
        if tag.name == 'img':
            src = tag.get('src')
            if src and re.search(r'\.(jpeg|jpg|png|gif)$', src, re.IGNORECASE):
                # Clean and construct URL if necessary
                cleaned_url = re.sub(r'/resize:[^/]+/', '/', src)
                images.append(cleaned_url)

        elif tag.name == 'pre' or tag.name == 'code':
            code_blocks.append(tag.get_text())

    # Remove code blocks from article content
    for code in code_blocks:
        article_content = article_content.replace(code, "")

    return title, article_content, images, code_blocks


def divide_text_into_chunks(text, limit=1000):
    """
    Divide the given text into chunks of approximately 'limit' characters.

    Args:
        text (str): The text to divide into chunks.
        limit (int): The maximum number of characters per chunk.

    Returns:
        list: A list of text chunks.
    """

    def chunker(contexts: list):
        chunks = []
        all_contexts = ' '.join(contexts).split('.')
        chunk = []
        for context in all_contexts:
            chunk.append(context)
            if len(chunk) >= 3 and len('.'.join(chunk)) > limit:
                # surpassed limit so add to chunks and reset
                chunks.append('.'.join(chunk).strip() + '.')
                # add some overlap between passages
                chunk = chunk[-2:]
        # if we finish and still have a chunk, add it
        if chunk:
            chunks.append('.'.join(chunk).strip() + '.')
        return chunks

    # Split text into a list based on paragraphs or new lines
    contexts = text.split('\n\n')  # Assuming paragraphs are separated by double new lines
    return chunker(contexts)