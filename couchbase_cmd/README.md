# Couchbase Command-Line Tool

Python script which provides utilities for simple operations on a [Couchbase](https://www.couchbase.com/) server.

## Setup

The Couchbase SDK is supported only up to [Python 2.7](https://www.python.org/download/releases/2.7/) or [Python 3.4](https://www.python.org/downloads/release/python-343/). Install one of these (if in doubt, go for Python 3).

Install the Couchbase Python SDK from the download list at the bottom of [this page](https://pypi.python.org/pypi/couchbase).

Install the pip dependency `requests`.

## Usage

The syntax for this tool is as follows:
```
python cb_cmd.py OPERATION [BUCKET_NAME] [DOCUMENT_NAME] [ADDITIONAL_FLAGS]
```

The supported operations are as follows:

| Supported Operation | Functionality |
| --- | --- |
| GET_BUCKETS | Lists the names of all buckets |
| GET | Retrieves the contents of a document |
| REPLACE | Changes the value of a specific JSON element in a document |
| DELETE | Permanently removes a document |

For example, to change the JSON element `office.location.latitude` to the value `123.456` in the document `document_b` within the bucket `bucket_a`, execute:
```
python cb_cmd.py REPLACE bucket_a document_b -sk office.location.latitude -sv 123.456
```
