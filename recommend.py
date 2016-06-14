#!/user/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import sys
import psycopg2
import psycopg2.extras
import dateutil.parser
import pguser
import numpy as np
import json
from bs4 import BeautifulSoup

url_media = "https://upload.twitter.com/1.1/media/upload.json"
url_text = "https://api.twitter.com/1.1/statuses/update.json"

def fetch_solved():
    connector = psycopg2.connect(pguser.arg)
    cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
    solved = []
    try:
        cur.execute("""SELECT * from solved;""")
        connector.commit()
        for row in cur:
            solved.append(row)
    except Exception as e:
        print(e.message)
    cur.close()
    connector.close()
    return solve

if __name__ == "__main__":

    exit(0)
