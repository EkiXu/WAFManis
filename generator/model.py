import json
from typing import List,Tuple,Callable,Any
from .config import grammar,TAINT_KEY,TAINT_VAL,PATH,CHARSET_POOL
from .utils import encode
import re

import random
from collections import deque
import copy

class Node:
    val:str
    is_terminal:bool
    fa: "Node"
    children:List["Node"]
    delete_mark:bool
    def __init__(self,fa:"Node"=None,val:str=None):
        self.fa = fa
        self.val = val
        self.is_terminal = False
        self.children = None
        self.delete_mark = False
        self.is_visited = False
        pass
    #随机扩展
    def expand(self) -> List["Node"]:
        #叶节点不扩展
        rule:str = None
        for node_type in grammar.keys():
            matched = re.match(node_type,self.val)
            if matched:
                # if node_type.endswith("param>"):
                #     matched.group(1)
                rule = node_type
                self.is_terminal = False
                break
        if rule == None:
            self.is_terminal = True
            return []

        if isinstance(grammar[rule][0],tuple):
            possible_rule = [child_rule for child_rule,_ in grammar[rule]]
            weight = [weight for _,weight in grammar[rule]]
            choice_rule = random.choices(possible_rule,weights=weight,k=1)[0]
        else:
            choice_rule = random.choice(grammar[rule])
        children:List[Node] = []
        for node_type in choice_rule:
            # if node_type.endswith("param>"):
            #     print("debug")
            real_node_type = re.sub(rule, node_type, self.val, 0, re.MULTILINE)
            children.append(Node(self,real_node_type))
        self.children = children
        return children
    def delete(self):
        #print("[debug] deleting node %s" % self.val)
        self.delete_mark = True
    def recover(self):
        #print("[debug] recovering node %s" % self.val)
        self.delete_mark = False

    def __repr__(self) -> str:
        return json.dumps(self,cls=RequestSampleEncoder)


class RequestSampleEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,Node):
            return {
                "val":o.val,
                "is_terminal": o.is_terminal,
                "delete_mark": o.delete_mark,
                "is_visited": o.is_visited,
                "children": o.children
            }
        if isinstance(o,RequestSample):
            return {
                "chosen_charset": o.chosen_charset,
                "root": o.root
            }
        else:
            return super().default(o)

# class RequestSampleDecoder(json.JSONDecoder):
#     def decode(self, s: str, _w: Callable[..., Any] = ...) -> Any:
#         dic = super().decode(s, _w)
#         for dic
#         return

