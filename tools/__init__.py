from tools.browser_tools import (
    open_url,
    inspect_page,
    click_link
)

from tools.search_tools import (
    web_search
)

from tools.human_tools import (
    request_human_intervention
)


tools = [
    web_search,

    open_url,
    inspect_page,
    click_link,

    request_human_intervention
]