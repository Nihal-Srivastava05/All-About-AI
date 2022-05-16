import math

player = 'x'
opponent = 'o'

ai_board = [['_' for x in range(3)] for y in range(3)]

def isMovesLeft(ai_board):
    for x in range(3):
        for y in range(3):
            if(ai_board[x][y] == '_'):
                return True    
    return False

def evaluationFunction(ai_board):
    for x in range(3):
        if(ai_board[x][0] == ai_board[x][1] and ai_board[x][1] == ai_board[x][2]):
            if(ai_board[x][0] == 'x'):
                return 10
            elif(ai_board[x][0] == 'o'):
                return -10
            
    for y in range(3):
        if(ai_board[0][y] == ai_board[1][y] and ai_board[1][y] == ai_board[2][y]):
            if(ai_board[0][y] == 'x'):
                return 10
            elif(ai_board[0][y] == 'o'):
                return -10
    
    if(ai_board[0][0] == ai_board[1][1] and ai_board[1][1] == ai_board[2][2]):
        if(ai_board[0][0] == 'x'):
            return 10
        elif(ai_board[0][0] == 'o'):
            return -10
    
    if(ai_board[0][2] == ai_board[1][1] and ai_board[1][1] == ai_board[2][0]):
        if(ai_board[0][2] == 'x'):
            return 10
        elif(ai_board[0][2] == 'o'):
            return -10
    
    return 0

def minmax(ai_board, depth, isMax):
    score = evaluationFunction(ai_board)
    if(score == 10):
        return score - depth
    
    if(score == -10):
        return score + depth
    
    if(isMovesLeft(ai_board) == False):
        return 0
    
    if(isMax):
        best = -math.inf
        for x in range(3):
            for y in range(3):
                if(ai_board[x][y] == '_'):
                    ai_board[x][y] = player
                    best = max(best, minmax(ai_board, depth+1, not isMax))
                    ai_board[x][y] = '_'
        return best
    else:
        best = math.inf
        for x in range(3):
            for y in range(3):
                if(ai_board[x][y] == '_'):
                    ai_board[x][y] = opponent
                    best = min(best, minmax(ai_board, depth+1, not isMax))
                    ai_board[x][y] = '_'
        return best

def findBestMove(ai_board):
    bestVal = -math.inf
    bestMove = (-1, -1)
    for x in range(3):
        for y in range(3):
            if(ai_board[x][y] == '_'):
                ai_board[x][y] = player
                moveVal = minmax(ai_board=ai_board, depth=0, isMax=False)
                ai_board[x][y] = '_'
                if(moveVal > bestVal):
                    bestVal = moveVal
                    bestMove = (x, y)
    return bestMove