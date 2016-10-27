import recommend
import os.path
import random

users = recommend.fetch_user()
random.shuffle(users)
for v in users:
    print(v['userid'])
    #if v['userid'] is not None and not os.path.exists("./cache/" + v['userid'] + ".pick"):
    if v['userid'] is not None:
        try:
            recommend.recommend_analysis(v['userid'])
        except Exception as e:
            print(e)
