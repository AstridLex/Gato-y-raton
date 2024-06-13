import pygame
import math

pygame.init()

N = 7
TAM_CELDA = 100
TAM_TABLERO = N * TAM_CELDA
ANCHO, ALTO = TAM_TABLERO, TAM_TABLERO
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('EL GATO Y EL RATON')

#ROJO,VERDE,AZUL
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE_OSCURO= (0,150,0)


imagen_raton = pygame.image.load('raton.png')
imagen_raton = pygame.transform.scale(imagen_raton, (TAM_CELDA, TAM_CELDA))
imagen_gato = pygame.image.load('gato.png')
imagen_gato = pygame.transform.scale(imagen_gato, (TAM_CELDA, TAM_CELDA))
imagen_madriguera = pygame.image.load('madriguera.jpg')
imagen_madriguera = pygame.transform.scale(imagen_madriguera, (TAM_CELDA, TAM_CELDA))

objetivo_raton = (3, 3)

def dibujar_tablero(raton_pos, gato_pos,objetivo_raton):
    VENTANA.fill(VERDE_OSCURO)
    for i in range(N):
        for j in range(N):
            pygame.draw.rect(VENTANA, NEGRO, (j * TAM_CELDA, i * TAM_CELDA, TAM_CELDA, TAM_CELDA), 1)
            if (i, j) == raton_pos:
                VENTANA.blit(imagen_raton, (j * TAM_CELDA, i * TAM_CELDA))
            elif (i, j) == gato_pos:
                VENTANA.blit(imagen_gato, (j * TAM_CELDA, i * TAM_CELDA))
            elif (i, j) == objetivo_raton:
                VENTANA.blit(imagen_madriguera, (j * TAM_CELDA, i * TAM_CELDA))

def raton_gana(pos):
    return pos == objetivo_raton

def gato_gana(raton_pos, gato_pos):
    return raton_pos == gato_pos

def movimientos_validos_raton(pos):
    x, y = pos
    movimientos = [
        (x-1, y), (x+1, y),  # arriba, abajo
        (x, y-1), (x, y+1)   # izquierda, derecha
    ]
    return [(i, j) for i, j in movimientos if 0 <= i < N and 0 <= j < N]

def movimientos_validos_gato(pos):
    x, y = pos
    movimientos = [
        (x-1, y-1), (x-1, y+1),   # 1 celda en diagonal hacia arriba
        (x+1, y-1), (x+1, y+1)    # 1 celda en diagonal hacia abajo
    ]
    return [(i, j) for i, j in movimientos if 0 <= i < N and 0 <= j < N]


def minimax(raton_pos, gato_pos, profundidad, es_maximizador, max_profundidad=5):
    if raton_gana(raton_pos):
        return 1
    if gato_gana(raton_pos, gato_pos):
        return -1
    if profundidad == max_profundidad:
        return 0 

    if es_maximizador:
        mejor_puntaje = -math.inf
        for mov in movimientos_validos_raton(raton_pos):
            puntaje = minimax(mov, gato_pos, profundidad + 1, False, max_profundidad)
            mejor_puntaje = max(puntaje, mejor_puntaje)
        return mejor_puntaje
    else:
        mejor_puntaje = math.inf
        for mov in movimientos_validos_gato(gato_pos):
            puntaje = minimax(raton_pos, mov, profundidad + 1, True, max_profundidad)
            mejor_puntaje = min(puntaje, mejor_puntaje)
        return mejor_puntaje

def encontrar_mejor_jugada_gato(raton_pos, gato_pos, max_profundidad=5):
    mejor_jugada = None
    mejor_puntaje = math.inf
    for mov in movimientos_validos_gato(gato_pos):
        puntaje = minimax(raton_pos, mov, 0, True, max_profundidad)
        if puntaje < mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_jugada = mov
    return mejor_jugada

def mostrar_mensaje(mensaje):
    fuente = pygame.font.SysFont(None, 55)
    texto = fuente.render(mensaje, True, (BLANCO))
    VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000) 

def jugar():
    raton_pos = (0, 0)
    gato_pos = (2, 3)
    turno_raton = True
    corriendo = True

    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

        if turno_raton:
            keys = pygame.key.get_pressed()
            nuevo_pos = raton_pos
            if keys[pygame.K_UP]:
                nuevo_pos = (raton_pos[0] - 1, raton_pos[1])
            elif keys[pygame.K_DOWN]:
                nuevo_pos = (raton_pos[0] + 1, raton_pos[1])
            elif keys[pygame.K_LEFT]:
                nuevo_pos = (raton_pos[0], raton_pos[1] - 1)
            elif keys[pygame.K_RIGHT]:
                nuevo_pos = (raton_pos[0], raton_pos[1] + 1)

            if nuevo_pos in movimientos_validos_raton(raton_pos):
                raton_pos = nuevo_pos
                turno_raton = False

            dibujar_tablero(raton_pos, gato_pos,objetivo_raton)
            pygame.display.update()

            if raton_gana(raton_pos):
                mostrar_mensaje("El ratón ha ganado")
                corriendo = False
                continue
            if gato_gana(raton_pos, gato_pos):
                mostrar_mensaje("El gato atrapó al ratón")
                corriendo = False
                continue

        else:
            pygame.time.delay(500)
            nuevo_gato_pos = encontrar_mejor_jugada_gato(raton_pos, gato_pos, max_profundidad=5)
            if nuevo_gato_pos:
                gato_pos = nuevo_gato_pos
            turno_raton = True

            dibujar_tablero(raton_pos, gato_pos,objetivo_raton)
            pygame.display.update()

            if raton_gana(raton_pos):
                mostrar_mensaje("El ratón ha ganado")
                corriendo = False
                continue
            if gato_gana(raton_pos, gato_pos):
                mostrar_mensaje("El gato atrapó al ratón")
                corriendo = False
                continue
jugar()
pygame.quit()
