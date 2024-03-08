import random
from .config import grammar
from .model import Node
from typing import List

def dumpRustConfig():
    #data = grammar
    class Rule:
        right:List[str]
        weight:float
        def __init__(self,right=[],weight=0) -> None:
            self.right = right
            self.weight = weight

    class RuleSet:
        left:str
        production:list[Rule]
        def __init__(self,left="",production=[]) ->None:
            self.left = left
            self.production = production

    class Config:
        grammar:dict[str,RuleSet]
        def __init__(self,grammar={}) -> None:
            self.grammar = grammar


    config = Config()
    for key in grammar.keys():
        ruleset = RuleSet(left=key,production=[])
        rules = grammar[key]
        #print(len(rules))
        for rule in rules:
            try:
                right,weight = rule
            except ValueError:
                right = rule
                weight = 1
            ruleset.production.append(Rule(right=right,weight=weight))

        config.grammar[key] = ruleset


    #print(config.grammar["<start>"].production)
    import json

    return json.dumps(config,default=lambda obj: obj.__dict__,indent=2)


# def generatorPacket(base=None,host=None,path=None,taint_key=None,taint_param=None):
#     if base == None:
#         base = f'''POST /{path} HTTP/1.1\r
# User-Agent: Chrome/104.0.5112.102\r
# Accept: */*\r
# Host: {host}\r
# '''
#     content_type_header = Generator("<content_type_header>").build_tree()

#     body = Generator("<body>").build_tree()

#     content_len = len(body)

#     content_len_header = "Content-Length: %d" % content_len

#     packet = base+content_type_header+"\r\n"+content_len_header+"\r\n\r\n"+body
#     return packet




# def outputPacket(base,body_tree:Generator):
#     body = body_tree.output()
#     body_begin = body.find("\r\n\r\n") + len("\r\n\r\n")
#     content_length = len(body) - body_begin
#     content_length_header = "Content-Length: %d" % content_length

#     packet = base + content_length_header +"\r\n" + body
