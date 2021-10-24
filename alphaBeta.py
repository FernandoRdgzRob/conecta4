from tablero import *
from random import shuffle

def AlphaBeta(Board, depth, player):
    validMovements = getValidMovements(Board)
    shuffle(validMovements)
    bestMovement = validMovements[0]
    bestScore = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    if player == AI: opponent = HUMAN
    else: opponent = AI
    for movement in validMovements:
        tempBoard = makeMovement(Board, movement, player)[0]
        boardScore = minimizeBeta(tempBoard, depth - 1, alpha, beta, player, opponent)
        if boardScore > bestScore:
            bestScore = boardScore
            bestMovement = movement
    return bestMovement

def minimizeBeta(Board, depth, a, b, player, opponent):
    validMovements = []
    for column in range(7):
        if isMovementValid(column, Board):
            temp = makeMovement(Board, column, player)[2]
            validMovements.append(temp)
    if depth == 0 or len(validMovements) == 0 or gameOver(Board):
        return stateFunction(Board, player)
    validMovements = getValidMovements(Board)
    beta = b

    for movement in validMovements:
        boardScore = float("inf")
        if a < beta:
            tempBoard = makeMovement(Board, movement, opponent)[0]
            boardScore = maximizeAlpha(tempBoard, depth - 1, a, beta, player)
        if boardScore < beta:
            beta = boardScore
    return beta

def maximizeAlpha(Board, depth, a, b, player, opponent):
    validMovements = []
    for column in range(7):
        if isMovementValid(column, Board):
            temp = makeMovement(Board, column, player)[2]
            validMovements.append(temp)
    if depth == 0 or len(validMovements) == 0 or gameOver(Board):
        return stateFunction(Board, player)
    alpha = a
    for movement in validMovements:
        boardScore = float("-inf")
        if alpha < b:
            tempBoard = makeMovement(Board, movement, player)[0]
            boardScore = minimizeBeta(tempBoard, depth - 1, alpha, b, player, opponent)
        if boardScore > alpha:
            alpha = boardScore
    return alpha
