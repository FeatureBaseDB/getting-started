# Star Trace in Python

## Usage

1. Run Pilosa server: [Starting Pilosa](https://www.pilosa.com/docs/getting-started/#starting-pilosa)
2. Initialize the schema: [Create the Schema](https://www.pilosa.com/docs/getting-started/#create-the-schema)
3. Import the sample data: [Import Some Data](https://www.pilosa.com/docs/getting-started/#import-some-data)
4. Create a virtual env:
	* Using Python 2.7: `virtualenv getting-started`
	* Using Python 3.5: `python3 -m venv getting-started`
5. Activate the virtual env:
	* On Linux, MacOS, other UNIX: `source getting-started/bin/activate`
	* On Windows: `getting-started\Scripts\activate`
6. Install requirements: `pip install -r requirements.txt`
7. Run the script with the dataset path and Pilosa server address:
    ```
    python startrace.py .. :10101
    ```
