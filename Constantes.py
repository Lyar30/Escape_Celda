import pygame

#MEDIDAS
ANCHO = 1000
ALTO = 700

#COLORES
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (120, 120, 120)
GRIS_OSCURO = (60, 60, 60)
AZUL = (70, 120, 220)
ROJO = (220, 70, 70)
VERDE = (70, 200, 100)
AMARILLO = (240, 220, 80)
MARRON = (120, 80, 50)
CELESTE = (170, 220, 255)
MORADO = (140, 90, 180)
NARANJA = (230, 140, 40)
MAGENTA= (255,0,255)

#BARRA SUPERIOR
ALTURA_SUP = 70
COLOR_SUP = (18, 18, 28)
BORDE_SUP = (70, 90, 110)

#JUGADOR
jugador = pygame.Rect(80, 110, 35, 35)
vel_jugador = 4
pos_ini_jugador = (30, 620)
vidas = 3

# OBJETOS
cama = pygame.Rect(70, 140, 120, 60)         # Puzzle 1
simbolos = pygame.Rect(320, 100, 110, 60)    # Puzzle 2 - VER 
teclado_obj = pygame.Rect(320, 500, 110, 60) # Puzzle 2 - INGRESAR 
manual = pygame.Rect(560, 100, 110, 60)      # Puzzle 3 - VER 
panel = pygame.Rect(780, 140, 90, 70)        # Puzzle 3 - INGRESAR 

# INTERACIÓN ACERTIJOS
zona_puzzle1 = pygame.Rect(80, 150, 80, 40)
zona_p2_ver = pygame.Rect(330, 110, 80, 40)
zona_p2_ingresar = pygame.Rect(330, 510, 80, 40)
zona_p3_ver = pygame.Rect(570, 110, 80, 40)
zona_p3_ingresar = pygame.Rect(790, 150, 70, 50)

# PUZZLE 1 - CÓDIGO NUMÉRICO
pregunta_p1 = "12 + 7 = ?"
respuesta_p1 = "19"
entrada_p1 = ""
mensaje_p1 = ""

# PUZZLE 2 - SECUENCIA
secuencia_objetivo = ["A", "D", "W", "S"]
entrada_secuencia = []
mensaje_p2 = ""

# PUZZLE 3 - PALANCAS
palancas = [0, 0, 0]
palancas_objetivo = [1, 0, 1]
indice_palanca = 0
mensaje_p3 = ""