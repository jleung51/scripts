#!/bin/python3

import json
import sys
from argparse import ArgumentParser

import requests
from couchbase.bucket import Bucket
from couchbase.exceptions import BucketNotFoundError
from couchbase.exceptions import CouchbaseNetworkError
from couchbase.exceptions import NotFoundError


def get_buckets(url):
    r = requests.get(url + "/pools/default/buckets")
    r.raise_for_status()

    names = []
    for bucket in r.json():
        names.append(bucket["name"])
    print(names)


def get_document_catch_error(bucket, doc):
    try:
        return bucket.get(doc).value
    except NotFoundError:
        sys.exit("Error: No document with ID " + doc + " exists.")


def get(bucket, doc):
    document = get_document_catch_error(bucket, doc)
    print(json.dumps(document, indent=2, sort_keys=True))


def replace(bucket, doc, set_json_key, set_json_value):
    if set_json_key is None:
        sys.exit("Error: A REPLACE operation requires a key to set (use the flag -sk KEY).")
    elif set_json_value is None:
        sys.exit("Error: A REPLACE operation requires a value to set (use the flag -sv VALUE).")

    document = get_document_catch_error(bucket, doc)

    iterator = document
    json_hierarchy = set_json_key.split(".")
    levels = len(json_hierarchy)
    for i in range(levels - 1):
        iterator = iterator[json_hierarchy[i]]
    iterator[json_hierarchy[levels - 1]] = set_json_value

    bucket.replace(doc, document)
    print("REPLACE operation was successful.")


def delete(bucket, doc):
    try:
        bucket.remove(doc)
    except NotFoundError:
        sys.exit("Error: No document with ID " + doc + " exists.")


def main():
    url = "http://localhost:8091"

    parser = ArgumentParser(description="Utility tool for interacting with Couchbase from the command line.")
    parser.add_argument(
        "operation", type=str, choices=["GET_BUCKETS", "GET", "REPLACE", "DELETE"],
        help="Operation to perform on Couchbase"
    )
    parser.add_argument("bucket", nargs="?", type=str, help="Name of the bucket")
    parser.add_argument("document", nargs="?", type=str, help="Unique ID of the Document")
    parser.add_argument("-sk", "--set_key", nargs="?", type=str, help="(REPLACE only) Key to replace")
    parser.add_argument(
        "-sv", "--set_value", nargs="?", type=str,
        help="(REPLACE only) Value to assign to the replaced key"
    )
    args = parser.parse_args()

    operations_require_document_and_bucket = ["GET", "REPLACE", "DELETE"]
    if args.operation in operations_require_document_and_bucket:
        if args.bucket is None:
            sys.exit("Error: This operation requires a bucket name as one of the arguments.")
        elif args.document is None:
            sys.exit("Error: This operation requires a document ID as one of the arguments.")

        try:
            bucket = Bucket(url + "/" + args.bucket)  # Instantiate bucket connection
        except CouchbaseNetworkError:
            sys.exit("Error: Could not connect to Couchbase at " + url + ".")
        except BucketNotFoundError:
            sys.exit("Error: The given bucket name " + args.bucket + " is invalid.")

        if args.operation == "GET":
            get(bucket, args.document)
        elif args.operation == "REPLACE":
            replace(bucket, args.document, args.set_key, args.set_value)
        elif args.operation == "DELETE":
            delete(bucket, args.document)

    elif args.operation == "GET_BUCKETS":
        get_buckets(url)
    else:
        print("Error: Operation not supported.")


if __name__ == "__main__":
    main()
