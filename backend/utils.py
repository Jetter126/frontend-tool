import requests, os

builtwith_api_key = os.environ["BUILTWITH_API_KEY"]

def find_tech_stack(url):
    """Uses a website's URL to find the tech stack used to build it"""

    api_url = f"https://api.builtwith.com/free1/api.json?KEY={builtwith_api_key}&LOOKUP={url}"
    response = requests.get(api_url)

    if int(response.status_code / 100) == 2:
        return response.json()
    else:
        print(f"Error {response.status_code}")
        return {}