import random
import copy
import re
from collections import deque
from python_mutators.tree_node import Node
from python_mutators.request import Request
from python_mutators.helper_functions import _print_exception
from python_mutators.config import Config

class Mutator:

    mutation_types = {0, # tree mutations
                     1} # string mutations

    def __init__(self, _input:Request, config:Config, seed='random', verbose=False, reproduce_mode = False):
        self.input = _input
        self.config=config
        if seed=='random':
            random.seed()
        else:
            random.seed(seed)
        self.max_num_mutations = config.max_num_mutations
        self.min_num_mutations = config.min_num_mutations
        self.reproduce_mode = reproduce_mode
        self.verbose = verbose
        self.mutation_messages = []
        #self.symbol_mutation_types = symbol_mutation_types
        self.char_pool = config.char_pool
        self.immutable_fields_num=config.immutable_fields_num

    # 做节点变异或结构变异
    def mutate_input(self, source_of_mutations = []):
        try:
            if source_of_mutations == []:
                #选择变异次数
                num_mutations = random.randint(self.min_num_mutations, self.max_num_mutations)
                num_done_mutations = 0
                if self.reproduce_mode:
                    self.input_initial_state = copy.deepcopy(self.input)
                    self.mutations = []                
                
                while num_done_mutations < num_mutations:
                    node_to_mutate_pool = [node for node in self.input.node_dict.values() if not node.symbol == "<start>"]
                    if node_to_mutate_pool == []:
                        break
                    node_to_mutate = random.choice(node_to_mutate_pool)
                    #part_to_mutate_name=random.choice(self.config.mutate_parts)
                    mutators=[]
                    extra_args={}

                    if self.verbose == True:
                        print("Now mutating input node",node_to_mutate)
                    
                    if node_to_mutate.is_terminal:
                        mutators.extend([
                            'remove_random_character',
                            'replace_random_character',
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

                    if self.reproduce_mode:
                        self.mutations.append([chosen_mutator, node_to_mutate, random.getstate()])
                    
                    #调用mutator
                    getattr(self, chosen_mutator)(node_to_mutate, self.verbose)
                    
                    if self.verbose == True:
                        print("After Mutating",node_to_mutate)
                
                    num_done_mutations += 1

            else:
                for mutation in source_of_mutations:
                    random.setstate(mutation[2])
                    self.__getattribute__(mutation[0])(mutation[1], False)

        except Exception as exception: 
            _print_exception()
            raise(exception)


    def remove_random_character(self, node:Node, verbose=False):
        """Remove a character at a random position"""
        value = node.value
        if value:
            pos = random.randint(0, len(value) - 1)
            if verbose:
                print("Removing character {} at pos {} of {}.".format(repr(value[pos]), pos, node.symbol))
            else:
                self.mutation_messages.append("Removing character {} at pos {} of {}.".format(repr(value[pos]), pos, node.symbol)) 

            node.value = value[:pos] + value[pos+1:]

    def insert_random_character(self, node:Node, verbose=False):
        """Insert a random character at a random position"""
        value = node.value
        if value:
            pos = random.randint(0, len(value) - 1)
            #random_character = chr(random.randrange(0, 127))
            #random_character = random_choose_with_weights(self.config.char_pool)
            random_character = random.choice(self.config.char_pool).encode()
            if verbose:
                print("Inserting character {} at pos {} of {}.".format(repr(random_character), pos, node.symbol))
            else:
                self.mutation_messages.append("Inserting character {} at pos {} of {}.".format(repr(random_character), pos, node.symbol))

            node.value = value[:pos] + random_character + value[pos:]

    def replace_random_character(self, node:Node, verbose=False):
        """Replace a character at a random position with a random character"""
        value = node.value
        if value:
            pos = random.randint(0, len(value) - 1)
            #random_character = chr(random.randrange(0, 127))
            random_character = random.choice(self.config.char_pool).encode()
            if verbose:
                print("Replacing character {} at pos {} with {}.".format(repr(node.symbol), pos, repr(random_character)))
            else:
                self.mutation_messages.append("Replacing character {} at pos {} with {}.".format(repr(node.symbol), pos, repr(random_character)))

            node.value = value[:pos] + random_character + value[pos+1:]
        

    def remove_random_node(self, node:Node, verbose=False):
        """Remove a child at a random position"""
        children = node.children
        if children:
            pos = random.randint(0, len(node.children) - 1)
            child = node.children[pos]
            if verbose:
                print("Remove child {} at pos {}.".format(repr(child), pos))
            else:
                self.mutation_messages.append("Remove child {} at pos {}.".format(repr(child.symbol), pos))
            try:
                self.input.node_dict.pop(child.id)
            except:
                pass
            node.children.pop(pos)
        

    def replace_random_node(self, node:Node, verbose=False):
        """Replace node children with another node children"""
        node_to_replace_pool = [v for v in self.input.node_dict.values() if v.id !=node.id and (not v.is_terminal) and (not v.is_father(node)) and (not node.is_father(v))]
        node_to_replace = random.choice(node_to_replace_pool)

        if verbose:
            print("Replace  {} 's children with {} 's children.".format(repr(node.id), repr(node_to_replace.id)))
        else:
            self.mutation_messages.append("Replace  {} 's children with {} 's children.".format(repr(node.id), repr(node_to_replace.id)))

        #swap
        node.children,node_to_replace.children = node_to_replace.children,node.children

        # children = node.children
        # if children:
        #     pos = random.randint(0, len(node.children) - 1)

        # node.children = children[:pos] + children[pos+1:]
        #pass

    def duplicate_random_node(self, node:Node, verbose=False):
        """Insert a child at a random position"""
        children = node.children
        if children:
            child = copy.deepcopy(random.choice(children))
            child.update_id()

            pos = random.randint(0, len(node.children) - 1)
            if verbose:
                print("Duplicate child {} at pos {} of {}.".format(repr(child.symbol), pos,node.symbol))
            else:
                self.mutation_messages.append("Duplicate child {} at pos {} of {}.".format(repr(child.symbol), pos,node.symbol))

            node.children.insert(pos,child)

    def reproduce():
        pass