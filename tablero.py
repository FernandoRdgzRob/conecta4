import math
from copy import deepcopy
from cont import *

WHITE   = '\033[1;37;40m'
BLUE    = '\033[1;34;40m'
RED     = '\033[1;31;40m'
YELLOW  = '\033[1;33;40m'
GREEN   = '\033[1;32;40m'
MAGENTA = '\033[1;35;40m'
RED_BG  = '\033[0;31;47m'
BLUE_BG = '\033[0;34;47m'

# Función para inicializar un tablero vacío
def initBoard():
    Board = []
    for i in range(BOARD_HEIGHT):
        Board.append([])
        for j in range(BOARD_WIDTH):
            Board[i].append(' ')
    return Board

# Función para comprobar el rango de búsqueda de filas y columnas del tablero
def isRangeValid(row, column):
    if row >= 0 and column >= 0 and row < BOARD_HEIGHT and column < BOARD_WIDTH:
        return True
    return False

# Comprobar si una columna se encuentra llena o no
def isColumnFull(Board, Column):
    if Board[0][Column] == ' ':
        return True
    return False

# Devolver todos los movimientos válidos (columnas vacías) dentro del tablero
def getValidMovements(Board):
    Columns = []
    for Column in range(BOARD_WIDTH):
        if isColumnFull(Board, Column):
            Columns.append(Column)
    return Columns

# Coloca el movimiento actual del jugador en la columna seleccionada dentro del tablero
# Se utiliza deepcopy para tomar una copia del tablero y no alterar el tablero original
def makeMovement(board, column, player):
    tempBoard = deepcopy(board)
    for row in range(5,-1,-1):
        if tempBoard[row][column] == ' ':
            tempBoard[row][column] = player
            return tempBoard, row, column

# Revisa si la jugada hecha se hizo en una columna vacía o no
def isMovementValid(column, board):
    for row in range(BOARD_HEIGHT):
        if board[row][column] == ' ':
            return True
    return False

# Revisa si el tablero se encuentra lleno
# Checa la primera fila y la columna seleccionada para ver si se encuentra llena o no
def isBoardFull(board):
    for row in range(BOARD_HEIGHT):
        for column in range(BOARD_WIDTH):
            if board[row][column] == ' ':
                return False
    return True

