BOARD_WIDTH = 7
BOARD_HEIGHT = 6
AI = 'o'
HUMAN = 'x'

# Dado el estado del tablero, el jugador y el largo de la secuencia que se quiere contar, se devuelve el conteo de las secuencias que tienen esa longitud
# Devuelve 1 si se encuentra una secuencia con la longitud requerida
def countSequence(board, player, length):

    def verticalSequence(row, column):
        count = 0
        for rowIndex in range(row, BOARD_HEIGHT):
            if board[rowIndex][column] == board[row][column]:
                count += 1
            else:
                break
        if count >= length:
            return 1
        else:
            return 0

    def horizontalSequence(row, column):
        count = 0
        for columnIndex in range(row, BOARD_WIDTH):
            if board[row][columnIndex] == board[row][column]:
                count += 1
            else:
                break
        if count >= length:
            return 1
        else:
            return 0

    def LDiagonalSequence(row, column):
        count = 0
        columnIndex = column
        for rowIndex in range(row, -1, -1):
            if columnIndex > BOARD_HEIGHT:
                break
            elif board[rowIndex][columnIndex] == board[row][column]:
                count += 1
            else:
                break
            columnIndex += 1
        if count >= length:
            return 1
        else:
            return 0

    def RDiagonalSequence(row, column):
        count = 0
        columnIndex = column
        for rowIndex in range(row, BOARD_HEIGHT):
            if columnIndex > BOARD_HEIGHT:
                break
            elif board[rowIndex][columnIndex] == board[row][column]:
                count += 1
            else:
                break
            columnIndex += 1
        if count >= length:
            return 1
        else:
            return 0
    totalCount = 0

    # Por cada pieza en el tablero se revisa si hay alguna secuencia de piezas
    for row in range(BOARD_HEIGHT):
        for column in range(BOARD_WIDTH):
            if board[row][column] == player:
                totalCount += verticalSequence(row, column)
                totalCount += horizontalSequence(row, column)
                totalCount += (RDiagonalSequence(row, column) + LDiagonalSequence(row, column))
    return totalCount

# En esta función se evalúa el estado del tablero y lo reporta a la función de llamada
# Se define como el puntaje del jugador que hace la llamada de la función
# El puntaje de cada jugador es la suma de las secuencias encontradas para ese jugador
def stateFunction(board, player):
    if player == HUMAN:
        opponent = AI
    else:
        opponent = HUMAN

    player4 = countSequence(board, player, 4)
    player3 = countSequence(board, player, 3)
    player2 = countSequence(board, player, 2)
    playerScore = player4*9999 + player3*999 + player2*99

    opponent4 = countSequence(board, opponent, 4)
    opponent3 = countSequence(board, opponent, 3)
    opponent2 = countSequence(board, opponent, 2)
    opponentScore = opponent4*9999 + opponent3*999 + opponent2*99

    # Significa que el jugador humano perdió el juego
    # Se devuelve un valor infinito negativo
    if opponent4 > 0:
        return float('-inf')
    else:
        # Se devuelve el puntaje del jugador
        return playerScore - opponentScore

# Revisa si hay algún ganador en el estado actual del tablero
def gameOver(board):
    if countSequence(board, HUMAN, 4) >= 1:
        return True
    elif countSequence(board, AI, 4) >= 1:
        return True
    else:
        return False