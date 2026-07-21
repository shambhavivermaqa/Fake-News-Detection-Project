from src.preprocess import build_input_text, clean_text


def test_clean_text_lowercases_and_strips_punctuation():
    assert clean_text("Hello, WORLD!!") == "hello world"


def test_clean_text_removes_urls_and_html():
    assert clean_text("Check http://example.com <b>now</b>") == "check now"


def test_clean_text_removes_digits():
    assert clean_text("Top 10 stories in 2024") == "top stories in"


def test_clean_text_handles_non_string_input():
    assert clean_text(None) == ""
    assert clean_text(float("nan")) == ""


def test_build_input_text_combines_title_and_body():
    result = build_input_text("Breaking News", "Something happened today.")
    assert "breaking news" in result
    assert "something happened today" in result


def test_build_input_text_handles_missing_fields():
    assert build_input_text("", "Body only text") == "body only text"
    assert build_input_text("Title only", "") == "title only title only"