class RequestSample:
    root:Node
    #非叶节点
    node_pool:List[Node]
    raw_data: bytes
    chosen_charset: str

    def __init__(self):
        self.node_pool = []
        pass

    def build_tree(self,init_state:str):
        self.root = Node(None,init_state)
        self.chosen_charset = random.choice(CHARSET_POOL)
        q = deque()
        q.appendleft(self.root)
        res:str = ""
        while q:
            cur:Node = q.popleft()
            self.node_pool.append(cur)
            children = cur.expand()
            if cur.is_terminal:
                res += cur.val
                continue
            children.reverse()
            q.extendleft(children)
        return res

    def dump2txt(self)->str:
        q = deque()
        q.appendleft(self.root)
        res:str = ""
        while q:
            cur:Node = q.popleft()
            #模拟删除
            if cur.delete_mark:
                continue
            children = cur.children
            if cur.is_terminal:
                res += cur.val
                continue
            # not terminal but no child:
            if children is None:
                cur.delete_mark = True
                continue
            #children.reverse()
            q.extendleft(children)
        return res

    def is_borken(self) -> bool:
        req_str = self.dump2txt()
        if (not "__PATH__" in req_str) or (not "__TAINTKEY__" in req_str) or (not "__TAINTVAL__" in req_str) or (not "__LEN__" in req_str) or (not "__HOST__" in req_str) or (not "__CHAR__" in req_str) or (not "__DUMBTAINTVAL__" in req_str):
            return True
        else:
            return False

    def dump2req(self,host,path=PATH,taint_key=TAINT_KEY,taint_val=TAINT_VAL)->bytes:
        raw_packet = self.dump2txt()
        if isinstance(raw_packet,str):
            raw_packet = raw_packet.encode()
        packet = copy.deepcopy(raw_packet)
        if isinstance(host,str):
            host = host.encode()
        if isinstance(taint_key,str):
            taint_key = taint_key.encode()
        if isinstance(taint_val,str):
            taint_val = taint_val.encode()
        if isinstance(path,str):
            path = path.encode()

        packet = packet.replace(b'__PATH__', path)
        packet = packet.replace(b'__TAINTKEY__', taint_key)
        packet = packet.replace(b'__TAINTVAL__',  encode(taint_val.decode(),self.chosen_charset))
        packet = packet.replace(b'__DUMBTAINTVAL__', taint_key)
        packet = packet.replace(b"__CHAR__",self.chosen_charset.encode())

        body_begin = packet.find(b"\r\n\r\n")
        if body_begin !=-1:
            body_begin += len(b"\r\n\r\n")
            content_length = len(packet) - body_begin
            packet = packet.replace(b"__LEN__",str(content_length).encode())

        packet = packet.replace(b"__HOST__",host)
        return packet

    # 随机删去一个非叶节点 返回对应的值
    def random_remove_node(self,seed=None,verbose=False)->Node:
        if len(self.node_pool) == 0:
            return None
        if verbose:
            print("[debug] pool amount %d" % len(self.node_pool))
        if seed != None:
            random.seed(seed)
        target = random.randrange(0,len(self.node_pool))
        while self.node_pool[target].delete_mark == True:
            self.node_pool.pop(target)
            if len(self.node_pool) == 0:
                return None
            target = random.randrange(0,len(self.node_pool))

        if verbose:
            print("[debug] deleteing node %s" % self.node_pool[target].val)

        target_node = self.node_pool[target]
        target_node.delete()
        self.node_pool.pop(target)
        return target_node

    #当节点确认被删除时，删除所有后代
    def remove_node_children(self,node:Node)->None:
        from collections import deque
        q = deque()
        q.appendleft(node)
        res:str = ""
        while q:
            cur:Node = q.popleft()
            #模拟删除
            cur.delete()
            if cur.is_terminal:
                continue
            # self.node_pool.append(cur)
            #children.reverse()
            if cur.children is None:
                continue
            q.extendleft(cur.children)
        return res
    def recover_node(self,node:Node)->bool:
        node.delete_mark = False
        self.node_pool.append(node)
        return True

    def serialize(self) -> str:
        return json.dumps(self,cls=RequestSampleEncoder)

    def undict(self,dict_data:dict) -> Node:
        cur = Node()
        for key in dict_data.keys():
            if key == "children":
                if dict_data[key] != None and len(dict_data[key]) > 0:
                    cur.children = []
                    for child_data in dict_data[key]:
                        child_node = self.undict(child_data)
                        child_node.fa = cur
                        cur.children.append(child_node)
                        self.node_pool.append(child_node)
            else:
                setattr(cur,key,dict_data[key])
        return cur

    def unserialize(self,raw:str):
        data:dict = json.loads(raw)
        self.node_pool = []
        self.chosen_charset = data["chosen_charset"]
        self.root = self.undict(data["root"])


class HTTPResponse:
    raw_packet:bytes
    status_code: int
    headers:dict
    body_json:dict
    def __init__(self,raw_packet:bytes) -> None:
        self.raw_packet = raw_packet
        self.headers = {}
        self.body_json = {}
        try:
            self.parse_header()
            self.parse_body()
        except:
            self.http_version = ""
            self.status_code = "000"

    def parse_header(self):
        if len(self.raw_packet):
            raw_lines = self.raw_packet.splitlines()
            self.http_version = raw_lines[0].split(b" ")[0]
            self.status_code = int(raw_lines[0].split(b" ")[1])
            for header in raw_lines[1:]:
                if header == b"":
                    break
                #print(header)
                key,val = header[:header.index(b":")],header[header.index(b":")+1:]
                self.headers[key.strip().lower()] = val.strip().lower()
        else:
            self.http_version = ""
            self.status_code = "000"
    def parse_body(self):
        body_start = self.raw_packet.find(b"\r\n\r\n")+4
        if body_start > len(self.raw_packet):
            return
        if b"content-Length" in self.headers.keys():
            body_end = int(self.headers[b"content-Length"]) + body_start
        else:
            body_end = len(self.raw_packet)
        #print(self.raw_packet[body_start:body_end])
        content_type = b""
        transfer_encoding = b""
        if b"content-type" in self.headers.keys():
            content_type = self.headers[b"content-type"]

        if b"transfer-encoding" in self.headers.keys():
            transfer_encoding  = self.headers[b"transfer-encoding"]

        if b"application/json" in content_type:
            try:
                self.body_json = json.loads(self.raw_packet[body_start:body_end])
            except Exception as e:
                try:
                    raw_body = self.raw_packet[body_start:body_end]
                    #print("debug here",e,raw_body[raw_body.find(b"{"): raw_body.rfind(b"}")+1])
                    self.body_json = json.loads(raw_body[raw_body.find(b"{"): raw_body.rfind(b"}")+1])
                except Exception as e2:
                    print("body json parser error",e2)
        # else:
        #     print(self.headers)
