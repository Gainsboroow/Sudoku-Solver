"""
Sudoku Solver
Created by Gainsboroow 
Github : https://github.com/Gainsboroow
Github Repository : https://github.com/Gainsboroow/Sudoku-Solver

How to use : Enter the numbers in the grid. 
Press F5 and see the results. 
Press F4 to erase the numbers.
"""

from tkinter import *
from tkinter.messagebox import *

from copy import deepcopy

from math import sqrt 

import sys
sys.setrecursionlimit(10**6)

window = Tk()
window.title("Sudoku Solveur")
window.geometry(str(360)+"x"+str(360)+"+0+0")

canvas = Canvas(window)
canvas.place(x=0,y=0, width = 400, height = 400)

tailleCote = 9
taillePetitCarre = int(sqrt(tailleCote))

def verif(grid):
    for lig in range(tailleCote):
        used = [False] * (tailleCote+1)
        used[0] = True 
        for col in range(tailleCote):
            nombre = grid[lig][col]
            if used[nombre] : return False 
            used[nombre] = True 
    
    for col in range(tailleCote):
        used = [False] * (tailleCote+1)
        used[0] = True 
        for lig in range(tailleCote):
            nombre = grid[lig][col]
            if used[nombre] : return False 
            used[nombre] = True 

    for debLig in range(0, tailleCote, taillePetitCarre):
        for debCol in range(0, tailleCote, taillePetitCarre):
            used = [False] * (tailleCote+1)
            used[0] = True 
            for ligPetitCarre in range(debLig, debLig + taillePetitCarre):
                for colPetitCarre in range(debCol, debCol + taillePetitCarre):
                    nombre = grid[ligPetitCarre][colPetitCarre]
                    if used[nombre] : return False 
                    used[nombre] = True          
    
    return True
            
def remplir(grid):
    for row in range(tailleCote):
        for col in range(tailleCote):
            nombre = grid[row][col]
            if nombre:
                entreesUtilisateur[row][col].set(nombre)


def check(_grille, _possibilites):
    file = [ (_grille, _possibilites) ]

    while file:

        grille, possibilites = file.pop(-1)
        update = True 

        while update:
            update = False 
            for lig in range(tailleCote):
                for col in range(tailleCote):
                    if len(possibilites[lig][col]) == 1:
                        grille[lig][col] = possibilites[lig][col][0]
                        nombre = grille[lig][col]
                        
                        for curCol in range(tailleCote):
                            if nombre in possibilites[lig][curCol]: 
                                possibilites[lig][curCol].remove(nombre)

                        for curLig in range(tailleCote):
                            if nombre in possibilites[curLig][col]:
                                possibilites[curLig][col].remove(nombre)

                        ligCarre = lig - (lig % taillePetitCarre)
                        colCarre = col - (col % taillePetitCarre)

                        for curLig in range(ligCarre, ligCarre + taillePetitCarre):
                            for curCol in range(colCarre, colCarre + taillePetitCarre):
                                if nombre in possibilites[curLig][curCol]:
                                    possibilites[curLig][curCol].remove(nombre)

                        update = True 

        quitter = False 
        
        for lig in range(tailleCote):
            for col in range(tailleCote):
                if quitter : break 

                if len(possibilites[lig][col]) > 1:
                    quitter = True 

                    for nombre in possibilites[lig][col]:
                        possibilites[lig][col] = [nombre]
                        file.append( (deepcopy(grille), deepcopy(possibilites)) )

        if not(quitter) and verif(grille):
            remplir(grille)
            return


def main(event):
    grille = [ [0 for i in range(tailleCote)] for a in range(tailleCote)]
    possibilites = [ [ [i for i in range(1, tailleCote+1)] for a in range(tailleCote)] for b in range(tailleCote) ]

    for lig in range(tailleCote):
        for col in range(tailleCote):
            nombre = entreesUtilisateur[lig][col].get()
            if nombre:
                nombre = int(nombre)
                casesInput[lig][col].config(bg = 'lawn green')
                possibilites[lig][col] = [nombre]

    check(grille, possibilites)

def reset(event):
    for row in range(tailleCote):
        for col in range(tailleCote):
            entreesUtilisateur[row][col].set('')

entreesUtilisateur = [ [None for i in range(tailleCote)] for a in range(tailleCote) ]
casesInput = [ [None for i in range(tailleCote)] for a in range(tailleCote) ]

for row in range(tailleCote):
    for col in range(tailleCote):
        entreesUtilisateur[row][col] = StringVar() 
        entreesUtilisateur[row][col].set('')
        casesInput[row][col] = Entry(window, textvariable = entreesUtilisateur[row][col])

        casesInput[row][col].place(x = 10 + 40*col, y = 10 + 40*row, width = 20, height = 20)

canvas.create_line(120, 0, 120, 400, width = 3)
canvas.create_line(240, 0, 240, 400, width = 3)
canvas.create_line(0, 120, 400, 120, width = 3)
canvas.create_line(0, 240, 400, 240, width = 3)


window.bind("<F5>", main)
window.bind("<F4>", reset)

window.mainloop()
