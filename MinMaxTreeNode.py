from copy import deepcopy
from Utilies import *
from Generate import *

class Node(object):
        
	def __init__(self, board, blackTurn=False, parent=None, nextNodes=None):
		if nextNodes == None:
			nextNodes = []
		self.board = board
		self.blackTurn = blackTurn
        if self.blackTurn:
            self.board = Inverted_Board(self.board)
		self.parent = parent
		self.nextNodes = nextNodes
                
    def make_children_opening(self):
        for i in range(0,21):
            if self.board[i] == 'x':
                temp_board = deepcopy(self.board)
                temp_board[i] = 'w'
                if CloseMill(i, temp_board):
                    self.GenerateRemove()
                else:
                    self.nextNodes.append(Node(temp_board, not self.blackTurn, self))

    def GenerateRemove(self):
        change = False
        for i in range(0,21):
            if self.board[i]=='B':
                if not CloseMill(i, self.board):
                    temp_board = deepcopy(self.board)
                    temp_board[i] = 'x'
                    self.nextNodes.append(Node(temp_board, not self.blackTurn, self))
                    change = True
                    
        if not change:      # check this! --------------------------
            self.nextNodes.append(board)