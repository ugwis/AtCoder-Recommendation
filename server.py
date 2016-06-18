from bottle import route,run,template
import recommend

@route('/<userid>')
def index(userid):
    return template('<a href={{url}}>{{url}}</a>', url=recommend.recommend_problem(userid))

run(host='localhost', port=8000)
