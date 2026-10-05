import os
import re
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import requests


# ============================================================
# Configuration
# ============================================================

REPO_URL = "https://github.com/aranya-code/LeetCode-ProblemSets/tree/main/"
README_PATH = "README.md"

START_MARKER = "<!---LeetCode Topics Start-->"
END_MARKER = "<!---LeetCode Topics End-->"

ACTIVITY_START_MARKER = "<!---LeetCode Activity Start-->"
ACTIVITY_END_MARKER = "<!---LeetCode Activity End-->"

LEETCODE_USERNAME = "aranya-code"

# Display dates in Indian Standard Time
DISPLAY_TIMEZONE = ZoneInfo("Asia/Kolkata")

# Number of recent LeetCode submissions to display
RECENT_SUBMISSIONS_LIMIT = 10


# ============================================================
# SVG Badge Definitions
# ============================================================

BADGE_EASY = "<img src='https://img.shields.io/badge/-Easy-brightgreen'>"
BADGE_MEDIUM = "<img src='https://img.shields.io/badge/-Medium-yellow'>"
BADGE_HARD = "<img src='https://img.shields.io/badge/-Hard-red'>"
BADGE_UNKNOWN = "<img src='https://img.shields.io/badge/-Unknown-lightgrey'>"


# ============================================================
# Difficulty
# ============================================================

def get_difficulty(folder_name):
    """
    Scans the local README.md inside the problem folder
    to find the difficulty.
    """

    local_readme = os.path.join(folder_name, "README.md")

    if not os.path.exists(local_readme):
        return BADGE_UNKNOWN

    try:
        with open(local_readme, "r", encoding="utf-8") as f:
            content = f.read(1000)

            if re.search(r"(?i)Difficulty.*?Easy", content) or "Easy" in content:
                return BADGE_EASY

            elif re.search(r"(?i)Difficulty.*?Medium", content) or "Medium" in content:
                return BADGE_MEDIUM

            elif re.search(r"(?i)Difficulty.*?Hard", content) or "Hard" in content:
                return BADGE_HARD

    except Exception:
        pass

    return BADGE_UNKNOWN


# ============================================================
# LeetCode Topic Tags
# ============================================================

def fetch_tags_from_leetcode(slug):
    """
    Queries LeetCode's GraphQL API to fetch topic tags
    for a given problem.
    """

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
        "variables": {
            "titleSlug": slug
        }
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/problems/{slug}/"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            if data.get("data") and data["data"].get("question"):
                tags = [
                    tag["name"]
                    for tag in data["data"]["question"]["topicTags"]
                ]

                return ", ".join(tags) if tags else "Uncategorized"

    except Exception as e:
        print(f"Failed to fetch tags for {slug}: {e}")

    return "Uncategorized"


# ============================================================
# Problem Folders
# ============================================================

def get_problem_folders():
    """
    Scans the directory for folders formatted as digits-problem-name.
    """

    folders = [
        f
        for f in os.listdir(".")
        if os.path.isdir(f) and re.match(r"^\d+-", f)
    ]

    folders.sort(
        key=lambda x: int(x.split("-")[0])
    )

    return folders


# ============================================================
# Problem Formatting
# ============================================================

def format_problem_name(folder_name):
    """
    Parses folder names and retrieves dynamically generated
    difficulty and tags.
    """

    parts = folder_name.split("-", 1)

    if len(parts) == 2:
        problem_id = parts[0].zfill(4)
        slug = parts[1]

        title = slug.replace("-", " ").title()

        difficulty = get_difficulty(folder_name)

        tags = fetch_tags_from_leetcode(slug)

        time.sleep(0.5)

        return problem_id, title, difficulty, tags, slug

    return "-", folder_name, BADGE_UNKNOWN, "Uncategorized", folder_name


# ============================================================
# Solved Problems Table
# ============================================================

def generate_markdown_table(folders):
    """
    Generates the complete solved-problems markdown table.
    """

    markdown = "## 📝 All Solved Problems\n\n"

    markdown += (
        "| # | Problem Title | Difficulty | Topic Tags | Solution |\n"
    )

    markdown += (
        "| :---: | :--- | :---: | :--- | :---: |\n"
    )

    seen_ids = set()

    for folder in folders:

        problem_id, title, difficulty, tags, slug = format_problem_name(folder)

        if problem_id in seen_ids:
            continue

        seen_ids.add(problem_id)

        if tags != "Uncategorized":
            formatted_tags = " ".join(
                [f"`{tag.strip()}`" for tag in tags.split(",")]
            )
        else:
            formatted_tags = "`Uncategorized`"

        markdown += (
            f"| {problem_id} | "
            f"**{title}** | "
            f"{difficulty} | "
            f"{formatted_tags} | "
            f"[💻&nbsp;View&nbsp;Code]({REPO_URL}{folder}) |\n"
        )

    return markdown


# ============================================================
# Recent LeetCode Activity
# ============================================================

