from bottle import route,run,template
import recommend

@route('/<userid>')
def index(userid):
    easy = recommend.recommend_problem(userid)
    return template('frame', userid=userid,easy=easy)

run(host='localhost', port=8000)
