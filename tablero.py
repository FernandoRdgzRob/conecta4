from copy import deepcopy
from cont import *

WHITE   = '\033[1;37;40m'
BLUE    = '\033[1;34;40m'
RED     = '\033[1;31;40m'

# Crear un tablero vacío
def initBoard():
    Board = []
    for i in range(BOARD_HEIGHT):
        Board.append([])
    for j in range(BOARD_WIDTH):
        Board[i].append(' ')
    return Board

# Revisar el rango de búsqueda de filas y columnas
def isRangeValid(row, column):
    if row >= 0 and column >= 0 and row < BOARD_HEIGHT and column < BOARD_WIDTH:
        return True
    return False

# Revisar si una columna se encuentra llena o no
def isColumnFull(Board, column):
    if Board[0][column] == ' ':
        return True
    return False

# Devolver movimientos válidos (lugares vacíos)
def getValidMovements(Board):
    Columns = []
    for column in range(BOARD_WIDTH):
        if isColumnFull(Board, column):
            Columns.append(column)
    return Columns

# Coloca el movimiento actual del jugador en la columna seleccionada dentro del tablero
# Se utiliza deepcopy para tomar una copia del tablero y no alterar el tablero original
def makeMovement(Board, column, player):
    tempBoard = deepcopy(Board)
    for row in range(5,-1,-1):
        if tempBoard[row][column] == ' ':
            tempBoard[row][column] = player
            return tempBoard, row, column

# Revisa si la jugada hecha se hizo en un lugar válido o no
def isMovementValid(column, Board):
    for row in range(BOARD_HEIGHT):
        if Board[row][column] == ' ':
            return True
    return False

# Revisa si el tablero se encuentra lleno
# Checa la primera fila y la columna seleccionada para ver si se encuentra llena o no
def isBoardFull(Board):
    for row in range(BOARD_HEIGHT):
        for column in range(BOARD_WIDTH):
            if Board[row][column] == ' ':
                return False
    return True

# Encuentra si ya hay 4 o más fichas del mismo tipo en cualquier dirección
def find4(Board):

    # Encuentra 4 o más fichas del mismo tipo en una dirección vertical
    def verticalInspection(row, column):
        fourInLine = False
        count = 0
        for rowIndex in range(row, BOARD_HEIGHT):
            if Board[rowIndex][column] == Board[row][column]:
                count += 1
            else:
                break
        if count >= 4:
            fourInLine = True

        return fourInLine, count

    # Encuentra 4 o más fichas del mismo tipo en una dirección horizontal
    def horizontalInspection(row, column):
        fourInLine = False
        count = 0
        for columnIndex in range(column, BOARD_WIDTH):
            if Board[row][columnIndex] == Board[row][column]:
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
            if columnIndex > BOARD_HEIGHT:
                break
            elif Board[rowIndex][columnIndex] == Board[row][column]:
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
        for rowIndex in range(row, -1, -1):
            if columnIndex > 6:
                break
            elif Board[rowIndex][columnIndex] == Board[row][column]:
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

    def capFourInLine(row, column, direction):
        if direction == 'vertical':
            for rowIndex in range(verticalCount):
                Board[row + rowIndex][column] = Board[row + rowIndex][column].upper()
        elif direction == 'horizontal':
            for columnIndex in range(horizontalCount):
                Board[row][column + columnIndex] = Board[row][column + columnIndex].upper()
        elif dir == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for diagonalIndex in range(posCount):
                    Board[row + diagonalIndex][column + diagonalIndex] = Board[row + diagonalIndex][column + diagonalIndex].upper()
            elif slope == 'negative' or slope == 'both':
                for diagonalIndex in range(negCount):
                    Board[row - diagonalIndex][column + diagonalIndex] = Board[row - diagonalIndex][column + diagonalIndex].upper()

    # Se inicializan las variables
    fourInLineFlag = False
    slope = None
    verticalCount = 0
    horizontalCount = 0
    posCount = 0
    negCount = 0

    for rowIndex in range(BOARD_HEIGHT):
        for columnIndex in range(BOARD_WIDTH):
            if Board[rowIndex][columnIndex] != ' ':
                fourInLine, verticalCount = verticalInspection(rowIndex, columnIndex)
                if fourInLine:
                    capFourInLine(rowIndex, columnIndex, 'vertical')
                    FourInLineFlag = True

                fourInLine, horizontalCount = horizontalInspection(rowIndex, columnIndex)
                if fourInLine:
                    capFourInLine(rowIndex, columnIndex, 'horizontal')
                    FourInLineFlag = True

                fourInLine, slope, posCount, negCount = diagonalInspection(rowIndex, columnIndex)
                if fourInLine:
                    capFourInLine(rowIndex, columnIndex, 'diagonal')
                    FourInLineFlag = True

    return FourInLineFlag

def getEmptySpaces(Board):
    emptySpaces = 0
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if Board[row][col] == ' ':
                emptySpaces += 1
    return emptySpaces

def printBoard(Board):
    emptySpaces = 42 - getEmptySpaces(Board)
    print('')
    print('Ronda #' + str(emptySpaces))
    print('')
    print('')
    print("\t      1   2   3   4   5   6   7 ")
    print("\t      -   -   -   -   -   -   - ")
    for i in range(0, BOARD_HEIGHT, 1):
        print("\t",i+1,' ',end="")
        for j in range(BOARD_WIDTH):
            if str(Board[i][j]) == 'x':
                print("| " + BLUE + str(Board[i][j]) +WHITE, end=" ")
            elif str(Board[i][j]) == 'o':
                print("| " + RED + str(Board[i][j]) +WHITE, end=" ")
            elif str(Board[i][j]) == 'X':
                print("| " + BLUE + str(Board[i][j]) +WHITE, end=" ")
            elif str(Board[i][j]) == 'O':
                print("| " + RED + str(Board[i][j]) +WHITE, end=" ")
            else:
                print("| " + str(Board[i][j]), end=" ")
        print("|")
    print('')