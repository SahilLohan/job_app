from langchain.tools import tool
# ============================================================
# TOOL — HUMAN INTERVENTION
# ============================================================

@tool
async def request_human_intervention(reason: str) -> str:
    """
    Pause the agent and ask the human to interact with
    the visible browser.

    Use this when the browser encounters CAPTCHA,
    reCAPTCHA, 'I am not a robot', Cloudflare verification,
    login requiring unavailable information, or another
    situation requiring human interaction.

    Never attempt to bypass security challenges.
    """
    global page
    print()
    print()
    print("=" * 70)
    print("!!! HUMAN INTERVENTION REQUIRED !!!")
    print("=" * 70)

    print()
    print("Reason:")
    print(reason)

    print()
    print("The browser is visible.")
    print("Please interact with it yourself.")

    print()
    print(
        "Complete the CAPTCHA / verification / login "
        "or other required interaction."
    )

    input(
        "\nPress ENTER here after you have finished..."
    )

    # Give the browser a moment to settle.
    await page.wait_for_timeout(2000)

    print()
    print("[HUMAN] Interaction completed.")
    print("[AGENT] Continuing...")

    return (
        "Human interaction has been completed. "
        "Inspect the page again before taking another action."
    )

