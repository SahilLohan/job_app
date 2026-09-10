import asyncio
from dotenv import load_dotenv

from services.browser_service import browser_service
from agents.career_page_agent import CareerPageAgent


load_dotenv()


careerPageAgent = CareerPageAgent()


# ============================================================
# MAIN
# ============================================================

async def main():
    company = input(
        "Enter company name: "
    ).strip()

    if not company:
        print("Company name cannot be empty.")
        return


    print()
    print("[SYSTEM] Starting browser...")

    await browser_service.start()

    print("[SYSTEM] Browser started.")


    task = f"""
Find the official careers/jobs page for:

{company}

Your final answer must contain the official career page URL.

Follow this strategy:

1. Search for the company's official careers page.
2. Examine the search results.
3. Open the most likely official result.
4. Inspect the resulting page.
5. Verify that it is actually the company's careers/jobs page.

6. If you encounter:
   - CAPTCHA
   - reCAPTCHA
   - "I am not a robot"
   - Cloudflare verification
   - suspicious traffic verification
   - any security challenge

   STOP and use the request_human_intervention tool.

7. After human intervention, inspect the page again.

8. Do not claim success unless the page is actually the
   company's official careers/jobs page.

Do not bypass CAPTCHAs or security controls.
"""


    print()
    print("=" * 70)
    print("STARTING AGENT")
    print("=" * 70)

    print(
        f"\nGoal: Find {company}'s official career page\n"
    )


    # result = await careerPageAgent.ainvoke(task)


    # print()
    # print("=" * 70)
    # print("AGENT FINISHED")
    # print("=" * 70)


    # final_message = result["messages"][-1]


    # print()
    # print(final_message.content)
    async for chunk in careerPageAgent._agent.astream(
    {
        "messages": [
            {
                "role": "user",
                "content": task
            }
        ]
    }
):

        print(chunk)

    print()
    print(
        f"Current browser URL: {browser_service.page.url}"
    )


    print()
    print("Press ENTER to close the browser...")

    input()


    await browser_service.close()



# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())