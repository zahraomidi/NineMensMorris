from Utilies import *

def GenerateAdd(board):
    L = []
    for i in range(0,21):
        if board[i] == 'x':
            temp_board = board
            temp_board[i] = 'w'
            if CloseMill(i, temp_board):
                GenerateRemove(temp_board, L)
            else:
                L.append(temp_board)


     
def GenerateRemove(board, List):
    change = False
    for i in range(0,21):
        if board[i]=='B':
            if not CloseMill(i, board):
                temp_board = board
                temp_board[i] = 'x'
                List.append(temp_board)
                change = True

    if change:
        List.append(board)
