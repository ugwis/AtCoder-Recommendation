from bottle import route,run,template
import recommend

@route('/')
def index():
    return template('index')

@route('/<userid>')
def index(userid):
    easy,medium,hard = recommend.recommend(userid)
    return template('frame', userid=userid,easy=easy,medium=medium,hard=hard)

run(host='localhost', port=8000)
