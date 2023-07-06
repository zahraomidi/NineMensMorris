from copy import deepcopy
from Utilies import *
from Generate import *
import math

class Node(object):
    def __init__(self, board, blackTurn=False, parent=None, children=None):
        if children == None:
            children = []
        self.board = board
        self.blackTurn = blackTurn
        # if self.blackTurn:
        #     self.board = Inverted_Board(self.board)
        #     print("inverted board")
        self.parent = parent
        self.children = children
        self.static = -math.inf
                
    def generate_opening_children(self):            #GenerateAdd function in handout
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
                    if self.board[neighbor]=='x':
                        temp_board = deepcopy(self.board)
                        temp_board[i]='x'
                        temp_board[neighbor]='W'
                        if CloseMill(neighbor, temp_board):
                            self.GenerateRemove(temp_board)
                        else:
                            self.children.append(Node(temp_board, not self.blackTurn, self))

    def MoveGeneratorBlack(self, phase):
        self.board = Inverted_Board(self.board)
        if phase=='opening':
            self.generate_opening_children()
        elif phase=="hopping":
            self.GenerateHopping()
        else:
            self.GenerateMove()
        
        for node in self.children:
            node.board = Inverted_Board(node.board)
        
        self.board = Inverted_Board(self.board)