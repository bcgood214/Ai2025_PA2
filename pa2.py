# Benjamin Good, Spring 2025
import numpy as np
import copy
from mcts import Node
import check_state
from tree import Tree
import tree_search as ts

def read_file(name):
    algo = ""
    player = ""
    board = []
    with open(name, "r") as file:
        algo = file.readline()
        player = file.readline()
        for i in range(6):
            board.append(file.readline().replace("\n", ""))
    return algo, player, board

def ur(board, player, runs = 0):
    open = [0 for _ in range(7)]
    for row in board:
        for i in range(7):
            if row[i] == 'O':
                open[i] = 1
    
    print(open)
    
    if open.count(1) > 0:
        while True:
            choice = np.random.choice(7)
            if open[choice] == 1:
                return choice
    return -1

def search_children(node, board):
    for child in node.children:
        count = 0
        for i in range(child.state.shape[0]):
            result = np.array_equal(child.state[i], board[i])
            if result == False:
                count += 1
                break
        if count == 0:
            return True

    
    return False

def get_next_moves(board, player):
    boards = []
    for _ in range(7):
        if board[0, _] == 'O':
            new_board = copy.deepcopy(board)
            new_board, current_pos, col = place(new_board, player, _)
            boards.append((new_board, current_pos, col))
    
    return boards

def get_children(node, player):
    moves = get_next_moves(node.state, player)
    print(f"State: {node.state}")
    print(f"Moves: {moves}")
    for move in moves:
        if not search_children(node, move[0]):
            node.add_child(move[0], move[1], move[2])
    
    node.print_child_states()
    return node

def playout(node, verbose=False):
    choice = ur(node.state, node.player)
    if choice == -1:
        return node
    board, x, y = place(node.state, node.player, choice)
    over = terminal(board, node.player, x, y)

    if not search_children(node, board):
        n = node.add_child(board, x, y)
        n.playouts += 1
    
    if over:
        return node
    
    try:
        return playout(node.get_child(board), verbose=verbose)
    except:
        pass
        # print(f"Final board: {board}")
        # print(f"Children: {node.print_child_states()}")

def mcts_selection(node, verbose=False):
    if node.parent is not None:
        if node.player == 'R':
            player = 'Y'
        else:
            player = 'R'
        over = terminal(node.state, player, node.row_pos, node.col_pos)
        if over:
            return node
    node = get_children(node, node.player)
    # print(f"Children before playout: {node.print_child_states()}")
    for child in node.children:
        if child.playouts == 0:
            child = playout(child)
            child.backpropagate(child.player)
            return child
    
    random_node = np.random.choice(node.children)
    return mcts_selection(random_node, verbose=verbose)
            

def init_board():
    board = np.zeros(shape=(6, 7))
    board = np.where(board == 0, 'O', board)
    print(board)
    return board

def check_right_horizontal(board, player, row, col):
    streak = 0
    i = 1
    while True:
        if col + i > 6 or streak >= 3:
            break
        if board[row, col + i] == player:
            streak += 1
        else:
            break
        i += 1
    
    return streak

def check_left_horizontal(board, player, row, col):
    streak = 0
    i = 1
    while True:
        if col - i < 0 or streak >= 3:
            break
        if board[row, col - i] == player:
            streak += 1
        else:
            break
        i += 1
    
    return streak

def check_horizontal(board, player, row, col):
    streak = 1
    streak += check_right_horizontal(board, player, row, col)
    streak += check_left_horizontal(board, player, row, col)
    if streak >= 4:
        print(f"Horizontal connection at {row}, {col}")
        return True
    return False

def check_upper_vertical(board, player, row, col):
    streak = 0
    i = 1
    while True:
        if row - i < 0 or streak >= 3:
            break
        if board[row - i, col] == player:
            streak += 1
        else:
            break
        i += 1
    
    return streak

def check_lower_vertical(board, player, row, col):
    streak = 0
    i = 1
    while True:
        if row + i > 5 or streak >= 3:
            break
        if board[row + i, col] == player:
            streak += 1
        else:
            break
        i += 1
    
    return streak

