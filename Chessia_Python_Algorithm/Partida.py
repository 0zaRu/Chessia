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
            r'^([a-h]x)?[a-h][2-7]$': self.jugada_peon,                        # Movimiento de peón
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
    
    def jugada_peon(self, partida, jugada):
        comer = posible_al_paso = False
        if jugada[1] == "x": comer = True
        if comer: antX = ord(jugada[len(jugada)-4].strip())-96
        nuevaX = ord(jugada[len(jugada)-2].strip())-96
        nuevaY = int(jugada[len(jugada)-1])

        if Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY) is (not None) if comer else (None):
            return -5

        #Se busca una pieza a 1 casilla de distancia
        pieza = Partida.comprueba_pieza_casilla(partida, antX if comer else nuevaX, nuevaY-(1 if self.mueveBlancas else -1), "Peon", "B" if self.mueveBlancas else "N" ) 

        if comer: 
            pieza_a_comer = Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY, "", "N" if self.mueveBlancas else "B")
            
            #Si hay una pieza válida a comer al paso, no hay pieza a donde queremos llegar, y estamos pegados a la pieza, es que es captura al paso.
            if self.al_paso_activo is not None and pieza_a_comer is None and self.al_paso_activo.x == nuevaX and self.al_paso_activo.y == nuevaY-(1 if self.mueveBlancas else -1):
                #Desplazamos la pieza a la casilla donde queremos movernos porque así no hay que modificar algoritmos de captura y movimiento
                if self.actualiza_pieza(partida, self.al_paso_activo, nuevaX, nuevaY) != 0 and pieza_a_comer is None and pieza is None or abs(antX-nuevaX) != 1:
                    return -3

            return self.actualiza_pieza(partida, pieza, nuevaX, nuevaY)
        
        else:
            #Si no había pieza a 1 casilla verificamos a 2 si es viable
            if pieza is None and (nuevaY == 4 and self.mueveBlancas or nuevaY == 5 and not self.mueveBlancas):
                pieza = Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY-(2 if self.mueveBlancas else -2), "Peon", "B" if self.mueveBlancas else "N")
                posible_al_paso = True

            #Si había pieza a 1 casilla distancia o si era viable que la hubiese a 2 y la hay, ubicamos la pieza en la lista y le actualizamos la x y la y
            if pieza is not None:
                devolver = self.actualiza_pieza(partida, pieza, nuevaX, nuevaY)
                
                #Si es una pieza a 2 casillas, la activamos como válida para comer al paso
                if posible_al_paso and devolver == 0: self.al_paso_activo = pieza
                return devolver

            return -4

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
                return self.actualiza_pieza(partida, pieza, nuevaX, nuevaY)
            
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
            return self.actualiza_pieza(partida, l_piezas[0], nuevaX, nuevaY)
        
        elif len(l_piezas) == 2 and len(jugada) >= 4 and jugada[1] != "x":
            if re.match(r'^[a-h]$', jugada[1]) and ((l_piezas[0].x != l_piezas[1].x and l_piezas[0].y != l_piezas[1].y) or (l_piezas[0].x != l_piezas[1].x and l_piezas[0].y == l_piezas[1].y)):
                return self.actualiza_pieza(partida, l_piezas[0] if ord(jugada[1].strip())-96 == l_piezas[0].x else l_piezas[1], nuevaX, nuevaY)

            elif re.match(r'^[1-8]$', jugada[1]) and ((l_piezas[0].x != l_piezas[1].x and l_piezas[0].y != l_piezas[1].y) or (l_piezas[0].x == l_piezas[1].x and l_piezas[0].y != l_piezas[1].y)):
                return self.actualiza_pieza(partida, l_piezas[0] if int(jugada[1]) == l_piezas[0].y else l_piezas[1], nuevaX, nuevaY)

        return -6
        
    def jugada_enroque(self, partida, jugada):
        torre = Partida.comprueba_pieza_casilla(partida, 8 if len(jugada) == 3 else 1, 1 if self.mueveBlancas else 8, "Torre", "B" if self.mueveBlancas else "N")
        rey = Partida.comprueba_pieza_casilla(partida, 5, 1 if self.mueveBlancas else 8, "Rey", "B" if self.mueveBlancas else "N")

        if torre is not None and rey is not None and torre.enrocable and rey.enrocable:

            for i in range(torre.x, rey.x+(1 if torre.x < rey.x else -1), 1 if torre.x < rey.x else -1):
                if (Partida.comprueba_pieza_casilla(partida, i, rey.y) is not None and i != torre.x and i != rey.x) or self.hay_jaque(partida, i, rey.y):
                    return -8

            self.actualiza_pieza(partida, torre, rey.x-(1 if torre.x < rey.x else -1), rey.y)
            self.actualiza_pieza(partida, rey, rey.x-(2 if torre.x < rey.x else -2), rey.y)
            return 0
    
    def jugada_promocion(self, partida, jugada):
        color = "B" if self.mueveBlancas else "N"
        #Si el movimiento no se puede realizar nos salimos
        if self.jugada_peon(partida, jugada[:-2]) == 0:
            peon_promocionado = Partida.comprueba_pieza_casilla(partida, ord(jugada[-4].strip())-96, int(jugada[-3]), "Peon")
            if peon_promocionado is not None:
                if   jugada[-1] == "D": peon_promocionado.nombre = "Dama"   + color
                elif jugada[-1] == "T": peon_promocionado.nombre = "Torre"  + color
                elif jugada[-1] == "A": peon_promocionado.nombre = "Alfil"  + color
                elif jugada[-1] == "C": peon_promocionado.nombre = "Caballo"+ color
                else: return -2
                return 0

        return -2

    def comprueba_pieza_casilla(partida, x, y, nombre="", color=""):
        try:
            recogido = next(filter(lambda pieza: pieza.x == x and pieza.y == y, partida.tablero))
            if nombre in recogido.nombre and color in recogido.nombre:
                return recogido
        
        except StopIteration: pass
        return None
        
    def actualiza_pieza(self, partida, pieza, nuevaX, nuevaY):
        #try:
            #Nos quedamos con las coordenadas originales por si hay que recoger cable
            antX = pieza.x; antY = pieza.y
            posible_mate = False

            #Nos quedamos con los reyes para validar en jugadas en función de jaques
            rey_blanco = next((ppieza for ppieza in self.tablero if ppieza.nombre == "Rey-B"), None)
            rey_negro  = next((ppieza for ppieza in self.tablero if ppieza.nombre == "Rey-N"), None)
            
            #Nos quedamos con la casilla a la que nos queremos mover, por si fuera comer y hubiese que borrarla
            pieza_a_borrar = Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY)

            #Si estamos haciendo una jagada de verdad, y no solo comprobando que otra ha llegado hasya la actualización de pieza, ejecutamos
            if self.validar_ejecucion:
                if pieza_a_borrar is not None: 
                    pieza_a_borrar.matar()

                pieza.x = nuevaX
                pieza.y = nuevaY
                posible_mate = self.hay_jaque(partida, (rey_negro if self.mueveBlancas else rey_blanco).x, (rey_negro if self.mueveBlancas else rey_blanco).y)


            #Validamos que al hacer movimiento no hemos dejado un rey al descubierto, y si lo hicimos, volvemos para atrás
            if (self.mueveBlancas and self.hay_jaque(partida, rey_blanco.x, rey_blanco.y)) or (not self.mueveBlancas and self.hay_jaque(partida, rey_negro.x, rey_negro.y)):
                pieza_a_borrar.revivir(nuevaX, nuevaY)
                pieza.x = antX
                pieza.y = antY
                return -9
            
            #Si hemos sido capaces de desplazar una torre o rey, quitamos su capacidad de enroque
            if pieza.nombre[0] in ["T", "R"] and self.validar_ejecucion: pieza.enrocable = False
            
            #Si hemos dado jaque, comprobamos si es mate 0 = No, 1 = Blancas, 2 = Negras
            if posible_mate: 
                return self.hay_mate(partida, rey_negro if self.mueveBlancas else rey_blanco)
            
            return 0

        #except Exception:
        #    return -7
        
    def hay_jaque(self, partida, x, y):
        self.validar_ejecucion = False; self.mueveBlancas = (False if self.mueveBlancas else True)
        hayJaque = False
        
        if Partida.jugada_peon(self, partida, f"{chr(x+95)}x{chr(x+96)}{y}") == 0 \
        or Partida.jugada_peon(self, partida, f"{chr(x+97)}x{chr(x+96)}{y}") == 0:
            hayJaque = True
        
        for i in ["T", "C", "A", "D", "R"]:
            if Partida.jugada_pieza(self, partida, f"{i}x{chr(x+96)}{y}") == 0 \
            or Partida.jugada_pieza(self, partida, f"{i}{chr(x+96)}x{chr(x+96)}{y}") == 0 \
            or Partida.jugada_pieza(self, partida, f"{i}{y}x{chr(x+96)}{y}") == 0:
                hayJaque = True
        

        self.validar_ejecucion = True; self.mueveBlancas = (False if self.mueveBlancas else True)
        return hayJaque
    
    def hay_mate(self, partida, rey):
        pass