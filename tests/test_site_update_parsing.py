import pytest

from scripts.generate_site_update import extract_field


def test_standard_formatting():
    text = "- **Number of bags:** 12"
    assert extract_field(text, "Number of bags") == "12"


def test_messy_spacing():
    text = " \t-   **Number of bags**    :   8   "
    assert extract_field(text, "Number of bags") == "8"


def test_different_bullet_points():
    text = "• **Number of bags:** 5"
    assert extract_field(text, "Number of bags") == "5"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("**Number of bags**: 15", "15"),
        ("- **Number of bags:** : 20", "20"),
    ],
)
def test_colon_variations(text: str, expected: str):
    assert extract_field(text, "Number of bags") == expected


def test_missing_values():
    text = """
    - **Notable items:** 
    - **Number of bags:** (e.g. list items)
    - **Approximate total volunteers who actually showed up (humans):** ~5
    """
    assert extract_field(text, "Notable items") is None
    assert extract_field(text, "Number of bags") is None
    assert extract_field(text, "Approximate total volunteers who actually showed up (humans)") is None


def test_unexpected_characters_preserved():
    text = "- **Number of bags:** 3 bags!!! @@##"
    assert extract_field(text, "Number of bags") == "3 bags!!! @@##"
