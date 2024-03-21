from Partida import Partida

'''
Álgebra posible de Movimientos de Ajedrez

    2 e4             - Peón de la misma columna

    3 Ne4            - Cualquier pieza menos el peón desplazándose a e4
    3 O-O            - Enroque corto
    
    4 exd6           - Peón de e5 come al paso el peón de d5, colocándose en d6. O el peón de e captura a un peón en d6. Solo es al paso si acaba de salir el peón a 2 casillas
    4 Nee4           - Cuando dos figuras iguales pueden optar a una casilla, 
    4 N4e4             se especifica haciendo referencia a su columna/fila distintiva previo a la casilla a la que se quiere mover
    4 Nxe4           - La pieza especificada come en e4
    4 g8=[D/T/C/A]   - El peón de g7 avanza a g8 y corona
    
    5 Nexe4          - La pieza que se especifica con su columna/fila distintiva por necesidad, captura en e4
    5 N4xe4   
    5 O-O-O          - Enroque largo
    
    6 hxg8=[D/T/C/A] - El peón de h7 captura en g8 y corona

    Consideramos los jaques (+) y los mates (#) como nomeclatura automática del programa. No es necesario especificarlos.

'''

class Main:

    @staticmethod
    def main():
        partida = Partida()

        while True:
            
            valido = False; partida.mueveBlancas = True
            
            while not valido:
                partida.visualizar_partida(partida)
                valido = partida.ejecuta_mov_entrada(input("\n\t    JUGADA DE BLANCAS: "))

            valido = False; partida.mueveBlancas = False

            while not valido:
                partida.visualizar_partida(partida)
                valido = partida.ejecuta_mov_entrada(input("\n\t    JUGADA DE NEGRAS: "))
            
            partida.turno +=1



Main.main()