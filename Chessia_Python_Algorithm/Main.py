from Partida import Partida

"""
Álgebra posible de Movimientos de Ajedrez

    e4             - Peón de la misma columna

    Ne4            - Cualquier pieza menos el peón desplazándose a e4
    O-O            - Enroque corto
    
    exd6           - Peón de e5 come al paso el peón de d5, colocándose en d6. O el peón de e captura a un peón en d6. Solo es al paso si acaba de salir el peón a 2 casillas
    Nee4           - Cuando dos figuras iguales pueden optar a una casilla, 
    N4e4             se especifica haciendo referencia a su columna/fila distintiva previo a la casilla a la que se quiere mover
    Nxe4           - La pieza especificada come en e4
    g8=[D/T/C/A]   - El peón de g7 avanza a g8 y corona
    
    Nexe4          - La pieza que se especifica con su columna/fila distintiva por necesidad, captura en e4
    N4xe4   
    O-O-O          - Enroque largo
    
    hxg8=[D/T/C/A] - El peón de h7 captura en g8 y corona

    Consideramos los jaques (+) y los mates (#) como nomeclatura automática del programa. No es necesario especificarlos.

    ==========================================================================================================================================================================
    
    Resultados del servidor:
    0 - Jugada válida
    
    1 - Victoria Blanca
    2 - Victoria Negra
    3 - Tablas
    4 - Jaque al blanco
    5 - Jaque al negro
    
   -1  - Error, sintaxis no válida ...
   -2  - Error, fallo intentando promocionar el peón ...
   -3  - Error en comida de peón
   -4  - Error, no hay un peón viable ...
   -5  - Error, fallo en relación al destino de la pieza ...
   -6  - Error, no se ha encontrado una pieza viable ...
   -7  - Excepción actualizando la pieza ...
   -8  - Error, pieza o jaque interfiriendo con el enroque ...
   -9  - Error, estás en jaque ...
   -10 - Error, jugada de peón de promoción no válida ...
   -11 - Error, no hay torre o rey en su casilla inicial ...
   -12 - Error, no puedes comer al Rey, aunque aquí no deberías poder llegawr ...

"""

class Main:
    def main():
        global partida; global valido; global finalizado
        partida = Partida()
        valido = False; finalizado = False

        while not finalizado:
            
            Main.nuevo_movimiento(partida)
            
            while not valido:
                Partida.visualizar_experimental(partida)
                Main.interpreta_resultado(partida.ejecuta_mov_entrada(input("\n\t    JUGADA DE BLANCAS: ")))

            if not finalizado:
                Main.nuevo_movimiento(partida, "N")

                while not valido:
                    Partida.visualizar_experimental(partida)
                    Main.interpreta_resultado(partida.ejecuta_mov_entrada(input("\n\t    JUGADA DE NEGRAS: ")))

    def nuevo_movimiento(partida, color="B"):
        global valido; global finalizado
        valido = False

        partida.mueveBlancas = True if color == "B" else False
        
        if partida.al_paso_activo is not None and color == partida.al_paso_activo.color: 
            partida.al_paso_activo = None
        
        if color == "B":
            partida.turno +=1

    def interpreta_resultado(resultado):
        global valido; global finalizado; global partida

        if resultado == 0: valido = True
        elif resultado in [1, 2, 3]:
            valido = finalizado = True
            Partida.visualizar_experimental(partida)
            
            input("\n\t    "+"="*44+"\n\t\t      "+("VICTORIA DE LAS BLANCAS" if resultado == 1 else(  "VICTORIA DE LAS NEGRAS " if resultado == 2 else   "        TABLAS         "))+"\n\t    "+"="*44)
        
        elif resultado in [4, 5]:
            valido = True
            input("\n\t    JAQUE AL REY "+("BLANCO" if resultado == 4 else "NEGRO"))
        
        elif resultado == -1:  input("\n\t    Error, sintaxis no válida ...")
        elif resultado == -2:  input("\n\t    Error, fallo intentando promocionar el peón ...")
        elif resultado == -3:  input("\n\t    Error en comida de peón")
        elif resultado == -4:  input("\n\t    Error, no hay un peón viable ...")
        elif resultado == -5:  input("\n\t    Error, fallo en relación al destino de la pieza ...")
        elif resultado == -6:  input("\n\t    Error, no se ha encontrado una pieza viable ...")
        elif resultado == -7:  input("\n\t    Excepción actualizando la pieza ...")
        elif resultado == -8:  input("\n\t    Error, pieza o jaque interfiriendo con el enroque ...")
        elif resultado == -9:  input("\n\t    Error, estás en jaque ...")
        elif resultado == -10: input("\n\t    Error, jugada de peón de promoción no válida ...")
        elif resultado == -11: input("\n\t    Error, no hay torre o rey en su casilla inicial ...")
        elif resultado == -12: input("\n\t    Error, no puedes comer al Rey, aunque aquí no deberías poder llegawr ...")
        else: input("¿?¿?¿?¿?")
        

Main.main()