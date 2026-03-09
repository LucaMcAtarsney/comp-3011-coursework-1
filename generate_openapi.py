import json
import subprocess
from main import app

def generate_docs():
    """
    Generates the OpenAPI specification and then uses widdershins
    to convert it into a static Markdown file for the API documentation.
    """
    # 1. Generate openapi.json from the main app
    spec = app.openapi()
    with open("docs/openapi.json", "w") as f:
        json.dump(spec, f, indent=2)
    print("✅ OpenAPI specification generated at docs/openapi.json")

    # 2. Use widdershins to convert the spec into a single Markdown file
    try:
        # The command to run. It reads openapi.json and outputs to api.md
        command = "widdershins --search false --language_tabs 'shell:Shell' 'python:Python' --summary docs/openapi.json -o docs/api.md"
        
        subprocess.run(
            command,
            shell=True, # Use shell=True to handle the command as a string
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Static API documentation generated at docs/api.md using widdershins")
    except subprocess.CalledProcessError as e:
        print("❌ Error generating static Markdown with widdershins.")
        print(e.stderr)
    except FileNotFoundError:
        print("❌ 'widdershins' command not found.")
        print("Please ensure you have installed it with: npm install -g widdershins")


if __name__ == "__main__":
    generate_docs()
