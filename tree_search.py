# Google's Gemini was used to provide a skeleton for this module.

import numpy as np
import random
import math
import check_state
from connect4 import check_winner

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.sa_pair = []
    
    def uct_value(self, c=1.4):
      if self.visits == 0:
        return float('inf')
      else:
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)

def monte_carlo_tree_search(root_state, iterations, player='R', random=False):
    root_node = Node(root_state)
    if check_winner(root_state) != 0:
        # print(root_state)
        return (root_node, -1)

    for _ in range(iterations):
        if random:
            node = select_random(root_node)
        else:
            node = select(root_node)
        if check_winner(node.state) == 0:
            node = expand(node,move=player)
            reward = simulate(node.state, move=player)
            backpropagate(node, reward)
    
    return best_option(root_node)

def select(node):
    while node.children and check_winner(node.state) == 0:
        best_child = max(node.children, key=lambda c: c.uct_value())
        node = best_child
        t_flag = False
    
    return node

def select_random(node):
    if node.children and check_winner(node.state) == 0:
        node = random.choice(node.children)
        t_flag = False
    
    return node

def expand(node, move='R'):
    possible_actions = get_possible_actions(node.state, move)
    for action in possible_actions:
        new_state = action[0]
        col = action[2]
        child_node = Node(new_state, parent=node)
        node.children.append(child_node)
        node.sa_pair.append((child_node, col))
    return random.choice(node.children)

def simulate(state, move='R'):
    col = None
    while check_winner(state) == 0:
        possible_actions = get_possible_actions(state, move)
        rand_choice = random.choice(possible_actions)
        state = rand_choice[0]
        col = rand_choice[2]
        # state = take_action(state, action)
    return get_reward(state, move)

def backpropagate(node, reward):
    while node is not None:
        node.visits += 1
        node.wins += reward
        node = node.parent

def best_child(node):
    return max(node.children, key=lambda c: c.visits)

def best_option(node):
    return max(node.sa_pair, key=lambda c: c[0].visits)

# def is_terminal(state):
#     for i in range(6):
#         for j in range(7):
#             red_won = check_state.terminal(state, 'R', i, j)
#             if red_won:
#                 return True
#             yellow_won = check_state.terminal(state, 'Y', i, j)
#             if yellow_won:
#                 return True
    
#     return False

def red_wins(state):
    if check_winner(state) == 'R':
        return True
    
    return False

def yellow_wins(state):
    if check_winner(state) == 'Y':
        return True
    
    return False

def get_possible_actions(state, player='R'):
    return check_state.get_next_moves(state, player)

def take_action(state, action):
    # Implementation depends on the specific game
    pass

def get_reward(state, move):
    red_won = red_wins(state)
    yellow_won = yellow_wins(state)
    if move == 'R' and red_won:
        return 1
    elif move == 'R' and yellow_won:
        return -1
    elif move == 'Y' and red_won:
        return -1
    elif move == 'Y' and yellow_won:
        return 1
    
    return 0