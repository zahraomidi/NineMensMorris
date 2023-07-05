class Node(object):
	def __init__(self, board, blackTurn, parent=None, nextNodes=None):
		if nextNodes == None:
			nextNodes = []
		self.board = board
		self.blackToMove = blackTurn
		self.parent = parent
		self.nextStates = nextNodes
		
    