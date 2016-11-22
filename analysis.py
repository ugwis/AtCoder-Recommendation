import recommend
import os.path
import random
import pymongo

connect = pymongo.MongoClient('localhost',27017)
db = connect.atcoder

collect = db.recommend

users = recommend.fetch_user()
random.shuffle(users)
user_solved = recommend.fetch_users_solveds()
for v in users:

    #if v['userid'] is not None and not os.path.exists("./cache/" + v['userid'] + ".pick"):
    if v['uid'] not in user_solved:
        continue
    if v['userid'] is not None:
        try:
            if collect.count({'userid':v['userid']}) != 0:
                collect.remove({'userid':v['userid']})
            recommend.recommend_analysis(user_solved, v['userid'])
        except Exception as e:
            print()
