import os
import re

# Ensure this matches your default branch (main)
REPO_URL = "https://github.com/aranya-code/LeetCode-ProblemSets/tree/main/" 
README_PATH = "README.md"
START_MARKER = "<!---LeetCode Topics Start-->"
END_MARKER = "<!---LeetCode Topics End-->"

def get_problem_folders():
    """Scans the directory for folders formatted as digits-problem-name."""
    # Matches any folder starting with one or more digits followed by a hyphen
    folders = [f for f in os.listdir('.') if os.path.isdir(f) and re.match(r'^\d+-', f)]
    
    # Sorts the folders numerically based on the integer value of the ID
    folders.sort(key=lambda x: int(x.split('-')[0]))
    
    return folders

def format_problem_name(folder_name):
    """Parses folder names and ensures a 4-digit ID format."""
    parts = folder_name.split('-', 1)
    if len(parts) == 2:
        # .zfill(4) ensures '175' becomes '0175' while '0001' stays '0001'
        problem_id = parts[0].zfill(4)
        # Replace hyphens with spaces and capitalize words
        title = parts[1].replace('-', ' ').title()
        return problem_id, title
    return "-", folder_name

def generate_markdown_table(folders):
    """Generates a clean, 3-column markdown table."""
    markdown = "## 📝 All Solved Problems\n\n"
    markdown += "| # | Problem Title | Solution |\n"
    markdown += "| :---: | :--- | :---: |\n"
    
    for folder in folders:
        problem_id, title = format_problem_name(folder)
        markdown += f"| {problem_id} | **{title}** | [💻 View Code]({REPO_URL}{folder}) |\n"
        
    return markdown

def update_readme():
    if not os.path.exists(README_PATH):
        print("README.md not found.")
        return

    with open(README_PATH, 'r', encoding='utf-8') as file:
        readme_content = file.read()

    start_idx = readme_content.find(START_MARKER)
    end_idx = readme_content.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print("Markers not found in README.md. Please ensure the HTML comments are present.")
        return

    folders = get_problem_folders()
    new_table = generate_markdown_table(folders)

    updated_content = (
        readme_content[:start_idx + len(START_MARKER)] + 
        "\n\n" + new_table + "\n" + 
        readme_content[end_idx:]
    )

    with open(README_PATH, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    print(f"Successfully updated README.md with {len(folders)} problems.")

if __name__ == "__main__":
    update_readme()
