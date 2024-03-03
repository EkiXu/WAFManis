import random
from typing import List,Tuple
import re
from config import grammar

class Node:
    val:str
    is_terminal:bool
    fa: "Node"
    children:List["Node"]
    delete_mark:bool
    def __init__(self,fa:"Node",val:str):
        self.fa = fa
        self.val = val
        self.is_terminal = False
        self.children = None
        self.delete_mark = False
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
        print("[debug] deleting node %s" % self.val)
        self.delete_mark = True
    def recover(self):
        print("[debug] recovering node %s" % self.val)
        self.delete_mark = False

class Generator:
    root:Node
    seed:int
    #非叶节点
    node_pool:List[Node]
    def __init__(self,init_state:str,seed=None):
        self.root = Node(None,init_state)
        self.node_pool = []
        if seed != None:
            random.seed(seed)
        pass
    def build_tree(self):
        from collections import deque
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
    def output(self)->str:
        from collections import deque
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
            #children.reverse()
            q.extendleft(children)
        return res

    # 随机删去一个非叶节点 返回对应的值
    def random_remove_node(self)->Node:
        if len(self.node_pool) == 0:
            return None
        print("[debug] pool amount %d" % len(self.node_pool))
        target = random.randrange(0,len(self.node_pool))
        while self.node_pool[target].delete_mark == True:
            self.node_pool.pop(target)
            if len(self.node_pool) == 0:
                return None
            target = random.randrange(0,len(self.node_pool))

        target_node = self.node_pool[target]
        target_node.delete()
        self.node_pool.pop(target)
        return target_node
        pass

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
            q.extendleft(cur.children)
        return res
    def recover_node(self,node:Node)->bool:
        self.node_pool.append(node)
        return True

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


#if __name__ == "__main__":
    #dumpRustConfig()
    #print(dumpRustConfig())
    #pass
    # res = genSample("<start>")
    # print(res)

    #print(generatorPacket())
