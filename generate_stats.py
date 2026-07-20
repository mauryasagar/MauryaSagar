import requests
import os
from datetime import datetime, timezone

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = "mauryasagar"

headers = {"Authorization": f"bearer {TOKEN}"}

# Get current year date range
now = datetime.now(timezone.utc)
start_of_year = f"{now.year}-01-01T00:00:00Z"
today = now.strftime("%Y-%m-%dT%H:%M:%SZ")

query = f"""
{{
  user(login: "mauryasagar") {{
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC) {{
      totalCount
    }}
    contributionsCollection(from: "{start_of_year}", to: "{today}") {{
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoriesWithContributedCommits
      contributionCalendar {{
        totalContributions
        weeks {{
          contributionDays {{
            contributionCount
            date
          }}
        }}
      }}
    }}
    followers {{
      totalCount
    }}
  }}
}}
"""

res = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers=headers
).json()

user = res["data"]["user"]
repos = user["repositories"]["totalCount"]
prs = user["contributionsCollection"]["totalPullRequestContributions"]
issues = user["contributionsCollection"]["totalIssueContributions"]
repos_contributed = user["contributionsCollection"]["totalRepositoriesWithContributedCommits"]
followers = user["followers"]["totalCount"]
total_contributions = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]

# Calculate current streak
weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
all_days = []
for week in weeks:
    for day in week["contributionDays"]:
        all_days.append(day)

# Sort by date descending
all_days.sort(key=lambda x: x["date"], reverse=True)

# Count streak from today backwards
streak = 0
for day in all_days:
    if day["date"] > now.strftime("%Y-%m-%d"):
        continue
    if day["contributionCount"] > 0:
        streak += 1
    else:
        break

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="180">
  <rect width="600" height="180" fill="transparent"/>

  <text x="0" y="25" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" font-weight="bold" fill="#e6edf3">GitHub Stats</text>

  <text x="0" y="60" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">Total contributions this year</text>
  <text x="250" y="60" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">{total_contributions}</text>

  <text x="0" y="90" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">Current streak</text>
  <text x="250" y="90" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">{streak} days</text>

  <text x="0" y="120" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">Pull Requests</text>
  <text x="250" y="120" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">{prs}</text>

  <text x="0" y="150" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">Issues opened</text>
  <text x="250" y="150" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">{issues}</text>

  <text x="0" y="180" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">Repos contributed to</text>
  <text x="250" y="180" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">{repos_contributed}</text>

</svg>"""

with open("stats.svg", "w") as f:
    f.write(svg)

print(f"Done! Contributions: {total_contributions}, Streak: {streak} days")