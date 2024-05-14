import pygame
import sys

class WindowTools:
    # Definir constantes
    RUTA_ORIGEN = "EVA/NEPTUNE/" # "./"
    RUTA_ADAM = "ADAM/Chessia_Python_Algorithm/"
    RUTA_DATOS = RUTA_ORIGEN + "LILITH/Datos Preprocesados"

    NARANJA_FONDO =  (228, 200, 161)
    NARANJA_CLARO =  (252, 237, 218)
    NARANJA_OSCURO = (224, 86, 47)

    AZUL_FONDO =  (65, 183, 197)
    AZUL_CLARO =  (177, 216, 215)
    AZUL_OSCURO = (101, 77, 113)

    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    GRIS = (220, 220, 220)

    ANCHO = 1100
    ALTO = 800
    TAM_CASILLA = 75
    FILAS = COLUMNAS = 8

    pygame.mixer.init()
    SONIDO_MOVER = pygame.mixer.Sound(RUTA_ORIGEN + "source/movimiento.mp3")
    SONIDO_NOTA  = pygame.mixer.Sound(RUTA_ORIGEN + "source/nota.mp3")

    # Función para mostrar texto en la pantalla
    def mostrar_texto(ventana, texto, x, y, color=BLANCO, tamano=30, centrar=False, font="JetBrainsMono.ttf"):
        if font is not None:
            font = WindowTools.RUTA_ORIGEN+"source/"+font

        fuente = pygame.font.Font(font, tamano)
        texto_renderizado = fuente.render(texto, True, color)
        if centrar:
            rect = texto_renderizado.get_rect(center=(x, y))
            ventana.blit(texto_renderizado, rect)
        else:
            ventana.blit(texto_renderizado, (x, y))

    # Función para limpiar la ventana
    def limpiar_ventana(ventana):
        nueva_superficie = pygame.Surface(ventana.get_size())  # Crear una nueva superficie del mismo tamaño que la ventana
        nueva_superficie.fill(WindowTools.NEGRO)  # Rellenar la nueva superficie con el color negro
        ventana.blit(nueva_superficie, (0, 0))  # Reemplazar la ventana actual con la nueva superficie

    # Clase para crear botones
    class Boton:
        def __init__(self, texto, x, y, ancho, alto, color, text_color, text_tam, funcion, font="JetBrainsMono.ttf", center_text=True):
            self.texto = texto
            self.x = x
            self.y = y
            self.ancho = ancho
            self.alto = alto
            self.color = color
            self.color_hover = color
            self.funcion = funcion
            self.text_color = text_color
            self.text_tam = text_tam
            self.font = font
            self.center_text = center_text

        def dibujar(self, ventana):
            pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.alto), border_radius=10)
            WindowTools.mostrar_texto(ventana, self.texto, self.x + self.ancho // 2, self.y + self.alto // 2, self.text_color, self.text_tam, centrar=self.center_text, font=self.font)
        
        def hover(self, mouse_pos):
            return self.x < mouse_pos[0] < self.x + self.ancho and self.y < mouse_pos[1] < self.y + self.alto

    class Boton_img:
        def __init__(self, imagen, x, y, ancho, alto, color_fondo, color_borde, funcion):
            self.imagen = imagen
            self.x = x
            self.y = y
            self.ancho = ancho
            self.alto = alto
            self.color_fondo = color_fondo
            self.color_borde = color_borde
            self.funcion = funcion

        def dibujar(self, ventana):
            pygame.draw.rect(ventana, self.color_fondo, (self.x, self.y, self.ancho, self.alto))
            pygame.draw.rect(ventana, self.color_borde, (self.x, self.y, self.ancho, self.alto), 2)
            
            # Cargar la imagen y ajustar su tamaño
            imagen = pygame.image.load(self.imagen)
            imagen = pygame.transform.scale(imagen, (self.ancho, self.alto))

            # Dibujar la imagen en el botón
            ventana.blit(imagen, (self.x, self.y))

        def hover(self, mouse_pos):
            return self.x < mouse_pos[0] < self.x + self.ancho and self.y < mouse_pos[1] < self.y + self.alto


    class CuadroTexto:
        def __init__(self, texto_predeterminado, x, y, ancho, alto, color_fondo, color_borde, color_texto, texto_tam, font="JetBrainsMono.ttf"):
            self.texto_predeterminado = texto_predeterminado
            self.texto_actual = texto_predeterminado
            self.x = x
            self.y = y
            self.ancho = ancho
            self.alto = alto
            self.color_fondo = color_fondo
            self.color_borde = color_borde
            self.color_texto = color_texto
            self.texto_tam = texto_tam
            self.font = font
            self.desplazamiento_y = 0
            self.factor_desplazamiento = 20  # Ajusta este valor según sea necesario

        def dibujar(self, ventana):
            # Dibujar el cuadro de texto
            pygame.draw.rect(ventana, self.color_fondo, (self.x, self.y, self.ancho, self.alto))
            pygame.draw.rect(ventana, self.color_borde, (self.x, self.y, self.ancho, self.alto), 2)

            # Mostrar el texto actual dentro del cuadro de texto
            fuente = pygame.font.Font(WindowTools.RUTA_ORIGEN + "source/" + self.font, self.texto_tam)
            lineas_por_linea = 2
            for i, linea in enumerate(self.texto_actual):
                texto_renderizado = fuente.render(linea, True, self.color_texto)
                linea_y = self.y + 5 + (i // lineas_por_linea) * (self.texto_tam + 5) - self.desplazamiento_y
                if linea_y < self.y + self.alto - self.texto_tam and linea_y > self.y:
                    ventana.blit(texto_renderizado, (self.x + 20 + (i % lineas_por_linea) * (self.ancho // 2), linea_y))

        def dentro(self, mouse_pos):
            # Verificar si la posición del ratón está dentro del cuadro de texto
            return self.x < mouse_pos[0] < self.x + self.ancho and self.y < mouse_pos[1] < self.y + self.alto

        def cambiar_texto(self, nuevo_texto):
            # Cambiar el texto actual del cuadro de texto
            if isinstance(nuevo_texto, str):
                self.texto_actual = [nuevo_texto]
            elif isinstance(nuevo_texto, list):
                self.texto_actual = nuevo_texto
            else:
                raise ValueError("El nuevo texto debe ser una cadena o una lista de cadenas")

            # Si el texto excede el tamaño del cuadro en altura, permitir desplazamiento vertical
            if len(self.texto_actual) * self.texto_tam > self.alto:
                self.desplazamiento_y = len(self.texto_actual) * self.texto_tam - self.alto
            else:
                self.desplazamiento_y = 0





    # Función para salir del juego
    def salir():
        pygame.quit()
        sys.exit()


    # Función de dibujar tablero de juego
    def dibujar_tablero(ventana, tablero, color_blanco, color_negro, color_vista="B", pieza_seleccionada=None):
        for fila in range(WindowTools.FILAS):
            for col in range(WindowTools.COLUMNAS):
                if color_vista == "B": color = color_blanco if (fila + col) % 2 == 0 else color_negro
                else:                  color = color_blanco if (fila + col) % 2 != 0 else color_negro
                pygame.draw.rect(ventana, color, ((col * WindowTools.TAM_CASILLA)+100, (fila * WindowTools.TAM_CASILLA)+100, WindowTools.TAM_CASILLA, WindowTools.TAM_CASILLA))
        
        for pieza in tablero:
            if pieza_seleccionada is not None and pieza_seleccionada == pieza:
                continue
            if not pieza.vivo:
                continue

            x_tablero = pieza.x - 1
            y_tablero = pieza.y - 1
            
            if color_vista == "B": y_tablero = 7 - y_tablero

            # Ajustar coordenadas x e y para centrar las piezas en las casillas
            x_ventana = x_tablero * WindowTools.TAM_CASILLA + 105
            y_ventana = y_tablero * WindowTools.TAM_CASILLA + 105 

            ruta_imagen = WindowTools.RUTA_ORIGEN+"source/piezas/"+pieza.nombre.split('-')[0].lower()+("-negro.png" if pieza.nombre[-1] == "N" else "-blanco.png")

            image = pygame.image.load(ruta_imagen)  
            image = pygame.transform.scale(image, (65, 65)) 

            ventana.blit(image, (x_ventana, y_ventana))