def check_vertical(board, player, x, y):
    streak = 1
    streak += check_upper_vertical(board, player, x, y)
    streak += check_lower_vertical(board, player, x, y)
    if streak >= 4:
        print(f"Vertical connection at {x}, {y}")
        return True
    return False

def check_bottomright_diag(board, player, x, y):
    streak = 0
    i = 1
    while True:
        if x+i > 5 or y+i > 6:
            return streak
        if board[x+i, y+i] == player:
            streak += 1
        else:
            return streak
        i += 1

def check_bottomleft_diag(board, player, x, y):
    streak = 0
    i = 1
    while True:
        if x+i > 5 or y-i < 0:
            return streak
        if board[x+i, y-i] == player:
            streak += 1
        else:
            return streak
        i += 1

def check_topright_diag(board, player, x, y):
    streak = 0
    i = 1
    while True:
        if x-i < 0 or y+i > 6:
            return streak
        if board[x-i, y+i] == player:
            streak += 1
        else:
            return streak
        i += 1

def check_topleft_diag(board, player, x, y):
    streak = 0
    i = 1
    while True:
        if x-i < 0 or y-i < 0:
            return streak
        if board[x-i, y-i] == player:
            streak += 1
        else:
            return streak
        i += 1

def diag_check(board, player, x, y):
    streak = 1
    streak += check_bottomright_diag(board, player, x, y)
    streak += check_topleft_diag(board, player, x, y)
    if streak >= 4:
        print(f"Diagonal connection at {x}, {y}")
        return True
    streak = 1
    streak += check_bottomleft_diag(board, player, x, y)
    streak += check_topright_diag(board, player, x, y)
    if streak >= 4:
        print(f"Diagonal connection at {x}, {y}")
        return True
    return False

def terminal(board, player, x, y):
    over = diag_check(board, player, x, y)
    if over:
        return over
    over = check_vertical(board, player, x, y)
    if over:
        return over
    over = check_horizontal(board, player, x, y)
    if over:
        return over
    return False

def place(board, player, col):
    i = 0
    current_pos = 0
    for place in board[: , col]:
        if place != 'O' and i == 0:
            break
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

def play(first_move="R", algo_r="ur", algo_y="ur", algo_r_iter=5, algo_y_iter=5):
    board = init_board()
    if algo_r == "mcts":
        node_r = Node(board)
        tree_r = Tree(node_r)
    if algo_y == "mcts":
        node_y  = Node(board)
        node_y.player = "Y"
        tree_y = Tree(node_y, move="Y")
    if algo_r == "uct":
        pass
    player = first_move
    over = False
    while not over:
        if player == "R":
            if algo_r == "ur":
                choice = ur(board, player)
            if algo_r == "mcts":
                choice = ts.monte_carlo_tree_search(board, algo_r_iter, random=True)[1]
            if algo_r == "uct":
                choice = ts.monte_carlo_tree_search(board, algo_r_iter)[1]
        else:
            if algo_y == "ur":
                choice = ur(board, player)
            if algo_y == "mcts":
                choice = ts.monte_carlo_tree_search(board, algo_y_iter, random=True)[1]
            if algo_y == "uct":
                choice = ts.monte_carlo_tree_search(board, algo_y_iter, player=player)[1]
        print(choice)
        if choice == -1:
            break

        board, x, y = place(board, player, choice)
        print(f"Board: {board}")
        print(f"row: {x}, column: {y}")
        over = check_state.terminal(board, player, x, y)
        if over:
            break
        if player == "R":
            player = "Y"
        else:
            player = "R"
            
    return board

def test_mcts_selection():
    board = init_board()
    node = Node(board)
    print(f"Playouts: {node.playouts}")
    print(f"Wins: {node.wins}")
    node.tree_search()
    print(f"Playouts: {node.playouts}")
    print(f"Wins: {node.wins}")


if __name__ == "__main__":
    play(algo_r="mcts", algo_r_iter=100)