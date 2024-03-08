import random
import copy
import re
from collections import deque
from generator.model import RequestSample,Node
from .config import CHAR_POOL,FROZEN_SYMBOL,ENCODE_TYPE
from .utils import encode

class Mutator:

    seed = 'random'

    def __init__(self, _input:RequestSample, seed='random', verbose=False):
        self.input:RequestSample = _input
        self.seed = seed
        if self.seed=='random':
            random.seed()
        else:
            random.seed(seed)
        self.verbose = verbose
        self.mutation_messages = []

    # 做节点变异或结构变异
    def mutate_input(self):
        node_to_mutate_pool = self.input.node_pool
        if node_to_mutate_pool == []:
            return
        node_to_mutate = random.choice(node_to_mutate_pool)
        mutators=[]
        while node_to_mutate.val in FROZEN_SYMBOL or (node_to_mutate.fa and node_to_mutate.fa.val in FROZEN_SYMBOL):
            node_to_mutate = random.choice(node_to_mutate_pool)


        if self.verbose == True:
            print("Now mutating input node",node_to_mutate)

        if node_to_mutate.is_terminal:
            mutators.extend([
                'remove_random_character',
                'encode_characters',
                'insert_random_character',
            ])
        else:
            mutators.extend([
                'replace_random_node',
                'remove_random_node',
                'duplicate_random_node',
            ])

        chosen_mutator = random.choice(mutators)

        if self.verbose == True:
            print("chosen",chosen_mutator )


        #调用mutator
        getattr(self, chosen_mutator)(node_to_mutate, self.verbose)

        if self.verbose == True:
            print("After Mutating",node_to_mutate)


    def remove_random_character(self, node:Node, verbose=False):
        """Remove a character at a random position"""
        val = node.val
        if val:
            pos = random.randint(0, len(val) - 1)
            if verbose:
                print("Removing character {} at pos {} of {}.".format(repr(val[pos]), pos, node.val))
            else:
                self.mutation_messages.append("Removing character {} at pos {} of {}.".format(repr(val[pos]), pos, node.val))

            node.val = val[:pos] + val[pos+1:]

    def insert_random_character(self, node:Node, verbose=False):
        """Insert a random character at a random position"""
        val = node.val
        if val:
            pos = random.randint(0, len(val) - 1)
            #random_character = chr(random.randrange(0, 127))
            #random_character = random_choose_with_weights(self.config.char_pool)
            random_character = random.choice(CHAR_POOL)
            if verbose:
                print("Inserting character {} at pos {} of {}.".format(repr(random_character), pos, node.val))
            else:
                self.mutation_messages.append("Inserting character {} at pos {} of {}.".format(repr(random_character), pos, node.val))

            node.val = val[:pos] + random_character + val[pos:]

    def replace_random_character(self, node:Node, verbose=False):
        """Replace a character at a random position with a random character"""
        value = node.val
        if value:
            pos = random.randint(0, len(value) - 1)
            #random_character = chr(random.randrange(0, 127))
            random_character = random.choice(CHAR_POOL)
            if verbose:
                print("Replacing character {} at pos {} with {}.".format(repr(node.val), pos, repr(random_character)))
            else:
                self.mutation_messages.append("Replacing character {} at pos {} with {}.".format(repr(node.val), pos, repr(random_character)))

            node.val = value[:pos] + random_character + value[pos+1:]


    def encode_characters(self, node:Node, verbose=False):
        """Replace a character at a random position with a random character"""
        value = node.val
        if value:
            encode_type = random.choice(ENCODE_TYPE)
            encode_msg = encode(value,encode_type)
            if verbose:
                print("Encoding {} with {}.".format(repr(node.val), encode_type))
            else:
                self.mutation_messages.append("Encoding {} with {}.".format(repr(node.val), encode_type))
            node.val = encode_msg
            
            

    def remove_random_node(self, node:Node, verbose=False):
        """Remove a child at a random position"""
        #self.input.random_remove_node(self.seed)
        children = node.children
        if children:
            pos = random.randint(0, len(node.children) - 1)
            child = node.children[pos]
            if verbose:
                print("Remove child {} ".format(repr(child), pos))
            else:
                self.mutation_messages.append("Remove child {} at pos {}.".format(repr(child.val), pos))
            try:
                self.input.remove_node_children(child)
            except:
                pass
            node.children.pop(pos)


    def replace_random_node(self, node:Node, verbose=False):
        """Replace node children with another node children"""
        node_to_replace_pool = [v for v in self.input.node_pool if (v is node) and (not v.is_terminal) and (not node.fa is v) and (not v.fa is node)]
        node_to_replace = random.choice(node_to_replace_pool)

        if verbose:
            print("Replace  {} 's children with {} 's children.".format(repr(node.val), repr(node_to_replace.val)))
        else:
            self.mutation_messages.append("Replace  {} 's children with {} 's children.".format(repr(node.val), repr(node_to_replace.val)))

        #swap
        node.children,node_to_replace.children = node_to_replace.children,node.children


    def duplicate_random_node(self, node:Node, verbose=False):
        """Insert a child at a random position"""
        children = node.children
        if children:
            child = copy.deepcopy(random.choice(children))

            pos = random.randint(0, len(node.children) - 1)
            if verbose:
                print("Duplicate child {} at pos {} of {}.".format(repr(child.val), pos,node.val))
            else:
                self.mutation_messages.append("Duplicate child {} at pos {} of {}.".format(repr(child.val), pos,node.val))

            node.children.insert(pos,child)
            self.input.node_pool.append(child)
