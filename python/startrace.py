import sys
import os
from datetime import datetime

from pilosa import Client, Index, TimeQuantum


def get_schema():
    repository = Index("repository", column_label="repo_id")
    stargazer = repository.frame("stargazer",
                                 row_label="stargazer_id",
                                 time_quantum=TimeQuantum.YEAR_MONTH_DAY,
                                 inverse_enabled=True)
    language = repository.frame("language",
                                row_label="language_id",
                                inverse_enabled=True)

    return repository, stargazer, language


def load_language_names(dataset_path):
    with open(os.path.join(dataset_path, "languages.txt")) as f:
        return dict(enumerate(line.strip() for line in f))


def main():
    if len(sys.argv) not in [2, 3]:
        print("Usage: python startrace.py PATH_TO_DATASET [pilosa_address]", file=sys.stderr)
        sys.exit(1)

    dataset_path = sys.argv[1]
    address = sys.argv[2] if len(sys.argv) > 2 else ":10101"
    client = Client(address)
    language_names = load_language_names(dataset_path)
    run_queries(client, language_names)


def print_topn(items):
    lines = ["\t{i}. {s[0]}: {s[1]} stars".format(s=s, i=i + 1) for i, s in enumerate(items)]
    print("\n".join(lines))


def print_ids(ids):
    print("\n".join("\t{i}. {id}".format(i=i + 1, id=id) for i, id in enumerate(ids)))


def run_queries(client, language_names):
    repository, stargazer, language = get_schema()

    # Who are the top 50 stargazers:
    top_stargazers = client.query(stargazer.topn(50)).result.count_items
    stargazer_items = [(item.id, item.count) for item in top_stargazers]
    print("Top stargazers:")
    print_topn(stargazer_items)

    print()

    # What are the top 10 languages:
    top_languages = client.query(language.topn(10)).result.count_items
    # note that we map language id to language name this time
    language_items = [(language_names[item.id], item.count)
                      for item in top_languages]
    print("Top Languages:")
    print_topn(language_items)

    print()

    # Which repositories were starred by all 10 top stargazers:
    top10 = [item.id for item in top_stargazers[:10]]
    top10_bitmaps = [stargazer.bitmap(stargazer_id) for stargazer_id in top10]
    response = client.query(repository.intersect(*top10_bitmaps))
    repository_ids = response.result.bitmap.bits
    print("The following repositories were starred by all of:", ", ".join(str(sid) for sid in top10))
    print("\t", repository_ids)

    print()

    # How many repositories did stargazer 10801 star in 2017:
    start_2017 = datetime(2017, 1, 1)
    end_2017 = datetime(2018, 1, 1)
    stargazer_id = 10801
    query = repository.count(stargazer.range(stargazer_id,
                                             start=start_2017,
                                             end=end_2017))
    repository_count = client.query(query).result.count
    print("{count} repositories were starred by stargazer {id} in 2017.".format(
        count=repository_count,
        id=stargazer_id))

if __name__ == "__main__":
    main()
