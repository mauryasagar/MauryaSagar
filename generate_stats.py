import requests
import os

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = "mauryasagar"

headers = {"Authorization": f"bearer {TOKEN}"}

query = """
{
  user(login: "mauryasagar") {
    repositories(ownerAffiliations: OWNER) {
      totalCount
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
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

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="160">
  <rect width="600" height="160" fill="transparent"/>

  <text x="0" y="25" font-family="monospace" font-size="16"
    font-weight="bold" fill="#58a6ff">&#128202; GitHub Stats</text>

  <text x="0" y="60" font-family="monospace" font-size="14" fill="#e6edf3">Repositories:</text>
  <text x="180" y="60" font-family="monospace" font-size="14" fill="#58a6ff" font-weight="bold">{repos}</text>

  <text x="0" y="90" font-family="monospace" font-size="14" fill="#e6edf3">Commits this year:</text>
  <text x="180" y="90" font-family="monospace" font-size="14" fill="#3fb950" font-weight="bold">{commits}</text>

  <text x="0" y="120" font-family="monospace" font-size="14" fill="#e6edf3">Pull Requests:</text>
  <text x="180" y="120" font-family="monospace" font-size="14" fill="#bc8cff" font-weight="bold">{prs}</text>

</svg>"""

with open("stats.svg", "w") as f:
    f.write(svg)

print("stats.svg generated!")