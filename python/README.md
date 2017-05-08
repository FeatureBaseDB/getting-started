# Star Trace in Python

This folder contains the sample Star Trace project in Python. 

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
6. Clone this repository, or download the [ZIP archive](https://github.com/pilosa/getting-started/archive/master.zip) and uncompress it.
7. Make sure you are in the `getting-started/python` directory.	
8. Install requirements: `pip install -r requirements.txt`
9. Run the script with the dataset path and Pilosa server address:
    ```
    python startrace.py .. :10101
    ```
