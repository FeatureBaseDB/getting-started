# Getting Started

## Schema

```
project
	col: project_id

	frame: stargazer
		row: stargazer_id

	frame: language (C, Go, Java, Python, etc.)
		row: language_id
```

### Sample Project

In order to get a glance of the capabilities of Pilosa, we will write a sample project called "Star Trace". The database for the project will contain information about most recently updated 1000 Github projects which have "Austin" in their names, including stargazers, programming languages used and tags. People who have starred a project are called that project's stargazers.

Although Pilosa doesn't keep the data in a tabular format, we will still use "columns" and "rows" when we talk about organizing our data. A common convention is putting the main focus (or subject) of a database in the columns, and properties of the subject in the rows. For instance, the columns of the "project" database would contain project IDs and the programming language(s) used for that project would be placed in the rows of the "language" *frame*.

#### Create the Schema

Before we can import data or run queries, we need to create the schema for our databases. Let's create the project database first:
```
$ curl -XPOST localhost:10101/db -d '{"db": "project", "options": {"columnLabel": "project_id"}}'
```

Project IDs are the main focus of the `project` database, so we chose `project_id` as the column label.

Let's create the `stargazer` frame which has user IDs of stargazers as its rows:
```
$ curl -XPOST localhost:10101/frame -d '{"db": "project", "frame": "stargazer", "options": {"rowLabel": "stargazer_id"}}'
```

Since our data contains time stamps for the time users starred repos, we will change the *time quantum* for the `stargazer` frame. Time quantum is the resolution of the time we want to use. We will set it to `YMD` (year, month, day) for `stargazer`:
```
$ curl -XPATCH localhost:10101/frame/time_quantum -d '{"db": "project", "frame": "stargazer", "time_quantum": "YMD"}'

Next up is the `language` frame, which will contain IDs for programming languages:
```
$ curl -XPOST localhost:10101/frame -d '{"db": "project", "frame": "language", "options": {"rowLabel": "language_id"}}'
```
#### Import Some Data

The sample data for the "Star Trace" project is at [Pilosa Getting Started repository](https://github.com/pilosa/getting-started). Download `*.csv` files in that repo and run the following commands to import the data into Pilosa.

If you are running the native compiled version of Pilosa, you can run:

```
$ pilosa import -d project -f stargazer project-stargazer.csv
$ pilosa import -d project -f language project-language.csv
```

If you are using a Docker container for Pilosa (with name `pilosa`), you should instead copy the `*.csv` file into the container and then import them:
```
$ docker cp project-stargazer.csv pilosa:/project-stargazer.csv
$ docker exec -it pilosa pilosa import -d project -f stargazer /project-stargazer.csv
$ docker cp project-language.csv pilosa:/project-language.csv
$ docker exec -it pilosa pilosa import -d project -f language /project-language.csv
```

Note that, both the user IDs and the project IDs were remapped to sequential integers in the data files, they don't correspond to actual Github IDs anymore. You can check `language.txt` out to see the mapping for languages.

#### Make Some Queries

Which projects did user 8 starred:
```
$ curl -XPOST 'localhost:10101/query?db=project' -d 'Bitmap(frame="stargazer", stargazer_id=8)'
```

What are the top 5 languages in the sample data:
```
$ curl -XPOST 'localhost:10101/query?db=project' -d 'TopN(frame="language", n=5)'
```

Which projects were starred by user 8 and 18:
```
$ curl -XPOST 'localhost:10101/query?db=project' -d 'Intersect(Bitmap(frame="stargazer", stargazer_id=8), Bitmap(frame="stargazer", stargazer_id=18))'
```

Which projects were starred by user 8 or 18:
```
$ curl -XPOST 'localhost:10101/query?db=project' -d 'Union(Bitmap(frame="stargazer", stargazer_id=8), Bitmap(frame="stargazer", stargazer_id=18))'
```

Which projects were starred by user 8 and 18 and also were written in language 1:
```
$ curl -XPOST 'localhost:10101/query?db=project' -d 'Intersect(Bitmap(frame="stargazer", stargazer_id=8), Bitmap(frame="stargazer", stargazer_id=18), Bitmap(frame="language", language_id=1))'
```

Set user 99999 as a stargazer for the project 77777:
```
$ curl -XPOST 'localhost:10101/query?db=project' -d 'SetBit(frame="stargazer", project_id=77777, stargazer_id=99999)'
```

