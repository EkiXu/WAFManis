import web
from json import dumps

urls = (
  '/', 'Index'
)

app = web.application(urls, globals())

class Index:
  def GET(self):
    # 获取所有发送的 GET 参数
    params = web.input()

    forms = {}
    # 遍历所有参数
    for k, v in params.items():
      # 打印参数名称和值
      print("%s: %s" % (k, v))
      forms[k] = v

    return dumps({"args":forms})

  def POST(self):
    # 获取所有发送的 POST 参数
    params = web.input()
    web.header('Content-Type', 'application/json')

    forms = {}
    # 遍历所有参数
    for k, v in params.items():
      # 打印参数名称和值
      print("%s: %s" % (k, v))
      forms[k] = v

    retMsg = dumps({"form":forms})
    web.header('Content-Length', len(retMsg))
    return retMsg

if __name__ == "__main__":
  app.run()
