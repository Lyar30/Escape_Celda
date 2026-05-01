import pygame
import sys
import random
import Constantes


pygame.init()

Ventana = pygame.display.set_mode((Constantes.ANCHO, Constantes.ALTO))
pygame.display.set_caption("Juego Scape")

RELOJ = pygame.time.Clock()  

FUENTE = pygame.font.SysFont("arial", 28)
FUENTE_GRANDE = pygame.font.SysFont("arial", 48)
FUENTE_PEQUENA = pygame.font.SysFont("arial", 22)

# ESTADOS DEL JUEGO
ESTADO_MENU = "Menu"
ESTADO_INSTRUCCIONES = "Instrucciones"
ESTADO_JUGANDO = "Jugando"
ESTADO_PUZZLE1 = "Puzzle1"
ESTADO_PUZZLE2_VER = "Puzzle2_ver"
ESTADO_PUZZLE2_INGRESAR = "Puzzle2_ingresar"
ESTADO_PUZZLE3_VER = "Puzzle3_ver"
ESTADO_PUZZLE3_INGRESAR = "Puzzle3_ingresar"
ESTADO_VICTORIA = "Victoria"
ESTADO_GAME_OVER = "Game_over"

estado = ESTADO_MENU

paredes = [
    pygame.Rect(0, Constantes.ALTURA_SUP, Constantes.ANCHO, 20),
    pygame.Rect(0, Constantes.ALTO - 20, Constantes.ANCHO, 20),
    pygame.Rect(0, 0, 20, Constantes.ALTO),
    pygame.Rect(Constantes.ANCHO - 20, 0, 20, Constantes.ALTO),

    pygame.Rect(250, Constantes.ALTURA_SUP + 20, 20, 250),
    pygame.Rect(250, 290, 20, 330),
    pygame.Rect(500, 150, 20, 530),
    pygame.Rect(700, Constantes.ALTURA_SUP + 20, 20, 190),
    pygame.Rect(700, 350, 20, 330),
]

# Puerta final
puerta = pygame.Rect(920, 290, 40, 120)
puerta_abierta = False

# POLICÍAS
class Policia:
    def __init__(self, x, y, color= Constantes.CELESTE):
        self.rect = pygame.Rect(x, y, 35, 35)
        self.vel = 3
        self.dx = random.choice([-1, 1]) * self.vel
        self.dy = random.choice([-1, 1]) * self.vel
        self.color = color
        self.timer_cambio = random.randint(60, 150)

    def mover(self):
        self.timer_cambio -= 1
        if self.timer_cambio <= 0:
            self.dx = random.choice([-self.vel, 0, self.vel])
            self.dy = random.choice([-self.vel, 0, self.vel])
            while self.dx == 0 and self.dy == 0:
                self.dx = random.choice([-self.vel, 0, self.vel])
                self.dy = random.choice([-self.vel, 0, self.vel])
            self.timer_cambio = random.randint(60, 150)

        x_ant = self.rect.x
        y_ant = self.rect.y

        self.rect.x += self.dx
        colision = False
        for pared in paredes:
            if self.rect.colliderect(pared):
                colision = True
                break
        if colision:
            self.rect.x = x_ant
            self.dx = -self.dx

        self.rect.y += self.dy
        colision = False
        for pared in paredes:
            if self.rect.colliderect(pared):
                colision = True
                break
        if colision:
            self.rect.y = y_ant
            self.dy = -self.dy

    def dibujar(self):
        pygame.draw.rect(Ventana, self.color, self.rect)
        dibujar_texto("P", FUENTE_PEQUENA, Constantes.NEGRO, self.rect.x + 10, self.rect.y + 5)

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.dx = random.choice([-self.vel, self.vel])
        self.dy = random.choice([-self.vel, self.vel])
        self.timer_cambio = random.randint(60, 150)

policia1 = Policia(320, 140)
policia2 = Policia(780, 500, color=(0, 255, 255))
cooldown_golpe = 0

# PROGRESO DE PUZZLES
puzzle1_completo = False
puzzle2_completo = False
puzzle3_completo = False
puzzle2_visto = False
puzzle3_visto = False

mensaje_global = ""
color_mensaje_global = Constantes.BLANCO
timer_mensaje_global = 0

