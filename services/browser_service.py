from playwright.async_api import (
    async_playwright,
    Browser,
    Page,
    Playwright,
)


class BrowserService:

    def __init__(self):

        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.page: Page | None = None


    # ========================================================
    # START BROWSER
    # ========================================================

    async def start(self):
        print("Inside browser service starter ...")
        if self.browser is not None:
            return


        self.playwright = await async_playwright().start()


        self.browser = await self.playwright.chromium.launch(
            headless=False,
            slow_mo=300,
        )


        self.page = await self.browser.new_page()



    # ========================================================
    # OPEN URL
    # ========================================================

    async def open(self, url: str):

        if self.page is None:
            raise Exception(
                "Browser is not initialized"
            )


        await self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000,
        )


        await self.page.wait_for_timeout(
            2000
        )


        return {
            "success": True,
            "url": self.page.url,
            "title": await self.page.title(),
        }



    # ========================================================
    # INSPECT CURRENT PAGE
    # ========================================================

    async def inspect(self):

        if self.page is None:
            raise Exception(
                "Browser is not initialized"
            )


        title = await self.page.title()


        body_text = await self.page.locator(
            "body"
        ).inner_text()


        # Limit size sent to LLM
        body_text = body_text[:12000]



        # -------------------------------
        # Visible links
        # -------------------------------

        links = await self.page.locator(
            "a:visible"
        ).evaluate_all(
            """
            anchors => anchors
                .map((a, index) => ({
                    id: index,
                    text: (a.innerText || a.textContent || "").trim(),
                    href: a.href
                }))
                .filter(x => x.text || x.href)
                .slice(0, 100)
            """
        )



        # -------------------------------
        # Visible buttons
        # -------------------------------

        buttons = await self.page.locator(
            "button:visible"
        ).evaluate_all(
            """
            buttons => buttons
                .map((b, index) => ({
                    id: index,
                    text: (b.innerText || b.textContent || "").trim()
                }))
                .filter(x => x.text)
                .slice(0, 50)
            """
        )



        # -------------------------------
        # Visible inputs
        # -------------------------------

        inputs = await self.page.locator(
            "input:visible"
        ).evaluate_all(
            """
            inputs => inputs
                .map((input, index) => ({
                    id: index,
                    type: input.type,
                    name: input.name,
                    placeholder: input.placeholder,
                    value: input.value
                }))
                .slice(0, 50)
            """
        )



        return {
            "url": self.page.url,
            "title": title,
            "text": body_text,
            "links": links,
            "buttons": buttons,
            "inputs": inputs,
        }




    # ========================================================
    # CLICK LINK BY ID
    # ========================================================

    async def click_link(self, link_id: int):

        if self.page is None:
            raise Exception(
                "Browser is not initialized"
            )


        links = await self.page.locator(
            "a:visible"
        ).all()



        if link_id < 0 or link_id >= len(links):

            return {
                "success": False,
                "error": (
                    f"Invalid link id {link_id}. "
                    f"Available: 0-{len(links)-1}"
                )
            }



        link = links[link_id]


        text = (
            await link.inner_text()
        ).strip()


        href = await link.get_attribute(
            "href"
        )



        await link.click()


        await self.page.wait_for_timeout(
            2000
        )



        return {
            "success": True,
            "clicked_text": text,
            "href": href,
            "url": self.page.url,
            "title": await self.page.title(),
        }



    # ========================================================
    # CURRENT PAGE INFO
    # ========================================================

    async def current_url(self):

        if self.page:
            return self.page.url

        return None



    # ========================================================
    # CLOSE BROWSER
    # ========================================================

    async def close(self):

        if self.browser:

            await self.browser.close()


        if self.playwright:

            await self.playwright.stop()



# ============================================================
# SINGLE SHARED INSTANCE
# ============================================================

browser_service = BrowserService()