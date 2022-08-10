from flask import Flask, g, Response, make_response, request
from flask import session
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.debug = True
app.config.update(
    SECRET_KEY='X1243yRH!mMwf',
    SESSION_COOKIE_NAME='pyweb_flask_session',
    PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days  cf. minutes=30
)

@app.route('/wc')
def wc():
  key = request.args.get('key')
  val = request.args.get('val')
  res = Response("SET COOKIE")
  res.set_cookie(key, val)
  session['Token'] = '123X'
  return make_response(res)
#def

@app.route('/rc')
def rc():
  key = request.args.get('key') #token
  val = request.cookies.get(key)
  return "cookie['" + key + "] = " + val + " , " + session.get('Token')
#def

@app.route('/delsess')
def delsses():
  if session.get('Token'):
    del session['Token']
  #if
  return "Session이 삭제되었습니다."
#def

@app.route('/reqenv')
def reqenv():
  #print(">> is_xhr", request.is_xhr)
  #print(">> json = ", request.get_json())
  return ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
        'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
        'PATH_INFO: %(PATH_INFO) s <br>'
        'QUERY_STRING: %(QUERY_STRING) s <br>'
        'SERVER_NAME: %(SERVER_NAME) s <br>'
        'SERVER_PORT: %(SERVER_PORT) s <br>'
        'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
        'wsgi.version: %(wsgi.version) s <br>'
        'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
        'wsgi.input: %(wsgi.input) s <br>'
        'wsgi.errors: %(wsgi.errors) s <br>'
        'wsgi.multithread: %(wsgi.multithread) s <br>'
        'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
        'wsgi.run_once: %(wsgi.run_once) s') % request.environ
#def

# app.config['SERVER_NAME'] = 'local.com:5001'

# @app.route('/sd')
# def helloworld_local():
#   return "Hello local.com"
# #def

# @app.route("/sd", subdomain='blog')
# def helloworld_blog():
#   return "Hello blog.local.com"
# #def

#request 처리 용 함수
def ymd(fmt):
  def trans(date_str):
    return datetime.strptime(date_str, fmt)
  #def
  return trans #함수를 리턴함, .get('date' 가 ate_str로 들어감
#def

#http://local.com:5001/dt?date=1968-02-15
@app.route('/dt')
def dt():
  datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
  return "우리나라 시간형식: " + str(datestr)
#def


# @app.route('/test', defaults={'page': 'index'})
# @app.route('/test/<page>')
# def testpage(page):
#   return 'TestPage ' + str(page)
# #def

# @app.route('/host', host='a.com:5001')
# @app.route('/host', host='b.com:5001')
# @app.route('/host', host='c.com:5001')
# def host():
#   if host == 'a.com:5001':
#     return "a.com"
#   elif host == 'b.com:5001':
#     return "b.com"
#   elif host == 'c.com:5001':
#     return "c.com"
#   else:
#     return "other.com"
#   #if
# #def

# @app.route('/host', host='b.com')
# def hostb():
#   return "b.com"
# #def

# @app.route('/host', host='c.com')
# def hostc():
#   return "c.com"
# #def

#localhost:5001/rp?q=123

@app.route('/rp')
def rp():
  #q = request.args.get('q')
  q = request.args.getlist('q')
  return "q= %s" % str(q)
#def

@app.route('/tidtest/<tid>')
def tidtest(tid):
  return 'tid is ' + str(tid)
#def

@app.route('/wsgi_test')
def wsgi_test():
  def application(environ, start_response):
    body = 'The request method was %s' % environ['REQUEST_METHOD']
    headers = [('Content-Type', 'text/plain; charset=utf-8'),
              ("Content-Length", str(len(body))),
              ('Created-By', 'Moon-Kee Bahk')]
    start_response('200 OK', headers)
    return [body]
  #def
  return make_response(application)
#def

@app.route("/res1")
def res1():
  custom_res = Response("Custom Response", 201, {'Created-By': 'Moon-Kee Bahk'})
  return make_response(custom_res) #Stream으로 만들어 보냄, 큰 파일 보낼 때 안정적이라서...
#def

# @app.before_first_request
# def before_first_request():
#   print("before_first_request!!!")
#   g.str = " bfq-> Global 변수호출"
# #def

# #Web filter 용도로 사용
# #db connect
# @app.before_request
# def before_request():
#   print("before_request!!!")
#   g.str = " br-> Global 변수호출"
# #def

# #db close
# @app.after_request
# def after_request():
#   print("after_request!!!")
#   g.str = " ar-> Global 변수호출"
# #def


@app.route("/gg")
def gg():
  return "Hello, I'm gg()!!! " + getattr(g, 'str', 'default_value')
#def

# @app.route("/api/v1/gg")
# def gg_v1():
#   return gg()
# #def


@app.route("/")
def __main__():
  return "Hello, I'm __main()__ " + getattr(g, 'str', 'default_value')
#def
