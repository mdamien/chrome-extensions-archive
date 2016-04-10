from secreeets import GITHUB_TOKEN
import sys

import github
from github import Github

g = None
org = None

def create_repo(ext_id, name):
	global g, org
	if not org:
		g = Github(GITHUB_TOKEN)
		org = g.get_organization('chrome-exts')
	try:
		org.create_repo(ext_id, description=name)
	except github.GithubException as e:
		print(e)

if __name__ == '__main__':
	EXT_ID = sys.argv[1]
	NAME = sys.argv[2]

	print(EXT_ID)
	if False:
		for repo in org.get_repos():
			repo.delete()
		lol
	create_repo(EXT_ID, NAME)

