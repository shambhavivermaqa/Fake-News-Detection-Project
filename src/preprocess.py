"""Text cleaning utilities shared by training and inference."""

import re
import string

_WHITESPACE_RE = re.compile(r"\s+")
_URL_RE = re.compile(r"https?://\S+|www\.\S+")
_HTML_RE = re.compile(r"<.*?>")
_NON_ALPHA_RE = re.compile(r"[^a-z\s]")


def clean_text(text: str) -> str:
    """Lowercase, strip URLs/HTML/punctuation/digits and collapse whitespace."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = _URL_RE.sub(" ", text)
    text = _HTML_RE.sub(" ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = _NON_ALPHA_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def build_input_text(title: str, body: str) -> str:
    """Combine title and body the same way for training and inference."""
    title = title or ""
    body = body or ""
    return clean_text(f"{title} {title} {body}")
