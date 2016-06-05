#!/usr/bin/python3

# This Python 3 file takes the URL for a tracklist from the website
# www.hikarinoakariost.info, scrapes the tracklist (removing leading/trailing
# whitespace and leading numbering), and prints the tracklist to the console
# with each track separated by a newline.
#
# Usage: ./url_scrape_div.py URL_TO_TRACKLIST

import lxml.html
import requests
import sys

def validate_url(url):
    """Ensure the URL is non-empty and uses the HTTP protocol.
    """

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
    """Return the content of the div at the given URL.
    """

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

def extract_tracklist_begin_num(content):
    """Return list of track names extracted from messy web content.

    The name of a track is defined as a line which begins with a number
    (excluding whitespace).
    """

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

def strip_leading_number(tracklist):
    """Remove the leading numbers for each track.
    """

    for track in tracklist:
        i = 0
        while(track[i].isdigit()):
            i += 1
        tracklist[tracklist.index(track)] = track[i:]

if len(sys.argv) < 2:
    raise RuntimeError("Please provide the URL to the page with "\
        "the target tracklist")

url = sys.argv[1]  # sys.argv[0] is the name of this script
validate_url(url)

div_id = "stcpDiv"
content = scrape_div(url, div_id)

tracklist = extract_tracklist_begin_num(content)
strip_leading_number(tracklist)

for track in tracklist:
    print(track.strip())
