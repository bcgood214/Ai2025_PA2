import numpy as np
import copy

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

def check_horizontal(board, player, row, col, verbose=False):
    streak = 1
    streak += check_right_horizontal(board, player, row, col)
    streak += check_left_horizontal(board, player, row, col)
    if streak >= 4:
        if verbose:
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

def check_vertical(board, player, x, y, verbose=False):
    streak = 1
    streak += check_upper_vertical(board, player, x, y)
    streak += check_lower_vertical(board, player, x, y)
    if streak >= 4:
        if verbose:
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

def diag_check(board, player, x, y, verbose=False):
    streak = 1
    streak += check_bottomright_diag(board, player, x, y)
    streak += check_topleft_diag(board, player, x, y)
    if streak >= 4:
        if verbose:
            print(f"Diagonal connection at {x}, {y}")
        return True
    streak = 1
    streak += check_bottomleft_diag(board, player, x, y)
    streak += check_topright_diag(board, player, x, y)
    if streak >= 4:
        if verbose:
            print(f"Diagonal connection at {x}, {y}")
        return True
    return False

def terminal(board, player, x, y, verbose=False):
    over = diag_check(board, player, x, y)
    if over:
        return over
    over = check_vertical(board, player, x, y, verbose=verbose)
    if over:
        return over
    over = check_horizontal(board, player, x, y, verbose=verbose)
    if over:
        return over
    return False