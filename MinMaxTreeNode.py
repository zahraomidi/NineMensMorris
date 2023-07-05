from copy import deepcopy
from Utilies import *
from Generate import *

class Node(object):
    def __init__(self, board, blackTurn=False, parent=None, nextNodes=None):
        if nextNodes == None:
            nextNodes = []
        self.board = board
        self.blackTurn = blackTurn
        # if self.blackTurn:
        #     self.board = Inverted_Board(self.board)
        #     print("inverted board")
        self.parent = parent
        self.nextNodes = nextNodes
                
    def generate_opening_children(self):            #GenerateAdd function in handout
        for i in range(0,21):
            if self.board[i] == 'x':
                temp_board = deepcopy(self.board)
                temp_board[i] = 'W'
                if CloseMill(i, temp_board):
                    self.GenerateRemove(temp_board)
                    
                else:
                    self.nextNodes.append(Node(temp_board, not self.blackTurn, self))

    def GenerateRemove(self, board):
        change = False
        for i in range(0,21):
            if board[i]=='B':
                if not CloseMill(i, board):
                    temp_board = deepcopy(board)
                    temp_board[i] = 'x'
                    self.nextNodes.append(Node(temp_board, not self.blackTurn, self))
                    change = True

        if not change:     
            self.nextNodes.append(Node(board, not self.blackTurn, self))
