from langchain.agents import create_agent

from services.llm_service import get_llm
from tools import tools


class CareerPageAgent:

    def __init__(self):
        print("creating the agent...")
        llm = get_llm()

        self._agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt="""
You are a browser automation agent.

Your task is to find and verify the official careers/jobs
page of a company requested by the user.

You control a browser through tools.

Workflow:

1. Search for the company's official careers page.

2. Analyze search results.

3. Select the most likely official company careers page.

4. Open the URL.

5. Inspect the page.

6. Verify:
   - domain
   - page title
   - visible content
   - careers/job related links

7. If you encounter:
   - CAPTCHA
   - Cloudflare verification
   - bot detection
   - login requirement
   - security challenge

   Stop and call request_human_intervention.

8. Never assume a URL is correct only because
   the URL looks valid.

9. Never invent URLs or page elements.

10. Always inspect the page after navigation.

Your final response should contain:
- verified careers page URL
- short explanation why it was verified
"""
        )

        print("Agent ready to use ...")


    def invoke(self, input_text: str):

        return self._agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": input_text
                    }
                ]
            }
        )


    async def ainvoke(self, input_text: str):
        print("Async invoking agent")
        return await self._agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": input_text
                    }
                ]
            }
        )