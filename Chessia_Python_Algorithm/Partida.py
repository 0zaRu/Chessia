from Pieza import Pieza
from os import system
import re

class Partida:
    def __init__(self):
        self.tablero = Pieza.crear_piezas_partida()
        self.turno = 1
        self.mueveBlancas = True
        self.posibles_jugadas_algebraicas = {
            r'^[a-h][1-8]$': self.movimiento_peon,                        # Movimiento de peón
            r'^[a-h]x[a-h][1-8]$': self.comer_de_peon,                    # Captura de peón
            r'^[RDTAC]([a-h1-8])?x?[a-h][1-8]$': self.jugada_pieza,       # Movimiento o captura de una pieza (!peon)
            r'^O-O(-O)?$': self.jugada_enroque,                           # Enroque ya sea largo o corto
            r'^([a-h]x)?[a-h][18](=[DTAC])$': self.jugada_promocion       # Promocíon de Peón a una pieza moviendo o comiendo
        }
    
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
        nuevaX = ord(jugada[len(jugada)-2].strip())-96
        nuevaY = int(jugada[len(jugada)-1])

        #Si la casilla a la que querenos mover está vacía
        if len(list(filter(lambda pieza: pieza.x == nuevaX and pieza.y == nuevaY, partida.tablero))) == 0:
            
            #Si la pieza está a 1 casilla de distancia y existe una válida
            posible_pieza = list(filter(lambda pieza: pieza.x == nuevaX and pieza.y == nuevaY-(1 if self.mueveBlancas else -1), partida.tablero))
            
            #Si no se ha encontrado pieza y es viable un desplazamiento de 2 casillas, se verifica si hay pieza a 2 casillas
            if (len(posible_pieza) == 0 and (nuevaY == 4 and self.mueveBlancas) or (nuevaY == 5 and not self.mueveBlancas)):
                posible_pieza = list(filter(lambda pieza: pieza.x == nuevaX and pieza.y == nuevaY-(2 if self.mueveBlancas else -2), partida.tablero))
            
            #Si hemos encontrado pieza en algun contexto y es un peón, desplazamos
            if(len(posible_pieza) == 1 and "Peon" in posible_pieza[0].nombre):
        
                #Ubicamos la pieza en la lista y le actualizamos la x y la y
                partida.tablero.__getitem__(partida.tablero.index(posible_pieza[0])).x = nuevaX
                partida.tablero.__getitem__(partida.tablero.index(posible_pieza[0])).y = nuevaY
                return True
            
            else:
                input("\n\t    Jugada incorrecta, ningun peón puede ...")
        else:
                input("\n\t    Jugada incorrecta, hay una pieza en esta casilla ...")
        
        return False

    def comer_de_peon(self, partida, jugada):
        nuevaX = ord(jugada[len(jugada)-2].strip())-96
        nuevaY = int(jugada[len(jugada)-1])

        #Si la casilla a la que querenos mover tiene una pieza
        if len(list(filter(lambda pieza: pieza.x == nuevaX and pieza.y == nuevaY, partida.tablero))) == 1:
            pass

    
    def jugada_pieza(self, partida, jugada):
        print(f"dasdads  --")

    def jugada_enroque(self, partida, jugada):
        print(f"dasdads  --")

    def jugada_promocion(self, partida, jugada):
        print(f"dasdads  --")