# BOTONES
# Menú principal
btn_jugar = pygame.Rect(Constantes.ANCHO // 2 - 120, 270, 240, 50)
btn_instrucciones = pygame.Rect(Constantes.ANCHO // 2 - 120, 340, 240, 50)
btn_salir = pygame.Rect(Constantes.ANCHO // 2 - 120, 410, 240, 50)
btn_volver_instr = pygame.Rect(Constantes.ANCHO // 2 - 120, 600, 240, 50)
# Barra superior
btn_menu_hud = pygame.Rect(Constantes.ANCHO - 220, 18, 90, 34)
btn_salir_hud = pygame.Rect(Constantes.ANCHO - 115, 18, 90, 34)

# Pantallas finales
btn_reintentar_final = pygame.Rect(Constantes.ANCHO // 2 - 140, 430, 280, 50)
btn_menu_final = pygame.Rect(Constantes.ANCHO // 2 - 140, 495, 280, 50)
btn_salir_final = pygame.Rect(Constantes.ANCHO // 2 - 140, 560, 280, 50)

# FUNCIONES AUXILIARES
def dibujar_texto(texto, fuente, color, x, y, centrado=False):
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect()
    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    Ventana.blit(superficie, rect)


def dibujar_boton(rect, texto, color_fondo, color_texto, hover=False):
    color = tuple(min(c + 30, 255) for c in color_fondo) if hover else color_fondo
    pygame.draw.rect(Ventana, color, rect, border_radius=10)
    pygame.draw.rect(Ventana, Constantes.BLANCO, rect, 2, border_radius=10)
    dibujar_texto(texto, FUENTE_PEQUENA if rect.height < 40 else FUENTE, color_texto, rect.centerx, rect.centery, centrado=True)


def dibujar_corazon(x, y, tam=16, color=(220, 50, 70)):
    pygame.draw.circle(Ventana, color, (x, y), tam // 2)
    pygame.draw.circle(Ventana, color, (x + tam, y), tam // 2)
    puntos = [
        (x - tam, y + 2),
        (x + tam * 2, y + 2),
        (x + tam // 2, y + tam * 2)
    ]
    pygame.draw.polygon(Ventana, color, puntos)


def mostrar_mensaje_temporal(texto, color=Constantes.BLANCO, duracion=150):
    global mensaje_global, color_mensaje_global, timer_mensaje_global
    mensaje_global = texto
    color_mensaje_global = color
    timer_mensaje_global = duracion


def dibujar_barra_superior():
    pygame.draw.rect(Ventana, Constantes.COLOR_SUP, (0, 0, Constantes.ANCHO, Constantes.ALTURA_SUP))
    pygame.draw.line(Ventana, Constantes.BORDE_SUP, (0, Constantes.ALTURA_SUP), (Constantes.ANCHO, Constantes.ALTURA_SUP), 2)

    dibujar_texto("Vidas:", FUENTE_PEQUENA, Constantes.BLANCO, 20, 24)

    for i in range(vidas):
        dibujar_corazon(95 + i * 38, 30, tam=16)

    completados = int(puzzle1_completo) + int(puzzle2_completo) + int(puzzle3_completo)
    dibujar_texto(f"Acertijos Completados: {completados}/3", FUENTE_PEQUENA, Constantes.BLANCO, 270, 24)

    color_p1 = Constantes.VERDE if puzzle1_completo else Constantes.AMARILLO
    dibujar_texto("Pista: Ve a la cama", FUENTE_PEQUENA, color_p1, 510, 24)

    mouse_pos = pygame.mouse.get_pos()
    dibujar_boton(btn_menu_hud, "MENÚ", Constantes.GRIS_OSCURO, Constantes.BLANCO, btn_menu_hud.collidepoint(mouse_pos))
    dibujar_boton(btn_salir_hud, "SALIR", Constantes.ROJO, Constantes.BLANCO, btn_salir_hud.collidepoint(mouse_pos))


def reiniciar_jugador():
    Constantes.jugador.x, Constantes.jugador.y = Constantes.pos_ini_jugador


def iniciar_partida():
    global estado, vidas, puerta_abierta
    global puzzle1_completo, puzzle2_completo, puzzle3_completo
    global puzzle2_visto, puzzle3_visto
    global entrada_p1, mensaje_p1
    global entrada_secuencia, mensaje_p2
    global palancas, indice_palanca, mensaje_p3
    global cooldown_golpe, mensaje_global, timer_mensaje_global

    estado = ESTADO_JUGANDO
    vidas = 3
    puerta_abierta = False

    puzzle1_completo = False
    puzzle2_completo = False
    puzzle3_completo = False
    puzzle2_visto = False
    puzzle3_visto = False

    entrada_p1 = ""
    mensaje_p1 = ""
    entrada_secuencia = []
    mensaje_p2 = ""
    palancas = [0, 0, 0]
    indice_palanca = 0
    mensaje_p3 = ""

    Constantes.jugador.x, Constantes.jugador.y = Constantes.pos_ini_jugador
    policia1.reset(320, 140)
    policia2.reset(780, 500)
    cooldown_golpe = 0

    mensaje_global = ""
    timer_mensaje_global = 0


def perder_vida_y_volver():
    global vidas, estado
    vidas -= 1
    reiniciar_jugador()
    if vidas <= 0:
        estado = ESTADO_GAME_OVER
        return True
    estado = ESTADO_JUGANDO
    return False


def volver_al_menu():
    global estado, mensaje_global, timer_mensaje_global
    estado = ESTADO_MENU
    mensaje_global = ""
    timer_mensaje_global = 0


def reiniciar_juego():
    volver_al_menu()
    iniciar_partida()
    volver_al_menu()

# MENÚ E INSTRUCCIONES
def dibujar_menu():
    Ventana.fill(Constantes.NEGRO)
    dibujar_texto("ESCAPE FROM PRISON", FUENTE_GRANDE, Constantes.BLANCO, Constantes.ANCHO // 2, 170, True)

    mouse_pos = pygame.mouse.get_pos()
    dibujar_boton(btn_jugar, "JUGAR", Constantes.AZUL, Constantes.BLANCO, btn_jugar.collidepoint(mouse_pos))
    dibujar_boton(btn_instrucciones, "INSTRUCCIONES", Constantes.GRIS_OSCURO, Constantes.BLANCO, btn_instrucciones.collidepoint(mouse_pos))
    dibujar_boton(btn_salir, "SALIR", Constantes.ROJO, Constantes.BLANCO, btn_salir.collidepoint(mouse_pos))

    dibujar_texto("(También puedes usar ESC para salir)", FUENTE_PEQUENA, Constantes.GRIS, Constantes.ANCHO // 2, 490, True)


def dibujar_instrucciones():
    Ventana.fill(Constantes.GRIS_OSCURO)
    dibujar_texto("INSTRUCCIONES", FUENTE_GRANDE, Constantes.NARANJA, Constantes.ANCHO // 2, 80, True)

    lineas = [
        " 1. Muévete con las flechas o con  W-A-S-D",
        " 2. Presiona E cerca de un objeto para interactuar con el",
        " 3. Resuelve los acertijos",
        " 4. Debes revisar en la cama primero ",
        " 5. Resuelve los 3 acertijos para escapar",
        " 6. Evita a los policías o perderás una vida",
        " 7. Respuesta incorrecta = pierdes una vida",
    ]
    for i, linea in enumerate(lineas):
        dibujar_texto(linea, FUENTE_PEQUENA, Constantes.BLANCO, 80, 180 + i * 40)
    mouse_pos = pygame.mouse.get_pos()
    dibujar_boton(
        btn_volver_instr,
        "Volver al menú",
        Constantes.AZUL,
        Constantes.BLANCO,
        btn_volver_instr.collidepoint(mouse_pos)
    )

# JUEGO PRINCIPAL

def dibujar_mapa():
    Ventana.fill((30, 30, 40))
    pygame.draw.rect(
        Ventana,
        (45, 45, 55),
        (20, Constantes.ALTURA_SUP + 20, Constantes.ANCHO - 40, Constantes.ALTO - Constantes.ALTURA_SUP - 40)
    )

    for pared in paredes:
        pygame.draw.rect(Ventana, Constantes.GRIS, pared)

    # Cama - Puzzle 1
    color_cam = Constantes.GRIS if puzzle1_completo else Constantes.MAGENTA
    pygame.draw.rect(Ventana, color_cam, Constantes.cama)
    dibujar_texto("CAMA", FUENTE_PEQUENA, Constantes.NEGRO, Constantes.cama.x + 30, Constantes.cama.y + 18)

    # Símbolos - ver secuencia puzzle 2
    color_sim = Constantes.GRIS if puzzle2_visto else Constantes.NARANJA
    pygame.draw.rect(Ventana, color_sim, Constantes.simbolos)
    dibujar_texto("SÍMBOLOS", FUENTE_PEQUENA, Constantes.NEGRO, Constantes.simbolos.x + 5, Constantes.simbolos.y + 18)

    # Teclado - ingresar secuencia puzzle 2
    color_tec = Constantes.GRIS if puzzle2_completo else Constantes.MORADO
    pygame.draw.rect(Ventana, color_tec, Constantes.teclado_obj)
    dibujar_texto("TECLADO", FUENTE_PEQUENA, Constantes.NEGRO, Constantes.teclado_obj.x + 10, Constantes.teclado_obj.y + 18)

    # Manual - ver config puzzle 3
    color_man = Constantes.GRIS if puzzle3_visto else Constantes.VERDE
    pygame.draw.rect(Ventana, color_man, Constantes.manual)
    dibujar_texto("MANUAL", FUENTE_PEQUENA, Constantes.NEGRO, Constantes.manual.x + 15, Constantes.manual.y + 18)

    # Panel - configurar palancas puzzle 3
    color_pan = Constantes.GRIS if puzzle3_completo else Constantes.AZUL
    pygame.draw.rect(Ventana, color_pan, Constantes.panel)
    dibujar_texto("PANEL", FUENTE_PEQUENA, Constantes.NEGRO, Constantes.panel.x + 15, Constantes.panel.y + 22)

    # Puerta
    color_puerta = Constantes.VERDE if puerta_abierta else Constantes.ROJO
    pygame.draw.rect(Ventana, color_puerta, puerta)
    dibujar_texto("SALIDA", FUENTE_PEQUENA, Constantes.BLANCO, puerta.x - 15, puerta.y - 30)


def dibujar_hud():
    dibujar_barra_superior()

    if timer_mensaje_global > 0 and mensaje_global:
        dibujar_texto(mensaje_global, FUENTE, color_mensaje_global, Constantes.ANCHO // 2, Constantes.ALTURA_SUP + 20, True)

def dibujar_juego():
    dibujar_mapa()
    pygame.draw.rect(Ventana, Constantes.AMARILLO, Constantes.jugador)
    policia1.dibujar()
    policia2.dibujar()
    dibujar_hud()

    if Constantes.jugador.colliderect(Constantes.zona_puzzle1) and not puzzle1_completo:
        dibujar_texto("E: Revisar la cama", FUENTE_PEQUENA, Constantes.BLANCO, 60, 220)
    if Constantes.jugador.colliderect(Constantes.zona_p2_ver) and not puzzle2_completo:
        dibujar_texto("E: Ver los símbolos", FUENTE_PEQUENA, Constantes.BLANCO, 270, 180)
    if Constantes.jugador.colliderect(Constantes.zona_p2_ingresar) and puzzle2_visto and not puzzle2_completo:
        dibujar_texto("E: Usar el teclado", FUENTE_PEQUENA, Constantes.BLANCO, 280, 580)
    if Constantes.jugador.colliderect(Constantes.zona_p2_ingresar) and not puzzle2_visto and not puzzle2_completo:
        dibujar_texto("Primero ve a los símbolos", FUENTE_PEQUENA, Constantes.ROJO, 260, 580)
    if Constantes.jugador.colliderect(Constantes.zona_p3_ver) and not puzzle3_completo:
        dibujar_texto("E: Ver el manual", FUENTE_PEQUENA, Constantes.BLANCO, 520, 180)
    if Constantes.jugador.colliderect(Constantes.zona_p3_ingresar) and puzzle3_visto and not puzzle3_completo:
        dibujar_texto("E: Usar el panel", FUENTE_PEQUENA, Constantes.BLANCO, 730, 230)
    if Constantes.jugador.colliderect(Constantes.zona_p3_ingresar) and not puzzle3_visto and not puzzle3_completo:
        dibujar_texto("Primero ve al manual", FUENTE_PEQUENA, Constantes.ROJO, 710, 230)

    if puerta_abierta:
        dibujar_texto("Puerta abierta. ¡Corre!", FUENTE, Constantes.VERDE, Constantes.ANCHO // 2, Constantes.ALTURA_SUP + 50, True)


def mover_jugador(teclas):
    x_anterior = Constantes.jugador.x
    y_anterior = Constantes.jugador.y

    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        Constantes.jugador.x -= Constantes.vel_jugador
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        Constantes.jugador.x += Constantes.vel_jugador
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
       Constantes.jugador.y -= Constantes.vel_jugador
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        Constantes.jugador.y += Constantes.vel_jugador

    for pared in paredes:
        if Constantes.jugador.colliderect(pared):
            Constantes.jugador.x = x_anterior
            Constantes.jugador.y = y_anterior
            break

def verificar_colision_policias():
    global cooldown_golpe
    if cooldown_golpe > 0:
        return
    if Constantes.jugador.colliderect(policia1.rect) or Constantes.jugador.colliderect(policia2.rect):
        mostrar_mensaje_temporal("¡Cuidado! Un policía te atrapó. Pierdes una vida.", Constantes.ROJO, 140)
        perder_vida_y_volver()
        cooldown_golpe = 90


def verificar_puerta():
    global puerta_abierta
    if puzzle1_completo and puzzle2_completo and puzzle3_completo:
        puerta_abierta = True

def verificar_victoria():
    global estado
    if puerta_abierta and Constantes.jugador.colliderect(puerta):
        estado = ESTADO_VICTORIA


# PUZZLE 1

def dibujar_puzzle1():
    Ventana.fill((20, 20, 50))
    dibujar_texto("CÓDIGO NUMÉRICO", FUENTE_GRANDE, Constantes.BLANCO, Constantes.ANCHO // 2, 120, True)
    dibujar_texto("Encontraste una nota escondida en la cama.", FUENTE, Constantes.BLANCO, Constantes.ANCHO // 2, 220, True)
    dibujar_texto(f"Resuelve la operación: {Constantes.pregunta_p1}", FUENTE, Constantes.AMARILLO, Constantes.ANCHO // 2, 290, True)
    dibujar_texto(f"Tu respuesta es: {entrada_p1}", FUENTE, Constantes.BLANCO, Constantes.ANCHO // 2, 360, True)
    dibujar_texto("Escribe el resultado y presiona ENTER", FUENTE_PEQUENA, Constantes.GRIS, Constantes.ANCHO // 2, 430, True)
    dibujar_texto("ESC para volver", FUENTE_PEQUENA, Constantes.BLANCO, Constantes.ANCHO // 2, 470, True)


def manejar_puzzle1(evento):
    global entrada_p1, mensaje_p1, puzzle1_completo, estado

    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
            estado = ESTADO_JUGANDO

        elif evento.key == pygame.K_RETURN:
            if entrada_p1 == Constantes.respuesta_p1:
                puzzle1_completo = True
                mostrar_mensaje_temporal("Resuelto correctamente.", Constantes.VERDE, 140)
                estado = ESTADO_JUGANDO
            else:
                entrada_p1 = ""
                mostrar_mensaje_temporal("Incorrecto. Pierdes una vida.", Constantes.ROJO, 160)
                perder_vida_y_volver()

        elif evento.key == pygame.K_BACKSPACE:
            entrada_p1 = entrada_p1[:-1]
        else:
            if evento.unicode.isdigit():
                entrada_p1 += evento.unicode


# PUZZLE 2
def dibujar_puzzle2_ver():
    Ventana.fill((20, 50, 20))
    dibujar_texto("SÍMBOLOS EN LA PARED", FUENTE_GRANDE, Constantes.BLANCO, Constantes.ANCHO // 2, 100, True)
    dibujar_texto("Hay símbolos grabados con una secuencia.", FUENTE, Constantes.BLANCO, Constantes.ANCHO // 2, 200, True)
    dibujar_texto("¡MEMORÍZALA!", FUENTE, Constantes.AMARILLO, Constantes.ANCHO // 2, 260, True)

    colores_teclas = [Constantes.AZUL, Constantes.VERDE, Constantes.ROJO, Constantes.MORADO]
    teclas_display = ["A", "D", "W", "S"]
    for i, (t, c) in enumerate(zip(teclas_display, colores_teclas)):
        x = 200 + i * 160
        pygame.draw.rect(Ventana, c, (x, 320, 100, 100), border_radius=12)
        pygame.draw.rect(Ventana, Constantes.BLANCO, (x, 320, 100, 100), 3, border_radius=12)
        dibujar_texto(t, FUENTE_GRANDE, Constantes.BLANCO, x + 50, 370, centrado=True)

    dibujar_texto("Ahora ve a teclado a ingresarla", FUENTE, Constantes.AMARILLO, Constantes.ANCHO // 2, 520, True)
    dibujar_texto("ESC para volver al mapa", FUENTE_PEQUENA, Constantes.BLANCO, Constantes.ANCHO // 2, 580, True)

def manejar_puzzle2_ver(evento):
    global estado, puzzle2_visto
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
            puzzle2_visto = True
            estado = ESTADO_JUGANDO


def dibujar_puzzle2_ingresar():
    Ventana.fill((10, 30, 10))
    dibujar_texto("TECLADO DE SEGURIDAD", FUENTE_GRANDE, Constantes.BLANCO, Constantes.ANCHO // 2, 100, True)
    dibujar_texto("Ingresa la secuencia que viste en los símbolos.", FUENTE, Constantes.BLANCO, Constantes.ANCHO // 2, 190, True)
    dibujar_texto("ESC para volver", FUENTE_PEQUENA, Constantes.BLANCO, Constantes.ANCHO // 2, 280, True)

    for i, t in enumerate(entrada_secuencia):
        x = 300 + i * 110
        pygame.draw.rect(Ventana, Constantes.AZUL, (x, 340, 80, 80), border_radius=10)
        pygame.draw.rect(Ventana, Constantes.BLANCO, (x, 340, 80, 80), 2, border_radius=10)
        dibujar_texto(t, FUENTE_GRANDE, Constantes.BLANCO, x + 40, 380, centrado=True)

    for i in range(len(entrada_secuencia), 4):
        x = 300 + i * 110
        pygame.draw.rect(Ventana, Constantes.GRIS_OSCURO, (x, 340, 80, 80), border_radius=10)
        pygame.draw.rect(Ventana, Constantes.GRIS, (x, 340, 80, 80), 2, border_radius=10)

    color_msg = Constantes.ROJO if "Incorrecta" in mensaje_p2.lower() or "incorrecto" in mensaje_p2.lower() else Constantes.VERDE
    dibujar_texto(mensaje_p2, FUENTE, color_msg, Constantes.ANCHO // 2, 480, True)


def manejar_puzzle2_ingresar(evento):
    global entrada_secuencia, mensaje_p2, puzzle2_completo, estado

    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
            estado = ESTADO_JUGANDO
            return

        tecla = None
        if evento.key == pygame.K_a:
            tecla = "A"
        elif evento.key == pygame.K_d:
            tecla = "D"
        elif evento.key == pygame.K_w:
            tecla = "W"
        elif evento.key == pygame.K_s:
            tecla = "S"

        if tecla:
            entrada_secuencia.append(tecla)
            esperado = Constantes.secuencia_objetivo[:len(entrada_secuencia)]

            if entrada_secuencia != esperado:
                entrada_secuencia = []
                mostrar_mensaje_temporal("Incorrecto Pierdes una vida.", Constantes.ROJO, 160)
                perder_vida_y_volver()
            elif len(entrada_secuencia) == len(Constantes.secuencia_objetivo):
                puzzle2_completo = True
                mostrar_mensaje_temporal("Resuelto correctamente.", Constantes.VERDE, 140)
                estado = ESTADO_JUGANDO

# PUZZLE 3 
def dibujar_puzzle3_ver():
    Ventana.fill((50, 20, 20))
    dibujar_texto("MANUAL ELÉCTRICO", FUENTE_GRANDE, Constantes.BLANCO, Constantes.ANCHO // 2, 80, True)
    dibujar_texto("Indica la configuración correcta del panel", FUENTE, Constantes.BLANCO, Constantes.ANCHO // 2, 170, True)
    config_nombres = ["ON", "OFF", "ON"]
    config_colores = [Constantes.VERDE, Constantes.ROJO, Constantes.VERDE]
    for i in range(3):
        x = 270 + i * 170
        pygame.draw.rect(Ventana, config_colores[i], (x, 290, 120, 120), border_radius=12)
        pygame.draw.rect(Ventana, Constantes.BLANCO, (x, 290, 120, 120), 3, border_radius=12)
        dibujar_texto(f"Palanca {i+1}", FUENTE_PEQUENA, Constantes.BLANCO, x + 60, 300, centrado=True)
        dibujar_texto(config_nombres[i], FUENTE_GRANDE, Constantes.BLANCO, x + 60, 350, centrado=True)

    dibujar_texto("¡MEMORIZA esta configuración!", FUENTE, Constantes.AMARILLO, Constantes.ANCHO // 2, 460, True)
    dibujar_texto("ESC para volver al mapa", FUENTE_PEQUENA, Constantes.BLANCO, Constantes.ANCHO // 2, 510, True)

def manejar_puzzle3_ver(evento):
    global estado, puzzle3_visto
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
            puzzle3_visto = True
            estado = ESTADO_JUGANDO


def dibujar_puzzle3_ingresar():
    Ventana.fill((30, 10, 10))
    dibujar_texto("PANEL ELÉCTRICO", FUENTE_GRANDE, Constantes.BLANCO, Constantes.ANCHO // 2, 80, True)
    dibujar_texto("Configura las palancas según el manual", FUENTE, Constantes.BLANCO, Constantes.ANCHO // 2, 160, True)
    dibujar_texto("← → para elegir palanca | ESPACIO para cambiar | ENTER para validar", FUENTE_PEQUENA, Constantes.GRIS, Constantes.ANCHO // 2, 210, True)
    dibujar_texto("ESC para volver", FUENTE_PEQUENA, Constantes.BLANCO, Constantes.ANCHO // 2, 245, True)

    for i in range(3):
        x = 270 + i * 170
        y = 310
        color = Constantes.VERDE if palancas[i] == 1 else Constantes.ROJO
        pygame.draw.rect(Ventana, color, (x, y, 120, 120), border_radius=12)
        pygame.draw.rect(Ventana, Constantes.BLANCO, (x, y, 120, 120), 3, border_radius=12)

        texto = "ON" if palancas[i] == 1 else "OFF"
        dibujar_texto(f"Palanca {i+1}", FUENTE_PEQUENA, Constantes.BLANCO, x + 60, y + 15, centrado=True)
        dibujar_texto(texto, FUENTE_GRANDE, Constantes.BLANCO, x + 60, y + 60, centrado=True)

        if i == indice_palanca:
            pygame.draw.rect(Ventana, Constantes.AMARILLO, (x - 6, y - 6, 132, 132), 3, border_radius=14)

    color_msg = Constantes.ROJO if "incorrecta" in mensaje_p3.lower() or "incorrecto" in mensaje_p3.lower() else Constantes.VERDE
    dibujar_texto(mensaje_p3, FUENTE, color_msg, Constantes.ANCHO // 2, 490, True)

def manejar_puzzle3_ingresar(evento):
    global indice_palanca, palancas, mensaje_p3, puzzle3_completo, estado

    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
            estado = ESTADO_JUGANDO
        elif evento.key == pygame.K_LEFT:
            indice_palanca = max(0, indice_palanca - 1)
        elif evento.key == pygame.K_RIGHT:
            indice_palanca = min(2, indice_palanca + 1)
        elif evento.key == pygame.K_SPACE:
            palancas[indice_palanca] = 1 - palancas[indice_palanca]
        elif evento.key == pygame.K_RETURN:
            if palancas == Constantes.palancas_objetivo:
                puzzle3_completo = True
                mensaje_p3 = "Puerta desbloqueada."
                mostrar_mensaje_temporal("Resuelto correctamente.", Constantes.VERDE, 140)
                estado = ESTADO_JUGANDO
            else:
                mensaje_p3 = "Incorrecto"
                palancas[:] = [0, 0, 0]
                indice_palanca = 0
                mostrar_mensaje_temporal("Incorrecto. Pierdes una vida.", Constantes.ROJO, 160)
                perder_vida_y_volver()


def dibujar_victoria():
    Ventana.fill((20, 80, 20))
    dibujar_texto("HAS ESCAPADO", FUENTE_GRANDE, Constantes.AMARILLO, Constantes.ANCHO // 2, 180, True)
    dibujar_texto("Lograste salir de la celda y escapar de la prisión.", FUENTE, Constantes.BLANCO, Constantes.ANCHO // 2, 260, True)

    mouse_pos = pygame.mouse.get_pos()
    dibujar_boton(btn_reintentar_final, "JUGAR DE NUEVO", Constantes.AZUL, Constantes.BLANCO, btn_reintentar_final.collidepoint(mouse_pos))
    dibujar_boton(btn_menu_final, "VOLVER AL MENÚ", Constantes.GRIS_OSCURO, Constantes.BLANCO, btn_menu_final.collidepoint(mouse_pos))
    dibujar_boton(btn_salir_final, "SALIR", Constantes.ROJO, Constantes.BLANCO, btn_salir_final.collidepoint(mouse_pos))

def dibujar_game_over():
    Ventana.fill((60, 0, 0))
    dibujar_texto("TE HAN ATRAPADO", FUENTE_GRANDE, Constantes.BLANCO, Constantes.ANCHO // 2, 180, True)
    dibujar_texto("Los policías impidieron tu escape.", FUENTE, Constantes.BLANCO, Constantes.ANCHO // 2, 260, True)

    mouse_pos = pygame.mouse.get_pos()
    dibujar_boton(btn_reintentar_final, "JUGAR DE NUEVO", Constantes.AZUL, Constantes.BLANCO, btn_reintentar_final.collidepoint(mouse_pos))
    dibujar_boton(btn_menu_final, "VOLVER AL MENÚ", Constantes.GRIS_OSCURO, Constantes.BLANCO, btn_menu_final.collidepoint(mouse_pos))
    dibujar_boton(btn_salir_final, "SALIR", Constantes.ROJO, Constantes.BLANCO, btn_salir_final.collidepoint(mouse_pos))


# BUCLE PRINCIPAL
ejecutando = True

while ejecutando:
    RELOJ.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if estado == ESTADO_MENU:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    iniciar_partida()
                elif evento.key == pygame.K_i:
                    estado = ESTADO_INSTRUCCIONES
                elif evento.key == pygame.K_ESCAPE:
                    ejecutando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if btn_jugar.collidepoint(pos):
                    iniciar_partida()
                elif btn_instrucciones.collidepoint(pos):
                    estado = ESTADO_INSTRUCCIONES
                elif btn_salir.collidepoint(pos):
                    ejecutando = False

        elif estado == ESTADO_INSTRUCCIONES:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos

                if btn_volver_instr.collidepoint(pos):
                    estado = ESTADO_MENU
        elif estado == ESTADO_JUGANDO:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if btn_menu_hud.collidepoint(pos):
                    volver_al_menu()
                elif btn_salir_hud.collidepoint(pos):
                    ejecutando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
                if Constantes.jugador.colliderect(Constantes.zona_puzzle1) and not puzzle1_completo:
                    estado = ESTADO_PUZZLE1
                elif Constantes.jugador.colliderect(Constantes.zona_p2_ver) and not puzzle2_completo:
                    estado = ESTADO_PUZZLE2_VER
                elif Constantes.jugador.colliderect(Constantes.zona_p2_ingresar) and puzzle2_visto and not puzzle2_completo:
                    entrada_secuencia = []
                    mensaje_p2 = ""
                    estado = ESTADO_PUZZLE2_INGRESAR
                elif Constantes.jugador.colliderect(Constantes.zona_p3_ver) and not puzzle3_completo:
                    estado = ESTADO_PUZZLE3_VER
                elif Constantes.jugador.colliderect(Constantes.zona_p3_ingresar) and puzzle3_visto and not puzzle3_completo:
                    palancas[:] = [0, 0, 0]
                    indice_palanca = 0
                    mensaje_p3 = ""
                    estado = ESTADO_PUZZLE3_INGRESAR
        elif estado == ESTADO_PUZZLE1:
            manejar_puzzle1(evento)

        elif estado == ESTADO_PUZZLE2_VER:
            manejar_puzzle2_ver(evento)

        elif estado == ESTADO_PUZZLE2_INGRESAR:
            manejar_puzzle2_ingresar(evento)

        elif estado == ESTADO_PUZZLE3_VER:
            manejar_puzzle3_ver(evento)

        elif estado == ESTADO_PUZZLE3_INGRESAR:
            manejar_puzzle3_ingresar(evento)
        elif estado == ESTADO_VICTORIA:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if btn_reintentar_final.collidepoint(pos):
                    iniciar_partida()
                elif btn_menu_final.collidepoint(pos):
                    volver_al_menu()
                elif btn_salir_final.collidepoint(pos):
                    ejecutando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    iniciar_partida()
                elif evento.key == pygame.K_m:
                    volver_al_menu()
                elif evento.key == pygame.K_ESCAPE:
                    ejecutando = False

        elif estado == ESTADO_GAME_OVER:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if btn_reintentar_final.collidepoint(pos):
                    iniciar_partida()
                elif btn_menu_final.collidepoint(pos):
                    volver_al_menu()
                elif btn_salir_final.collidepoint(pos):
                    ejecutando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    iniciar_partida()
                elif evento.key == pygame.K_m:
                    volver_al_menu()
                elif evento.key == pygame.K_ESCAPE:
                    ejecutando = False

    if estado == ESTADO_JUGANDO:
        teclas = pygame.key.get_pressed()
        mover_jugador(teclas)
        policia1.mover()
        policia2.mover()
        verificar_colision_policias()
        verificar_puerta()
        verificar_victoria()

    if timer_mensaje_global > 0:
        timer_mensaje_global -= 1
        if timer_mensaje_global == 0:
            mensaje_global = ""

    if cooldown_golpe > 0:
        cooldown_golpe -= 1

    if estado == ESTADO_MENU:
        dibujar_menu()
    elif estado == ESTADO_INSTRUCCIONES:
        dibujar_instrucciones()
    elif estado == ESTADO_JUGANDO:
        dibujar_juego()
    elif estado == ESTADO_PUZZLE1:
        dibujar_puzzle1()
    elif estado == ESTADO_PUZZLE2_VER:
        dibujar_puzzle2_ver()
    elif estado == ESTADO_PUZZLE2_INGRESAR:
        dibujar_puzzle2_ingresar()
    elif estado == ESTADO_PUZZLE3_VER:
        dibujar_puzzle3_ver()
    elif estado == ESTADO_PUZZLE3_INGRESAR:
        dibujar_puzzle3_ingresar()
    elif estado == ESTADO_VICTORIA:
        dibujar_victoria()
    elif estado == ESTADO_GAME_OVER:
        dibujar_game_over()

    pygame.display.flip()

pygame.quit()
sys.exit()