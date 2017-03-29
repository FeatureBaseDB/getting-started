
import os
from github import Github

TIME_FORMAT = "%Y-%m-%dT%H:%S"


class StarTrace:

    def __init__(self, path=os.getcwd(),  token=None):
        self.path = path
        self.token = token
        # external ID to project ID (internal)
        self.e2p = {}
        # external ID to stargazer ID (internal)
        self.e2s = {}
        # language to language ID (internal)
        self.e2l = {}

    def search(self, query):
        stargazer_frame = open(self.get_path("project-stargazer.csv"), "w")
        language_frame = open(self.get_path("project-language.csv"), "w")

        try:
            gh = Github(self.token)
            search = gh.search_repositories(query, sort='stars')
            for i, repo in enumerate(search):
                print(i, repo.id)
                project_id = self.add_or_get_project(repo.id)
                for lang in repo.get_languages().keys():
                    language_frame.write("{lang_id},{project_id}\n".format(
                        lang_id=self.add_or_get_language(lang),
                        project_id=project_id
                    ))
                for stargazer in repo.get_stargazers_with_dates():
                    stargazer_frame.write("{stargazer_id},{project_id},{starred_at}\n".format(
                        stargazer_id=self.add_or_get_stargazer(stargazer.user.id),
                        project_id=project_id,
                        starred_at=stargazer.starred_at.strftime("%Y-%m-%dT%H:%S")
                    ))
        finally:
            stargazer_frame.close()
            language_frame.close()

            with open(self.get_path("languages.txt"), "w") as f:
                f.write('\n'.join(k for k, v in sorted(self.e2l.items(), key=lambda kv: kv[1])))

    def add_or_get_project(self, repo_id):
        return self._add_or_get(repo_id, self.e2p)

    def add_or_get_stargazer(self, user_id):
        return self._add_or_get(user_id, self.e2s)

    def add_or_get_language(self, language):
        return self._add_or_get(language, self.e2l)

    def get_path(self, filename):
        return os.path.join(self.path, filename)

    @classmethod
    def _add_or_get(cls, external_id, store):
        id = store.get(external_id)
        if id is None:
            id = len(store)
            store[external_id] = id
        return id

def main():
    if os.path.exists("token"):
        token = open("token").read().strip()
    else:
        token = None
    st = StarTrace(token=token)
    st.search("Austin")

if __name__ == '__main__':
    main()
