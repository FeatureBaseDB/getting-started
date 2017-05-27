# Getting Started

<a href="https://github.com/pilosa"><img src="https://img.shields.io/badge/pilosa-v0.3.1-blue.svg"></a>

This repository contains the dataset and sample code for the [Getting Started](https://www.pilosa.com/docs/getting-started/) section of [Pilosa documentation](https://www.pilosa.com/docs/introduction/).

## The Dataset

The sample dataset contains stargazer and language data for Github projects which were retrieved for the search keyword "Go". See the *Generating the Dataset* section below to create other datasets.

* `language.txt`: Language name to languageID mapping. The line number corresponds to the languageID.
* `language.csv`: languageID, projectID
* `stargazer.csv`: stargazerID, projectID, timestamp(starred)

## Usage

1. Pilosa server should be running: [Starting Pilosa](https://www.pilosa.com/docs/getting-started/#starting-pilosa)
2. The appropriate schema should be initialized: [Create the Schema](https://www.pilosa.com/docs/getting-started/#create-the-schema)
3. Finally, the data can be imported: [Import Some Data](https://www.pilosa.com/docs/getting-started/#import-some-data)

## Sample Projects

* [Python](https://github.com/pilosa/getting-started/python)

## Generating the Dataset

`fetch.py` script searches Github for a given keyword, and creates the dataset explained in *The Dataset* section.

Using a Github token is strongly recommended for avoiding throttling. If you don't already have a token for the [GitHub API](https://developer.github.com/v3/), see [Creating a personal access token for the command line](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/).

A recent version of Python is required. We test the script with 2.7 and 3.5.

Below are the steps to run `fetch.py`:

1. Create a virtual env:
	* Using Python 2.7: `virtualenv getting-started`
	* Using Python 3.5: `python3 -m venv getting-started`
2. Activate the virtual env:
	* On Linux, MacOS, other UNIX: `source getting-started/bin/activate`
	* On Windows: `getting-started\Scripts\activate`
3. Install requirements: `pip install -r requirements.txt`
4. If you have a Github token, save it as `token` in the root directory of the project.
5. Run the script: `python fetch.py KEYWORD`
