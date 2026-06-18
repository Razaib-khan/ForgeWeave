"""Pydantic models for the Deep Research MCP."""

from pydantic import BaseModel


class ExtractedContent(BaseModel):
    url: str | None = None
    title: str | None = None
    author: str | None = None
    date: str | None = None
    text: str | None = None
    source: str | None = None
    error: str | None = None


class DocumentMetadata(BaseModel):
    doc_id: str
    url: str
    title: str = ""
    source: str = ""
    date: str = ""
    doc_type: str = "article"
    content_hash: str = ""
    text_preview: str = ""


class SearchResult(BaseModel):
    doc_id: str
    text: str
    metadata: dict | None = None
    distance: float | None = None


class ResearchSummary(BaseModel):
    title: str
    key_findings: list[str]
    methodology: str | None = None
    sources_used: list[str] = []
    confidence: float = 0.0


class ResearchReport(BaseModel):
    query: str
    summary: ResearchSummary
    sources: list[DocumentMetadata]
    total_sources_used: int
