import os
import re

# Ensure this matches your default branch (main)
REPO_URL = "https://github.com/aranya-code/LeetCode-ProblemSets/tree/main/" 
README_PATH = "README.md"
START_MARKER = "<!---LeetCode Topics Start-->"
END_MARKER = "<!---LeetCode Topics End-->"

# Dictionary mapping problem slugs to (Difficulty, Topic Tags)
PROBLEM_DATA = {
    "two-sum": ("🟢 Easy", "Array, Hash Table"),
    "add-two-numbers": ("🟡 Medium", "Linked List, Math, Recursion"),
    "palindrome-number": ("🟢 Easy", "Math"),
    "remove-nth-node-from-end-of-list": ("🟡 Medium", "Linked List, Two Pointers"),
    "merge-two-sorted-lists": ("🟢 Easy", "Linked List, Recursion"),
    "remove-element": ("🟢 Easy", "Array, Two Pointers"),
    "rotate-image": ("🟡 Medium", "Array, Math, Matrix"),
    "plus-one": ("🟢 Easy", "Array, Math"),
    "remove-duplicates-from-sorted-list-ii": ("🟡 Medium", "Linked List, Two Pointers"),
    "remove-duplicates-from-sorted-list": ("🟢 Easy", "Linked List"),
    "partition-list": ("🟡 Medium", "Linked List, Two Pointers"),
    "same-tree": ("🟢 Easy", "Tree, Depth-First Search, Breadth-First Search"),
    "intersection-of-two-linked-lists": ("🟢 Easy", "Hash Table, Linked List, Two Pointers"),
    "rotate-array": ("🟡 Medium", "Array, Math, Two Pointers"),
    "remove-linked-list-elements": ("🟢 Easy", "Linked List, Recursion"),
    "reverse-linked-list": ("🟢 Easy", "Linked List, Recursion"),
    "contains-duplicate": ("🟢 Easy", "Array, Hash Table, Sorting"),
    "palindrome-linked-list": ("🟢 Easy", "Linked List, Two Pointers, Stack, Recursion"),
    "missing-number": ("🟢 Easy", "Array, Hash Table, Math, Binary Search, Bit Manipulation"),
    "third-maximum-number": ("🟢 Easy", "Array, Sorting"),
    "middle-of-the-linked-list": ("🟢 Easy", "Linked List, Two Pointers"),
    "maximum-product-of-two-elements-in-an-array": ("🟢 Easy", "Array, Sorting, Heap"),
    "find-the-winner-of-the-circular-game": ("🟡 Medium", "Array, Math, Recursion, Queue, Simulation"),
    "combine-two-tables": ("🟢 Easy", "Database")
}

def get_problem_folders():
    """Scans the directory for folders formatted as digits-problem-name."""
    folders = [f for f in os.listdir('.') if os.path.isdir(f) and re.match(r'^\d+-', f)]
    folders.sort(key=lambda x: int(x.split('-')[0]))
    return folders

def format_problem_name(folder_name):
    """Parses folder names and retrieves associated difficulty and tags."""
    parts = folder_name.split('-', 1)
    if len(parts) == 2:
        problem_id = parts[0].zfill(4)
        slug = parts[1]
        
        # Format title and fetch data
        title = slug.replace('-', ' ').title()
        difficulty, tags = PROBLEM_DATA.get(slug, ("⚪ Unknown", "Uncategorized"))
        
        return problem_id, title, difficulty, tags, slug
    return "-", folder_name, "⚪ Unknown", "Uncategorized", folder_name

def generate_markdown_table(folders):
    """Generates a clean, 5-column markdown table including difficulty and tags."""
    markdown = "## 📝 All Solved Problems\n\n"
    markdown += "| # | Problem Title | Difficulty | Topic Tags | Solution |\n"
    markdown += "| :---: | :--- | :---: | :--- | :---: |\n"
    
    seen_ids = set()
    
    for folder in folders:
        problem_id, title, difficulty, tags, slug = format_problem_name(folder)
        
        # Skip this iteration if we already added a folder for this problem ID
        if problem_id in seen_ids:
            continue
        seen_ids.add(problem_id)
        
        # Inject non-breaking spaces to prevent GitHub from wrapping the text
        difficulty_nowrap = difficulty.replace(" ", "&nbsp;")
        
        # Format tags with inline code blocks for a clean UI look
        formatted_tags = " ".join([f"`{tag.strip()}`" for tag in tags.split(',')]) if tags != "Uncategorized" else "`Uncategorized`"
        
        # Added non-breaking spaces to "View Code" as well to keep it perfectly aligned
        markdown += f"| {problem_id} | **{title}** | {difficulty_nowrap} | {formatted_tags} | [💻&nbsp;View&nbsp;Code]({REPO_URL}{folder}) |\n"
        
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
    print(f"Successfully updated README.md with {len(seen_ids)} unique problems.")

if __name__ == "__main__":
    update_readme()
