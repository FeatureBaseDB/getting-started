from __future__ import print_function

import sys
import os

from pilosa import Client, Index, TimeQuantum


def load_language_names(dataset_path):
    with open(os.path.join(dataset_path, "languages.txt")) as f:
        return [line.strip() for line in f]


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
    # Let's load the schema from the server.
    schema = client.schema()
    
    # We need to refer to indexes and frames before we can use them in a query.
    repository = schema.index("repository")
    stargazer = repository.frame("stargazer")
    language = repository.frame("language")

    # Which repositories did user 14 star:
    repository_ids = client.query(stargazer.bitmap(14)).result.bitmap.bits
    print("User 14 starred:")
    print_ids(repository_ids)

    print()

    # What are the top 5 languages in the sample data:
    top_languages = client.query(language.topn(5)).result.count_items
    # note that we map language id to language name this time
    language_items = [(language_names[item.id], item.count)
                      for item in top_languages]
    print("Top Languages:")
    print_topn(language_items)

    print()

    # Which repositories were starred by both user 14 and 19:
    query = repository.intersect(
        stargazer.bitmap(14),
        stargazer.bitmap(19)
    )
    mutually_starred = client.query(query).result.bitmap.bits
    print("Both user 14 and 19 starred:")
    print_ids(mutually_starred)

    print()

    # Which repositories were starred by user 14 or 19:
    query = repository.union(
        stargazer.bitmap(14),
        stargazer.bitmap(19)
    )
    either_starred = client.query(query).result.bitmap.bits
    print("User 14 or 19 starred:")
    print_ids(either_starred)

    print()

    # Which repositories were starred by user 14 or 19 and were written in language 1:
    query = repository.intersect(
        repository.union(
            stargazer.bitmap(14),
            stargazer.bitmap(19)
        ),
        language.bitmap(1)
    )
    mutually_starred = client.query(query).result.bitmap.bits
    print("User 14 or 19 starred, written in language 1:")
    print_ids(mutually_starred)

    print()

    # Set user 99999 as a stargazer for repository 77777:
    client.query(stargazer.setbit(99999, 77777))
    print("Set user 99999 as a stargazer for repository 77777\n")

if __name__ == "__main__":
    main()
