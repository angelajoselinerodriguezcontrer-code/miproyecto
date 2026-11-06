import pygame 
import sys
import random

# CONFIGURACIÓN E INICIALIZACIÓN

pygame.init()

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Microproyecto: Estilo Pac-Man con Figuras Simples")

# Reloj para controlar los FPS (Rendimiento)
reloj = pygame.time.Clock()
FPS = 60

# Colores (RGB)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)

# VARIABLES DEL JUEGO

# Jugador (Pac-Man - Círculo)
jugador_x = ANCHO // 2
jugador_y = ALTO // 2
jugador_radio = 20
jugador_velocidad = 5

# Enemigo (Fantasma - Cuadrado)
enemigo_x = 100
enemigo_y = 100
enemigo_tamano = 35
enemigo_velocidad = 3

# Monedas (Puntos - Círculos pequeños)
monedas = []
CANTIDAD_MONEDAS = 10
moneda_radio = 8

# Puntuación y Estado del Juego
puntuacion = 0
juego_terminado = False
fuente =pygame .font.SysFont("Arial", 30)

# FUNCIONES AUXILIARES

def generar_monedas():
    """Genera posiciones aleatorias para las monedas en la pantalla."""
    global monedas
    monedas = []
    for _ in range(CANTIDAD_MONEDAS):
        x = random.randint(50, ANCHO - 50)
        y = random.randint(50, ALTO - 50)
        monedas.append([x, y])

def mover_enemigo():
    """Lógica de IA simple: el enemigo persigue la posición del jugador."""
    global enemigo_x, enemigo_y
    if enemigo_x < jugador_x:
        enemigo_x += enemigo_velocity_ajustada()
    elif enemigo_x > jugador_x:
        enemigo_x -= enemigo_velocity_ajustada()
        
    if enemigo_y < jugador_y:
        enemigo_y += enemigo_velocity_ajustada()
    elif enemigo_y > jugador_y:
        enemigo_y -= enemigo_velocity_ajustada()

def enemigo_velocity_ajustada():
    """Retorna la velocidad del enemigo asegurando que no sobrepase al jugador."""
    return min(enemigo_velocidad, abs(enemigo_x - jugador_x))

def verificar_colisiones():
    """Maneja las colisiones del jugador con las monedas y con el enemigo."""
    global puntuacion, juego_terminado, jugador_x, jugador_y
    
    # 1. Colisión Jugador - Monedas (Distancia matemática entre círculos)
    for moneda in monedas[:]:
        distancia = ((jugador_x - moneda[0])**2 + (jugador_y - moneda[1])**2)**0.5
        if distancia < (jugador_radio + moneda_radio):
            monedas.remove(moneda)
            puntuacion += 10
            
    # Si se acaban las monedas, se genera una nueva ronda
    if len(monedas) == 0:
        generar_monedas()

    # 2. Colisión Jugador - Enemigo (Círculo contra Cuadrado aproximado)
    # Revisa si el centro del jugador entra en el área del cuadrado enemigo
    if (enemigo_x < jugador_x < enemigo_x + enemigo_tamano) and \
       (enemigo_y < jugador_y < enemigo_y + enemigo_tamano):
        juego_terminado = True

# Inicializar primera ronda de monedas
generar_monedas()

# CICLO PRINCIPAL DEL JUEGO (GAME LOOP)

ejecutando = True
while ejecutando:
    
    # --- 1. GESTIÓN DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
    # --- 2. ACTUALIZACIÓN DEL ESTADO ---
    if not juego_terminado:
        # Captura de teclas presionadas para mover al jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador_x - jugador_radio > 0:
            jugador_x -= jugador_velocidad
        if teclas[pygame.K_RIGHT] and jugador_x + jugador_radio < ANCHO:
            jugador_x += jugador_velocidad
        if teclas[pygame.K_UP] and jugador_y - jugador_radio > 0:
            jugador_y -= jugador_velocidad
        if teclas[pygame.K_DOWN] and jugador_y + jugador_radio < ALTO:
            jugador_y += jugador_velocidad

        # Mover Inteligencia Artificial y verificar colisiones
        mover_enemigo()
        verificar_colisiones()

    # --- 3. RENDERIZADO / DIBUJO ---
    pantalla.fill(NEGRO) # Limpiar pantalla con fondo negro

    if not juego_terminado:
        # Dibujar Monedas (Puntos blancos)
        for moneda in monedas:
            pygame.draw.circle(pantalla, BLANCO, (moneda[0], moneda[1]), moneda_radio)

        # Dibujar Jugador (Pac-Man - Círculo Amarillo)
        pygame.draw.circle(pantalla, AMARILLO, (jugador_x, jugador_y), jugador_radio)

        # Dibujar Enemigo (Fantasma - Cuadrado Rojo)
        pygame.draw.rect(pantalla, ROJO, (enemigo_x, enemigo_y, enemigo_tamano, enemigo_tamano))

        # Dibujar Puntuación en pantalla
        texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, AZUL)
        pantalla.blit(texto_puntos, (20, 20))
    else:
        # Pantalla de Game Over
        texto_game_over = fuente.render("¡GAME OVER! El fantasma te atrapó.", True, ROJO)
        texto_reiniciar = fuente.render(f"Puntuación final: {puntuacion} puntos.", True, BLANCO)
        
        # Centrar los textos en pantalla
        pantalla.blit(texto_game_over, (ANCHO // 2 - 200, ALTO // 2 - 50))
        pantalla.blit(texto_reiniciar, (ANCHO // 2 - 150, ALTO // 2 + 10))

    # Actualizar los gráficos en la ventana
    pygame.display.flip()
    
    # Controlar la velocidad del juego
    reloj.tick(FPS)

# Salir de pygame limpiamente
pygame.quit()
sys.exit()