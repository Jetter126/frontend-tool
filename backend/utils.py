from typing import List

import builtwith


def clean_url(url: str) -> str:
    """Returns a clean version of the input URL (formatted as https://example.com/)."""
    # Remove and save protocol
    protocol = "https://"
    if url.startswith("http://"):
        protocol = "http://"
        url = url[len(protocol):]
    elif url.startswith("https://"):
        url = url[len(protocol):]
    
    # Remove anything after the domain and www.
    for sep in ["/", "?", "#"]:
        if sep in url:
            url = url.split(sep)[0]
    if url.startswith("www."):
        url = url[len("www."):]

    # Return the clean URL
    return f"{protocol}{url}/"


def extract_tech_stack(url: str) -> List[str]:
    """Extracts and return the tech stack of a website."""
    results = builtwith.parse(url)
    tech_stack = []

    if results:
        for tools in results.values():
            tech_stack.extend(tools)

    return list(set(tech_stack))