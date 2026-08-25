import os
import re

# Your repository base URL
REPO_URL = "https://github.com/aranya-code/LeetCode-ProblemSets/tree/master/"
README_PATH = "README.md"
START_MARKER = "<!---LeetCode Topics Start-->"
END_MARKER = "<!---LeetCode Topics End-->"

def get_problem_folders():
    """Scans the directory for folders formatted as XXXX-problem-name."""
    folders = [f for f in os.listdir('.') if os.path.isdir(f) and re.match(r'^\d{4}-', f)]
    folders.sort() # Sorts them by problem number
    return folders

def generate_markdown_table(folders):
    """Generates the markdown table for the README."""
    markdown = "## All Solved Problems\n"
    markdown += "| Problem |\n| ------- |\n"
    for folder in folders:
        markdown += f"| [{folder}]({REPO_URL}{folder}) |\n"
    return markdown

def update_readme():
    """Replaces the content between the markers in the README."""
    if not os.path.exists(README_PATH):
        print("README.md not found.")
        return

    with open(README_PATH, 'r') as file:
        readme_content = file.read()

    # Find the positions of the markers
    start_idx = readme_content.find(START_MARKER)
    end_idx = readme_content.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print("Markers not found in README.md. Please ensure the HTML comments are present.")
        return

    # Generate new content
    folders = get_problem_folders()
    new_table = generate_markdown_table(folders)

    # Rebuild the README string
    updated_content = (
        readme_content[:start_idx + len(START_MARKER)] + 
        "\n" + new_table + 
        readme_content[end_idx:]
    )

    with open(README_PATH, 'w') as file:
        file.write(updated_content)
    print(f"Successfully updated README.md with {len(folders)} problems.")

if __name__ == "__main__":
    update_readme()
