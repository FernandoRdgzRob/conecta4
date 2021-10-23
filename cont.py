BOARD_WIDTH = 7
BOARD_HEIGHT = 6
AI = 'o'
HUMAN = 'x'

def countSequence(Board, player, length):

    def verticalSequence(row, column):
        count = 0
        for rowIndex in range(row, BOARD_HEIGHT):
            if Board[rowIndex][column] == Board[row][column]:
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
            if Board[row][columnIndex] == Board[row][column]:
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
            elif Board[rowIndex][columnIndex] == Board[row][column]:
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
            elif Board[rowIndex][columnIndex] == Board[row][column]:
                count += 1
            else:
                break
            columnIndex += 1
        if count >= length:
            return 1
        else:
            return 0

    totalCount = 0

    for row in range(BOARD_HEIGHT):
        for column in range(BOARD_WIDTH):
            if Board[row][column] == player:
                totalCount += verticalSequence(row, column)
                totalCount += horizontalSequence(row, column)
                totalCount += (RDiagonalSequence(row, column) + LDiagonalSequence(row, column))
    return totalCount

def stateFunction(Board, player):
    if player == HUMAN:
        opponent = AI
    else:
        opponent = HUMAN

    player4 = countSequence(Board, player, 4)
    player3 = countSequence(Board, player, 3)
    player2 = countSequence(Board, player, 2)
    playerScore = player4*9999 + player3*999 + player2*99

    opponent4 = countSequence(Board, player, 4)
    opponent3 = countSequence(Board, player, 3)
    opponent2 = countSequence(Board, player, 2)
    opponentScore = opponent4*9999 + opponent3*999 + opponent2*99

    if opponent4 > 0:
        return float('-inf')
    else:
        return playerScore - opponentScore

def gameOver(Board):
    if countSequence(Board, HUMAN, 4) >= 1:
        return True
    elif countSequence(Board, AI, 4) >= 1:
        return True
    else:
        return False