# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 04:03:47 2018

@author: Ittipat
"""

# Tic Tac Toe

import random
import numpy as np

x = 1 
o = 2

def state2board(state):
    board = (np.random.randn(9, 1) + 0.5) / 1000000
    for i in range(9):
        v = state % 3
        state = state // 3
        if v == 0:
          board[i] = 0
        elif v == 1:
          board[i] = 1
        elif v == 2:
          board[i] = 2

    return board

def board2state(board):
    """h = v * (3 ** k)"""
    h = 0
    k = 0
    v = 0
    for i in range(len(board)):
        if board[i] == 0:
            v = 0
        elif board[i] == x:
            v = 1
        elif board[i] == o:
            v = 2
        h += (3**k) * v
        k += 1
    return h

def drawboard(board):
    
    board_str = []
    for i in range(9):
        if board[i] == 0:
            board_str.append(' ')
        elif board[i] == 1:
            board_str.append('X')
        else:
            board_str.append('O')

    print( '|', board_str[6], '|', board_str[7], '|', board_str[8],  '|')
    print( '|', board_str[3], '|', board_str[4], '|', board_str[5],  '|')
    print( '|', board_str[0], '|', board_str[1], '|', board_str[2],  '|')

def winner(board, x):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    results = ((board[6] == x and board[7] == x and board[8] == x) or # across the top
    (board[3] == x and board[4] == x and board[5] == x) or # across the middle
    (board[0] == x and board[1] == x and board[2] == x) or # across the bottom
    (board[6] == x and board[3] == x and board[0] == x) or # down the left side
    (board[7] == x and board[4] == x and board[1] == x) or # down the middle
    (board[8] == x and board[5] == x and board[2] == x) or # down the right side
    (board[6] == x and board[4] == x and board[2] == x) or # diagonal
    (board[8] == x and board[4] == x and board[0] == x)) # diagonal
    return results
    
def draw(board, x, o):
    if end_game(board):
        results = winner(board, x) == False or winner(board, o) == False
    else:
        results = False
                
    return results
    
def end_game(board):
    results = False
    if winner(board, x) or winner(board, o):
        results = True
    elif all(board != 0):
        results = True
    return results
    

def clear(board):
    state_temp = 0
    return state2board(state_temp)

#class Agent:
#    def __init__(self, state_score, state_his, eps=0.1, alpha=0.5, sym):
#        self.score = np.zeros(3 ** 9)
#        self.state_his = []
#        self.eps = eps
#        self.alpha = alpha
#        self.sym = sym

def make_score():
    return np.zeros((3 ** 9, 2))

def state_score(state_n, score):
    return score[state_n]
    
def take_action(board, sym, eps, score):
    winner_p = None
    if end_game(board) == False:
        global next_move
        next_move = None
        available_state = []
        available_state_score = []
        global state
        state = board2state(board)
        board2 = state2board(state)
        for i in range(9):
            if board[i] == 0:
                board2[i] = sym
                available_statei = board2state(board2)
                available_state_scorei = state_score(board2state(board2), score)
                available_state.append(available_statei)
                available_state_score.append(available_state_scorei)
#                drawboard(board2)
#                print('_________')
            board2 = state2board(state)

        r = np.random.rand()
        if r < eps:
            j = np.random.choice(len(available_state))
            k = available_state[j]
        else:
            j = np.argmax(available_state_score, axis=0)
            k = available_state[j[0]]
        next_move = k
        state = next_move
        board = state2board(state)
    else:
        if winner(board, o):
            winner_p = o
        elif winner(board, x):
            winner_p = x
        else:
            winner_p = 'draw'
      
    return board, state, sym, winner_p
    

def next_play(current_play):
    if current_play == x:
        next_play = o
    else:
        next_play = x
    return next_play

def append_his(his, state):
    his.append(state)
    

def available_state_num(state):
    avai_state = []
    board_n = state2board(state)
    for i in range(9):
        if board_n[i] == 0:
            avai_state.append(i)
   
    return len(avai_state)
    
    
    

    
#def get_available(state)

    
#state = 2187
#board = state2board(state)
#state = board2state(board)
#drawboard(board)

#xiswinner = winner(board, x)
#oiswinner = winner(board, o)
#isdraw = draw(board, x, o)
#endgame = end_game(board)
    

#board = clear(board)
#drawboard(board)
#board = take_action(board, x, 1)
#drawboard(board)
#board = take_action(board, o, 5)
#drawboard(board) 
score_all = make_score()
current_play = x
lr = 0.001

for i in range(500000):
    state = 0
    board = state2board(state)
    his_1 = []
    his_2 = []
    while end_game(board) == False:
        
        board, state, current_play, winner_p = take_action(board, current_play, 0.1, score_all[:, (current_play - 1):current_play])    
        if current_play == x:
            append_his(his_1, state)
#            drawboard(board)
#            print('================')

        elif current_play == o:
            append_his(his_2, state)
#            drawboard(board)
#            print('================')
        
        else:
            print("wrong!!!")
        
        current_play = next_play(current_play)
    
    his_1 = np.flip(his_1, axis=0)
    his_2 = np.flip(his_2, axis=0)
        
    if winner(board, o):
        winner_p = o
        N = np.array(his_2).shape[0]
        for l in range(N):
            if l != 0:
                score_all[:, 1:2][(his_2[l])] += 1 * lr / available_state_num(his_2[l])
            else:
                score_all[:, 1:2][(his_2[l])] += 1 * lr / (l + 1)
                score_all[:, 0:1][(his_2[l])] += - 1 * lr / (l + 1)
        M = np.array(his_1).shape[0]
        for l in range(M):
            if l != 0:
                score_all[:, 0:1][(his_1[l])] += - 1 * lr / available_state_num(his_1[l])
            else:
                score_all[:, 0:1][(his_1[l])] += - 1 * lr / (l + 1) 
    elif winner(board, x):
        winner_p = x
        N = np.array(his_1).shape[0]
        for l in range(N):
            if l != 0:
                score_all[:, 0:1][(his_1[l])] += 1 * lr / available_state_num(his_1[l])
            else:
                score_all[:, 0:1][(his_1[l])] += 1 * lr / (l + 1) 
                score_all[:, 1:2][(his_1[l])] += - 1 * lr / (l + 1)

        M = np.array(his_2).shape[0]
        for l in range(M):
            if l != 0:
                score_all[:, 1:2][(his_2[l])] += - 1 * lr / available_state_num(his_2[l])
            else:
                score_all[:, 1:2][(his_2[l])] += - 1 * lr / (l + 1) 
    else:
        winner_p = 'draw'
#    print("winner is : ", winner_p)
    his_1 = np.flip(his_1, axis=0)
    his_2 = np.flip(his_2, axis=0)
    if i % 1000 == 0:
        print(i)











current_play = x
state = 0
board = state2board(state)
board, state, current_play, winner_p = take_action(board, current_play, 0, score_all[:, (current_play - 1):current_play]) 
drawboard(board)


score = score_all[:, 0:1]

drawboard(board)

board2state(board)
drawboard(state2board(19557))


board = state2board(1)
drawboard(board)
board2state(board)
score_all[81][0]
score_all[1][0]
score_all[9][0]
score_all[7976][0]
score_all[10136][0]









def drawBoard(board):
    # This function prints out the board that it was passed.

    # "board" is a list of 10 strings representing the board (ignore index 0)
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')

def inputPlayerLetter():
    # Lets the player type which letter they want to be.
    # Returns a list with the player's letter as the first item, and the computer's letter as the second.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()

    # the first element in the tuple is the player's letter, the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
    (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

def getBoardCopy(board):
    # Make a duplicate of the board list and return it the duplicate.
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard

def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '

def getPlayerMove(board):
    # Let the player type in his move.
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)

def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


print('Welcome to Tic Tac Toe!')

while True:
    # Reset the board
    theBoard = [' '] * 10
    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'player':
            # Player's turn.
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)

            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('Hooray! You have won the game!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'computer'

        else:
            # Computer's turn.
            move = getComputerMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, move)

            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('The computer has beaten you! You lose.')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'player'

    if not playAgain():
        break