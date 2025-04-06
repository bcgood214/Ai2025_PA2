# This code as taken, with some modification, from Google's Gemini
import random
import time


def check_winner(board):
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] != 'O':
                return board[row][col]

    # Check vertical
    for col in range(7):
        for row in range(3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] != 'O':
                return board[row][col]

    # Check diagonals
    for col in range(4):
        for row in range(3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] != 'O':
                return board[row][col]
    for col in range(4):
        for row in range(5, 2, -1):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] != 'O':
                return board[row][col]
    
    if all(all(cell != 'O' for cell in row) for row in board):
        return -1
    
    return 0