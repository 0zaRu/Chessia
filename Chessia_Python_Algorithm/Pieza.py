class Pieza:
    def __init__(self, nombre="", color="", x="0", y="0", enrocable = False):
        self.nombre = nombre
        self.color = color
        self.vivo = True
        self.x = x
        self.y = y
        if enrocable: self.enrocable = True

    def ver_piezas(piezas, i=1):
        for pieza in piezas:
            print(f"{i:<3} {pieza.nombre:<11} | {chr(pieza.x+96)}{pieza.y} | {'O' if pieza.vivo is True else 'X'}")
            i+=1

    def matar(self):
        #Podría borrar el objeto, todavía no lo se
        self.vivo = False
        self.x = 0
        self.y = 0

    def revivir(self, nuevaX, nuevaY):
        #Podría borrar el objeto, todavía no lo se
        self.vivo = True
        self.x = nuevaX
        self.y = nuevaY

    @classmethod
    def crear_piezas_partida(self, color="B"):
        piezas = []
        filaPeones  = 2 if color == "B" else 7
        filaTrasera = 1 if color == "B" else 8

        for x in range(1, 9):
            piezas.append(Pieza(f"Peon-{chr(x+64)}-{color}", color, x, filaPeones))

        for x in range(1, 9):
            if x == 1 or x == 8:
                piezas.append(Pieza(f"Torre-{color}", color, x, filaTrasera, True))
            if x == 2 or x == 7:
                piezas.append(Pieza(f"Caballo-{color}", color, x, filaTrasera))
            if x == 3 or x == 6:
                piezas.append(Pieza(f"Alfil-{color}", color, x, filaTrasera))
            if x == 4:
                piezas.append(Pieza(f"Dama-{color}", color, x, filaTrasera))
            if x == 5:
                piezas.append(Pieza(f"Rey-{color}", color, x, filaTrasera, True))
        
        if color == "B":
            piezas += (self.crear_piezas_partida("N")) 
            
        return piezas