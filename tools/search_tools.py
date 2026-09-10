import json
from urllib.parse import quote

from langchain.tools import tool

from services.browser_service import browser_service
from helpers.url_helpers import resolve_url


# ============================================================
# TOOL — WEB SEARCH
# ============================================================

@tool
async def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo and return search result links.

    This tool only performs search.
    It does not decide which result is relevant.
    """

    encoded_query = quote(query)

    search_url = (
        "https://html.duckduckgo.com/html/"
        f"?q={encoded_query}"
    )

    print()
    print("=" * 70)
    print("TOOL: web_search")
    print("=" * 70)

    print(f"Query: {query}")
    print(f"Search URL: {search_url}")

    try:

        await browser_service.open(
            search_url
        )

    except Exception as e:

        return json.dumps(
            {
                "success": False,
                "error": str(e)
            },
            indent=2
        )


    # Get current page links
    page_data = await browser_service.inspect()


    # If inspect returns JSON string
    if isinstance(page_data, str):
        page_data = json.loads(page_data)


    links = page_data.get(
        "links",
        []
    )


    cleaned_results = []

    seen_urls = set()


    for link in links:

        url = resolve_url(
            link.get("href")
        )

        text = (
            link.get("text")
            or ""
        ).strip()


        if not url:
            continue


        if url in seen_urls:
            continue


        seen_urls.add(url)


        cleaned_results.append(
            {
                "title": text,
                "url": url
            }
        )


    print(
        f"Found {len(cleaned_results)} unique links."
    )


    return json.dumps(
        {
            "query": query,
            "search_url": page_data.get(
                "url"
            ),
            "results": cleaned_results
        },
        indent=2,
    )