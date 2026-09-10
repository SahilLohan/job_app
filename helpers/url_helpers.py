
from urllib.parse import parse_qs, unquote, urlparse


def resolve_url(url: str) -> str:
    """
    Convert search-engine redirect URLs into their real URL.

    Example:

    //duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.infosys.com...

    becomes:

    https://www.infosys.com/...
    """

    if not url:
        return url

    # DuckDuckGo redirect
    if "duckduckgo.com/l/" in url:

        parsed = urlparse(url)

        params = parse_qs(parsed.query)

        if "uddg" in params:
            return unquote(params["uddg"][0])

    # Protocol-relative URL
    if url.startswith("//"):
        return "https:" + url

    return url
