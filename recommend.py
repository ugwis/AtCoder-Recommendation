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

contest_atcoder = "contest.atcoder.jp"

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

def count_solved(pid):
    connector = psycopg2.connect(pguser.arg)
    cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
    count=0
    try:
        cur.execute("""SELECT count(0) from solved where pid=(%s)""",(pid,))
        connector.commit()
        for row in cur:
            count = row['count']
    except Exception as e:
        print(e.message)
    cur.close()
    connector.close()
    return count

def fetch_problem_url(pid):
    connector = psycopg2.connect(pguser.arg)
    cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
    url = ""
    try:
        cur.execute("""select 'http://' || contestid || '.contest.atcoder.jp/tasks/' || problemid as url from problems left join contests on problems.cid=contests.cid where pid=(%s);""",(pid,))
        connector.commit()
        for row in cur:
            url = row['url']
    except Exception as e:
        print(e.message)
    cur.close()
    connector.close()
    return url

def fetch_contestid(pid):
    connector = psycopg2.connect(pguser.arg)
    cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
    contestid = ""
    try:
        cur.execute("""SELECT contestid FROM contests LEFT JOIN problems on contests.cid=problems.cid WHERE pid=(%s)""",(pid,))
        connector.commit()
        for row in cur:
            contestid = row['contestid']
    except Exception as e:
        print(e.message)
    cur.close()
    connector.close()
    return contestid

def fetch_problemid(pid):
    connector = psycopg2.connect(pguser.arg)
    cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
    problemid = ""
    try:
        cur.execute("""SELECT problemid FROM problems WHERE pid=(%s)""",(pid,))
        connector.commit()
        for row in cur:
            problemid = row['problemid']
    except Exception as e:
        print(e.message)
    cur.close()
    connector.close()
    return problemid

def fetch_userid(uid):
    connector = psycopg2.connect(pguser.arg)
    cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
    userid = ""
    try:
        cur.execute("""SELECT userid FROM users WHERE uid=(%s)""",(uid,))
        connector.commit()
        for row in cur:
            userid = row['userid']
    except Exception as e:
        print(e.message)
    cur.close()
    connector.close()
    return userid

def is_solved(pid,uid):
    contestid = fetch_contestid(pid)
    problemid = fetch_problemid(pid)
    userid = fetch_userid(uid)
    url = "http://" + contestid + "." + contest_atcoder + "/submissions/all?task_screen_name=" + problemid + "&user_screen_name=" + userid + "&status=AC"
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode(r.encoding),"html.parser")
    succ = soup.find_all("tr")
    return len(succ) > 0

def recommend_problem(userid):
    uid = fetch_uid(userid)
    user_solved = fetch_users_solveds()
    users = fetch_user()
    distances = []
    for user in users:
        # case: user does not solve any problem
        if user['uid'] not in user_solved:
            continue
        distance = sim_distance(user_solved, uid, user['uid'])
        distances.append([user['uid'],distance])
    cand = {}
    for rank, dist in zip(range(50,0,-1),sorted(distances, key=lambda x:x[1], reverse=True)):
        for solved_pid in user_solved[dist[0]] - user_solved[uid]:
            if not solved_pid in cand:
                cand[solved_pid] = 0.0
            cand[solved_pid] += rank
    for k,v in cand.items():
        count = count_solved(k)
        if count == 0:
            cand[k] = 0
    recommended_pid = max(cand,key=(lambda x:cand[x]))
    for k,v in sorted(cand.items(),key=lambda x:x[1],reverse=True):
        print(fetch_problem_url(k),v)
        #if not is_solved(k,uid):
        #    return fetch_problem_url(k)
    return fetch_problem_url(recommended_pid)

"""
def prev_recommend_problem(userid):
    uid=fetch_uid(userid)
    user_solved = fetch_users_solveds()
    users = fetch_user()
    # candidate for problem
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
        count = count_solved(k)
        if count == 0:
            cand[k]=0
        else:
            cand[k]-=count
    recommended_pid = max(cand,key=(lambda x:cand[x]))
    for k,v in sorted(cand.items(),key=lambda x:x[1],reverse=True):
        print(fetch_problem_url(k),v)
        #if not is_solved(k,uid):
        #    return fetch_problem_url(k)
    return fetch_problem_url(recommended_pid)"""
