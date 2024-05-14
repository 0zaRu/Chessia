from WindowTools import WindowTools as W
import JugarOff as JOff
import JugarIA as JIA
import pygame

def dibujar(ventana):
    W.limpiar_ventana(ventana)

    # Cargar imagen del logo
    menu_icon = pygame.image.load(W.RUTA_ORIGEN+"source/EVA01 icon.png")  
    pygame.display.set_icon(menu_icon)
    pygame.display.set_caption("Menú de Ajedrez")
    
    logo = pygame.image.load(W.RUTA_ORIGEN+"source/logo_Chessia.png")  
    logo = pygame.transform.scale(logo, (540, 540)) 

    perfil_boton =       W.Boton("Perfil",           710, 130, 180, 80, W.NEGRO, W.BLANCO, 21, W.salir)
    friends_boton =      W.Boton("Amigos",           903, 130, 107, 80, W.NEGRO, W.BLANCO, 21, W.salir)
    jugar_solo_boton =   W.Boton("Jugar offline",    710, 255, 300, 80, W.NEGRO, W.BLANCO, 21, JOff.dibujar)
    jugar_ia_boton =     W.Boton("Jugar con LILITH", 710, 380, 300, 80, W.NEGRO, W.BLANCO, 21, JIA.dibujar)
    jugar_online_boton = W.Boton("Jugar online",     710, 505, 300, 80, W.NEGRO, W.BLANCO, 21, W.salir)
    salir_boton =        W.Boton("Salir",            710, 630, 180, 40, W.NEGRO, W.BLANCO, 21, W.salir)
    config_boton =       W.Boton("Config",           903, 630, 107, 40, W.NEGRO, W.BLANCO, 21, W.salir)
    text_boton =         W.Boton("CHESSIA - Chess with AI Python Proyect", 90, 580, 540, 80, W.GRIS, W.NEGRO, 26, W.salir)


    ventana.fill(W.GRIS)
    ventana.blit(logo, (90, 80))
    
    perfil_boton.dibujar(ventana)
    friends_boton.dibujar(ventana)
    jugar_solo_boton.dibujar(ventana)
    jugar_ia_boton.dibujar(ventana)
    jugar_online_boton.dibujar(ventana)
    config_boton.dibujar(ventana)
    salir_boton.dibujar(ventana)
    text_boton.dibujar(ventana)

    while True:    
        

        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            
            if evento.type == pygame.QUIT:
                W.salir()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                
                if perfil_boton.hover(mouse_pos):
                    perfil_boton.funcion()
                elif friends_boton.hover(mouse_pos):
                    friends_boton.funcion()
                elif jugar_solo_boton.hover(mouse_pos):
                    jugar_solo_boton.funcion(ventana)
                elif jugar_ia_boton.hover(mouse_pos):
                    jugar_ia_boton.funcion(ventana)
                elif jugar_online_boton.hover(mouse_pos):
                    jugar_online_boton.funcion()
                elif salir_boton.hover(mouse_pos):
                    salir_boton.funcion()
                elif config_boton.hover(mouse_pos):
                    config_boton.funcion()
                elif text_boton.hover(mouse_pos):
                    text_boton.funcion()

        pygame.display.update()