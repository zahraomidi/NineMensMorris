from copy import deepcopy
from Utilies import *
import math

class Node(object):
    def __init__(self, board, blackTurn=False, parent=None, children=None):
        if children == None:
            children = []
        self.board = board
        self.blackTurn = blackTurn
        self.parent = parent
        self.children = children
        self.static = None
        self.MidGame = False
                
    def GenerateMovesOpening(self):           
        for i in range(0,21):
            if self.board[i] == 'x':
                temp_board = deepcopy(self.board)
                temp_board[i] = 'W'
                if CloseMill(i, temp_board):
                    self.GenerateRemove(temp_board)
                    
                else:
                    self.children.append(Node(temp_board, not self.blackTurn, self))

    def GenerateRemove(self, board):
        change = False
        for i in range(0,21):
            if board[i]=='B':
                if not CloseMill(i, board):
                    temp_board = deepcopy(board)
                    temp_board[i] = 'x'
                    self.children.append(Node(temp_board, not self.blackTurn, self))
                    change = True

        if not change:     
            self.children.append(Node(board, not self.blackTurn, self))

    def GenerateHopping(self):
        for i in range(0,21):
            if self.board[i]=='W':
                for j in range(0,21):
                    if self.board[j]=='x':
                        temp_board = deepcopy(self.board)
                        temp_board[i] = 'x'
                        temp_board[j] = 'W'
                        if CloseMill(j, temp_board):
                            self.GenerateRemove(temp_board)
                        else:
                            self.children.append(Node(temp_board, not self.blackTurn, self))

    def GenerateMove(self):
        for i in range(0,21):
            if self.board[i]=='W':
                neighbors = adjacent_locations(i)
                for neighbor in neighbors:
                    if self.board[neighbor] == 'x':
                        
                        temp_board = deepcopy(self.board)
                        temp_board[i]='x'
                        temp_board[neighbor]='W'
                        if CloseMill(neighbor, temp_board):
                            self.GenerateRemove(temp_board)
                        else:
                            self.children.append(Node(temp_board, not self.blackTurn, self))

    
    def GenerateMovesMidgameEndgame(self):
        if self.board.count('W') == 3:
            self.GenerateHopping()
        else:
            self.GenerateMove()
    
    # def MoveGeneratorBlack(self, phase):
    #     self.board = Inverted_Board(self.board)
    #     if phase=='opening':
    #         self.GenerateMovesOpening()
    #     else:
    #         self.GenerateMovesMidgameEndgame()
        
    #     for node in self.children:
    #         node.board = Inverted_Board(node.board)
        
    #     self.board = Inverted_Board(self.board)

    def generate_next_positions(self, phase):
        Midgame_phase = False

        if self.blackTurn:
            self.board = Inverted_Board(self.board)

        playercount = self.board.count('W')
        if playercount >= 8:
            self.MidGame = True

        if self.MidGame or phase == 'midend':
            self.GenerateMovesMidgameEndgame()
        else: 
           self.GenerateMovesOpening()

        if self.blackTurn:
            for node in self.children:
                node.board = Inverted_Board(node.board)
            self.board = Inverted_Board(self.board)


    def static_estimation(self):
        numWhitePieces = self.board.count('W')
        numBlackPieces = self.board.count('B')

        temp_board = Node(self.board)
        temp_board.MoveGeneratorBlack('midend')
        numBlackMoves = len(temp_board.children)

        if numBlackPieces <= 2: self.static = 10000
        elif numWhitePieces <= 2: self.static = -10000
        elif numBlackMoves == 0: self.static = 10000
        else: self.static = (1000*(numWhitePieces - numBlackPieces) - numBlackMoves)

    def static_estimation_opening(self):
        numWhitePieces = self.board.count('W')
        numBlackPieces = self.board.count('B')
        self.static = numWhitePieces - numBlackPieces

    def static_estimation_black(self):
        numWhitePieces = self.board.count('W')
        numBlackPieces = self.board.count('B')

        temp_board = Node(self.board)
        temp_board.GenerateMovesMidgameEndgame()
        numWhiteMoves = len(temp_board.children)

        if numBlackPieces <= 2: self.static = -10000
        elif numWhitePieces <= 2: self.static = 10000
        elif numWhiteMoves == 0: self.static = 10000
        else: self.static = (1000*(numBlackPieces - numWhitePieces) - numWhiteMoves)

    def static_estimation_opening_black(self):
        numWhitePieces = self.board.count('W')
        numBlackPieces = self.board.count('B')
        self.static = numBlackPieces - numWhitePieces


    def static_estimation_opening_improved(self):
        numWhitePieces = self.board.count('W')
        numBlackPieces = self.board.count('B')

        diffInPieces = numWhitePieces - numBlackPieces
        diffIn2pieces = count_2pieces(self.board, 'W') - count_2pieces(self.board, 'B')
        diffInMills = count_mills(self.board, 'W') - count_mills(self.board, 'B')
        diffInNumberOfClosedPieces = countClosedPieces(self.board, 'B') - countClosedPieces(self.board, 'W')

        static = 10 * diffInPieces + \
                    25 * diffIn2pieces + \
                    20 * diffInMills + \
                    10 * diffInNumberOfClosedPieces
        self.static = static 

    def static_estimation_improved(self):
        numWhitePieces = self.board.count('W')
        numBlackPieces = self.board.count('B')

        diffInPieces = numWhitePieces - numBlackPieces
        diffIn2pieces = count_2pieces(self.board, 'W') - count_2pieces(self.board, 'B')
        diffInMills = count_mills(self.board, 'W') - count_mills(self.board, 'B')
        diffInNumberOfClosedPieces = countClosedPieces(self.board, 'B') - countClosedPieces(self.board, 'W')

        if self.MidGame:
            static = 12 * diffInPieces + \
                        30 * diffIn2pieces + \
                        40 * diffInMills + \
                        15 * diffInNumberOfClosedPieces + \
                        2000 * winningConfig(self.board)
        else:
            static = 10 * diffInPieces + \
                    35 * diffIn2pieces + \
                    20 * diffInMills + \
                    10 * diffInNumberOfClosedPieces
        self.static = static 

    def PrintBoard(self):
        board = self.board
        
        print('\n'
	      '                     {}--------------{}---------------{} \n'
		  '                     |               |                |\n'
		  '                     |    {}---------{}----------{}   |\n'
		  '                     |    |          |           |    |\n'
		  '                     |    |    {}----{}-----{}   |    |\n'
		  '                     |    |    |            |    |    |\n'
		  '                     {}---{}---{}           {}---{}---{}\n'
		  '                     |    |    |            |    |    |\n'
		  '                     |    |    {}-----------{}   |    |\n'
		  '                     |    |                      |    |\n'
		  '                     |    {}---------------------{}   |\n'
		  '                     |                                |\n'
		  '                     {}-------------------------------{}\n'.format(
		ch(board[18]),ch(board[19]),ch(board[20]),ch(board[15]),ch(board[16]),ch(board[17]),ch(board[12]),ch(board[13]),
		ch(board[14]),ch(board[6]),ch(board[7]),ch(board[8]),ch(board[9]),ch(board[10]),ch(board[11]),ch(board[4]),
		ch(board[5]),ch(board[2]),ch(board[3]),ch(board[0]),ch(board[1])))
        print()
        print(board_position_to_str(board))