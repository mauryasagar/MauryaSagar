import requests
import os
from datetime import datetime, timezone, timedelta

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = "mauryasagar"

headers = {"Authorization": f"bearer {TOKEN}"}

now = datetime.now(timezone.utc)
one_year_ago = (now - timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
today = now.strftime("%Y-%m-%dT%H:%M:%SZ")

query = f"""
{{
  user(login: "mauryasagar") {{
    contributionsCollection(from: "{one_year_ago}", to: "{today}") {{
      totalPullRequestContributions
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
    issues(filterBy: {{createdBy: "mauryasagar"}}) {{
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
total_contributions = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
issues = user["issues"]["totalCount"]

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

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 185" width="500">
  <rect width="500" height="185" fill="transparent"/>

  <text x="0" y="20" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    font-size="14" font-weight="600" fill="#e6edf3">GitHub Stats</text>

  <text x="0" y="52" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    font-size="13" fill="#e6edf3">Contributions</text>
  <text x="200" y="52" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    font-size="13" fill="#e6edf3">{total_contributions}</text>

  <text x="0" y="82" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    font-size="13" fill="#e6edf3">Current Streak</text>
  <text x="200" y="82" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    font-size="13" fill="#e6edf3">{streak} days</text>

  <text x="0" y="112" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    font-size="13" fill="#e6edf3">Longest Streak</text>
  <text x="200" y="112" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    font-size="13" fill="#e6edf3">{longest} days</text>

  <text x="0" y="142" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    font-size="13" fill="#e6edf3">Pull Requests</text>
  <text x="200" y="142" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    font-size="13" fill="#e6edf3">{prs}</text>

  <text x="0" y="172" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    font-size="13" fill="#e6edf3">Issues opened</text>
  <text x="200" y="172" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"
    font-size="13" fill="#e6edf3">{issues}</text>

</svg>"""

with open("stats.svg", "w") as f:
    f.write(svg)

print(f"Done! Contributions: {total_contributions}, Streak: {streak}, Longest: {longest}, PRs: {prs}, Issues: {issues}")