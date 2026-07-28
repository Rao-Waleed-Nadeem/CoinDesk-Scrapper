from urllib.parse import urljoin

BASE_URL = "https://www.coindesk.com"


def clean_text(text: str | None) -> str | None:
    """
    Clean whitespace from extracted text.

    Example:
        "\n  Bitcoin   Hits  \n"
        ->
        "Bitcoin Hits"
    """
    if not text:
        return None

    return " ".join(text.split())


def extract_text(element) -> str | None:
    """
    Safely extract text from a BeautifulSoup element.

    Returns:
        Cleaned text or None.
    """
    if element is None:
        return None

    return clean_text(element.get_text(strip=True))


def extract_attr(element, attribute: str) -> str | None:
    """
    Safely extract an HTML attribute.

    Example:
        href
        src
        datetime
        content
    """
    if element is None:
        return None

    return element.get(attribute)


def normalize_url(url: str | None) -> str | None:
    """
    Convert relative URLs into absolute URLs.

    Example:
        /markets/bitcoin
            ->
        https://www.coindesk.com/markets/bitcoin
    """
    if not url:
        return None

    return urljoin(BASE_URL, url)


def validate_required(data: dict, required_fields: list[str]) -> bool:
    """
    Check whether all required fields exist.

    Returns:
        True if valid.
    """
    for field in required_fields:
        if not data.get(field):
            return False

    return True


def safe_select(parent, selector: str):
    """
    Safely select one element.

    Returns:
        BeautifulSoup Tag or None.
    """
    if parent is None:
        return None

    return parent.select_one(selector)


def safe_select_all(parent, selector: str):
    """
    Safely select multiple elements.

    Returns:
        List of BeautifulSoup Tags.
    """
    if parent is None:
        return []

    return parent.select(selector)


def extract_list_text(elements) -> list[str]:
    """
    Convert a list of BeautifulSoup elements into
    a list of cleaned strings.

    Example:
        [<span>AI</span>, <span>Crypto</span>]

        ->
        ["AI", "Crypto"]
    """
    if not elements:
        return []

    return [clean_text(element.get_text(strip=True)) for element in elements if element]
