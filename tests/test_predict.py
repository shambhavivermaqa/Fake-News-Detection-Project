import pytest

from src.predict import predict


def test_predict_returns_expected_shape():
    result = predict("Local council approves new park budget", "The city council voted 7-2 to approve funding.")
    assert result["label"] in {"FAKE", "REAL"}
    assert 0 <= result["confidence"] <= 100
    assert result["cleaned_word_count"] > 0


def test_predict_raises_on_empty_input():
    with pytest.raises(ValueError):
        predict("", "")
