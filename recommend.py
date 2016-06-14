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
from operator import itemgetter
from sets import Set
import math

url_media = "https://upload.twitter.com/1.1/media/upload.json"
url_text = "https://api.twitter.com/1.1/statuses/update.json"

def fetch_users_solveds():
    connector = psycopg2.connect(pguser.arg)
    cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
    solveds = []
    try:
        cur.execute("""SELECT * from solved;""")
        connector.commit()
        for row in cur:
            solveds.append(row)
    except Exception as e:
        print(e.message)
    cur.close()
    connector.close()
    users = {}
    for solved in solveds:
        if not solved['uid'] in users:
            users[solved['uid']] = Set([])
        users[solved['uid']].add(solved['pid'])
    return users

def sim_distance(users,person1,person2):
    #return len(users[person1] ^ users[person2])
    return 1./(1.+math.sqrt(len(users[person1] ^ users[person2])))

def fetch_user():
    connector = psycopg2.connect(pguser.arg)
    cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
    users = []
    try:
        cur.execute("""SELECT uid,userid FROM users;""")
        connector.commit()
        for row in cur:
            users.append(row)
    except Exception as e:
        print(e.message)
    cur.close()
    connector.close()
    return users

def fetch_uid(userid):
    connector = psycopg2.connect(pguser.arg)
    cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
    uid = None
    try:
        cur.execute("""SELECT uid FROM users WHERE userid=(%s);""",(userid,))
        connector.commit()
        for row in cur:
            uid = row['uid']
    except Exception as e:
        print(e.message)
    cur.close()
    connector.close()
    return uid

if __name__ == "__main__":
    userid="murashin"
    user_solved = fetch_users_solveds()
    users = fetch_user()
    sim_user = []
    for user in users:
        if user['uid'] in user_solved:
            distance = sim_distance(user_solved,fetch_uid(userid),user['uid'])
            sim_user.append([
                user['userid'],
                distance
            ])
    sim_user = sorted(sim_user,key=lambda x:x[1], reverse=True)
    print(sim_user)
    """for user in sim_user[:20]:
        print(user)"""
    exit(0)
