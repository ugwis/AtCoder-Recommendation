#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route,run,template
import recommend

@route('/')
def index():
    return template('index')

@route('/<userid>')
def index(userid):
    easy,medium,hard = recommend.recommend(userid)
    shareText = userid+'さんのお勧め問題は'
    problems = []
    for p in easy:
        problems.append('「' + p['title'] + '」')
    shareText+=','.join(problems)
    return template('frame', userid=userid,easy=easy,medium=medium,hard=hard,shareText=shareText)

run(host='localhost', port=8000)
