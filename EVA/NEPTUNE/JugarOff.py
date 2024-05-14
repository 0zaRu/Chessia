from WindowTools import WindowTools as W
from ADAM.Partida import Partida
import Menu
import pygame

global coronando, pieza, jugada_promocion, alertas, finalizado, jugadas
alertas = W.CuadroTexto("", 750, 40, 300, 40, W.NARANJA_FONDO, W.NARANJA_FONDO, W.NARANJA_OSCURO, 14)
coronando = finalizado = False
pieza = jugada_promocion = ""
jugadas = []

def nueva_partida():
    global finalizado, alertas, jugadas
    finalizado = False
    alertas.cambiar_texto("")
    jugadas = []
    return Partida()

def rendicion(partida):
    interpreta_resultado(partida, 2 if partida.mueveBlancas else 1, "0-1" if partida.mueveBlancas else "1-0")

def nuevo_movimiento(partida, color="B"):
    partida.mueveBlancas = True if color == "B" else False
    
    if partida.al_paso_activo is not None and color == partida.al_paso_activo.color: 
        partida.al_paso_activo = None
    
    if color == "B":
        partida.turno +=1

def interpreta_resultado(partida, resultado, jugada):
    global alertas, finalizado, jugadas
    if resultado == 0: 
        W.SONIDO_MOVER.play(maxtime=2000)
        alertas.cambiar_texto("")
        nuevo_movimiento(partida, "B" if partida.mueveBlancas == False else "N")
        
        jugadas.append(jugada)
        return

    elif resultado in [1, 2, 3]:
        finalizado = True
        alertas.cambiar_texto("VICTORIA DE LAS BLANCAS" if resultado == 1 else(" VICTORIA DE LAS NEGRAS" if resultado == 2 else   "      TABLAS       "))
        jugada += "+"
        jugadas.append(jugada)
        jugadas.append(jugadas.append("1-0" if resultado == 1 else ("0-1" if resultado == 2 else "1/2-1/2")))
    
    elif resultado in [4, 5]:
        alertas.cambiar_texto("JAQUE AL REY "+("BLANCO" if resultado == 4 else "NEGRO"))
        jugada += "+"
        jugadas.append(jugada)

        nuevo_movimiento(partida, "B" if partida.mueveBlancas == False else "N")
    
    elif resultado == -1:  alertas.cambiar_texto("Error, sintaxis no válida ...")
    elif resultado == -2:  alertas.cambiar_texto("Error, fallo intentando promocionar...")
    elif resultado == -3:  alertas.cambiar_texto("Error en comida de peón")
    elif resultado == -4:  alertas.cambiar_texto("Error, no hay un peón viable ...")
    elif resultado == -5:  alertas.cambiar_texto("Error, fallo en relación al destino ...")
    elif resultado == -6:  alertas.cambiar_texto("Error, no se ha encontrado pieza viable ...")
    elif resultado == -7:  alertas.cambiar_texto("Excepción actualizando la pieza ...")
    elif resultado == -8:  alertas.cambiar_texto("Error, pieza o jaque interfiriendo...")
    elif resultado == -9:  alertas.cambiar_texto("Error, estás en jaque ...")
    elif resultado == -10: alertas.cambiar_texto("Error, jugada depromoción no válida ...")
    elif resultado == -11: alertas.cambiar_texto("Error, no hay torre o rey ...")
    elif resultado == -12: alertas.cambiar_texto("Error, no puedes comer al Rey ...")
    else: alertas.cambiar_texto("¿?¿?¿?¿?")
    W.SONIDO_NOTA.play()

def select_pieza_promo(partida, pieza_select):
    global coronando, pieza, jugada_promocion
    pieza = pieza_select

    interpreta_resultado(partida, partida.ejecutar_jugada(jugada_promocion+'='+pieza_select), jugada_promocion+'='+pieza_select)
    
    jugada_promocion = ""
    coronando = False

def comprobar_click_sobre_pieza(partida, mouse_pos):
    # Comprobar si se ha hecho clic en una pieza
    for pieza in partida.tablero:
        x, y = (pieza.x - 1) * W.TAM_CASILLA + 105, (8 - pieza.y) * W.TAM_CASILLA + 105
        if x <= mouse_pos[0] <= x + W.TAM_CASILLA and y <= mouse_pos[1] <= y + W.TAM_CASILLA:
            pieza_seleccionada = pieza
            offset_x = mouse_pos[0] - x -43
            offset_y = mouse_pos[1] - y -41
            return pieza_seleccionada, [offset_x, offset_y]

