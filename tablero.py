import math
#import os
from copy import deepcopy
from cont import *

#crear un tablero vacío
def initBoard():
    Board = []
    for i in range(BOARD_HEIGHT):
        Board.append([])
    for j in range(BOARD_WIDTH):
        Board[i].append(' ')
    return Board

#Revisar el rango de búsqueda de filas y columnas
def isRangeValid(row, column):
    if row >= 0 and column >= 0 and row < BOARD_HEIGHT and column < BOARD_WIDTH:
        return True
    return False

#Revisar si una columna se encuentra llena o no
def isColumnFull(Board, column):
    if Board[0][column] == ' ':
        return True
    return False

#Devolver movimientos válidos (lugares vacíos)
def getValidMovements(Board):
    Columns = []
    for column in range(BOARD_WIDTH):
        if isColumnFull(Board, column):
            Columns.append(column)
    return Columns

#Coloca el movimiento actual del jugador en la columna seleccionada dentro del tablero
#Se utiliza deepcopy para tomar una copia del tablero y no alterar el tablero original
def makeMovement(Board, column, player):
    tempBoard = deepcopy(Board)
    for row in range(5,-1,-1):
        if tempBoard[row][column] == ' ':
            tempBoard[row][column] = player
            return tempBoard, row, column

#Revisa si la jugada hecha se hizo en un lugar válido o no
def isMovementValid(column, Board):
    for row in range(BOARD_HEIGHT):
        if Board[row][column] == ' ':
            return True
    return False

#Revisa si el tablero se encuentra lleno
#Checa la primera fila y la columna seleccionada para ver si se encuentra llena o no
def isBoardFull(Board):
    for row in range(BOARD_HEIGHT):
        for column in range(BOARD_WIDTH):
            if Board[row][column] == ' ':
                return False
    return True

#Encuentra si ya hay 4 o más fichas del mismo tipo en cualquier dirección
def find4(Board):
    def verticalInspection(row, column):
        