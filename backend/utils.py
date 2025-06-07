import requests, os

builtwith_api_key = os.environ["BUILTWITH_API_KEY"]

def clean_url(url: str) -> str | int:
    """Returns a clean version of the input URL (formatted as https://example.com/) or 
    -1 if the input URL doesn't contain a protocol.
    """
    if url.startswith("http://"):
        protocol = "http://"
        url = url[len(protocol):]
    elif url.startswith("https://"):
        protocol = "https://"
        url = url[len(protocol):]
    else:
        return -1
    
    # Remove anything after the domain and www.
    for sep in ["/", "?", "#"]:
        if sep in url:
            url = url.split(sep)[0]
    if url.startswith("www."):
        url = url[len("www."):]

    # Return the clean URL
    return f"{protocol}{url}/"
    

def find_tech_stack(url: str):
    """Uses a website's URL to find the tech stack used to build it"""

    api_url = f"https://api.builtwith.com/free1/api.json?KEY={builtwith_api_key}&LOOKUP={url}"
    response = requests.get(api_url)

    if int(response.status_code / 100) == 2:
        return response.json()
    else:
        print(f"Error {response.status_code}")
        return {}