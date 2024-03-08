from generator.model import Node,RequestSample,HTTPResponse
import copy
import time
from utils import request, waf_verfication, webapp_verfication,md5
from config import WAF,WEBAPP_VALIDATOR,MINI_EVASION_DIR,MINI_SAMPLE_DIR,INPUT_EVASION_DIR,FROZEN_SYMBOL
from urllib.parse import urlparse
import os
from threading import Thread
from queue import Queue
import time

class Centrifuge:

    def __init__(self,waf_name,waf_url,verbose=False) -> None:
        self.verbose = verbose
        self.waf_name = waf_name
        url_info = urlparse(waf_url)
        self.waf_host = url_info.hostname
        self.waf_port = url_info.port
        self.waf_netloc = url_info.netloc

    # run_simple is faster but may not explore all the possible minimization
    def run_simple(self,initial_req:RequestSample,webapp:dict,evasion_output_dir=None,sample_output_dir=None):
        req:RequestSample = copy.deepcopy(initial_req)
        initial_str = initial_req.serialize()
        initial_req = req.dump2req(host=self.waf_netloc,
                                        path=webapp["path"],
                                        taint_key=webapp["expected_taint"]["taint_key"],
                                        taint_val=webapp["expected_taint"]["taint_val"])
        resp = request(self.waf_host,self.waf_port,initial_req,timeout=0.5,retry=1)
        bypassed,real_req = waf_verfication(resp)

        if not bypassed:
            print("[Warning] Initial request "+ md5(initial_str) +" is not valid for WAF" +self.waf_name)
            real_req = initial_req

        resp = request(webapp["host"],webapp["port"],real_req,timeout=0.5,retry=1)

        if self.verbose:
            print("[Debug] webapp " + webapp["name"] + " resp: " + str(resp.body_json))

        if not webapp_verfication(resp,webapp["expected_taint"]):
            print("[Error] Initial request "+ md5(initial_str) +" is not valid for " + webapp["name"] + " webapp")
            return

        print("[Info] Start to minimize request "+ md5(initial_str) +" for " + webapp["name"] + " webapp")

        recover_pool = []
        if evasion_output_dir == None:
            evasion_output_dir = os.path.join(MINI_EVASION_DIR,self.waf_name,webapp["name"],md5(initial_str))
            if not os.path.exists(evasion_output_dir):
                os.makedirs(evasion_output_dir)

        if bypassed:
            with open(os.path.join(evasion_output_dir,"orginal."+md5(real_req))+".case","wb") as f:
                f.write(real_req)

        if sample_output_dir == None:
            sample_output_dir = os.path.join(MINI_SAMPLE_DIR,webapp["name"])
            if not os.path.exists(sample_output_dir):
                os.makedirs(sample_output_dir)

        # initial check. centrifuge can only minimize the request which is valid at begining.
        while True:
            removed_node = req.random_remove_node(self.verbose)
            if removed_node == None:
                req_str = req.serialize()
                with open(os.path.join(sample_output_dir,"minimized."+md5(req_str))+".input","w") as f:
                    f.write(req_str)
                break

            req_packet = req.dump2req(host=self.waf_netloc,
                                      path = webapp["path"],
                                      taint_key=webapp["expected_taint"]["taint_key"],
                                      taint_val=webapp["expected_taint"]["taint_val"])
            if self.verbose:
                # print("[Debug] --Minize--")
                # print(req_packet.decode())
                # print("----")
                print("[Debug] webapp " + webapp["name"] + " resp: " + str(resp.body_json))


            waf_resp = request(self.waf_host,self.waf_port,req_packet,timeout=0.5,retry=3)

            bypassed,real_req = waf_verfication(waf_resp)

            if self.verbose:
                print("bypassed",bypassed)

            if not bypassed:
                real_req = req_packet

            resp = request(webapp["host"],webapp["port"],real_req,timeout=0.5,retry=1)
            if self.verbose:
                print("[Debug] status_code",resp.status_code)
                print(resp.body_json)

            valid = webapp_verfication(resp,webapp["expected_taint"])

            if valid and bypassed:
                print("[Info] find evasion for " + self.waf_name + " and " + webapp["name"] + " webapp")
                with open(os.path.join(evasion_output_dir,md5(real_req)+".case"),"wb") as f:
                    f.write(real_req)

            if valid:
                # this node and its tree are not needed
                req.remove_node_children(removed_node)
                req.node_pool.extend(recover_pool)
                recover_pool = []
            else:
                # need to recover this node
                removed_node.recover()
                recover_pool.append(removed_node)

    def run(self,initial_req:RequestSample,webapp:dict,evasion_output_dir=None,sample_output_dir=None):
        req:RequestSample = copy.deepcopy(initial_req)
        initial_str = initial_req.serialize()
        initial_req = req.dump2req(host=self.waf_netloc,
                                        path=webapp["path"],
                                        taint_key=webapp["expected_taint"]["taint_key"],
                                        taint_val=webapp["expected_taint"]["taint_val"])
        resp = request(self.waf_host,self.waf_port,initial_req,timeout=0.5,retry=1)
        bypassed,real_req = waf_verfication(resp)

        if not bypassed:
            print("[Warning] Initial request "+ md5(initial_str) +" is not valid for WAF" +self.waf_name)
            return

        resp = request(webapp["host"],webapp["port"],real_req,timeout=0.5,retry=1)

        if self.verbose:
            print("[Debug] webapp " + webapp["name"] + "resp: " + str(resp.body_json))

        # initial check. centrifuge can only minimize the request which is valid at begining.
        if not webapp_verfication(resp,webapp["expected_taint"]):
            print("[Error] Initial request "+ md5(initial_str) +" is not valid for " + webapp["name"] + " webapp")
            return

        print("[Info] Start to minimize request "+ md5(initial_str) +" for " + webapp["name"] + " webapp")

        if evasion_output_dir == None:
            evasion_output_dir = os.path.join(MINI_EVASION_DIR,self.waf_name,webapp["name"],md5(initial_str))
            if not os.path.exists(evasion_output_dir):
                os.makedirs(evasion_output_dir)

        if bypassed:
            with open(os.path.join(evasion_output_dir,"orginal."+md5(initial_req))+".case","wb") as f:
                f.write(initial_req)

        if sample_output_dir == None:
            sample_output_dir = os.path.join(MINI_SAMPLE_DIR,webapp["name"])
            if not os.path.exists(sample_output_dir):
                os.makedirs(sample_output_dir)

        hash_table = set()

        q = Queue()
        q.put(req)
        while not q.empty():
            node_pool:list[Node] = []
            t_now:RequestSample = q.get()


            if self.verbose:
                print("[Debug] now queue amount is  "+str(q.qsize()))
                print("[Debug] now request is "+t_now.dump2txt())

            for node in t_now.node_pool:
                if (not node.is_terminal) and (not (node.val in FROZEN_SYMBOL)) and (not node.is_visited) and (not node.delete_mark):
                    node_pool.append(node)

            if self.verbose:
                print("[Debug] now node pool amount is "+ str(len(node_pool)))


            if len(node_pool) == 0:
                if self.verbose:
                    print("[Debug] minimized request is "+t_now.dump2txt())
                req_bytes = t_now.dump2req(host=self.waf_netloc,
                                      path = webapp["path"],
                                      taint_key=webapp["expected_taint"]["taint_key"],
                                      taint_val=webapp["expected_taint"]["taint_val"])
                with open(os.path.join(evasion_output_dir,"minimized."+md5(req_bytes))+".case","wb") as f:
                    f.write(req_bytes)
                continue

            inital_req_bytes = t_now.dump2req(host=self.waf_netloc,
                                      path = webapp["path"],
                                      taint_key=webapp["expected_taint"]["taint_key"],
                                      taint_val=webapp["expected_taint"]["taint_val"])

            # try to delete as much node as possible in this stage
            minimized_flag = False
            for node in node_pool:
                node.is_visited = True
                node.delete_mark = True
                if self.verbose:
                    print("[Debug] deleting node "+node.val)
                # If the requst sample is broken, we don't need to further delete it
                if t_now.is_borken():
                    t_now.recover_node(node)
                    continue


                req_packet = t_now.dump2req(host=self.waf_netloc,
                                      path = webapp["path"],
                                      taint_key=webapp["expected_taint"]["taint_key"],
                                      taint_val=webapp["expected_taint"]["taint_val"])

                # We don't need to send the requests if the request is already in the hash table
                if md5(req_packet) in hash_table:
                    continue
                else:
                    hash_table.add(md5(req_packet))

                bypassed,real_req = waf_verfication(request(self.waf_host,self.waf_port,req_packet,timeout=0.5,retry=3))
                if bypassed:
                    if self.verbose:
                        print("[Debug] \n" + real_req.decode() + "\n")
                        print("[Debug] find bypassed request")
                        time.sleep(1)
                    # We don't add the request to the queue if it is not valid for the webapp
                    resp = request(webapp["host"],webapp["port"],real_req,timeout=0.05,retry=1)
                    if self.verbose:
                        print("[Debug] webapp " + webapp["name"] + "resp: " + str(resp.body_json))
                    if not webapp_verfication(resp,webapp["expected_taint"]):
                        if self.verbose:
                            print("[Debug] the request is not valid for the webapp")
                        t_now.recover_node(node)
                        continue
                    # sample can be minimized
                    minimized_flag = True
                    # Confirm to remove the node
                    t_now.remove_node_children(node)
                else:

                    req_str = t_now.serialize()

                    # the sample can not bypass the WAF, so we put it to the corpus to further mutate
                    with open(os.path.join(sample_output_dir,md5(req_str))+".input","w") as f:
                        f.write(req_str)

                    t_now.recover_node(node)
                    # We don't add the request to the queue if it is not valid for the webapp
                    resp = request(webapp["host"],webapp["port"],req_packet,timeout=0.05,retry=1)
                    if self.verbose:
                        print("[Debug] webapp " + webapp["name"] + "resp: " + str(resp.body_json))
                    if not webapp_verfication(resp,webapp["expected_taint"]):
                        if self.verbose:
                            print("[Debug] the request is not valid for the webapp")
                        t_now.recover_node(node)
                        continue

                    # if the sample can not parsed by the webapp, we don't need to further mutate it
                    #if not webapp_verfication(request(webapp["host"],webapp["port"],real_req,timeout=0.05,retry=1),webapp["expected_taint"]):


                if t_now.is_borken():
                    continue

                new_req = copy.deepcopy(t_now)
                q.put(new_req)
            # the request cannot be furhter minimized

            # this request is minimized
            if not minimized_flag:
                bypassed,real_req = waf_verfication(request(self.waf_host,self.waf_port,inital_req_bytes,timeout=0.5,retry=3))
                if bypassed:
                    resp = request(webapp["host"],webapp["port"],real_req,timeout=0.05,retry=1)
                    if webapp_verfication(resp,webapp["expected_taint"]):
                        if self.verbose:
                            print("[Debug] minimized request is "+t_now.dump2txt())
                        with open(os.path.join(evasion_output_dir,"minimized."+md5(inital_req_bytes))+".case","wb") as f:
                            f.write(inital_req_bytes)





