import numpy as np
from mcts import Node

class Tree:
    def __init__(self, node, move="R", curr=None):
        self.root = node
        if curr is None:
            self.currnode = self.root
        else:
            self.currnode = curr
        self.curr_move = move
    
    def build_root(self):
        if len(self.root.children) == 0:
            self.root.load_children()
    
    def find_from_curr(self, board, repeat=True):
        self.currnode.load_children()

        if self.currnode.state_equal(board):
            return self.currnode

        for child in self.currnode.children:
            if child.state_equal(board):
                self.currnode = child
                return child
            if repeat:
                self.currnode = child
                new_node = self.find_from_curr(board, repeat=False)
                if new_node is not None:
                    self.currnode = new_node
                    return new_node
                else:
                    self.currnode = self.currnode.parent