from bs4 import BeautifulSoup

from scripts.generate_site_update import (
    extract_devoe_evidence,
    extract_stat,
    find_devoe_description_element,
    find_stat_number_element,
)


def test_stat_box_parsing_extracts_number_and_label_match():
    html = """
    <div class="stats">
        <div class="stat-box">
            <div class="label">Parks Cleaned (so far)</div>
            <div class="number">3</div>
        </div>
        <div class="stat-box">
            <div class="label">Volunteers</div>
            <div class="number">12</div>
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    parks_cleaned_el = find_stat_number_element(soup, "Parks Cleaned (so far)")
    assert parks_cleaned_el is not None
    assert parks_cleaned_el.get_text(strip=True) == "3"
    assert extract_stat(soup, "Volunteers") == "12"


def test_devoe_evidence_box_parsing_returns_heading_and_description():
    html = """
    <section>
        <h2>Before & After</h2>
        <div class="evidence-box">
            <p><strong>Devoe Park Cleanup</strong></p>
            <p>Cleanup complete! 10 volunteers collected 5 bags.</p>
        </div>
        <div class="evidence-box">
            <p><strong>Another Park</strong></p>
            <p>Different description.</p>
        </div>
    </section>
    """
    soup = BeautifulSoup(html, "html.parser")

    devoe_evidence = extract_devoe_evidence(soup)
    assert devoe_evidence is not None
    heading, description = devoe_evidence
    assert heading == "Devoe Park Cleanup"
    assert description == "Cleanup complete! 10 volunteers collected 5 bags."

    description_el = find_devoe_description_element(soup)
    assert description_el is not None
    assert description_el.get_text(" ", strip=True) == "Cleanup complete! 10 volunteers collected 5 bags."


def test_missing_elements_return_none():
    html = """
    <div class="stat-box">
        <div class="label">Unrelated Stat</div>
        <div class="number">99</div>
    </div>
    <section>
        <h2>Gallery</h2>
        <div class="evidence-box">
            <p><strong>Another Park</strong></p>
            <p>Something else.</p>
        </div>
    </section>
    """
    soup = BeautifulSoup(html, "html.parser")

    assert find_stat_number_element(soup, "Parks Cleaned (so far)") is None
    assert extract_stat(soup, "Parks Cleaned (so far)") is None
    assert extract_devoe_evidence(soup) is None
    assert find_devoe_description_element(soup) is None
