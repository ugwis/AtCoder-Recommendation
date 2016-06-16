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

def fetch_count_problems():
    connector = psycopg2.connect(pguser.arg)
    cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
    count = 0
    try:
        cur.execute("""SELECT count(*) FROM problems;""")
        connector.commit()
        for row in cur:
            count = row['count']
    except Exception as e:
        print(e.message)
    cur.close()
    connector.close()
    return count

count = fetch_count_problems()

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
    return 1./(1 + len(users[person1] ^ users[person2]))

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

def count_solved(solveds,pid):
    count=0
    for solved in solveds:
        if pid == solved:
            count+=1
    return count

if __name__ == "__main__":
    userid=sys.argv[1]
    uid=fetch_uid(userid)
    user_solved = fetch_users_solveds()
    users = fetch_user()
    cand = {}
    for user in users:
        if user['uid'] in user_solved:
            distance = sim_distance(user_solved,uid,user['uid'])
            #print(user['userid'] + " " + str(distance))
            for solved_pid in user_solved[user['uid']] - user_solved[uid]:
                if not solved_pid in cand:
                    cand[solved_pid] = 0.0
                cand[solved_pid] += distance
    for k,v in cand.items():
        v*=count_solved(user_solved,k)
    recommended_pid = max(cand,key=(lambda x:cand[x]))
    print(str(recommended_pid) + " " + str(cand[recommended_pid]))
    """for k,v in sorted(cand.items(),key=lambda x:x[1]):
        print(k,v)"""
    exit(0)
