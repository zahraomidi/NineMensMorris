from Utilies import *
from MinMaxTreeNode import Node
import math
import time

global position_num

w2 = open('ABtouropening_children.txt', 'w')

def write_children(node, depth):
    w2.write(str(depth))
    w2.write('  ')
    w2.write(board_position_to_str(node.board))
    w2.write('\t')
    if not node.static == None:
        w2.write(str(node.static))
    w2.write('\n')
    for child in node.children:
        write_children(child, depth+1)

def traverse_tree(init_node, depth, max_depth):
    init_node.generate_next_positions('opening')
    if (time.time() - start)<19 and depth<max_depth:
        for child in init_node.children:
            traverse_tree(child, depth+1, max_depth)


def MaxMin(init_node, alpha, betha):

    global position_num
    position_num += 1

    if init_node.children == None or init_node.children == []:
        init_node.static_estimation_improved()
        return init_node.static
    
    # v = -math.inf
    v = -200000
    for child in init_node.children:
        v = max(v, MinMax(child, alpha, betha)) 
        if v >= betha:
            init_node.static = v
            return v
        else:
            alpha = max(v, alpha)

    init_node.static = v
    return v

def MinMax(init_node, alpha, betha):

    global position_num
    position_num += 1

    if init_node.children == None or init_node.children == []:
        init_node.static_estimation_improved()
        return init_node.static
    
    # v = math.inf
    v = 200000
    for child in init_node.children:
        v = min(v, MaxMin(child, alpha, betha))
        if v <= alpha:
            init_node.static = v
            return v
        else:
            betha = min(v, betha)

    init_node.static = v
    return v

if __name__ == '__main__':
    
    board = 'BBBBxxxWxBWWxxxWBWWBW'
    board = 'xxxxxxxxxxxxxBxxxxxxx'
    board = [item for item in board]

    max_depth = 40
    # temp_board = Node(board=board)
    temp_board = Node(board=board, blackTurn=True)
    temp_board.PrintBoard()

    position_num = 0
    
    start = time.time()
    traverse_tree(temp_board, 0, max_depth)
    
    output_static = MaxMin(temp_board, -math.inf, math.inf)
    end = time.time()

    print(str((end-start)))
    write_children(temp_board, 0)

    Best_Move = temp_board
    Best_static = -math.inf
    for child in temp_board.children:
        # print(child.static)
        if child.static > Best_static:
            Best_static = child.static
            Best_Move = child

    Best_Move.PrintBoard()
    # print(str(board_position_to_str(Best_Move.board)))

    # w = open(output_file, 'w')

    # w.write('Board Position:\t')
    # w.write(str(board_position_to_str(Best_Move.board)) + '\n')

    # w.write('Positions evaluated by static estimation:\t')
    # w.write(str(position_num)+'\n')

    # w.write('MINIMAX estimate:\t')
    # w.write(str(Best_Move.static))