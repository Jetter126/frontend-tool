from utils import find_tech_stack
import json

url = "https://www.github.com/"
result = find_tech_stack(url)
print(result)