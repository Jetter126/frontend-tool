from typing import List


class FrontendDevelopmentPrompts:
    """Collection of prompts for automating frontend development"""

    # Code generation prompts
    CODE_GENERATION_SYSTEM = """You are a frontend developer. Write code for a web development project.
                            You are proficient in all major web development languages, tools, and frameworks.
                            Write concise, correct code that will run without errors."""
    
    @staticmethod
    def code_generation_user(sample_website: str, tech_stack: List[str]) -> str:
        return f"""
                Write code to produce a frontend similar to the one at {sample_website}.
                Do this using this tech stack: {', '.join(tech_stack)}

                Rules:
                - Only write code that runs without errors (e.g. syntax errors)
                - Only use technologies that are present in the given tech stack
                - Your code may span multiple files (e.g. index.html, style.css, script.js)
                - For each file, display the file name (in one line only) and then start writing the code on the next line
                - Write 'FILE ' before each file name
                - Leave a blank line between each file
                - Indent the code correctly, in accordance with each language or framework's convention.

                Example format:
                FILE index.html
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta http-equiv="X-UA-Compatible" content="ie=edge">
                    <title>Home</title>
                    <link rel="stylesheet" href="style.css">
                </head>
                <body>
                    <script src="index.js"></script>
                </body>
                </html>

                FILE style.css
                body {{
                background-color: powderblue;
                }}

                FILE index.js
                document.addEventListener("DOMContentLoaded", function () {{
                    console.log("JavaScript is connected and the DOM is fully loaded.");

                    const heading = document.createElement("h1");
                    heading.textContent = "Welcome to the Home Page!";
                    document.body.appendChild(heading);
                }});
                """