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
            r'^[RDTAC][a-h1-8]?[a-h][1-8]$': self.movimiento_pieza,       # Movimiento o captura de una pieza (!peon)
            r'^[RDTAC][a-h1-8]?x[a-h][1-8]$': self.comer_de_pieza,       # Movimiento o captura de una pieza (!peon)
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


    def movimiento_pieza(self, partida, jugada):
        # Si la jugada es de 4 letras, es que se ha especificado el origen de la pieza, hay que guardar este parámetro 
        # y comparar que realmente otra pieza de este tipo también podía hacer la jugada
        antP = None
        if len(jugada) is 4:
            antP = ord(jugada[1].strip())-96 if str(jugada[1]).isalpha() else int(jugada[1])
            esX = True if str(jugada[1]).isalpha() else False
        
        nuevaX = ord(jugada[len(jugada)-2].strip())-96
        nuevaY = int(jugada[len(jugada)-1])

        if Partida.comprueba_pieza_casilla(partida, nuevaX, nuevaY) is not None:
            input("\n\t    Jugada incorrecta, hay una pieza en esta casilla ...")
            return False
        
        if jugada[0] is "T":
            if antP is not None:
                pieza = Partida.comprueba_pieza_casilla(partida, antP if esX else nuevaX, antP if not esX else nuevaY, "T", "B" if self.mueveBlancas else "N")
        
                if pieza is None:
                    input("\n\t    Jugada incorrecta, no hay un Torre que pueda hacerla ..."); return False
                
                #Comprobamos todas las filas entre la pieza y el destino para ver que está vacío, podría comprobar solo un eje pero hago los dos pawra que sea más fácil extrapolar en un futuro
                #for i in range(pieza.X, nuevaX, 1 if pieza.X < nuevaX else (-1 if pieza.X > nuevaX else 0)):
                #    for j in range(pieza.Y, nuevaY, 1 if pieza.Y < nuevaY else (-1 if pieza.Y > nuevaY else 0)):
                #        if Partida.comprueba_pieza_casilla(partida, i, j) is not None:
                #            input("\n\t    Jugada incorrecta, no hay una Torre con visibilidad válida ..."); return False
                
                for i in range(pieza.x, nuevaX, 1 if pieza.x < nuevaX else -1):
                    for j in range(pieza.y, nuevaY, 1 if pieza.y < nuevaY else -1):
                        print("ou")
                        if Partida.comprueba_pieza_casilla(partida, i, j) is not None:
                            input("\n\t    Jugada incorrecta, no hay una Torre con visibilidad válida ..."); return False
                        else:
                            input("yeiiiiiiiii")
                
                return Partida.actualiza_pieza(partida, pieza, nuevaX, nuevaY)



    def comer_de_pieza(self, partida, jugada):
        pass


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