from Utilies import *
from MinMaxTreeNode import Node
import math

w2 = open('bb_game.txt', 'w')

def write_children(node):
    w2.write(board_position_to_str(node.board))
    w2.write('\t')
    w2.write(str(node.static))
    w2.write('\n')
    for child in node.children:
        write_children(child)


def traverse_tree(init_node, node_depth, tree_depth):
    if node_depth < tree_depth:
        if init_node.blackTurn:
            init_node.MoveGeneratorBlack('midend')
        else:
            init_node.GenerateMovesMidgameEndgame()

        for child in init_node.children:
            traverse_tree(child, node_depth+1, tree_depth)

def MaxMin(init_node):

    global position_num
    position_num += 1

    if init_node.children == None or init_node.children == []:
        init_node.static_estimation()
        return init_node.static
    
    v = -math.inf
    for child in init_node.children:
        v = max(v, MinMax(child)) 
    
    init_node.static = v
    return v

def MinMax(init_node):

    global position_num
    position_num += 1
     
    if init_node.children == None or init_node.children == []:
        init_node.static_estimation()
        return init_node.static
    
    v = math.inf
    for child in init_node.children:
        v = min(v, MaxMin(child))

    init_node.static = v
    return v

if __name__ == '__main__':
    # input_file = input("Please enter the input file name:\n")
    # output_file = input("Please enter the output file name:\n")
    # depth = int(input("Please enter the depth:\n"))

    input_file = 'b1.txt'
    output_file = 'b4.txt'
    depth = 2

    global position_num
    position_num = 0

    f = open(input_file, "r")
    board = f.read()
    board = [item for item in board]
    temp_board = Node(board=board)
    
    traverse_tree(temp_board, 0, depth)
    
    output_static = MaxMin(temp_board)

    write_children(temp_board)

    print(position_num)

    Best_Move = temp_board
    Best_static = -math.inf
    for child in temp_board.children:
        if child.static > Best_static:
            Best_static = child.static
            Best_Move = child

    Best_Move.PrintBoard()

    w = open(output_file, 'w')

    w.write('Board Position:\t')
    w.write(str(board_position_to_str(Best_Move.board)) + '\n')

    w.write('Positions evaluated by static estimation:\t')
    w.write(str(position_num)+'\n')

    w.write('MINIMAX estimate:\t')
    w.write(str(Best_Move.static))