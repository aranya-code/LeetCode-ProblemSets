import os
import re
import time
import requests

# Ensure this matches your default branch (main)
REPO_URL = "https://github.com/aranya-code/LeetCode-ProblemSets/tree/main/" 
README_PATH = "README.md"
START_MARKER = "<!---LeetCode Topics Start-->"
END_MARKER = "<!---LeetCode Topics End-->"

# SVG Badge Definitions
BADGE_EASY = "<img src='https://img.shields.io/badge/-Easy-brightgreen'>"
BADGE_MEDIUM = "<img src='https://img.shields.io/badge/-Medium-yellow'>"
BADGE_HARD = "<img src='https://img.shields.io/badge/-Hard-red'>"
BADGE_UNKNOWN = "<img src='https://img.shields.io/badge/-Unknown-lightgrey'>"

def get_difficulty(folder_name):
    """Scans the local README.md inside the problem folder to find the difficulty."""
    local_readme = os.path.join(folder_name, "README.md")
    
    if not os.path.exists(local_readme):
        return BADGE_UNKNOWN

    try:
        with open(local_readme, 'r', encoding='utf-8') as f:
            content = f.read(1000) 
            
            if re.search(r'(?i)Difficulty.*?Easy', content) or "Easy" in content:
                return BADGE_EASY
            elif re.search(r'(?i)Difficulty.*?Medium', content) or "Medium" in content:
                return BADGE_MEDIUM
            elif re.search(r'(?i)Difficulty.*?Hard', content) or "Hard" in content:
                return BADGE_HARD
    except Exception:
        pass
        
    return BADGE_UNKNOWN

def fetch_tags_from_leetcode(slug):
    """Queries LeetCode's GraphQL API to fetch topic tags for a given problem."""
    url = "https://leetcode.com/graphql"
    
    payload = {
        "query": """
            query singleQuestionTopicTags($titleSlug: String!) {
              question(titleSlug: $titleSlug) {
                topicTags {
                  name
                }
              }
            }
        """,
        "variables": {"titleSlug": slug}
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/problems/{slug}/"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and data['data'].get('question'):
                tags = [tag['name'] for tag in data['data']['question']['topicTags']]
                return ", ".join(tags) if tags else "Uncategorized"
    except Exception as e:
        print(f"Failed to fetch tags for {slug}: {e}")
        
    return "Uncategorized"

def get_problem_folders():
    """Scans the directory for folders formatted as digits-problem-name."""
    folders = [f for f in os.listdir('.') if os.path.isdir(f) and re.match(r'^\d+-', f)]
    folders.sort(key=lambda x: int(x.split('-')[0]))
    return folders

def format_problem_name(folder_name):
    """Parses folder names and retrieves dynamically generated difficulty and tags."""
    parts = folder_name.split('-', 1)
    if len(parts) == 2:
        problem_id = parts[0].zfill(4)
        slug = parts[1]
        
        # Format title
        title = slug.replace('-', ' ').title()
        
        # Scrape difficulty from local file
        difficulty = get_difficulty(folder_name)
        
        # Fetch tags via GraphQL and throttle slightly to avoid rate limits
        tags = fetch_tags_from_leetcode(slug)
        time.sleep(0.5) 
        
        return problem_id, title, difficulty, tags, slug
    return "-", folder_name, BADGE_UNKNOWN, "Uncategorized", folder_name

def generate_markdown_table(folders):
    """Generates a clean, 5-column markdown table including dynamic SVG difficulty badges."""
    markdown = "## 📝 All Solved Problems\n\n"
    markdown += "| # | Problem Title | Difficulty | Topic Tags | Solution |\n"
    markdown += "| :---: | :--- | :---: | :--- | :---: |\n"
    
    seen_ids = set()
    
    for folder in folders:
        problem_id, title, difficulty, tags, slug = format_problem_name(folder)
        
        if problem_id in seen_ids:
            continue
        seen_ids.add(problem_id)
        
        formatted_tags = " ".join([f"`{tag.strip()}`" for tag in tags.split(',')]) if tags != "Uncategorized" else "`Uncategorized`"
        
        markdown += f"| {problem_id} | **{title}** | {difficulty} | {formatted_tags} | [💻&nbsp;View&nbsp;Code]({REPO_URL}{folder}) |\n"
        
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
    print(f"Processing {len(folders)} folders...")
    new_table = generate_markdown_table(folders)

    updated_content = (
        readme_content[:start_idx + len(START_MARKER)] + 
        "\n\n" + new_table + "\n" + 
        readme_content[end_idx:]
    )

    with open(README_PATH, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    print("Successfully updated README.md.")

if __name__ == "__main__":
    update_readme()
