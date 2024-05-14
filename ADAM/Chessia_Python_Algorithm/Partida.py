from Pieza import Pieza

from os import system
from copy import deepcopy
import re

class Partida: 
    def __init__(self):
        self.tablero = Pieza.crear_piezas_partida()
        self.turno = 0
        self.mueveBlancas = True
        self.jugada = ""
        self.al_paso_activo = None
        self.validar_mas = True
        self.posibles_jugadas_algebraicas = {
            r'^([a-h]x)?[a-h][2-7]([+#])?$': self.jugada_peon,                   # Movimiento de peón
            r'^[RDTAC][a-h1-8]?x?[a-h][1-8]([+#])?$': self.jugada_pieza,         # Movimiento o captura de una pieza (!peon)
            r'^O-O(-O)?([+#])?$': self.jugada_enroque,                           # Enroque ya sea largo o corto
            r'^([a-h]x)?[a-h][18](=[DTAC])([+#])?$': self.jugada_promocion       # Promocíon de Peón a una pieza moviendo o comiendo
        }
        self.caracteres_ajedrez = {
            "P": "♟",
            "T": "♜",
            "C": "♞",
            "A": "♝",
            "D": "♛",
            "R": "♚"
        }
    
    def visualizar_partida(self, color):
        hayPieza=False
        # system("cls")

        print("\n",("\t")*3,"RONDA",self.turno)
        print(("\t   ")*1,"=================================")

        if color == "B": print("\t      a   b   c   d   e   f   g   h \t")
        else:            print("\t      h   g   f   e   d   c   b   a \t")
        print("\t    ╔"+("═══╦")*7+"═══╗ \t")

        for i in (range(7, -1, -1) if color == "B" else range(0, 8)):
            print(f"\t  {i+1} ", end="")
            for j in (range(7, -1, -1) if color == "B" else range(0, 8)):
                for pieza in self.tablero:
                    if pieza.y-1 == i and pieza.x-1 == 7-j:
                        print("║ "+self.caracteres_ajedrez[pieza.nombre[0]]+" "    if pieza.color == "B" else   "║ \033[31m"+self.caracteres_ajedrez[pieza.nombre[0]]+"\033[0m ", end="")
                        hayPieza = True
                        break
                if not hayPieza:
                    print("║   ", end="")
                else:
                    hayPieza = False
            
            print("║\n"+("\t    ╚"+("═══╩"*7)+"═══╝ \t" if i == (0 if color == "B" else 7) else "\t    ╠"+("═══╬"*7)+"═══╣ \t"))

    def ejecutar_jugada(self, jugada, validacionContraria=True, validarMas=True):
        self.validar_mas = validarMas
        for reg, funcion in self.posibles_jugadas_algebraicas.items():
            if re.fullmatch(reg, jugada):
                if jugada[-1] in ["#", "+"]:
                    jugada = jugada[:-1]
                
                self.jugada = jugada
                devolver = funcion()
                
                #Validamos que no se haya quedado en tablas
                if validacionContraria:
                    contrario_puede_mover = True
                    if devolver in [0, 4, 5]: contrario_puede_mover = self.hay_mov_general("N" if self.mueveBlancas else "B")
                    
                    if devolver == 0 and not contrario_puede_mover:   return 3    #Tablas
                    elif devolver == 4 and not contrario_puede_mover: return 2  #Gana negras
                    elif devolver == 5 and not contrario_puede_mover: return 1  #Gana blancas
                    
                return devolver
        return -1
    
    def jugada_peon(self, jugada=None):
        comer = posible_al_paso = False
    
        if jugada is None:
            jugada = self.jugada

        nuevaX = ord(jugada[len(jugada)-2].strip())-96
        nuevaY = int(jugada[len(jugada)-1])

        if jugada[1] == "x": 
            comer = True
            antX = ord(jugada[len(jugada)-4].strip())-96

        if Partida.comprueba_pieza_casilla(self, nuevaX, nuevaY) is (not None) if comer else (None):
            return -5

        #Se busca una pieza a 1 casilla de distancia
        pieza = Partida.comprueba_pieza_casilla(self, antX if comer else nuevaX, nuevaY-(1 if self.mueveBlancas else -1), "Peon", "B" if self.mueveBlancas else "N" )

        if comer and abs(antX-nuevaX) == 1:
            pieza_a_comer = Partida.comprueba_pieza_casilla(self, nuevaX, nuevaY, "", "N" if self.mueveBlancas else "B")
            
            #Si hay una pieza válida a comer al paso, no hay pieza a donde queremos llegar, y estamos pegados a la pieza, es que es captura al paso.
            if self.al_paso_activo is not None and pieza_a_comer is None: #and self.al_paso_activo.x == nuevaX and self.al_paso_activo.y == nuevaY-(1 if self.mueveBlancas else -1):
                #Desplazamos la pieza a la casilla donde queremos movernos porque así no hay que modificar algoritmos de captura y movimiento
                if Partida.comprueba_pieza_casilla(self, nuevaX, nuevaY-(1 if self.mueveBlancas else -1)) is not self.al_paso_activo \
                or self.actualiza_pieza(self.al_paso_activo, nuevaX, nuevaY, jugadaLarga=True) != 0:
                    return -3
                
                else: pieza_a_comer = self.al_paso_activo

            if pieza is not None and pieza_a_comer is not None:
                return self.actualiza_pieza(pieza, nuevaX, nuevaY)
        
        elif not comer:
            #Si no había pieza a 1 casilla verificamos a 2 si es viable
            if pieza is None and (nuevaY == 4 and self.mueveBlancas or nuevaY == 5 and not self.mueveBlancas):
                pieza = Partida.comprueba_pieza_casilla(self, nuevaX, nuevaY-(2 if self.mueveBlancas else -2), "Peon", "B" if self.mueveBlancas else "N")
                posible_al_paso = True

            #Si había pieza a 1 casilla distancia o si era viable que la hubiese a 2 y la hay, ubicamos la pieza en la lista y le actualizamos la x y la y
            if pieza is not None:
                devolver = self.actualiza_pieza(pieza, nuevaX, nuevaY)
                
                #Si es una pieza a 2 casillas, la activamos como válida para comer al paso
                if posible_al_paso and devolver == 0: self.al_paso_activo = pieza
                return devolver

        return -4
        
    def jugada_pieza(self):
        #Almacenamiento de nueva casilla de destino
        nuevaX = ord(self.jugada[len(self.jugada)-2].strip())-96
        nuevaY = int(self.jugada[len(self.jugada)-1])
        l_piezas = []

        #Se recoge la nueva casilla y se comprueba que si hay algo es del otro equipo y es para comer y que si no hay nada es para mover
        destino = Partida.comprueba_pieza_casilla(self, nuevaX, nuevaY)
        if ("x" in self.jugada and (destino is None or ("B" if self.mueveBlancas else "N") == destino.nombre[-1])) or ("x" not in self.jugada and destino is not None):
            return -5
        
        #Se recorren todas las piezas del tablero
        for pieza in self.tablero:
            if ("N" if self.mueveBlancas else "B") in pieza.nombre[-1] or self.jugada[0] != pieza.nombre[0] or not pieza.vivo: continue

            #Filtramos primero los caballos, que no necesitan comprobar casillas vacias
            if (pieza.nombre[0] == "C" and (abs(nuevaX - pieza.x)+abs(nuevaY - pieza.y) == 3) and (nuevaX != pieza.x and nuevaY != pieza.y)): 
                l_piezas.append(pieza)
            
            #Filtramos la piezas, deben ser del color del turno y tener la letra de la jugada en el nombre, además de ser T, D o R si están en la misma fila o columna y ser A, D o R si es diagonal
            if pieza.nombre[0] != "C" \
            and (((pieza.x == nuevaX or pieza.y == nuevaY) and self.jugada[0] in ["T", "D"]) \
            or (abs(pieza.x - nuevaX) == abs(pieza.y - nuevaY) and self.jugada[0] in ["A", "D"]) \
            or (self.jugada[0] in ["R"] and (abs(pieza.x-nuevaX) <= 1 and abs(pieza.y-nuevaY) <= 1))):
                valido = True
                
                #zip 1: comparte columna (torre o dama)        #zip 2: comparte fila (torre o dama)       #zip 3: no comparte nada (alfil o dama)        
                for i, j in \
                zip(list(nuevaX for x in range(1, 9)), range(nuevaY-(1 if pieza.y < nuevaY else -1), pieza.y, 1 if nuevaY < pieza.y else -1)) if nuevaX == pieza.x else (\
                zip(range(nuevaX-(1 if pieza.x < nuevaX else -1), pieza.x, 1 if nuevaX < pieza.x else -1), list(nuevaY for y in range(1, 9))) if nuevaY == pieza.y else \
                zip(range(nuevaX-(1 if pieza.x < nuevaX else -1), pieza.x, 1 if nuevaX < pieza.x else -1), range(nuevaY-(1 if pieza.y < nuevaY else -1), pieza.y, 1 if nuevaY < pieza.y else -1))):    
                    
                    if Partida.comprueba_pieza_casilla(self, i, j) is not None:
                        valido = False

                if valido and pieza.vivo: l_piezas.append(pieza)
        
        if len(l_piezas) == 1 and ((len(self.jugada) == 4 and self.jugada[1] == "x") or (len(self.jugada) <= 3)): 
            return self.actualiza_pieza(l_piezas[0], nuevaX, nuevaY)
        
        elif len(l_piezas) == 2 and len(self.jugada) >= 4 and self.jugada[1] != "x":
            if re.match(r'^[a-h]$', self.jugada[1]) and ((l_piezas[0].x != l_piezas[1].x and l_piezas[0].y != l_piezas[1].y) or (l_piezas[0].x != l_piezas[1].x and l_piezas[0].y == l_piezas[1].y)):
                return self.actualiza_pieza(l_piezas[0] if ord(self.jugada[1].strip())-96 == l_piezas[0].x else l_piezas[1], nuevaX, nuevaY)

            elif re.match(r'^[1-8]$', self.jugada[1]) and ((l_piezas[0].x != l_piezas[1].x and l_piezas[0].y != l_piezas[1].y) or (l_piezas[0].x == l_piezas[1].x and l_piezas[0].y != l_piezas[1].y)):
                return self.actualiza_pieza(l_piezas[0] if int(self.jugada[1]) == l_piezas[0].y else l_piezas[1], nuevaX, nuevaY)

        return -6
        
    def jugada_enroque(self):
        torre = Partida.comprueba_pieza_casilla(self, 8 if len(self.jugada) == 3 else 1, 1 if self.mueveBlancas else 8, "Torre", "B" if self.mueveBlancas else "N")
        rey = Partida.comprueba_pieza_casilla(self, 5, 1 if self.mueveBlancas else 8, "Rey", "B" if self.mueveBlancas else "N")

        if torre is not None and rey is not None and torre.enrocable and rey.enrocable:

            for i in range(torre.x, rey.x+(1 if torre.x < rey.x else -1), 1 if torre.x < rey.x else -1):
                if (Partida.comprueba_pieza_casilla(self, i, rey.y) is not None and i != torre.x and i != rey.x) \
                or self.hay_mov(i, rey.y, "N" if self.mueveBlancas else "B", comer=(True if i == torre.x or i == rey.x else False)):
                    return -8

            self.actualiza_pieza(torre, rey.x-(1 if torre.x < rey.x else -1), rey.y, jugadaLarga=True)
            self.actualiza_pieza(rey, rey.x-(2 if torre.x < rey.x else -2), rey.y)
            return 0
        return -11
    
    def jugada_promocion(self):
        if self.jugada[-1] in ['+', '#']:
            self.jugada = self.jugada[:-1]

        color = "B" if self.mueveBlancas else "N"
        #Si el movimiento no se puede realizar nos salimos
        if self.jugada_peon(self.jugada[:-2]) == 0:
            peon_promocionado = Partida.comprueba_pieza_casilla(self, ord(self.jugada[-4].strip())-96, int(self.jugada[-3]), "Peon")
            if peon_promocionado is not None:
                if   self.jugada[-1] == "D": peon_promocionado.nombre = "Dama-"   + color.upper()
                elif self.jugada[-1] == "T": peon_promocionado.nombre = "Torre-"  + color.upper()
                elif self.jugada[-1] == "A": peon_promocionado.nombre = "Alfil-"  + color.upper()
                elif self.jugada[-1] == "C": peon_promocionado.nombre = "Caballo-"+ color.upper()
                else: return -2
                return 0

        return -10

    def comprueba_pieza_casilla(self, x, y, nombre="", color=""):
        try:
            recogido = next(filter(lambda pieza: pieza.x == x and pieza.y == y, self.tablero))
            if nombre in recogido.nombre and color in recogido.nombre:
                return recogido
        
        except StopIteration: pass
        return None
        
    def actualiza_pieza(self, pieza, nuevaX, nuevaY, jugadaLarga=False):
        try:
            #Si por alguna razón la pieza que ha llegado está muerta, nos salimos
            if not pieza.vivo:
                return -7
            
            #Nos quedamos con las coordenadas originales por si hay que recoger cable
            antX = pieza.x; antY = pieza.y

            #Nos quedamos con los reyes para validar en jugadas en función de jaques
            rey_blanco = next((ppieza for ppieza in self.tablero if ppieza.nombre == "Rey-B"), None)
            rey_negro  = next((ppieza for ppieza in self.tablero if ppieza.nombre == "Rey-N"), None)
            
            #Nos quedamos con la casilla a la que nos queremos mover, por si fuera comer y hubiese que borrarla
            pieza_a_borrar = Partida.comprueba_pieza_casilla(self, nuevaX, nuevaY)

            pieza.x = nuevaX
            pieza.y = nuevaY

            if pieza_a_borrar is not None: 
                pieza_a_borrar.matar()

            #Validamos que al hacer movimiento no hemos dejado un rey al descubierto, y si lo hicimos, volvemos para atrás
            if self.validar_mas and ((self.mueveBlancas and self.hay_mov(rey_blanco.x, rey_blanco.y, "N", comer=True, validarMas=False)) \
            or (not self.mueveBlancas and self.hay_mov(rey_negro.x, rey_negro.y, "B", comer=True, validarMas=False))):
                pieza.x = antX
                pieza.y = antY
                if pieza_a_borrar is not None:
                    pieza_a_borrar.revivir(nuevaX, nuevaY)

                return -9
            

            #Si hemos sido capaces de desplazar una torre o rey, quitamos su capacidad de enroque
            if pieza.nombre[0] in ["T", "R"]: pieza.enrocable = False    

            #Si hemos dado jaque con una jugada válida, devolvemos 4 o 5 y no estamos a mitad de una jugada larga (comer al paso o enroque)
            if not jugadaLarga:
                if self.mueveBlancas and self.hay_mov(rey_negro.x, rey_negro.y, "B", comer=True):       return 5
                if not self.mueveBlancas and self.hay_mov(rey_blanco.x, rey_blanco.y, "N", comer=True): return 4

            return 0

        except Exception:
            print("eii")
            return -7
        
    def hay_mov(self, desX, desY, color_a_mover, comer=False, validarMas=True):
        #Vamos a coger una copia para simular una jugada en ella
        partida_copia = deepcopy(self)
        partida_copia.mueveBlancas = (True if color_a_mover == "B" else False)

        #Si la pieza es nula o es una pieza diferente de un peón, vamos a intentar ejecutar un movimiento directamente con esta
        for i in ["T", "C", "A", "D", "R"]:
            if partida_copia.ejecutar_jugada(f"{i}x{chr(desX+96)}{desY}"               if comer else   f"{i}{chr(desX+96)}{desY}"              , False, validarMas) >= 0 \
            or partida_copia.ejecutar_jugada(f"{i}{chr(desX+96)}x{chr(desX+96)}{desY}" if comer else   f"{i}{chr(desX+96)}{chr(desX+96)}{desY}", False, validarMas) >= 0 \
            or partida_copia.ejecutar_jugada(f"{i}{desY}x{chr(desX+96)}{desY}"         if comer else   f"{i}{desY}{chr(desX+96)}{desY}"        , False, validarMas) >= 0:
                return True
        
        if (comer     and partida_copia.ejecutar_jugada(f"{chr(desX+95)}x{chr(desX+96)}{desY}", False, validarMas) >= 0 )\
        or (comer     and partida_copia.ejecutar_jugada(f"{chr(desX+97)}x{chr(desX+96)}{desY}", False, validarMas) >= 0 )\
        or (not comer and partida_copia.ejecutar_jugada(f"{chr(desX+96)}{desY}"               , False, validarMas) >= 0 ):
            return True
        
        return False
    
    def hay_mov_general(self, color):
        for i in range(1, 9):
            for j in range(1, 9):
                destino = self.comprueba_pieza_casilla(i, j)
                if (destino is None and self.hay_mov(i, j, color, comer=False)) \
                or (destino is not None and destino.nombre[-1] == ("B" if color == "N" else "N") and self.hay_mov(i, j, color, comer=True)):
                    return True
                
        return False
    
