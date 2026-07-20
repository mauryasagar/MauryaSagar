import requests
import os

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = "mauryasagar"

headers = {"Authorization": f"bearer {TOKEN}"}

query = """
{
  user(login: "mauryasagar") {
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC) {
      totalCount
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoriesWithContributedCommits
    }
    followers {
      totalCount
    }
  }
}
"""

res = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers=headers
).json()

user = res["data"]["user"]
repos = user["repositories"]["totalCount"]
commits = user["contributionsCollection"]["totalCommitContributions"]
prs = user["contributionsCollection"]["totalPullRequestContributions"]
issues = user["contributionsCollection"]["totalIssueContributions"]
repos_contributed = user["contributionsCollection"]["totalRepositoriesWithContributedCommits"]
followers = user["followers"]["totalCount"]

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="220">
  <rect width="600" height="220" fill="transparent"/>

  <text x="0" y="25" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="16" font-weight="bold" fill="#e6edf3">GitHub Stats</text>

  <text x="0" y="60" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">Repositories</text>
  <text x="220" y="60" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">{repos}</text>

  <text x="0" y="90" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">Commits this year</text>
  <text x="220" y="90" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">{commits}</text>

  <text x="0" y="120" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">Pull Requests</text>
  <text x="220" y="120" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">{prs}</text>

  <text x="0" y="150" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">Issues opened</text>
  <text x="220" y="150" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">{issues}</text>

  <text x="0" y="180" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">Repos contributed to</text>
  <text x="220" y="180" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">{repos_contributed}</text>

  <text x="0" y="210" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">Followers</text>
  <text x="220" y="210" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"
    font-size="14" fill="#e6edf3">{followers}</text>

</svg>"""

with open("stats.svg", "w") as f:
    f.write(svg)

print("stats.svg generated!")