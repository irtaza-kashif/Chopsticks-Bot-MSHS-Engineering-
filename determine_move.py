from possible_moves import p1Moves, p2Moves

searchDepth = 15

def evaluatePos(position):
    if position[0] == [0, 0]:
            return -1 # Player 2 wins
    elif position[1] == [0, 0]:
            return 1 # Player 1 wins
    return 0 # No one has won

def minimax(position, depth, alpha, beta, maximizing_player):
    score = evaluatePos(position) / (depth + 1) # Prioritizes sooner wins and later losses
    
    if (depth == searchDepth) or (score != 0):
        return score

    if maximizing_player:
        maxEval = float('-inf')
        children = p1Moves(position[0], position[1])
        
        for child in children:
            eval = minimax(child, depth + 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')        
        children = p2Moves(position[0], position[1])        
        for child in children:
            eval = minimax(child, depth + 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
    return minEval

def find_best_move(position):
    best_val = float("-inf")
    best_move = None
    children = p1Moves(position[0], position[1])
    
    for child in children:
        move_val = minimax(child, 0, float("-inf"), float("inf"), False)  
        if move_val > best_val:
            best_val = move_val
            best_move = child
    
    return best_move

# test_moves = [[[1, 1], [1, 1]], [[4, 0], [1, 0]], [[0, 2], [3, 0]], [[0, 4], [0, 1]]]

# for move in test_moves:
#     print(find_best_moveP1(move))