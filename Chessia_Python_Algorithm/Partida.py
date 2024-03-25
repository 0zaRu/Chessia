from Pieza import Pieza
from os import system
import re

class Partida:
    def __init__(self):
        self.tablero = Pieza.crear_piezas_partida()
        self.turno = 0
        self.mueveBlancas = True
        self.al_paso_activo = None
        self.posibles_jugadas_algebraicas = {
            r'^[a-h][1-8]$': self.movimiento_peon,                        # Movimiento de peón
            r'^[a-h]x[a-h][1-8]$': self.comer_de_peon,                    # Captura de peón
            r'^[RDTAC][a-h1-8]?x?[a-h][1-8]$': self.jugada_pieza,           # Movimiento o captura de una pieza (!peon)
            r'^O-O(-O)?$': self.jugada_enroque,                           # Enroque ya sea largo o corto
            r'^([a-h]x)?[a-h][18](=[DTAC])$': self.jugada_promocion       # Promocíon de Peón a una pieza moviendo o comiendo
        }
        #self.verificaciones = {
        #    "T": self.verifica_fila_columna,
        #    "A": self.verifica_diagonal,
        #    "C": self.verifica_saltos,
        #    "R": self.verifica_1_distancia,
        #    "D": self.verifica_fila_columna or self.verifica_diagonal
        #}
    
    @staticmethod
    def visualizar_partida(partida, hayPieza=False):
        system("cls")

        print("\n",("\t")*3,"RONDA",partida.turno)
        print(("\t   ")*1,"=================================")

        print("\t      a   b   c   d   e   f   g   h \t")
        print("\t    ╔"+("═══╦")*7+"═══╗ \t")

        for i in range(7, -1, -1):
            print(f"\t  {i+1} ", end="")
            for j in range(7, -1, -1):
                for pieza in partida.tablero:
                    if pieza.y-1 is i and pieza.x-1 is 7-j:
                        print("║ "+pieza.nombre[0]+" "    if pieza.color == "B" else   "║ \033[31m"+pieza.nombre[0]+"\033[0m ", end="")
                        hayPieza = True
                        break
                if not hayPieza:
                    print("║   ", end="")
                else:
                    hayPieza = False
            
            print("║\n"+("\t    ╚"+("═══╩"*7)+"═══╝ \t" if i == 0 else "\t    ╠"+("═══╬"*7)+"═══╣ \t"))

    def ejecuta_mov_entrada(self, jugada):
        for reg, funcion in self.posibles_jugadas_algebraicas.items():
            if re.fullmatch(reg, jugada):
                return funcion(self, jugada)                
            
        input("\n\t    Jugada introducida no válida ...")
        return False
            
    def movimiento_peon(self, partida, jugada):
        posible_al_paso = False
        #Guardamos las nuevas coordenadas a las que ir
        nuevaX = ord(jugada[len(jugada)-2].strip())-96
        nuevaY = int(jugada[len(jugada)-1])

        #Si la casilla a la que queremos mover tiene pieza, nos salimos
        if Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY) is not None:
            input("\n\t    Jugada incorrecta, hay una pieza en esta casilla ...")
            return False

        #Se busca una pieza a 1 casilla de distancia
        pieza = Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY-(1 if self.mueveBlancas else -1), "Peon", "B" if self.mueveBlancas else "N" ) 
        
        #Si no se cuentra pieza a 1 casilla de distancia
        #Y la casilla a la que se quiere llegar es de fila 4 o 5, se busca peón a 2 casillas
        if pieza is None and (nuevaY == 4 and self.mueveBlancas or nuevaY == 5 and not self.mueveBlancas):
            pieza = Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY-(2 if self.mueveBlancas else -2), "Peon", "B" if self.mueveBlancas else "N")
            posible_al_paso = True
            
        #Si había pieza a 1 casilla distancia o si era viable que la hubiese a 2 y la hay, ubicamos la pieza en la lista y le actualizamos la x y la y
        if pieza is not None:
            devolver = Partida.actualiza_pieza(partida, pieza, nuevaX, nuevaY)
            
            #Si es una pieza a 2 casillas, la activamos como válida para comer al paso
            if posible_al_paso and devolver: self.al_paso_activo = pieza
            return devolver

        input("\n\t    Jugada incorrecta, no hay un Peón que pueda hacerla ...")
        return False
        
    def comer_de_peon(self, partida, jugada):
        #Guardamos las nuevas coordenadas a las que ir y la columna antigua
        antX   = ord(jugada[len(jugada)-4].strip())-96
        nuevaX = ord(jugada[len(jugada)-2].strip())-96
        nuevaY = int(jugada[len(jugada)-1])

        #Recogemos la posición del supuesto peón que va a comer, considerando que sea del color que toca. También la casilla donde comemos
        pieza = Partida.comprueba_pieza_casilla(partida, antX, nuevaY-(1 if self.mueveBlancas else -1), "Peon", "B" if self.mueveBlancas else "N")
        pieza_a_comer = Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY, "", "N" if self.mueveBlancas else "B")
    
        #Si hay una pieza válida a comer al paso, no hay pieza a donde queremos llegar, y estamos pegados a la pieza, es que es captura al paso.
        if self.al_paso_activo is not None and pieza_a_comer is None and self.al_paso_activo.x == nuevaX and self.al_paso_activo.y == nuevaY-(1 if self.mueveBlancas else -1):
            #Desplazamos la pieza a la casilla donde queremos movernos porque así no hay que modificar algoritmos de captura y movimiento
            Partida.actualiza_pieza(partida, self.al_paso_activo, nuevaX, nuevaY)
            pieza_a_comer = self.al_paso_activo
            
        #Si la casilla a la que queremos mover no tiene pieza, es de mi color o no hay peón donde nos decían, nos salimos
        if pieza_a_comer is None \
        or pieza is None \
        or abs(antX-nuevaX) != 1:

            input("\n\t    Jugada incorrecta, no hay una pieza o peón válido en estas casillas ...")
            return False

        return Partida.actualiza_pieza(partida, pieza, nuevaX, nuevaY)


    def jugada_pieza(self, partida, jugada):
        #Almacenamiento de nueva casilla de destino
        nuevaX = ord(jugada[len(jugada)-2].strip())-96
        nuevaY = int(jugada[len(jugada)-1])

        #Se recoge la nueva casilla y se comprueba que si hay algo es del otro equipo y es para comer y que si no hay nada es para mover
        destino = Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY)
        if ("x" in jugada and (destino is None or ("B" if self.mueveBlancas else "N") is destino.nombre[-1])) \
            or ("x" not in jugada and destino is not None):
            input("\n\t    Jugada incorrecta, problema en la casilla de destino ...")
            return False
        
        #Se recorren todas las piezas del tablero
        for pieza in partida.tablero:
            #Filtramos primero los caballos, que no necesitan comprobar casillas vacias
            if ((abs(nuevaX - pieza.x)+abs(nuevaY - pieza.y) is 3) and nuevaX != pieza.x and nuevaY != pieza.y and jugada[0] is "C" and pieza.nombre[0] is "C"): 
                return Partida.actualiza_pieza(partida, pieza, nuevaX, nuevaY)
            
            #Filtramos la piezas, deben ser del color del turno y tener la letra de la jugada en el nombre, además de ser T, D o R si están en la misma fila o columna y ser A, D o R si es diagonal
            if (("B" if partida.mueveBlancas else "N") in pieza.nombre and jugada[0] in pieza.nombre[0]) \
            and (((pieza.x == nuevaX or pieza.y == nuevaY) and jugada[0] in ["T", "D", "R"] and (pieza.x-nuevaX == 1 or pieza.y-nuevaY == 1) if jugada[0] in ["R"] else True) \
            or (abs(pieza.x - nuevaX) == abs(pieza.y - nuevaY) and jugada[0] in ["A", "D", "R"] and (pieza.x-nuevaX == 1 or pieza.y-nuevaY == 1) if jugada[0] in ["R"] else True)):
                valido = True
                
                #zip 1: comparte columna (torre o dama)        #zip 2: comparte fila (torre o dama)       #zip 3: no comparte nada (alfil o dama)        
                for i, j in \
                zip(list(nuevaX for x in range(1, 9)), range(nuevaY-(1 if pieza.y < nuevaY else -1), pieza.y, 1 if nuevaY < pieza.y else -1)) if nuevaX is pieza.x else (\
                zip(range(nuevaX-(1 if pieza.x < nuevaX else -1), pieza.x, 1 if nuevaX < pieza.x else -1), list(nuevaY for y in range(1, 9))) if nuevaY is pieza.y else \
                zip(range(nuevaX-(1 if pieza.x < nuevaX else -1), pieza.x, 1 if nuevaX < pieza.x else -1), range(nuevaY-(1 if pieza.y < nuevaY else -1), pieza.y, 1 if nuevaY < pieza.y else -1))):    
                    
                    if Partida.comprueba_pieza_casilla(partida, i, j) is not None:
                        valido = False

                if valido: return Partida.actualiza_pieza(partida, pieza, nuevaX, nuevaY)    
        
        input("\n\t    Jugada incorrecta, no hay piezas viables ...")
        return False
        

    def jugada_enroque(self, partida, jugada):
        print(f"dasdads  --")

    def jugada_promocion(self, partida, jugada):
        print(f"dasdads  --")

    def comprueba_pieza_casilla(partida, x, y, nombre="", color=""):
        try:
            recogido = next(filter(lambda pieza: pieza.x == x and pieza.y == y, partida.tablero))
            if nombre in recogido.nombre and color in recogido.nombre:
                return recogido
        
        except StopIteration: pass
        return None
        
    def actualiza_pieza(partida, pieza, nuevaX, nuevaY):
        try:

            pieza_a_borrar = Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY)
            if pieza_a_borrar is not None:
                partida.tablero.__getitem__(partida.tablero.index(pieza_a_borrar)).matar()

            partida.tablero.__getitem__(partida.tablero.index(pieza)).x = nuevaX
            partida.tablero.__getitem__(partida.tablero.index(pieza)).y = nuevaY
            return True

        except Exception:
            input("\n\t    Error en actualiza_pieza(...) en Partida")
            return False