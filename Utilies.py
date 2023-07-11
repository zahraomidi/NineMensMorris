MILLS = ((0, 6, 18), (1, 11, 20), (2, 7, 15), (3, 10, 17), 
         (4, 8, 12), (5, 9, 14), (6, 7, 8), (9, 10, 11),
         (15, 16, 17), (13, 16, 19), (18, 19, 20))

def count_2pieces(board, player):
    count = 0
    for trio in MILLS:
        if board[trio[0]] == board[trio[1]] == player and board[trio[2]] == 'x':
            count += 1
        if board[trio[0]] == board[trio[2]] == player and board[trio[1]] == 'x':
            count += 1
        if board[trio[2]] == board[trio[1]] == player and board[trio[0]] == 'x':
            count += 1
    
    return count

def count_mills(board, player):
    count = 0
    for trio in MILLS:
        if board[trio[0]] == board[trio[1]] == board[trio[2]] == player:
            count += 1
        if board[trio[0]] == board[trio[2]] == board[trio[1]] == player:
            count += 1
        if board[trio[2]] == board[trio[1]] == board[trio[0]] == player:
            count += 1
    
    return count

def countClosedPieces(board, player):
    count = 0
    for loc in range(0, 21):
        if board[loc] == player:
            temp = True
            adjacents = adjacent_locations(loc)
            for adj in adjacents:
                if board[adj] == 'x':
                    temp = False
            if temp: count += 1
    
    return count

def allPlayerPiecesClosed(board, player):
    if board.count(player) == countClosedPieces(board, player):
        return True
    return False

def winningConfig(board):
    if allPlayerPiecesClosed(board, 'W') or board.count('W') < 3:
        return 1
    if allPlayerPiecesClosed(board, 'B') or board.count('B') < 3:
        return -1
    return 0


def adjacent_locations(location):
    adjacent_locs = [
        [1,6],
        [0,11],
        [3,7],
        [2,10],
        [5,8],
        [4,9],
        [0,7,18],
        [2,6,8,15],
        [4,7,12],
        [5,10,14],
        [3,9,11,17],
        [1,20],
        [8,13],
        [12,14,16],
        [9,13],
        [7,16],
        [15,17],
        [10,16],
        [6,19],
        [16,18,20],
        [11,19]
    ]

    return adjacent_locs[location]

def get_Mill_neighbors(location):
    # if length is 2 then this location makes only one mill
    # if length is 4 then the first 2 make one mill and the second 2 numbers make the second mill
    Mill_neighbors = [
        [6,18],
        [11,20],
        [7,15],
        [10,17],
        [8,12],
        [9,14],
        [0,18,7,8],
        [6,8,2,15],
        [6,7,4,12],
        [5,14,10,11],
        [9,11,3,17],
        [1,20,9,10],
        [4,8,13,14],
        [12,14,16,19],
        [5,9,12,13],
        [2,7,16,17],
        [15,17,13,19],
        [3,10,15,16],
        [0,6,19,20],
        [18,20,13,16],
        [1,11,18,19]
    ]
    return Mill_neighbors[location]


def CloseMill(loc, board):
    C = board[loc]
    if C == 'x':
        return False
    neighbors = get_Mill_neighbors(loc)
    if len(neighbors)==2:
        if board[neighbors[0]] == C and board[neighbors[1]] == C:
            return True
        else:
            False
    else:
        if board[neighbors[0]] == C and board[neighbors[1]] == C:
            return True
        elif board[neighbors[2]] == C and board[neighbors[3]] == C:
            return True
        else:
            return False


def Inverted_Board(board):
    inverted_Board = ['x' for i in range(21)] 
    for index, piece in enumerate(board):
        if piece == 'W':
            inverted_Board[index] = 'B'
        elif piece == 'B':
            inverted_Board[index] = 'W'
        else:
            inverted_Board[index] = 'x'

    return inverted_Board


def generateInvertedBoardList(board_list):
    result = []
    for i in board_list:
        result.append(Inverted_Board(i))

    return result


def board_position_to_str(board):
    result = ''
    for item in board:
        result += str(item)

    return result