# Busca si ya hay 4 o más fichas del mismo tipo en cualquier dirección
def find4(board):

    # Busca 4 o más fichas del mismo tipo en una dirección vertical
    def verticalInspection(row, column):
        fourInLine = False
        count = 0
        for rowIndex in range(row, BOARD_HEIGHT):
            if board[rowIndex][column] == board[row][column]:
                count += 1
            else:
                break
        if count >= 4:
            fourInLine = True

        return fourInLine, count

    # Busca 4 o más fichas del mismo tipo en una dirección horizontal
    def horizontalInspection(row, column):
        fourInLine = False
        count = 0
        for columnIndex in range(column, BOARD_WIDTH):
            if board[row][columnIndex] == board[row][column]:
                count += 1
            else:
                break
        if count >= 4:
            fourInLine = True

        return fourInLine, count

    # Encuentra 4 o más fichas del mismo tipo en una diagonal positiva (hacia la derecha)
    def RDiagonalInspection(row, column):
        count = 0
        slope = None
        columnIndex = column
        # Revisa si hay diagonales con una pendiente positiva
        for rowIndex in range(row, BOARD_HEIGHT):
            if columnIndex > BOARD_HEIGHT: # checa que no exceda los límites del tablero
                break
            elif board[rowIndex][columnIndex] == board[row][column]:
                count += 1
            else:
                break
            columnIndex += 1 # Se va incrementando en 1 la columna cuando se incrementa la fila
        if count >= 4:
            slope = 'positive'

        return slope, count

    # Encuentra 4 o más fichas del mismo tipo en una diagonal negativa (hacia la izquierda)
    def LDiagonalInspection(row, column):
        count = 0
        slope = None
        columnIndex = column
        for rowIndex in range(row, -1, -1): # Revisa que no se salga de los límites del tablero
            if columnIndex > 6:
                break
            elif board[rowIndex][columnIndex] == board[row][column]:
                count += 1
            else:
                break
            columnIndex += 1 # Se va incrementando en 1 la columna cuando se disminuye la fila
        if count >= 4:
            slope = 'negative'

        return slope, count

    # Encuentra 4 o más fichas del mismo tipo en cualquier dirección en diagonal
    def diagonalInspection(row, column):
        positiveSlope, posCount = RDiagonalInspection(row, column)
        negativeSlope, negCount = LDiagonalInspection(row, column)

        if positiveSlope == 'positive' and negativeSlope == 'negative':
            fourInLine = True
            slope = 'both'
        elif positiveSlope == None and negativeSlope == 'negative':
            fourInLine = True
            slope = 'negative'
        elif positiveSlope == 'positive' and negativeSlope == None:
            fourInLine = True
            slope = 'positive'
        else:
            fourInLine = False
            slope = None

        return fourInLine, slope, posCount, negCount

    # Mostrar en mayúsculas los elementos de la jugada ganadora
    def capFourInLine(row, column, direction):
        if direction == 'vertical':
            for rowIndex in range(verticalCount):
                board[row + rowIndex][column] = board[row + rowIndex][column].upper()
        elif direction == 'horizontal':
            for columnIndex in range(horizontalCount):
                board[row][column + columnIndex] = board[row][column + columnIndex].upper()
        elif dir == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for diagonalIndex in range(posCount):
                    board[row + diagonalIndex][column + diagonalIndex] = board[row + diagonalIndex][column + diagonalIndex].upper()
            elif slope == 'negative' or slope == 'both':
                for diagonalIndex in range(negCount):
                    board[row - diagonalIndex][column + diagonalIndex] = board[row - diagonalIndex][column + diagonalIndex].upper()

    # Se inicializan las variables
    fourInLineFlag = False
    slope = None
    verticalCount = 0
    horizontalCount = 0
    posCount = 0
    negCount = 0
    # En caso de que el tablero no se encuentre vacío, se revisa si hay 4 o más elementos del mismo tipo en línea (vertical, horizontal o diagonal)
    for rowIndex in range(BOARD_HEIGHT):
        for columnIndex in range(BOARD_WIDTH):
            if board[rowIndex][columnIndex] != ' ':
                fourInLine, verticalCount = verticalInspection(rowIndex, columnIndex)
                if fourInLine:
                    capFourInLine(rowIndex, columnIndex, 'vertical')
                    fourInLineFlag = True

                fourInLine, horizontalCount = horizontalInspection(rowIndex, columnIndex)
                if fourInLine:
                    capFourInLine(rowIndex, columnIndex, 'horizontal')
                    fourInLineFlag = True

                fourInLine, slope, posCount, negCount = diagonalInspection(rowIndex, columnIndex)
                if fourInLine:
                    capFourInLine(rowIndex, columnIndex, 'diagonal')
                    fourInLineFlag = True
    return fourInLineFlag

# Se obtiene el numero de ubicaciones válidas dentro del tablero
def getEmptySpaces(board):
    emptySpaces = 0
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == ' ':
                emptySpaces += 1
    return emptySpaces

# Se imprime el tablero
def printBoard(Board):
    # Se llama el método para obtener el numero de espacios vacíos
    emptySpaces = 42 - getEmptySpaces(Board)
    print('')
    print(YELLOW + '         Ronda #' + str(emptySpaces), end='')
    print('')
    print('')
    print("\t      1   2   3   4   5   6   7 ")
    print("\t      -   -   -   -   -   -   - ")
    for i in range(0, BOARD_HEIGHT, 1):
        print(WHITE+"\t",i+1,' ',end="")
        for j in range(BOARD_WIDTH):
            # Se imprimen las "fichas" de cada jugador en un color distinto
            if str(Board[i][j]) == 'x':
                print("| " + BLUE + str(Board[i][j]) +WHITE, end=" ")
            elif str(Board[i][j]) == 'o':
                print("| " + RED + str(Board[i][j]) +WHITE, end=" ")
            elif str(Board[i][j]) == 'X':
                print("| " + BLUE_BG + str(Board[i][j]) +WHITE, end=" ")
            elif str(Board[i][j]) == 'O':
                print("| " + RED_BG + str(Board[i][j]) +WHITE, end=" ")
            else:
                print("| " + str(Board[i][j]), end=" ")
        print("|")
    print('')