def seguimiento_pieza(ventana, mouse_pos, pieza_seleccionada, offset):
    # Verificar si el mouse está dentro de los límites del tablero
    if 80 <= mouse_pos[0] <= W.TAM_CASILLA*8+100 and 80 <= mouse_pos[1] <= W.TAM_CASILLA*8+100:
        ruta_imagen = W.RUTA_ORIGEN+"source/piezas/"+pieza_seleccionada.nombre.split('-')[0].lower()+("-negro.png" if pieza_seleccionada.nombre[-1] == "N" else "-blanco.png")
        image = pygame.image.load(ruta_imagen)  
        image = pygame.transform.scale(image, (65, 65)) 

        ventana.blit(image, (mouse_pos[0] - offset[0] -43, mouse_pos[1] - offset[1] -41))

def soltar_pieza(partida, mouse_pos, pieza_seleccionada, offset):
    # Determinar la casilla de destino
    nueva_x = (mouse_pos[0] - offset[0] - 105) // W.TAM_CASILLA + 1
    nueva_y = 8 - ((mouse_pos[1] - offset[1] - 105) // W.TAM_CASILLA)
    
    if pieza_seleccionada.x == nueva_x and pieza_seleccionada.y == nueva_y: return

    jugada = ""

    pieza_a_comer = next((ppieza for ppieza in partida.tablero if ppieza.x == nueva_x and ppieza.y == nueva_y), None)

    if "Rey" in pieza_seleccionada.nombre and pieza_seleccionada.x == 5 and nueva_x in [3, 7]:
        if nueva_x == 3:
            jugada = "O-O-O"
        else:
            jugada = "O-O"
        
        interpreta_resultado(partida, partida.ejecutar_jugada(jugada), jugada)

    elif "Peon" not in pieza_seleccionada.nombre:
        jugada = pieza_seleccionada.nombre[0]
        
        if pieza_a_comer is not None:
            jugada += "x"
        
        jugada += chr(ord('a')+nueva_x-1)
        jugada += str(nueva_y)

        resultado = partida.ejecutar_jugada(jugada)
        if resultado in [-6, -1]:
            jugada = jugada[0] + chr(ord('a')+pieza_seleccionada.x-1) + jugada[1:]
            resultado = partida.ejecutar_jugada(jugada)

            if resultado in [-6, -1]:
                jugada = jugada[0] + str(pieza_seleccionada.y) + jugada[1:]
                resultado = partida.ejecutar_jugada(jugada)
            
            interpreta_resultado(partida, resultado, jugada)
        
        else:
            interpreta_resultado(partida, resultado, jugada)

    else:
        if pieza_a_comer is not None \
        or (partida.al_paso_activo is not None \
            and partida.al_paso_activo.x == nueva_x \
            and abs(partida.al_paso_activo.y - nueva_y) == 1 \
            and abs(pieza_seleccionada.x - nueva_x) == 1):
            
            jugada = chr(ord('a')+pieza_seleccionada.x-1) + "x"
        
        jugada += chr(ord('a')+nueva_x-1) + str(nueva_y)
        resultado = partida.ejecutar_jugada(jugada)
        
        if resultado == -1 and nueva_y in [1, 8]:
            global coronando, jugada_promocion
            coronando = True

            jugada_promocion += jugada
        else:
            interpreta_resultado(partida, resultado, jugada)


'''Función para iniciar el juego'''
def dibujar(ventana):
    W.limpiar_ventana(ventana)
    global coronando, finalizado, alertas, jugadas

    partida = Partida()
    finalizado = False

    pieza_seleccionada = None

    # Cargar imagen del logo
    menu_icon = pygame.image.load(W.RUTA_ORIGEN+"source/ADAM icon.png")  
    pygame.display.set_icon(menu_icon)
    pygame.display.set_caption("Juego offline")
    
    volver_boton = W.Boton("←", 10, 10, 40, 40, W.NARANJA_OSCURO, W.NARANJA_CLARO, 40, Menu.dibujar)
    rendirse_boton =       W.Boton("Rendirse",           750, 130, 300, 80, W.NEGRO, W.BLANCO, 21, rendicion)
    nueva_partida_btn =    W.Boton("Nueva partida",      750, 230, 300, 80, W.NEGRO, W.BLANCO, 21, nueva_partida)
    cuadro_jugadas =       W.CuadroTexto("",             750, 355, 300, 345,W.NARANJA_CLARO, W.NARANJA_OSCURO, W.NARANJA_OSCURO, 18)
    salir_boton =          W.Boton("Salir",              900, 750, 180, 40, W.NEGRO, W.BLANCO, 21, W.salir)
    config_boton =         W.Boton("Config",             943, 630, 107, 40, W.NEGRO, W.BLANCO, 21, W.salir)
    text_botonB =          W.Boton("Turno Blanco",        33, 670, 540, 80, W.NARANJA_FONDO, W.NEGRO, 26, W.salir, center_text=False)
    text_botonN =          W.Boton("Turno Negro",        162,  17, 300, 80, W.NARANJA_FONDO, W.NEGRO, 26, W.salir, center_text=False)

    menu_seleccion =   W.CuadroTexto("", 205, 335, 375, 120, W.NARANJA_CLARO, W.NARANJA_OSCURO, W.NARANJA_OSCURO, 18)
    menu_seleccion.cambiar_texto(" SELECCIONA UNA PARA PROMOCIONAR")
    dama_boton =       W.Boton_img(W.RUTA_ORIGEN + "source/piezas/dama-blanco.png",    253, 370, 68, 68, W.NARANJA_CLARO, W.NARANJA_OSCURO, select_pieza_promo)
    caballo_boton =    W.Boton_img(W.RUTA_ORIGEN + "source/piezas/caballo-blanco.png", 328, 370, 68, 68, W.NARANJA_CLARO, W.NARANJA_OSCURO, select_pieza_promo)
    alfil_boton =      W.Boton_img(W.RUTA_ORIGEN + "source/piezas/alfil-blanco.png",   403, 370, 68, 68, W.NARANJA_CLARO, W.NARANJA_OSCURO, select_pieza_promo)
    torre_boton =      W.Boton_img(W.RUTA_ORIGEN + "source/piezas/torre-blanco.png",   478, 370, 68, 68, W.NARANJA_CLARO, W.NARANJA_OSCURO, select_pieza_promo)

    while True:
        ventana.fill(W.NARANJA_FONDO)
        volver_boton.dibujar(ventana)
        rendirse_boton.dibujar(ventana)
        nueva_partida_btn.dibujar(ventana)
        alertas.dibujar(ventana)
        salir_boton.dibujar(ventana)
        cuadro_jugadas.dibujar(ventana)
        cuadro_jugadas.cambiar_texto(jugadas)
        
        if partida.mueveBlancas:
            text_botonB.dibujar(ventana)
        else:
            text_botonN.dibujar(ventana)
        
        mouse_pos = pygame.mouse.get_pos()

        W.dibujar_tablero(ventana, partida.tablero, W.NARANJA_CLARO, W.NARANJA_OSCURO, "B", pieza_seleccionada)
        if coronando:
            menu_seleccion.dibujar(ventana)
            dama_boton.dibujar(ventana)
            caballo_boton.dibujar(ventana)
            alfil_boton.dibujar(ventana)
            torre_boton.dibujar(ventana)

        for evento in pygame.event.get():
            if   evento.type == pygame.QUIT: 
                W.salir()
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if volver_boton.hover(mouse_pos):
                    volver_boton.funcion(ventana)

                elif nueva_partida_btn.hover(mouse_pos):
                    partida = nueva_partida_btn.funcion()
                
                elif rendirse_boton.hover(mouse_pos) and not finalizado:
                    rendirse_boton.funcion(partida)
                
                elif salir_boton.hover(mouse_pos):
                    salir_boton.funcion()
                
                elif dama_boton.hover(mouse_pos):
                    dama_boton.funcion(partida, "D")                
                elif caballo_boton.hover(mouse_pos):
                    caballo_boton.funcion(partida, "C")
                elif alfil_boton.hover(mouse_pos):
                    alfil_boton.funcion(partida, "A")
                elif torre_boton.hover(mouse_pos):
                    torre_boton.funcion(partida, "T")
                    
                elif pieza_seleccionada is None and not finalizado:
                    resultado_comprobacion = comprobar_click_sobre_pieza(partida, mouse_pos)
                    if resultado_comprobacion is not None:
                        pieza_seleccionada, offset = resultado_comprobacion

            elif evento.type == pygame.MOUSEBUTTONUP:
                if pieza_seleccionada:
                    soltar_pieza(partida, mouse_pos, pieza_seleccionada, offset)
                    pieza_seleccionada = None
                    offset[0], offset[1] = 0, 0

        # Actualizar la posición de la pieza seleccionada durante el arrastre
        if pieza_seleccionada:
            seguimiento_pieza(ventana, mouse_pos, pieza_seleccionada, offset)

        pygame.display.update()