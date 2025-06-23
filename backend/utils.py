import os
from typing import Dict, List

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


def parse_generated_code(code: str) -> Dict[str, str]:
    """Parses LLM-generated frontend code into a dictionary with a key for each code file."""
    lines = code.strip().splitlines()
    result = {}
    current_file = None
    current_lines = []

    for line in lines:
        if line.strip().startswith("FILE "):
            if current_file is not None:
                result[current_file] = '\n'.join(current_lines).strip()
            current_file = line.strip()[5:]
            current_lines = []
        else:
            current_lines.append(line)

    if current_file is not None:
        result[current_file] = '\n'.join(current_lines).strip()

    return result


def write_generated_code(current_dir: str, base_output_dir: str, filename: str, content: str) -> None:
    """Writes LLM-generated `content` into the file `base_output_dir`/`filename`."""
    os.chdir(current_dir)
    if "/" in filename:
        split_path = filename.split("/")
        output_dir = base_output_dir
        for dir in split_path[:-1]:
            if dir not in os.listdir(output_dir):
                os.chdir(output_dir)
                os.mkdir(dir)
            output_dir = os.path.join(output_dir, dir)
        with open(os.path.join(output_dir, split_path[-1]), "w") as file:
            file.write(content)
    else:
        with open(os.path.join(base_output_dir, filename), "w") as file:
            file.write(content)