# chr(27)+"[9;31m"+"X"+chr(27)+"[0;37m"
import os
from random import *

class Tablero():
    t: list

    def __init__(self, nTablero = 2, nLineas = 10, nColumnas = 10, valorCasilla = " "):
        tableros = []
        for i in range(nTablero):
            tablero = []
            for j in range(nLineas):
                columna = []
                for k in range(nColumnas):
                    columna.append(valorCasilla)
                tablero.append(columna)
            tableros.append(tablero)
        self.t = tableros

    class RegistroConstruccionT():
        nBarcos = {
            "C": [4, 1],
            "T": [3, 2],
            "D": [2, 3],
            "U": [1, 4]}

        horizontal: bool
        pH: int
        pV: int
        letraBarco: str
        tamBarco: int

def impresion(tableros):
    os.system("cls")

    cont = 0
    print("\t     a   b   c   d   e   f   g   h   i   j \t"*2)
    print(("\t   ╔"+("═══╦")*9+"═══╗ \t")*2)
    
    for filaT1, filaT2 in zip(tableros[0], tableros[1]):
        
        print("\t",cont,"║", end="")
        for casilla in filaT1:
            #print("   ║" if casilla in {".", " "} else " X ║", end="")
            print(" "+casilla+" ║" if casilla != "." else "   ║", end="")
            #print(" "+casilla+" ║", end="")
        
        print("\t\t",cont,"║", end="")
        for casilla in filaT2:
            #print("   ║" if casilla in {".", " "} else " X ║", end="")
            print(" "+casilla+" ║" if casilla != "." else "   ║", end="")
            #print(" "+casilla+" ║", end="")
    
        print()
        if cont != 9: print(("\t   ╠"+("═══╬"*9)+"═══╣ \t")*2)
        cont+=1
    
    print(("\t   ╚"+("═══╩"*9)+"═══╝ \t")*2)
    print((" ")*27+"JUGADOR 1"+(" ")*47+"JUGADOR 2\n\n")

def rodeaCasilla(t, pH, pV):
    for h in [-1, 0, 1]:
        for v in [-1, 0, 1]:
            if pH+h in range(len(t)) and pV+v in range(len(t[0])) and t[pH+h][pV+v] == " ": 
                t[pH+h][pV+v] = "."

    return t

def gestionaEspacio(t, c: Tablero.RegistroConstruccionT):
    #primero compruebo que en los espacios se puede poner un barco
    for i in range(c.tamBarco):
        if c.horizontal:
            if t[c.pH+i][c.pV] != " ": return False, t
        if not c.horizontal:
            if t[c.pH][c.pV+i] != " ": return False, t
    
    #luego lo pongo y guardo sus posiciones
    casillasBarco = []
    for i in range(c.tamBarco):
        if c.horizontal:
            t[c.pH+i][c.pV] = c.letraBarco
            casillasBarco.append([c.pH+i, c.pV])
        
        if not c.horizontal:
            t[c.pH][c.pV+i] = c.letraBarco
            casillasBarco.append([c.pH, c.pV+i])
        
    #escribo puntos alrededor del barco que acabo de colocar
    for casilla in casillasBarco:
        t = rodeaCasilla(t, casilla[0], casilla[1])

    return True, t

def generaBarcos(t):
    c = Tablero.RegistroConstruccionT

    #recorro el diccionario de barcos
    for n, v in c.nBarcos.items():        
        c.pH, c.pV = -1, -1
        #doy tantas vueltas como barcos haya que poner del tipo en el que estamos
        for cantBarcos in range(v[1]):
            #establezco la orientación del próximo barco
            c.horizontal = True if randint(0, 1) == 0 else False
            salir = False

            #doy vueltas seleccionando casillas hasta encontrar una válida y colocar el barco
            while not salir:
                c.pH = randint(0, len(t)-v[0]) if c.horizontal else randint(0, len(t)-1)
                c.pV = randint(0, len(t[0])-v[0]) if not c.horizontal else randint(0, len(t[0])-1)
                
                c.letraBarco = n; c.tamBarco = v[0]
                salir, t = gestionaEspacio(t, c)
    
    return t


t = Tablero()

t.t[0] = generaBarcos(t.t[0])
t.t[1] = generaBarcos(t.t[1])

impresion(t.t)