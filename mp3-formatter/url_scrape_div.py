#!/usr/bin/python3

# sudo apt-get install python3-pip
# pip3 install requests

import lxml.html
import requests
import sys

def validate_url(url):
    if not url:
        raise SystemError("validate_url() was given an empty URL")

    protocol = "http://"
    protocol_error_message = ValueError("A URL beginning with " \
        "'http://' is required")

    if len(url) < len(protocol):
        raise protocol_error_message

    if url[:len(protocol)] != protocol:
        raise protocol_error_message

def scrape_div(url, div_id):
    div_id_lookup_string = '//div[contains(@id, "' + div_id + '")]'

    try:
        html_page = requests.get(url)
    except:
        e = sys.exc_info()[0]
        raise ValueError("Request could not be completed. Perhaps the " \
            "URL provided was invalid?")

    html_page.raise_for_status()

    html_tree = lxml.html.fromstring(html_page.content)
    content = html_tree.xpath(div_id_lookup_string)

    if len(content) < 1:
        raise LookupError("The requested div could not be found")
    elif len(content) > 1:
        raise LookupError("More than one of the requested divs were found")

    return str(content[0].text_content())

# A line is determined to be the name of a track if it begins with a number
def extract_tracklist_begin_num(content):
    tracklist = []
    for line in content.splitlines():

        # Empty line
        if not line:
            continue

        # Strip leading and trailing whitespace
        line.lstrip()
        line.rstrip()

        if line[0].isdigit():
            tracklist.append(line)

    return tracklist

# Removes leading numbers and whitespace
def strip_leading_index(tracklist):
    tracklist_new = []
    for track in tracklist:

        for i in range(len(track)):
            if track[i].isdigit() or track[i] == " ":
                i += 1
            else:
                tracklist_new.append(track[i:])
                tracklist[tracklist.index(track)] = track[i:]
                break

if len(sys.argv) < 2:
    raise RuntimeError("Please provide the URL to the page with "\
        "the target tracklist")

url = sys.argv[1]  # sys.argv[0] is the name of this script
validate_url(url)

div_id = "stcpDiv"

content = scrape_div(url, div_id)
tracklist = extract_tracklist_begin_num(content)
strip_leading_index(tracklist)

for track in tracklist:
    print(track)
