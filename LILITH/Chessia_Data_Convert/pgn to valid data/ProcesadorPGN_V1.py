import os
import re
import json

"""
Se han tomado:    103.371 partidas para la conversión
De resultado hay: 103.351 partidas convertidas
"""

class Partida:
    def __init__(self):
        self.movimientos = []
        self.resultado = None

DIRECTORIO_FUENTE = "Chessia_Data_Convert/Source Data"
FICHERO_DESTINO_V1 = "Chessia_Data_Convert/Target Data/Datos Preprocesados"
FICHERO_DESTINO_V2 = "Chessia_Data_Convert/Target Data/Datos-JSON.json"
conversion_valores = {
    "1": "01",
    "2": "02",
    "3": "03",
    "4": "04",
    "5": "05",
    "6": "06",
    "7": "07",
    "8": "08",
    "a": "11",
    "b": "12",
    "c": "13",
    "d": "14",
    "e": "15",
    "f": "16",
    "g": "17",
    "h": "18",
    "K": "21", # Rey
    "Q": "22", # Dama
    "R": "23", # Torre
    "B": "24", # Alfil
    "N": "25", # Caballo
    "x": "31",
    "+": "32",
    "=": "33",
    "O": "34",
    "-": "35"
}

def codifica_jugada(movimiento):
    devolver = "00"*(7-len(movimiento))
    
    for char in movimiento:
        # print(f"{conversion_valores.get(char)} -- {char}")
        devolver += conversion_valores.get(char)
    
    return devolver

def procesar_fichero_pgn_fase_1(archivo_pgn, archivo_destino):
    with open(archivo_pgn, 'r') as lector, open(archivo_destino, 'a') as escritor:
        partida_tmp = []

        for linea in lector:
            if linea.startswith("[") or len(linea.strip()) == 0:
                continue

            linea = linea.replace("  ", " ").strip()
            linea = linea.replace("* ", "")
            linea += " "
            linea = re.sub(r'[0-9]?[0-9]?[0-9]\.', "", linea)
            partida_tmp.append(linea)


            if partida_tmp[-1].endswith("1-0 ") or partida_tmp[-1].endswith("0-1 ") or partida_tmp[-1].endswith("1/2-1/2 "):
                partida = "".join(partida_tmp)

                if   partida.endswith("1-0 "):     partida = partida.replace("1-0", "1\n")
                elif partida.endswith("0-1 "):     partida = partida.replace("0-1", "2\n")
                elif partida.endswith("1/2-1/2 "): partida = partida.replace("1/2-1/2", "0\n")
                
                if "*" not in partida:
                    escritor.write(partida.strip() + '\n')
                
                partida_tmp = []

def procesar_fichero_pgn_fase_2(archivo_preprocesado, archivo_destino):
    with open(archivo_preprocesado, 'r') as lector, open(archivo_destino, 'a') as escritor:
        escritor.write("[\n")  # Abrir la lista de partidas
        primera_partida = True  # Bandera para controlar la escritura de comas

        for linea in lector:    
            if len(linea.strip()) == 0:
                continue
            
            partida = Partida()
            partida.movimientos = linea[:-3].split(" ")
            partida.resultado = linea[-2]

            for i in range(len(partida.movimientos)):
                partida.movimientos[i] = codifica_jugada(partida.movimientos[i])
            
            while len(partida.movimientos) < 500:
                partida.movimientos.insert(0, '00000000000000')

            # Crear un diccionario con la estructura deseada
            partida_dict = {
                "movimientos": partida.movimientos,  # Guardar los movimientos como una lista
                "resultado": partida.resultado
            }

            if not primera_partida: 
                escritor.write(",\n")
            else:                   
                primera_partida = False

            # Escribir manualmente la lista en el archivo sin separar en líneas
            escritor.write(json.dumps({"partida": partida_dict}, indent=None))
            
        escritor.write("\n]")

def main():
    """
    El fichero JSON no se sube a git por tamaño
    """
    # Apertura de ficheros
    directorio_fuente = os.listdir(DIRECTORIO_FUENTE)

    if os.path.exists(FICHERO_DESTINO_V1):
         os.remove(FICHERO_DESTINO_V1)

    if os.path.exists(FICHERO_DESTINO_V2):
        os.remove(FICHERO_DESTINO_V2)
    
    #  Recorrido de ficheros de origen para el primer procesado de datos
    with open(FICHERO_DESTINO_V1, 'w') as archivo_destino: pass
    for archivo_pgn in directorio_fuente:
        procesar_fichero_pgn_fase_1(os.path.join(DIRECTORIO_FUENTE, archivo_pgn), FICHERO_DESTINO_V1)

    # Recorrido de fichero preprocesado de datos para la conversión a JSON
    with open(FICHERO_DESTINO_V2, 'w') as archivo_destino: pass
    procesar_fichero_pgn_fase_2(FICHERO_DESTINO_V1, FICHERO_DESTINO_V2)  # Corrección aquí

if __name__ == "__main__":
    main()
