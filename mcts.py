import numpy as np
import copy
import check_state

def place(board, player, col):
    i = 0
    current_pos = 0
    for place in board[: , col]:
        if place == 'O' and i < 5:
            current_pos = i
        elif place != 'O':
            board[current_pos, col] = player
            break
        else:
            board[i, col] = player
            break
        i += 1
    
    return board, current_pos, col

def get_next_moves(board, player):
    boards = []
    for _ in range(7):
        if board[0, _] == 'O':
            new_board = copy.deepcopy(board)
            new_board, current_pos, col = place(new_board, player, _)
            boards.append((new_board, current_pos, col))
    
    return boards

class Node:
    def __init__(self, board, row=None, col=None):
        self.wins = 0
        self.playouts = 0
        self.state = board
        self.row_pos = row
        self.col_pos = col
        self.children = np.array([])
        self.parent = None
        self.terminal = False
        self.player = 'R'
    
    def add_child(self, board, row, col):
        n = Node(board)
        if self.player == 'R':
            n.player = 'Y'
        else:
            n.player = 'R'
        n.parent = self
        n.row_pos = row
        n.col_pos = col
        self.children = np.append(self.children, n)
        return n
    
    def print_child_states(self):
        for child in self.children:
            print(child.state)
    
    def state_equal(self, board):
        i = 0
        for row in self.state:
            if not np.array_equal(row, board[i]):
                return False
            i += 1
        
        return True
    
    def get_child(self, board):
        for child in self.children:
            i = 0
            equal = True
            for row in child.state:
                if not np.array_equal(row, board[i]):
                    equal = False
                    break
            if equal:
                return child
        
        return None
    
    def load_children(self):
        moves = check_state.get_next_moves(self.state, self.player)
        # print(moves)
        if len(self.children) == 0:
            for move in moves:
                n = Node(move[0], move[1], move[2])
                if self.player == 'R':
                    n.player = 'Y'
                else:
                    n.player = 'R'
                n.terminal = check_state.terminal(move[0], self.player, n.row_pos, n.col_pos)
                n.parent = self
                self.children = np.append(self.children, n)
    
    def ur(self):
        self.load_children()
        
        return np.random.choice(self.children)
    
    def tree_search(self, runs=5):
        for i in range(runs):
            self.random_rollout()
        
    def pick_best_mcts(self):
        best_child = self.children[0]
        best_rate = 0

        for child in self.children:
            if child.playouts == 0:
                continue
            rate = child.wins / child.playouts
            if rate > best_rate:
                rate = best_rate
                best_child = child
        
        return best_child
    
    def backpropagate(self, winner):
        self.playouts += 1
        if winner == self.player:
            self.wins += 1
        
        if self.parent is not None:
            self.parent.backpropagate(winner)
    
    def random_rollout(self):
        if self.terminal:
            # print(self.state)
            if self.player == 'R':
                winner = 'Y'
            else:
                winner = 'R'
            self.backpropagate(winner)
            return
            
        result = None
        self.load_children()
        if len(self.children) == 0:
            self.terminal = True
            self.backpropagate("N")
            return
        
        children_no_playout = [c.playouts == 0 for c in self.children]
        # print(children_no_playout)
        if True in children_no_playout:
            children_filtered = self.children[np.array([c.playouts == 0 for c in self.children])]
            if len(children_filtered) > 0:
                child = np.random.choice(children_filtered)
        else:
            child = np.random.choice(self.children)
        
        child.random_rollout()

def play_game(node, first_move="R", algo_r="ur", algo_y="ur"):
    over = False
    node.player = first_move
    while not over:
        if node.player == "R":
            if algo_r == "ur":
                choice = node.ur()
            elif algo_r == "mcts":
                node.tree_search()
                choice = node.pick_best_mcts()
        elif node.player == "Y":
            if algo_y == "ur":
                choice = node.ur()
            elif algo_y == "mcts":
                node.tree_search()
                choice = node.pick_best_mcts()
        
        over = choice.terminal
        node = choice
    
    return node.state