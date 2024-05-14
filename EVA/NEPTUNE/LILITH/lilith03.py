from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from WindowTools import WindowTools as W
from typing import List
import tensorflow as tf
import pickle

mapeo_es_a_en = {
    "T": "R",
    "D": "Q",
    "C": "N",
    "A": "B",
    "R": "K"
}

def contador_partidas_iguales(partidas, cadena_jugada, color_ia):
    # Contar las ocurrencias de cada cadena en el archivo de partidas
    partidas_iguales = 0
    for partida in partidas:
        resultado = partida[-2]

        if resultado == str(color_ia) and cadena_jugada in partida[:len(cadena_jugada)+1]:
            partidas_iguales += 1

    return partidas_iguales

def recoge_modelo():
    # Creación del tokenizer y carga del modelo
    tokenizer = Tokenizer()
    with open(W.RUTA_ORIGEN + "LILITH/tokens03.pkl", "rb") as f:
        tokenizer = pickle.load(f)
    
    lilith03 = tf.keras.models.load_model(W.RUTA_ORIGEN + "LILITH/lilith03.keras")
    return lilith03, tokenizer

def convertir_a_ingles(total_movimientos_es):
    total_movimientos_en = []
    
    for movimientos_es in total_movimientos_es:
        movimientos_en = "".join(mapeo_es_a_en.get(caracter.upper(), caracter) if caracter.isupper() else caracter for caracter in movimientos_es)
        total_movimientos_en.append(movimientos_en)
    
    return total_movimientos_en

class Lilith_Predictor:
    def predecir_mejores_10(jugadas_es: List[str], posibles_movs_es: List[str], partidas, color_ia=2):
        
        # Creación de todas las posibles cadenas de movimientos y traducción al inglés
        movimientos_es = [" ".join(jugadas_es) + " " + movimiento for movimiento in posibles_movs_es]
        movimientos_en = convertir_a_ingles(movimientos_es)

        # Recogida de modelo y COnversión a tensores de los movimientos posibles
        lilith03, tokenizer = recoge_modelo()
        tensor_mov_pred = tf.constant(pad_sequences(tokenizer.texts_to_sequences(movimientos_en), maxlen=500, padding="pre"))
        
        # Realizar la predicción
        resultados = lilith03.predict(tensor_mov_pred)

        # COntar apariciones de las cadenas en el fichero de partidas
        apariciones_cadenas = []
        for mov in movimientos_en:
            apariciones_cadenas.append(contador_partidas_iguales(partidas, mov, color_ia))
        
        # UNificación de la información predicha en relación a los movimientos y ordenarla
        informacion_total = []
        for movimiento, resultado, apariciones in zip(posibles_movs_es, resultados, apariciones_cadenas):
            informacion_total.append([resultado[color_ia], apariciones, movimiento])

        informacion_total = sorted(informacion_total, key=lambda x: (x[1], x[0]), reverse=True)
        
        if len(informacion_total) > 10:
            mejores_10 = informacion_total[:10]
        else:
            mejores_10 = informacion_total
        
        return [item[2] for item in mejores_10]