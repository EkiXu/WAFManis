import atheris
from multiprocessing import Process
import sys,os,datetime
from datetime import datetime
import time
import config
from utils import request,waf_verfication,webapp_verfication,md5,get_free_tcp_port
from mutator.mutator import Mutator
from generator.model import RequestSample


with atheris.instrument_imports():
    #from webapp_validator.python_app.fastapi_app import app
    from webapp_validator.python_app.flask_app import app

# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
# log.disabled = True

target:Process
port: int = config.APP_PORT

def CustomMutator(data, max_size, seed) -> bytes:
    req = RequestSample()
    try:
        req.unserialize(data)
    except Exception as e:
        if config.DEBUG:
            with open('{}/{}-{}'.format(config.QUEUE_DIR, "mutator-corrput", datetime.now().strftime('%H:%M:%S.%f')), 'wb') as f:
                f.write(data)
            pass
        req.build_tree("<start>")

    mutator = Mutator(req,seed)
    mutator.mutate_input()

    serialized_data = req.serialize().encode()

    while len(serialized_data) > max_size:
        req = RequestSample()
        req.build_tree("<start>")
        serialized_data = req.serialize().encode()
    return serialized_data


def startApp(port):
    global target
    target = Process(target=app.run_server, kwargs={'host':'localhost','port': port})
    target.start()


def TestOneInput(data):
    global tot_cnt
    global target
    global port

    if data==b'':
        return
    #real_data = markup(data,TAINT,f"http://127.0.0.1:{port}")

    #target.start()
    # if tot_cnt % 1000 == 0:
    #     try:
    #         target.kill()
    #     except:
    #         pass
    #     port = get_free_tcp_port()
    #     if port == 0:
    #         port = config.APP_PORT
    #     startApp(port)
    #     time.sleep(1.5)

    #res = local_request("./tmp.socket",real_data)
    req_bytes = None
    try:
        req = RequestSample()
        req.unserialize(data)
        req_bytes = req.dump2req(host=f"localhost:{port}",
                                 path="/",
                                taint_key=config.EXPECTED_TAINT["taint_key"],
                                taint_val=config.EXPECTED_TAINT["taint_val"]
                                 )
    except Exception as e:
        if config.DEBUG:
            with open('{}/{}-{}'.format(config.QUEUE_DIR, "corrput", datetime.now().strftime('%H:%M:%S.%f')), 'wb') as f:
                f.write(data)
            pass

    if req_bytes is None:
        return
    resp = request("localhost",port,req_bytes)
    print(resp.body_json)
    # target.kill()
    #print(res.raw_packet)

    if webapp_verfication(resp,config.EXPECTED_TAINT,config.VALIDATE_MODE):
        #print("[Info] webapp_verfication passed")


        try:
            resp = request(config.WAF_HOST,config.WAF_PORT,req.dump2req(
                    host=config.WAF_HOST+":"+str(config.WAF_PORT),
                    path="/",
                    taint_key=config.EXPECTED_TAINT["taint_key"],
                    taint_val=config.EXPECTED_TAINT["taint_val"]
                ),timeout=1,retry=3)
        except Exception as e:
            print("[Error]"+ e)
            return

        bypassed,req_bytes2 = waf_verfication(resp)
        if bypassed:
            #print("[Info] waf_verfication passed")
            #raise Exception("bypassed")
            resp2 = request("localhost",port,req_bytes2,timeout=0.05,retry=1)
            if webapp_verfication(resp2,config.EXPECTED_TAINT,config.VALIDATE_MODE):
                case_name = md5(data)
                with open('{}/{}-{}.input'.format(config.SOLUTION_DIR, "solution", case_name), 'wb') as f:
                    f.write(data)
                with open('{}/{}-{}.case'.format(config.SOLUTION_DIR, "solution", case_name), 'wb') as f:
                    f.write(req_bytes2)




    # write data into file in config.QUEUE_DIR to debug
    if config.DEBUG:
        with open('{}/{}-{}'.format(config.QUEUE_DIR, "sample", datetime.now().strftime('%H:%M:%S.%f')), 'wb') as f:
            f.write(data)
            f.write("\nReq:-----\n".encode())
            f.write(req_bytes)
            f.write("\nRes:-----\n".encode())
            f.write(resp.raw_packet)
    tot_cnt += 1

# target = Process(target=app.run, kwargs={'host': 'unix://./tmp.socket'})
#target.start()

if __name__ =='__main__':
    tot_cnt = 0
    if not os.path.exists(config.QUEUE_DIR):
        os.makedirs( config.QUEUE_DIR)
    else:
        if os.listdir(config.QUEUE_DIR):
            os.rename(config.QUEUE_DIR, '{}_{}_bkup'.format(config.QUEUE_DIR,datetime.now().strftime("%Y%m%d-%H%M%S")))
            os.makedirs(config.QUEUE_DIR)
    if not os.path.exists(config.SOLUTION_DIR):
        os.makedirs(config.SOLUTION_DIR)
    #atheris.Setup(sys.argv, TestOneInput)
    atheris.Setup(sys.argv, TestOneInput,custom_mutator=CustomMutator)
    #startApp()
    #app.run_server(config.APP_PORT)
    #time.sleep(1)
    atheris.Fuzz()
