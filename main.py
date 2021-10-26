from alphaBeta import *

WHITE   = '\033[1;37;40m'
BLUE    = '\033[1;34;40m'
RED     = '\033[1;31;40m'
YELLOW  = '\033[1;33;40m'
GREEN   = '\033[1;32;40m'
MAGENTA = '\033[1;35;40m'
RED_BG  = '\033[0;31;47m'
BLUE_BG = '\033[0;34;47m'

# Se definen todas las acciones a realizar cuando es el turno del humano
def playerTurn(board):
    Col = input(YELLOW + 'Elige una columna entre 1 y 7: ' + WHITE)
    if not(Col.isdigit()):
        print(MAGENTA + "La entrada debe ser un número entero" + WHITE)
        return playerTurn(board)

    playerMove = int(Col) - 1

    if playerMove < 0 or playerMove > 6:
        print(MAGENTA + "El numero de columna debe ser entre 1 y 7" + WHITE)
        return playerTurn(board)
    if not(isColumnFull(board, playerMove)):
        print(MAGENTA + "La columna seleccionada está llena" + WHITE)
        return playerTurn(board)

    board = makeMovement(board, playerMove, HUMAN)[0]
    playerFourInLine = find4(board)
    print('')
    return board, playerFourInLine

# Se define lo que se hace si el humano gana
def playerWins(board):
    printBoard(board)
    print('                    '+GREEN+"Has ganado!!\n" +WHITE)
    playagain = True if input(YELLOW +'¿Quieres jugar de nuevo(s/n)?'+WHITE).lower() == 's' else False
    if playagain:
        board = None
        mainFunction()
    return 0, board

# Se definen acciones a realizar cuando es el turno de la computadora
def aiTurn(board, depth):
    aiMovement = AlphaBeta(board, depth, AI)
    board = makeMovement(board, aiMovement, AI)[0]
    aiFourInLine = find4(board)
    return board, aiFourInLine

# Se definen las acciones que se realizan cuando la computadora gana
def aiWins(Board):
    printBoard(Board)
    print('                    '+RED+ "La computadora ha ganado\n" +WHITE)
    playagain = True if input(YELLOW+'¿Quieres jugar de nuevo(s/n)?'+WHITE).lower() == 's' else False
    #saveBoard(board)
    if playagain:
        board = None
        mainFunction()
    return 0, board

# Se crean dificultades, esto ligado con la profundidad del árbol a evaluar con el algoritmo de poda Alpha-Beta
def getDepth():
    depth = input (YELLOW + 'Ingresa la dificultad del juego, puede ser desde 1 hasta 5: ' + WHITE)
    if not(depth.isdigit()):
        print(MAGENTA + "La entrada debe ser un numero entero" + WHITE)
        return getDepth()
    depth = int(depth, 10)

    if depth < 1 or depth > 5:
        print(MAGENTA + "La dificultad debe ser entre 1 y 5" + WHITE)
        return getDepth()

    return depth

# Función principal en donde se inicializan variables
def mainFunction():
    # Se inicializa un nuevo tablero
    board = initBoard()
    if board == None:
        board = initBoard()
    printBoard(board)
    # Se obtiene la profundidad del árbol
    depth = getDepth()
    whileCondition = 1
    whomStart = True
    # Se pregunta al usuario si quiere empezar o le cede el turno a la computadora
    whomStart = True if input(YELLOW + '¿Quieres tener el primer turno(s/n)? ' + WHITE).lower() == 's' else False
    while(whileCondition):
        if isBoardFull(board):
            print("Juego terminado\n")
            break
        # Se van cambiando los turnos de los jugadores, dependiendo de la respuesta del usuario
        if whomStart:
            board, playerFourInLine = playerTurn(board)
            if playerFourInLine:
                whileCondition = playerWins(board)
                if whileCondition == 0:
                    break

            board, aiFourInLine = aiTurn(board, depth)
            if aiFourInLine:
                whileCondition = aiWins(board)
                if whileCondition == 0:
                    break
            printBoard(board)

        else:
            board, aiFourInLine = aiTurn(board, depth)
            if aiFourInLine:
                whileCondition = aiWins(board)
                if whileCondition == 0:
                    break
            printBoard(board)

            board, playerFourInLine = playerTurn(board)
            if playerFourInLine:
                whileCondition = playerWins(board)
                if whileCondition == 0:
                    break
            printBoard(board)
mainFunction()