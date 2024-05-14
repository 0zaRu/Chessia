from WindowTools import WindowTools as W
import Menu
import pygame

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((W.ANCHO, W.ALTO))

Menu.dibujar(ventana)
