import recommend
import os.path
import random
import pymongo

connect = pymongo.MongoClient('localhost',27017)
db = connect.atcoder

collect = db.recommend

users = recommend.fetch_user()
random.shuffle(users)
for v in users:
    print(v['userid'])
    #if v['userid'] is not None and not os.path.exists("./cache/" + v['userid'] + ".pick"):
    if v['userid'] is not None:
        try:
            if collect.count({'userid':v['userid']}) == 0:
                recommend.recommend_analysis(v['userid'])
        except Exception as e:
            print(e)
