import json

from langchain.tools import tool

from services.browser_service import browser_service
from helpers.url_helpers import resolve_url


# ============================================================
# TOOL — OPEN URL
# ============================================================

@tool
async def open_url(url: str) -> str:
    """
    Open a URL in the browser.

    Use this after deciding which link should be opened.
    """
    print(
        f"[BrowserService] Opening URL: {url}"
    )

    url = resolve_url(url)

    print()
    print("=" * 70)
    print("TOOL: open_url")
    print("=" * 70)

    print(f"Opening: {url}")


    try:

        result = await browser_service.open(url)

    except Exception as e:

        return (
            f"Navigation failed.\n"
            f"URL: {url}\n"
            f"Error: {e}"
        )


    return json.dumps(
        result,
        indent=2
    )



# ============================================================
# TOOL — INSPECT PAGE
# ============================================================

@tool
async def inspect_page(dummy: str = "") -> str:
    """
    Inspect the current browser page.

    Returns:
    - current URL
    - page title
    - visible text
    - visible links
    - visible buttons
    - visible inputs
    """

    print()
    print("=" * 70)
    print("TOOL: inspect_page")
    print("=" * 70)


    try:

        result = await browser_service.inspect()


        return json.dumps(
            result,
            indent=2
        )


    except Exception as e:

        return f"Inspection failed: {e}"



# ============================================================
# TOOL — CLICK LINK
# ============================================================

@tool
async def click_link(link_id: int) -> str:
    """
    Click a visible link using the link id returned
    by inspect_page.
    """

    print()
    print("=" * 70)
    print("TOOL: click_link")
    print("=" * 70)


    try:

        result = await browser_service.click_link(
            link_id
        )


        return json.dumps(
            result,
            indent=2
        )


    except Exception as e:

        return f"Click failed: {e}"