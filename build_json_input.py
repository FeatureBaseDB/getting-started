import json
import os
import sys
from github import Github

TIME_FORMAT = "%Y-%m-%dT%H:%S"


class StarTrace:

    def __init__(self, path=os.getcwd(),  token=None):
        self.path = path
        self.token = token

    def search(self, query):
        data = []
        json_input = open(self.get_path("json_input.json"), "w")
        gh = Github(self.token)
        search = gh.search_repositories(query, sort='stars')
        for repo in search:
            field = {}
            field["repo_id"] = repo.id
            languages = repo.get_languages().keys()
            stargazers = repo.get_stargazers_with_dates()
            for lang in languages:
                field["language_id"] = lang

            for stargazer in stargazers:
                field["stargazer_id"] = stargazer.user.id
                field["time_value"] = stargazer.starred_at.strftime("%Y-%m-%dT%H:%S")

            data.append(field)
        input_data = json.dumps(data, indent=4, sort_keys=True)
        json_input.write(input_data)

    def get_path(self, filename):
        return os.path.join(self.path, filename)

def main():
    if len(sys.argv) != 2:
        print("Usage: python fetch.py keyword")
        sys.exit(1)

    if os.path.exists("token"):
        token = open("token").read().strip()
        print("Found the Github API token")
    else:
        token = None
        print("WARNING: No Github API token was found")
    st = StarTrace(token=token)
    st.search(sys.argv[1])

if __name__ == '__main__':
    main()
