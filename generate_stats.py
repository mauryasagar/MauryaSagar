import requests
import os
from datetime import datetime, timezone

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = "mauryasagar"

headers = {"Authorization": f"bearer {TOKEN}"}

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
      totalPullRequestContributions
      totalIssueContributions
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
prs = user["contributionsCollection"]["totalPullRequestContributions"]
issues = user["contributionsCollection"]["totalIssueContributions"]
total_contributions = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]

# Build days list
weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
all_days = []
for week in weeks:
    for day in week["contributionDays"]:
        all_days.append(day)

all_days.sort(key=lambda x: x["date"])

# Current streak
all_days_desc = list(reversed(all_days))
streak = 0
for day in all_days_desc:
    if day["date"] > now.strftime("%Y-%m-%d"):
        continue
    if day["contributionCount"] > 0:
        streak += 1
    else:
        break

# Longest streak
longest = 0
current = 0
for day in all_days:
    if day["contributionCount"] > 0:
        current += 1
        longest = max(longest, current)
    else:
        current = 0

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 230" width="100%" height="auto">
  <rect width="600" height="230" fill="transparent"/>

  <text x="0" y="25" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="18" font-weight="bold" fill="#e6edf3">GitHub Stats</text>

  <text x="0" y="65" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" fill="#e6edf3">Contributions</text>
  <text x="250" y="65" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" fill="#e6edf3">{total_contributions}</text>

  <text x="0" y="100" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" fill="#e6edf3">Current Streak</text>
  <text x="250" y="100" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" fill="#e6edf3">{streak} days</text>

  <text x="0" y="135" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" fill="#e6edf3">Streak</text>
  <text x="250" y="135" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" fill="#e6edf3">{longest} days</text>

  <text x="0" y="170" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" fill="#e6edf3">Pull Requests</text>
  <text x="250" y="170" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" fill="#e6edf3">{prs}</text>

  <text x="0" y="205" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" fill="#e6edf3">Issues opened</text>
  <text x="250" y="205" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" fill="#e6edf3">{issues}</text>

</svg>"""

with open("stats.svg", "w") as f:
    f.write(svg)

print(f"Done! Contributions: {total_contributions}, Streak: {streak}, Longest: {longest}")