from pathlib import Path

import requests
from bs4 import BeautifulSoup
from docx import Document
from pypdf import PdfReader


def extract_url(url: str) -> str:
    """
    Extract readable text from a webpage.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/131.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    # Remove elements that usually don't contain
    # useful document information.
    for element in soup(
        [
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript",
        ]
    ):
        element.decompose()

    text = soup.get_text(
        separator="\n"
    )

    # Clean excessive whitespace.
    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def extract_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    """

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def extract_text(file_path: str) -> str:
    """
    Extract text automatically based on file extension.

    Supported formats:
    - PDF
    - DOCX
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    if extension == ".docx":
        return extract_docx(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}. "
        "Supported formats are PDF and DOCX."
    )