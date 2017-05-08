# Star Trace in Go

This folder contains the sample Star Trace project in Go.

## Requirements

* Go 1.7 and higher

## Usage

1. Run Pilosa server: [Starting Pilosa](https://www.pilosa.com/docs/getting-started/#starting-pilosa)
2. Initialize the schema: [Create the Schema](https://www.pilosa.com/docs/getting-started/#create-the-schema)
3. Import the sample data: [Import Some Data](https://www.pilosa.com/docs/getting-started/#import-some-data)
4. Clone this repository, or download the [ZIP archive](https://github.com/pilosa/getting-started/archive/master.zip) and uncompress it.
4. Make sure you are in the `getting-started/go` directory.
4. Install Pilosa client library:
    ```
    go get github.com/pilosa/go-pilosa
    ```
5. Run `startrace.go`. The path to the dataset is required. You can optionally specify the Pilosa server's address:
    ```
    go run startrace.go .. :10101
    ```

