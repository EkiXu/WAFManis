from fastapi import FastAPI,Form
import uvicorn

def run_server(host="0.0.0.0",port:int=6000):
    app = FastAPI()
    @app.post("/")
    def get_request(taint:str=Form()):
        return {"form": {"taint":taint}}

    @app.post("/post")
    def get_request(taint:str=Form()):
        return {"form": {"taint":taint}}
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server()
