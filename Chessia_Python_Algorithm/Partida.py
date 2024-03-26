from Pieza import Pieza
from os import system
import re

class Partida:
    def __init__(self):
        self.tablero = Pieza.crear_piezas_partida()
        self.turno = 0
        self.mueveBlancas = True
        self.al_paso_activo = None
        self.validar_ejecucion = True
        self.posibles_jugadas_algebraicas = {
            r'^[a-h][1-8]$': self.movimiento_peon,                        # Movimiento de peón
            r'^[a-h]x[a-h][1-8]$': self.comer_de_peon,                    # Captura de peón
            r'^[RDTAC][a-h1-8]?x?[a-h][1-8]$': self.jugada_pieza,         # Movimiento o captura de una pieza (!peon)
            r'^O-O(-O)?$': self.jugada_enroque,                           # Enroque ya sea largo o corto
            r'^([a-h]x)?[a-h][18](=[DTAC])$': self.jugada_promocion       # Promocíon de Peón a una pieza moviendo o comiendo
        }
    
    def visualizar_partida(partida):
        hayPieza=False
        system("cls")

        print("\n",("\t")*3,"RONDA",partida.turno)
        print(("\t   ")*1,"=================================")

        print("\t      a   b   c   d   e   f   g   h \t")
        print("\t    ╔"+("═══╦")*7+"═══╗ \t")

        for i in range(7, -1, -1):
            print(f"\t  {i+1} ", end="")
            for j in range(7, -1, -1):
                for pieza in partida.tablero:
                    if pieza.y-1 == i and pieza.x-1 == 7-j:
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
            
        return -1
    
    def movimiento_peon(self, partida, jugada):
        #Guardamos las nuevas coordenadas a las que ir
        nuevaX = ord(jugada[len(jugada)-2].strip())-96
        nuevaY = int(jugada[len(jugada)-1])
        posible_al_paso = False

        #Si la casilla a la que queremos mover tiene pieza, nos salimos
        if Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY) is not None:
            return -2

        #Se busca una pieza a 1 casilla de distancia
        pieza = Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY-(1 if self.mueveBlancas else -1), "Peon", "B" if self.mueveBlancas else "N" ) 
        
        #Si no había pieza a 1 casilla verificamos a 2 si es viable
        if pieza is None and (nuevaY == 4 and self.mueveBlancas or nuevaY == 5 and not self.mueveBlancas):
            pieza = Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY-(2 if self.mueveBlancas else -2), "Peon", "B" if self.mueveBlancas else "N")
            posible_al_paso = True
            
        #Si había pieza a 1 casilla distancia o si era viable que la hubiese a 2 y la hay, ubicamos la pieza en la lista y le actualizamos la x y la y
        if pieza is not None:
            devolver = Partida.actualiza_pieza(partida, pieza, nuevaX, nuevaY)
            
            #Si es una pieza a 2 casillas, la activamos como válida para comer al paso
            if posible_al_paso and devolver: self.al_paso_activo = pieza
            return 0

        return -4
        
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

            return -3

        return Partida.actualiza_pieza(partida, pieza, nuevaX, nuevaY)

    def jugada_pieza(self, partida, jugada):
        #Almacenamiento de nueva casilla de destino
        nuevaX = ord(jugada[len(jugada)-2].strip())-96
        nuevaY = int(jugada[len(jugada)-1])
        l_piezas = []

        #Se recoge la nueva casilla y se comprueba que si hay algo es del otro equipo y es para comer y que si no hay nada es para mover
        destino = Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY)
        if ("x" in jugada and (destino is None or ("B" if self.mueveBlancas else "N") == destino.nombre[-1])) or ("x" not in jugada and destino is not None):
            return -5
        
        #Se recorren todas las piezas del tablero
        for pieza in partida.tablero:
            if ("N" if self.mueveBlancas else "B") in pieza.nombre[-1] or jugada[0] != pieza.nombre[0]: continue

            #Filtramos primero los caballos, que no necesitan comprobar casillas vacias
            if (pieza.nombre[0] == "C" and (abs(nuevaX - pieza.x)+abs(nuevaY - pieza.y) == 3) and (nuevaX != pieza.x and nuevaY != pieza.y)): 
                return Partida.actualiza_pieza(partida, pieza, nuevaX, nuevaY)
            
            #Filtramos la piezas, deben ser del color del turno y tener la letra de la jugada en el nombre, además de ser T, D o R si están en la misma fila o columna y ser A, D o R si es diagonal
            if (((pieza.x == nuevaX or pieza.y == nuevaY) and jugada[0] in ["T", "D"]) \
            or (abs(pieza.x - nuevaX) == abs(pieza.y - nuevaY) and jugada[0] in ["A", "D"]) \
            or (jugada[0] in ["R"] and (abs(pieza.x-nuevaX) <= 1 and abs(pieza.y-nuevaY) <= 1))):
                valido = True
                
                #zip 1: comparte columna (torre o dama)        #zip 2: comparte fila (torre o dama)       #zip 3: no comparte nada (alfil o dama)        
                for i, j in \
                zip(list(nuevaX for x in range(1, 9)), range(nuevaY-(1 if pieza.y < nuevaY else -1), pieza.y, 1 if nuevaY < pieza.y else -1)) if nuevaX == pieza.x else (\
                zip(range(nuevaX-(1 if pieza.x < nuevaX else -1), pieza.x, 1 if nuevaX < pieza.x else -1), list(nuevaY for y in range(1, 9))) if nuevaY == pieza.y else \
                zip(range(nuevaX-(1 if pieza.x < nuevaX else -1), pieza.x, 1 if nuevaX < pieza.x else -1), range(nuevaY-(1 if pieza.y < nuevaY else -1), pieza.y, 1 if nuevaY < pieza.y else -1))):    
                    
                    if Partida.comprueba_pieza_casilla(partida, i, j) is not None:
                        valido = False

                if valido: l_piezas.append(pieza)
        
        if len(l_piezas) == 1 and ((len(jugada) == 4 and jugada[1] == "x") or (len(jugada) <= 3)): 
            return Partida.actualiza_pieza(partida, l_piezas[0], nuevaX, nuevaY)
        
        elif len(l_piezas) == 2 and len(jugada) >= 4 and jugada[1] != "x":
            if re.match(r'^[a-h]$', jugada[1]) and ((l_piezas[0].x != l_piezas[1].x and l_piezas[0].y != l_piezas[1].y) or (l_piezas[0].x != l_piezas[1].x and l_piezas[0].y == l_piezas[1].y)):
                return Partida.actualiza_pieza(partida, l_piezas[0] if ord(jugada[1].strip())-96 == l_piezas[0].x else l_piezas[1], nuevaX, nuevaY)

            elif re.match(r'^[1-8]$', jugada[1]) and ((l_piezas[0].x != l_piezas[1].x and l_piezas[0].y != l_piezas[1].y) or (l_piezas[0].x == l_piezas[1].x and l_piezas[0].y != l_piezas[1].y)):
                return Partida.actualiza_pieza(partida, l_piezas[0] if int(jugada[1]) == l_piezas[0].y else l_piezas[1], nuevaX, nuevaY)

        return -6
        
    def jugada_enroque(self, partida, jugada):
        torre = Partida.comprueba_pieza_casilla(partida, 8 if len(jugada) == 3 else 1, 1 if self.mueveBlancas else 8, "Torre", "B" if self.mueveBlancas else "N")
        rey = Partida.comprueba_pieza_casilla(partida, 5, 1 if self.mueveBlancas else 8, "Rey", "B" if self.mueveBlancas else "N")

        if torre is not None and rey is not None and torre.enrocable and rey.enrocable:

            for i in range(torre.x, rey.x+(1 if torre.x < rey.x else -1), 1 if torre.x < rey.x else -1):
                if (Partida.comprueba_pieza_casilla(partida, i, rey.y) is not None and i != torre.x and i != rey.x) or self.hay_jaque(partida, i, rey.y):
                    return -8

            Partida.actualiza_pieza(partida, torre, rey.x-(1 if torre.x < rey.x else -1), rey.y)
            Partida.actualiza_pieza(partida, rey, rey.x-(2 if torre.x < rey.x else -2), rey.y)
            return 0
    
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
            if pieza_a_borrar is not None and partida.validar_ejecucion:
                partida.tablero.__getitem__(partida.tablero.index(pieza_a_borrar)).matar()

            if partida.validar_ejecucion:
                partida.tablero.__getitem__(partida.tablero.index(pieza)).x = nuevaX
                partida.tablero.__getitem__(partida.tablero.index(pieza)).y = nuevaY
                if pieza.nombre[0] in ["T", "R"]: pieza.enrocable = False

            return 0

        except Exception:
            return -7
        
    def hay_jaque(self, partida, x, y):
        self.validar_ejecucion = False; self.mueveBlancas = (False if self.mueveBlancas else True)
        hayJaque = False
        
        if Partida.comer_de_peon(self, partida, f"{chr(x+95)}x{chr(x+96)}{y}") \
        or Partida.comer_de_peon(self, partida, f"{chr(x+97)}x{chr(x+96)}{y}"):
            hayJaque = True
        
        for i in ["T", "C", "A", "D", "R"]:
            if Partida.jugada_pieza(self, partida, f"{i}x{chr(x+96)}{y}") \
            or Partida.jugada_pieza(self, partida, f"{i}{chr(x+96)}x{chr(x+96)}{y}") \
            or Partida.jugada_pieza(self, partida, f"{i}{y}x{chr(x+96)}{y}"):
                hayJaque = True
        

        self.validar_ejecucion = True; self.mueveBlancas = (False if self.mueveBlancas else True)
        if hayJaque: return True
        return False