def fetch_recent_submissions():
    """
    Fetches the user's recent LeetCode submissions.

    LeetCode returns the actual submission timestamp, so the
    README date does NOT depend on when GitHub Actions runs.
    """

    url = "https://leetcode.com/graphql"

    payload = {
        "query": """
            query recentAcSubmissionList(
                $username: String!
                $limit: Int!
            ) {
                recentAcSubmissionList(
                    username: $username
                    limit: $limit
                ) {
                    title
                    titleSlug
                    statusDisplay
                    lang
                    timestamp
                }
            }
        """,
        "variables": {
            "username": LEETCODE_USERNAME,
            "limit": RECENT_SUBMISSIONS_LIMIT
        }
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/{LEETCODE_USERNAME}/"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        submissions = (
            data
            .get("data", {})
            .get("recentAcSubmissionList", [])
        )

        return submissions

    except Exception as e:
        print(f"Failed to fetch recent LeetCode submissions: {e}")
        return []


def format_submission_date(timestamp):
    """
    Converts the LeetCode Unix timestamp into:

        DD-MMM-YYYY

    Example:

        05-Oct-2026
    """

    try:
        submission_time = datetime.fromtimestamp(
            int(timestamp),
            tz=timezone.utc
        )

        local_time = submission_time.astimezone(
            DISPLAY_TIMEZONE
        )

        return local_time.strftime("%d-%b-%Y")

    except Exception:
        return "Unknown"


def format_status(status):
    """
    Adds a simple visual indicator to the submission status.
    """

    status_upper = status.upper()

    if status_upper == "ACCEPTED":
        return "✅ Accepted"

    if status_upper == "TLE":
        return "⏱️ TLE"

    if status_upper == "WRONG ANSWER":
        return "❌ Wrong Answer"

    if status_upper == "RUNTIME ERROR":
        return "💥 Runtime Error"

    if status_upper == "MEMORY LIMIT EXCEEDED":
        return "💾 Memory Limit"

    return status


def generate_activity_table():
    """
    Generates the Recent Activities section using actual
    LeetCode submission timestamps.
    """

    submissions = fetch_recent_submissions()

    markdown = "## 🕒 Recent Activities\n\n"

    markdown += (
        "| Date | Status | Problem | Language |\n"
    )

    markdown += (
        "| :---: | :---: | :--- | :---: |\n"
    )

    if not submissions:
        markdown += (
            "| - | - | Unable to fetch recent LeetCode activity | - |\n"
        )

        return markdown

    for submission in submissions:

        date = format_submission_date(
            submission.get("timestamp", "")
        )

        status = format_status(
            submission.get("statusDisplay", "Unknown")
        )

        title = submission.get(
            "title",
            "Unknown Problem"
        )

        title_slug = submission.get(
            "titleSlug",
            ""
        )

        language = submission.get(
            "lang",
            "Unknown"
        )

        if title_slug:
            problem_link = (
                f"[{title}]"
                f"(https://leetcode.com/problems/{title_slug}/)"
            )
        else:
            problem_link = title

        markdown += (
            f"| {date} | "
            f"{status} | "
            f"{problem_link} | "
            f"{language} |\n"
        )

    return markdown


# ============================================================
# README Activity Section
# ============================================================

def update_activity_section(readme_content):
    """
    Replaces the Recent Activities section.

    If the markers don't exist yet, the section is inserted
    before the Solutions Table.
    """

    activity_table = generate_activity_table()

    start_idx = readme_content.find(
        ACTIVITY_START_MARKER
    )

    end_idx = readme_content.find(
        ACTIVITY_END_MARKER
    )

    if start_idx != -1 and end_idx != -1:

        return (
            readme_content[:start_idx + len(ACTIVITY_START_MARKER)]
            + "\n\n"
            + activity_table
            + "\n"
            + readme_content[end_idx:]
        )

    # Insert the activity section before Solutions Table
    solutions_marker = "\n---\n\n## 📂 Solutions Table"

    if solutions_marker in readme_content:

        activity_section = (
            "\n"
            + ACTIVITY_START_MARKER
            + "\n\n"
            + activity_table
            + "\n"
            + ACTIVITY_END_MARKER
            + "\n"
        )

        return readme_content.replace(
            solutions_marker,
            activity_section + solutions_marker,
            1
        )

    print(
        "Could not find Solutions Table location. "
        "Recent Activities section was not inserted."
    )

    return readme_content


# ============================================================
# README Update
# ============================================================

def update_readme():

    if not os.path.exists(README_PATH):
        print("README.md not found.")
        return

    with open(
        README_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        readme_content = file.read()

    # --------------------------------------------------------
    # Update All Solved Problems
    # --------------------------------------------------------

    start_idx = readme_content.find(
        START_MARKER
    )

    end_idx = readme_content.find(
        END_MARKER
    )

    if start_idx == -1 or end_idx == -1:

        print(
            "Markers not found in README.md. "
            "Please ensure the HTML comments are present."
        )

        return

    folders = get_problem_folders()

    print(
        f"Processing {len(folders)} folders..."
    )

    new_table = generate_markdown_table(
        folders
    )

    updated_content = (
        readme_content[:start_idx + len(START_MARKER)]
        + "\n\n"
        + new_table
        + "\n"
        + readme_content[end_idx:]
    )

    # --------------------------------------------------------
    # Update Recent Activities
    # --------------------------------------------------------

    updated_content = update_activity_section(
        updated_content
    )

    # --------------------------------------------------------
    # Write README
    # --------------------------------------------------------

    with open(
        README_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            updated_content
        )

    print(
        "Successfully updated README.md."
    )


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    update_readme()
