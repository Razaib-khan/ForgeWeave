"""Document extraction — PyMuPDF for PDFs, MarkItDown for multi-format.

Skill used: document-processor
Pattern: pymupdf.open with page iteration, find_tables, metadata extraction,
         markitdown for DOCX/HTML/CSV/PPTX/XLSX conversion
"""

from pathlib import Path

import pymupdf
from markitdown import MarkItDown


def extract_pdf_text(filepath: str) -> dict:
    doc = pymupdf.open(filepath)
    metadata = dict(doc.metadata)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return {
        "text": "\n\n".join(pages),
        "metadata": metadata,
        "page_count": len(pages),
    }


def extract_pdf_text_with_layout(filepath: str) -> dict:
    doc = pymupdf.open(filepath)
    pages = []
    for page in doc:
        block_data = page.get_text("dict")
        lines = []
        for block in block_data.get("blocks", []):
            if block.get("type") == 0:
                for line in block.get("lines", []):
                    span_texts = []
                    for span in line.get("spans", []):
                        span_texts.append(span.get("text", ""))
                    lines.append(" ".join(span_texts))
        pages.append("\n".join(lines))
    doc.close()
    return {"text": "\n\n".join(pages), "page_count": len(pages)}


def extract_pdf_tables(filepath: str) -> list[list[list[str]]]:
    doc = pymupdf.open(filepath)
    all_tables = []
    for page in doc:
        tables = page.find_tables()
        for table in tables:
            all_tables.append(table.extract())
    doc.close()
    return all_tables


def extract_pdf_metadata(filepath: str) -> dict:
    doc = pymupdf.open(filepath)
    metadata = dict(doc.metadata)
    doc.close()
    return metadata


def convert_to_markdown(filepath: str) -> str:
    md = MarkItDown()
    result = md.convert(filepath)
    return result.text_content


def extract_document(filepath: str) -> dict:
    ext = Path(filepath).suffix.lower()

    if ext == ".pdf":
        return extract_pdf_text(filepath)
    elif ext in (".docx", ".html", ".htm", ".csv", ".pptx", ".xlsx", ".json", ".xml"):
        text = convert_to_markdown(filepath)
        return {"text": text, "format": ext[1:]}
    else:
        raise ValueError(f"Unsupported format: {ext}")
