from Utilies import *
# from MinMaxTreeNode import Node

# def GenerateAdd(board):
#     L = []
#     for i in range(0,21):
#         if board[i] == 'x':
#             temp_board = board
#             temp_board[i] = 'w'
#             if CloseMill(i, temp_board):
#                 GenerateRemove(temp_board, L)
#             else:
#                 L.append(temp_board)
#     return L

def GenerateHopping(board):
    List = []
    for i in range(0,21):
        if board[i]=='W':
            for j in range(0,21):
                if board[j]=='x':
                    temp_board = board
                    board[i] = 'x'
                    board[j] = 'W'
                    if CloseMill(j, temp_board):
                        GenerateRemove(temp_board, List=List)
                    else:
                        List.append(temp_board)
    return List

def GenerateMove(board):
    List = []
    for i in range(0,21):
        if board[i]=='W':
            n = adjacent_locations(i)
            for neighbor in n:
                if board[neighbor]=='x':
                    temp_board = board
                    temp_board[i]='x'
                    temp_board[neighbor]='W'
                    if CloseMill(neighbor, temp_board):
                        GenerateRemove(temp_board, List)
                    else:
                        List.append(temp_board)
    return List
   
# def GenerateRemove(board, List):
#     change = False
#     for i in range(0,21):
#         if board[i]=='B':
#             if not CloseMill(i, board):
#                 temp_board = board
#                 temp_board[i] = 'x'
#                 List.append(temp_board)
#                 change = True
#     if change:      # check this! --------------------------
#         List.append(board)

#     return List


def MidgameEndgameGeneration(board):
    if board.count('W') == 3:
        return GenerateHopping(board=board)
    else:
        return GenerateMove(board)