import flask
from json import dumps

def run_server(host="0.0.0.0",port:int=6000):
    app = flask.Flask(__name__)
    @app.route("/", methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE', 'CONNECT'])
    def parse1():
        return (dumps({"args":flask.request.args,"form":flask.request.form,"json":flask.request.json if flask.request.is_json else None}),200,[("Content-Type","application/json")])

    @app.route("/<any>", methods=['GET', 'POST','PUT','DELETE','PATCH','OPTIONS','HEAD','TRACE','CONNECT'])
    def parse2(any):
        return (dumps({"args":flask.request.args,"form":flask.request.form,"json":flask.request.json if flask.request.is_json else None}),200,[("Content-Type","application/json")])

    app.run(host=host,port=port)


if __name__ == "__main__":
    run_server(host="0.0.0.0",port=6000)
