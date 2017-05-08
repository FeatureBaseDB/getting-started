# Star Trace in Java

This folder contains the sample Star Trace project in Java.

## Requirements

* Java 8
* Maven 3

## Usage

1. Run Pilosa server: [Starting Pilosa](https://www.pilosa.com/docs/getting-started/#starting-pilosa)
2. Initialize the schema: [Create the Schema](https://www.pilosa.com/docs/getting-started/#create-the-schema)
3. Import the sample data: [Import Some Data](https://www.pilosa.com/docs/getting-started/#import-some-data)
4. Create the uber JAR:
	```
    mvn -f startrace/pom.xml clean package
    ```    
5. Run the created JAR with the dataset path and Pilosa server address::
	```
    java -jar startrace/target/getting-started-0.3.2.jar .. :10101
    ```
