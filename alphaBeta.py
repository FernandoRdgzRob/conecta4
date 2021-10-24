from tablero import *
from random import shuffle

def AlphaBeta(board, depth, player):

    # Se obtiene un arreglo con los posibles movimientos (espacios vacíos dentro del tablero)
    validMovements = getValidMovements(board)
    shuffle(validMovements)
    bestMovement = validMovements[0]
    bestScore = float("-inf")

    # Se inicializan los valores de Alpha y Beta, infinito y menos infinito
    alpha = float("-inf")
    beta = float("inf")
    if player == AI:
        opponent = HUMAN
    else:
        opponent = AI

    # Se recorrren todas las copias de los tableros
    for movement in validMovements:
        # Se crea un nuevo tablero a raíz de un movimiento
        tempBoard = makeMovement(board, movement, player)[0]
        # Se llama la función de minimizar Beta en el nuevo tablero
        boardScore = minimizeBeta(tempBoard, depth - 1, alpha, beta, player, opponent)
        if boardScore > bestScore:
            bestScore = boardScore
            bestMovement = movement
    return bestMovement

def minimizeBeta(board, depth, a, b, player, opponent):
    validMovements = []
    for column in range(7):
        # Se revisa si es un movimiento válido
        if isMovementValid(column, board):
            # Se realiza el movimiento para el jugador actual
            temp = makeMovement(board, column, player)[2]
            validMovements.append(temp)

    # Se revisa si ya se terminó el juego
    if depth == 0 or len(validMovements) == 0 or gameOver(board):
        return stateFunction(board, player)
    validMovements = getValidMovements(board)
    beta = b

    # Si es el final del árbol, se revisa el puntaje
    for movement in validMovements:
        boardScore = float("inf")
        # De otra forma, se continúa recorriendo el árbol mientras "a" y "b" cumplan con las condiciones
        if a < beta:
            tempBoard = makeMovement(board, movement, opponent)[0]
            boardScore = maximizeAlpha(tempBoard, depth - 1, a, beta, player, opponent)
        if boardScore < beta:
            beta = boardScore
    return beta

def maximizeAlpha(board, depth, a, b, player, opponent):
    validMovements = []
    for column in range(7):
        # Se revisa si es un movimiento válido
        if isMovementValid(column, board):
            # Se realiza el movimiento para el juador actual
            temp = makeMovement(board, column, player)[2]
            validMovements.append(temp)

    # Se revisa si ya terminó el juego
    if depth == 0 or len(validMovements) == 0 or gameOver(board):
        return stateFunction(board, player)
    alpha = a

    # Si llegó al final del árbol, se evalúa el puntaje del jugador
    for movement in validMovements:
        boardScore = float("-inf")
        # De otra forma, se continúa recorriendo el árbol mientras "a" y "b" cumplan con las condiciones
        if alpha < b:
            tempBoard = makeMovement(board, movement, player)[0]
            boardScore = minimizeBeta(tempBoard, depth - 1, alpha, b, player, opponent)
        if boardScore > alpha:
            alpha = boardScore
    return alpha
