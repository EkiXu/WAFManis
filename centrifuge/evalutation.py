import config
import sys
from generator.model import RequestSample
from utils import webapp_verfication,request
import copy

def markup_on_byes(raw_packet,host,path):
    if isinstance(raw_packet,str):
        raw_packet = raw_packet.encode()
    packet = copy.deepcopy(raw_packet)
    if isinstance(host,str):
        host = host.encode()
    if isinstance(path,str):
        path = path.encode()

    packet = packet.replace(b'__PATH__', path)

    body_begin = packet.find(b"\r\n\r\n")
    if body_begin !=-1:
        body_begin += len(b"\r\n\r\n")
        content_length = len(packet) - body_begin
        packet = packet.replace(b"__LEN__",str(content_length).encode())

    packet = packet.replace(b"__HOST__",host)
    return packet

if __name__ == "__main__":
    evasion_path = sys.argv[1]
    req_bytes = open(evasion_path, 'rb').read()
    for webapp_name in config.WEBAPP_VALIDATOR:
        webapp = config.WEBAPP_VALIDATOR[webapp_name]
        print(f"Testing {webapp_name}")
        real_req = markup_on_byes(req_bytes,webapp["host"]+":"+str(webapp["port"]),webapp["path"])
        #print(real_req)
        resp = request(webapp["host"],webapp["port"],real_req,timeout=0.05,retry=1)
        print(resp.body_json)
        if webapp_verfication(resp,webapp["expected_taint"]):
            print(f"[Info] {webapp_name} webapp_verfication passed")
