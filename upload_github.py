from secreeets import GITHUB_TOKEN
import sys

EXT_ID = sys.argv[1]
NAME = sys.argv[2]

print(EXT_ID)

from github import Github

g = Github(GITHUB_TOKEN)

org = g.get_organization('chrome-exts')


if False:
	for repo in org.get_repos():
		repo.delete()
	lol

org.create_repo(EXT_ID, description=NAME)