class CentrifugeThread(Thread):
    def __init__(self,centrifuge:Centrifuge,initial_req:RequestSample,webapp:dict) -> None:
        super().__init__()
        self.centrifuge = centrifuge
        self.initial_req = initial_req
        self.webapp = webapp
        pass

    def run(self) -> None:
        self.centrifuge.run_simple(self.initial_req,self.webapp)

def centrifuge_task(centrifuge:Centrifuge,initial_req:RequestSample,webapp:dict):
    centrifuge.run(initial_req,webapp)

def run_centrifuge_on_sample(sample_path:str,waf_name:str):
    test_req = RequestSample()
    thread_list = []
    with open(sample_path,"r") as f:
        test_req.unserialize(f.read())

    centrifuge = Centrifuge(WAF[waf_name]["name"],WAF[waf_name]["url"],verbose=True)

    for webapp in WEBAPP_VALIDATOR:
        t = CentrifugeThread(centrifuge,test_req,WEBAPP_VALIDATOR[webapp])
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()


if __name__ == "__main__":
    # further acceleration can be achieved by multi-processing
    for evasion_case in os.listdir(INPUT_EVASION_DIR):
        if evasion_case.endswith(".gitkeep"):
            continue
        run_centrifuge_on_sample(os.path.join(INPUT_EVASION_DIR,evasion_case),"aliyun")

