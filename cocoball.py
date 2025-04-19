import math
import pygame
import random  # Importar para generar posiciones aleatorias
import os
from enum import Enum
import csv

class Action(Enum):
    NONE = "none"
    MOV_LEFT = "mov_left"
    MOV_RIGHT = "mov_right"
    MOV_UP = "mov_up"
    MOV_DOWN = "mov_down"
    FIRE = "fire"

# Inicializar pygame
pygame.init()

# Inicializar el módulo de sonido
pygame.mixer.init()

pygame.joystick.init()

# Directorio de los recursos
image_directory = "imagenes/"
music_directory = "sonido/"
fonts_directory = "fuentes/"


# Cargar efectos de sonido
disparo_sonido = pygame.mixer.Sound("sonido/disparo.wav")  # Sonido de disparo
enemigo_eliminado_sonido = pygame.mixer.Sound("sonido/enemigo_eliminado.wav")  # Sonido al eliminar un enemigo
vida_sonido = pygame.mixer.Sound("sonido/vida.wav")  # Sonido al tocar la canasta
level_up_sonido = pygame.mixer.Sound("sonido/level up.wav")  # Sonido al cambiar de sprite en la ronda 10
daño_jugador_sonido = pygame.mixer.Sound("sonido/daño_jugador.wav")  # Sonido al recibir daño

# Cargar música de fondo
pygame.mixer.music.load("sonido/cocosong.mp3")  # Asegúrate de tener un archivo musica_fondo.mp3 en tu directorio
pygame.mixer.music.set_volume(30)  # Ajustar el volumen de la música al 0%
pygame.mixer.music.play(-1)  # Reproducir la música en bucle (-1 significa infinito)

# Configurar pantalla
WIDTH, HEIGHT = 960, 540  # Dimensiones base de la pantalla
SCREEN_SCALE = 2  # Escala para agrandar la pantalla
REAL_WIDTH, REAL_HEIGHT = WIDTH * SCREEN_SCALE, HEIGHT * SCREEN_SCALE
screen = pygame.Surface((WIDTH, HEIGHT))
screen_real = pygame.display.set_mode((REAL_WIDTH, REAL_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Cocoball, el cocodrilo espacial!")

# Colores
WHITE = (255, 255, 255)
DARK_PURPLE = (48, 25, 52)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)


# Configurar fuente para el contador de rondas
font20 = pygame.font.Font(f"{fonts_directory}/cocoball_fuente.otf", 20)  # Tamaño reducido a 20
font40 = pygame.font.Font(f"{fonts_directory}/cocoball_fuente.otf", 40) 
font50 = pygame.font.Font(f"{fonts_directory}/cocoball_fuente.otf", 50) 


# Cargar recursos desde directorio
def get_resources_from_dir(path, prefix, suffix):
    file_name_list = []
    for file_name in sorted(os.listdir(path)):
        if file_name.startswith(prefix) and file_name.endswith(suffix):
            file_name_list.append(os.path.join(path, file_name))
    return file_name_list

def load_images(file_name_list, scale=(50, 50),rotation=0):
    images = []
    for file_name in file_name_list:
        image = pygame.image.load(file_name)
        scaled_image = pygame.transform.scale(image, scale)  # Escalar al tamaño deseado
        if rotation!=0:
            scaled_image = pygame.transform.rotate(scaled_image, rotation) # Rotar la imagen  
        images.append(scaled_image)
    return images

# *************************************  COCO  *************************************
# Configurar personaje
max_health = 100  # Vida máxima del jugador
player = {
    "x": WIDTH // 2,  # Posición inicial X del jugador
    "y": HEIGHT // 2,  # Posición inicial Y del jugador
    "angle": 0,  # Ángulo inicial del jugador
    "speed": 3,  # Velocidad base del jugador
    "speed_0": 0.05, # Velocidad mínima del jugador
    "vel_x": 0,  # Velocidad en el eje X
    "vel_y": 0,  # Velocidad en el eje Y
    "acceleration": 0.4,  # Aceleración del jugador
    "deceleration": 0.2,  # Desaceleración cuando no hay entrada
    "float_angle": 0,  # Desplazamiento para el efecto de flotación
    "x0_float": 0, # Posición inicial para el efecto de flotación
    "y0_float": 0, # Posición inicial para el efecto de flotación
    "float_radius": 5,  # Radio del efecto de flotación
    "image": None  # Imagen del jugador (se cargará más adelante)
}
# Cargar imagen del personaje
player["image"] =  load_images(get_resources_from_dir(image_directory, "coco_", ".png"), scale=(50, 100),rotation=-90)  # Cargar imágenes del cocodrilo


# *************************************  PELOTA  *************************************
# Configurar personaje-bala
bullet = {
    "x": 0,  # Posición inicial de la bala
    "y": 0,  # Posición inicial de la bala
    "angle": 0,  # Ángulo inicial de la bala
    "is_fired": False,  # Estado de disparo
    "speed": 7,  # Velocidad de la bala
    "image": None,  # Imagen de la bala (se cargará más adelante)
    "last_shot_time": 0,  # Tiempo del último disparo
    "cooldown_time": 1500,  # Tiempo inicial de espera (1.5 segundos)
    "min_cooldown_time": 300  # Tiempo mínimo de espera entre disparos
}
# Cargar imagen de la bala
bullet_image = pygame.image.load(f"{image_directory}/pelota.png")  # Imagen de la bala
bullet_image = pygame.transform.scale(bullet_image, (50, 50))  # Escalar la imagen al tamaño deseado
bullet_image_large = pygame.transform.scale(bullet_image, (70, 70))  # Incrementar el tamaño de la pelota
bullet["image"] = [bullet_image, bullet_image_large]  # Asignar la imagen al diccionario de la bala

# *************************************  POWER UP  *************************************
# Configurar powerup
power_up = {
    "is_active": False,  # Estado de power-up
    "start_time": 0,  # Tiempo de inicio del power-up
    "duration": 10000,  # Duración del power-up en milisegundos (10 segundos)
    "rounds": 0,  # Contador de rondas para el power-up
    "max_rounds": 10, # Número máximo de rondas para llenar la barra 
    "image": None,  # Imagen de la barra de progreso (se cargará más adelante) 
}
# Cargar imágenes de la barra de progreso por rondas
power_up["image"] = load_images(get_resources_from_dir(image_directory, "progreso_", ".png"), scale=(200, 40))  # Cargar imágenes de la barra de progreso


# *************************************  ENEMIGOS ************************************* 
# Configurar enemigos
enemy_template = {
    "change_round":10,  # Cambiar de sprite cada 10 rondas
    "num_base_enemigos": 3, # Número de enemigos al arrancar el juego
    "round_speed_inc": 0.01,  # Incremento de velocidad por ronda
    "base_speed": 2,  # Velocidad base de los enemigos
    "images": [] # Lista para almacenar las imágenes de los enemigos
}
# Cargar imágenes de enemigos desde el directorio
enemy_template["images"] = load_images(get_resources_from_dir(image_directory, "enemigo_", ".png"), scale=(50, 50))  # Cargar imágenes de enemigos

# Función para generar enemigos con velocidad incrementada y enemigos adicionales
def generate_enemies(round_count):
    speed_multiplier = enemy_template["round_speed_inc"] * round_count  # Incremento de velocidad por ronda
    additional_enemies = (round_count+1) // 20  # Un alien adicional cada 20 rondas
    total_enemies = enemy_template["num_base_enemigos"] + additional_enemies  # Total de enemigos a generar
    return [
        {
            "fase": (round_count//enemy_template["change_round"]) if (round_count//enemy_template["change_round"]<len(enemy_template["images"])) else len(enemy_template["images"])-1 , 
            "x": random.randint(50, WIDTH - 50), 
            "y": random.randint(50, HEIGHT - 50), 
            "speed": enemy_template["base_speed"] + speed_multiplier
        }
        for _ in range(total_enemies)
    ]

# Función para mover enemigos hacia el jugador
def move_enemy(enemy, player):
    # Calcular la dirección hacia el jugador
    dx = player["x"] - enemy["x"]
    dy = player["y"] - enemy["y"]
    distance = math.sqrt(dx**2 + dy**2)
    if distance > 0:  # Evitar división por cero
        enemy["x"] += enemy["speed"] * (dx / distance)
        enemy["y"] += enemy["speed"] * (dy / distance)

# *************************************  ESCENAS *************************************
# Lista de fondos con sus características
scene = {
    "change_round":10,  # Cambiar de fondo cada 10 rondas
    "idx_scene":0,  # Índice de la escena actual
    "image": None,  # Lista de imágenes de fondo
    "music": None # Lista de música de fondo
}

# Lista para almacenar las imágenes de fondo
scene["image"] = load_images(get_resources_from_dir(image_directory, "escena_", ".png"), scale=(WIDTH, HEIGHT))  # Cargar imágenes de fondo
scene["music"] = get_resources_from_dir(music_directory, "musica_", ".mp3")  # Cargar música de fondo



# *************************************  EXPLOSIONES *************************************
# Cargar imagen de la explosión
explosion_image = pygame.image.load(f"{image_directory}/explosion.png")  # Imagen de la explosión
explosion_image = pygame.transform.scale(explosion_image, (50, 50))  # Escalar al tamaño deseado

# Lista de explosiones activas
explosions = []

# *************************************  ARO *************************************
# Variables para el aro de básquet
aro = {
    "x": (WIDTH // 2) - 25,  # Centrar el aro horizontalmente (ajustar por el tamaño del sprite)
    "y": (HEIGHT // 2) - 25,  # Centrar el aro verticalmente (ajustar por el tamaño del sprite)
    "visible": True,  # El aro es visible al inicio
    "image": None  # Imagen del aro (se cargará más adelante)
}
aro_image = pygame.image.load(f"{image_directory}/aro.png")  # Asegúrate de tener un archivo aro.png
aro["image"] = pygame.transform.scale(aro_image, (50, 50))  # Escalar al tamaño deseado


# *************************************  BARRA DE VIDA *************************************
# Cargar imágenes de la barra de vida
health_images = load_images(get_resources_from_dir(image_directory, "barra_", ".png"), scale=(200, 80))  # Cargar imágenes de la barra de vida

# Función para obtener la imagen de la barra de vida según la vida actual
def get_health_image(player_health, max_health):
    health_index = (player_health *5 // max_health) 
    return health_images[health_index]


# *************************************  PANTALLA DE INICIO *************************************
# Cargar imagen de inicio
inicio_image = pygame.image.load(f"{image_directory}/fondo_inicio.png")  # Imagen de la pantalla de inicio
inicio_image = pygame.transform.scale(inicio_image, (WIDTH, HEIGHT))  # Escalar al tamaño de la pantalla

def capturar_evento_inicio(joystick):
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True  # Salir de la pantalla de inicio y comenzar el juego
            if event.key == pygame.K_ESCAPE:  # Detectar la tecla Esc
                pygame.quit()
                exit()
        if joystick and event.type == pygame.JOYBUTTONDOWN:
            if joystick.get_button(9):  # Botón "Start" del joystick
                return True  # Salir de la pantalla de inicio y comenzar el juego
            if joystick.get_button(8):  # Botón "Select" del joystick
                pygame.quit()
                exit()
    return False


# Pantalla de inicio
def mostrar_pantalla_inicio(joystick):
    if joystick:
        start_text = "Presiona Start!"
    else:
        start_text = "Presiona Espacio!"
    start_text_render_yellow = font40.render(start_text, True, YELLOW)
    start_text_render_purple = font40.render(start_text, True, DARK_PURPLE)
    x_text = WIDTH // 2 - start_text_render_yellow.get_width() // 2
    y_text = HEIGHT - start_text_render_yellow.get_height() * 2

    tiempo_inicio = pygame.time.get_ticks()
    mostrar_highscores = False  # Alternar entre splash screen y highscores

    while True:
        # Alternar entre splash screen y highscores cada 10 segundos
        tiempo_actual = pygame.time.get_ticks()
        if (tiempo_actual - tiempo_inicio) / 1000 > 10:
            mostrar_highscores = not mostrar_highscores
            tiempo_inicio = tiempo_actual

        # Dibujar la pantalla correspondiente
        if mostrar_highscores:
            # Dibujar la lista de highscores
            screen.fill(BLACK)
            titulo = font50.render("HIGHSCORES", True, WHITE)
            screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))
            y = 150
            for idx, score in enumerate(highscores):
                texto = font20.render(f"{idx+1}. {score['name']} - {score['rounds']} rondas", True, WHITE)
                screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, y))
                y += 30
        else:
            # Dibujar la imagen de inicio
            screen.blit(inicio_image, (0, 0))  # Dibujar la imagen de inicio
            screen.blit(start_text_render_purple, (x_text-5, y_text+2))  # Dibujar el texto de inicio
            screen.blit(start_text_render_yellow, (x_text, y_text))  # Dibujar el texto de inicio

        pygame.transform.scale(screen, (REAL_WIDTH, REAL_HEIGHT), screen_real)
        pygame.display.flip()  # Actualizar la pantalla

        #mostrar_highscore(highscores)
        
        if capturar_evento_inicio(joystick):  # Capturar eventos de teclado o joystick
            return

# *************************************  PANTALLA DE FIN *********************************
def mostrar_pantalla_fin(joystick):
    game_over_text = font50.render("¡Game over!", True, WHITE)
    if joystick:
        restart_text = font20.render("Presiona Start para reiniciar, Select para salir", True, WHITE)
    else:
        restart_text = font20.render("Presiona Espacio para reiniciar, Esc para salir", True, WHITE)

    # Cargar la imagen de fondo para la pantalla de Game Over
    game_over_image = pygame.image.load(f"{image_directory}/fondo_game_over.png")
    game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))  # Escalar al tamaño de la pantalla

    while True:
        # Dibujar la imagen de fondo de Game Over
        screen.blit(game_over_image, (0, 0))

        # Dibujar los textos
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 30))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - restart_text.get_height()*2))

        # Escalar y mostrar en pantalla
        pygame.transform.scale(screen, (REAL_WIDTH, REAL_HEIGHT), screen_real)
        pygame.display.flip()

        # Capturar eventos para reiniciar o salir
        if capturar_evento_inicio(joystick):  # Capturar eventos de teclado o joystick
            return




# ****************************** LOGICA DEL JUEGO ***********************************************

def capturar_eventos_teclado(player):
    running = True
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capturar teclas presionadas (continuamente)
    keys = pygame.key.get_pressed()

    if keys == pygame.K_ESCAPE:
        pygame.quit()
        exit()

    if keys[pygame.K_d]:
        player["vel_x"] += player["acceleration"]
    elif keys[pygame.K_a]:
        player["vel_x"] -= player["acceleration"]
    else:
        if player["vel_x"] > player["speed_0"]:
            player["vel_x"] -= player["deceleration"]
        elif player["vel_x"] < -player["speed_0"]:
            player["vel_x"] += player["deceleration"]

    if keys[pygame.K_w]:
        player["vel_y"] -= player["acceleration"]
    elif keys[pygame.K_s]:
        player["vel_y"] += player["acceleration"] 
    else:
        # Aplicar desaceleración en el eje Y
        if player["vel_y"] > player["speed_0"]:
            player["vel_y"] -= player["deceleration"]
        elif player["vel_y"] < -player["speed_0"]:
            player["vel_y"] += player["deceleration"]

    # Limitar la velocidad máxima
    player["vel_x"] = max(-player["speed"], min(player["vel_x"], player["speed"]))
    player["vel_y"] = max(-player["speed"], min(player["vel_y"], player["speed"]))
   
    # Rotar el jugador
    if keys[pygame.K_k]:
        player["angle"] += 5
    if keys[pygame.K_j]:
        player["angle"] -= 5
    if keys[pygame.K_SPACE]:
        action_fire = True
    else:   
        action_fire = False
    if keys[pygame.K_t]:
        action_powerup = True
    else:   
        action_powerup = False

    return running, action_fire, action_powerup

def capturar_eventos_joystick(player, joystick):
    running = True
    action_fire = False
    action_powerup = False

    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capturar el estado del joystick
    if joystick:
        # Movimiento del jugador usando los ejes del joystick
        axis_x = joystick.get_axis(0)  # Eje horizontal (izquierda/derecha)
        axis_y = joystick.get_axis(1)  # Eje vertical (arriba/abajo)

        #print(f"eje X:{axis_x}   eje Y:{axis_y}")
        # Aplicar aceleración si hay entrada del joystick
        if abs(axis_x) > 0.1:  # Umbral para evitar movimientos no deseados
            player["vel_x"] += axis_x * player["acceleration"]
        else:
            # Aplicar desaceleración en el eje X
            if player["vel_x"] > 0:
                player["vel_x"] -= player["deceleration"]
            elif player["vel_x"] < 0:
                player["vel_x"] += player["deceleration"]

        if abs(axis_y) > 0.1:  # Umbral para evitar movimientos no deseados
            player["vel_y"] += axis_y * player["acceleration"]
        else:
            # Aplicar desaceleración en el eje Y
            if player["vel_y"] > 0:
                player["vel_y"] -= player["deceleration"]
            elif player["vel_y"] < 0:
                player["vel_y"] += player["deceleration"]

        # Limitar la velocidad máxima
        player["vel_x"] = max(-player["speed"], min(player["vel_x"], player["speed"]))
        player["vel_y"] = max(-player["speed"], min(player["vel_y"], player["speed"]))

        # Rotar el jugador usando los botones L1 y R1
        if joystick.get_button(4):  # L1
            player["angle"] -= 5
        if joystick.get_button(5):  # R1
            player["angle"] += 5

        # Disparar usando el botón Cruz (botón 0 en mandos de PlayStation)
        if joystick.get_button(0):  # Cruz
            action_fire = True

        # Activar power-up usando el botón Cuadrado (botón 3 en mandos de PlayStation)
        if joystick.get_button(3):  # Cuadrado
            action_powerup = True

    return running, action_fire, action_powerup

# Función para detectar colisiones
def detect_collision(x1, y1, x2, y2, size=50):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) < size

def shoot_ball(player, bullet):
    current_time = pygame.time.get_ticks()
    if bullet["is_fired"] or current_time - bullet["last_shot_time"] < bullet["cooldown_time"]:
        return 
    # Disparar
    bullet["x"] = player["x"] + 50 + 45 * math.cos(math.radians(player["angle"]))
    bullet["y"] = player["y"] + 45 - 45 * math.sin(math.radians(player["angle"]))
    bullet["angle"] = player["angle"]
    bullet["is_fired"]  = True
    bullet["last_shot_time"] = current_time  # Actualizar el tiempo del último disparo

    # Reproducir sonido de disparo
    disparo_sonido.play()

def refresh_ball_position(bullet):
    if bullet["is_fired"]:
        # Verificar si la bala está fuera de la pantalla
        if bullet["x"] < 0 or bullet["x"] > WIDTH or bullet["y"] < 0 or bullet["y"] > HEIGHT:
            bullet["is_fired"] = False

        # Calcular la nueva posición de la bala
        bullet["x"] += bullet["speed"] * math.cos(math.radians(bullet["angle"]))
        bullet["y"] -= bullet["speed"] * math.sin(math.radians(bullet["angle"]))
        #print(f"Posicion de la pelota (x, y): ({bullet["x"]}, {bullet["y"]})")  # Imprimir la posición de la pelota
        # Dibujar la bala
        rotated_bullet_image = pygame.transform.rotate(bullet["image"][1] if power_up["is_active"] else bullet["image"][0], bullet["angle"])
        bullet_rect = rotated_bullet_image.get_rect(center=(bullet["x"], bullet["y"]))
        screen.blit(rotated_bullet_image, bullet_rect.topleft)


def process_power_up(power_up,action_powerup):  # Procesar el power-up
    # Detectar si la barra de progreso está llena y si se presiona la tecla T
    if power_up["rounds"] == power_up["max_rounds"] and not power_up["is_active"]:
        if action_powerup:
            print("¡Power-up activado!")
            power_up["is_active"] = True  # Activar el estado de power-up
            power_up["start_time"] = pygame.time.get_ticks()  # Registrar el tiempo de inicio del power-up

            # Reiniciar la barra de progreso
            power_up["rounds"] = 0

    # Verificar si el efecto de power-up ha terminado
    if power_up["is_active"]:
        current_time = pygame.time.get_ticks()
        if current_time - power_up["start_time"] >= power_up["duration"]:
            print("¡Power-up terminado!")
            power_up["is_active"] = False  # Desactivar el estado de power-up




# Función para capturar eventos de teclado en la pantalla final
def capturar_eventos_teclado_fin():
    running = True
    action_restart = False
    action_quit = False

#
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reiniciar el juego
                action_restart = True
            if event.key == pygame.K_q:  # Salir del juego
                action_quit = True

    return running, action_restart, action_quit

def aplicar_movimiento_flotante(player):
    if abs(player["vel_x"]) < player["speed_0"] and abs(player["vel_y"]) < player["speed_0"]:  # Si el jugador está casi quieto
        if player["float_angle"] == 0:
            player["x0_float"] = player["x"]  # Guardar la posición inicial para el efecto de flotación
            player["y0_float"] = player["y"]  # Guardar la posición inicial para el efecto de flotación

        player["float_angle"] += 0.1  # Incrementar el ángulo de flotación
        player["x"] = player["x0_float"] + player["float_radius"] * (math.cos(player["float_angle"])-1)  # Calcular el desplazamiento en X
        player["y"] = player["y0_float"] + player["float_radius"] * math.sin(player["float_angle"])  # Calcular el desplazamiento en Y
    else:
        player["float_angle"] = 0  # Reiniciar el ángulo de flotación


def aplicar_movimiento(player, power_up):    
    power_up_multiplier = (2 if power_up["is_active"] else 1)

    # Actualizar la posición del jugador
    player["x"] += player["vel_x"] * power_up_multiplier
    player["y"] += player["vel_y"] * power_up_multiplier

    # Aplicar movimiento flotante si no hay entrada
    aplicar_movimiento_flotante(player)

    # Limitar la posición del jugador dentro de la pantalla
    if player["x"] < 0:
        player["x"] = 0
    if player["x"] > WIDTH - 100:  # Ajustar por el tamaño del sprite
        player["x"] = WIDTH - 100
    if player["y"] < 0:
        player["y"] = 0
    if player["y"] > HEIGHT - 100:  # Ajustar por el tamaño del sprite
        player["y"] = HEIGHT - 100


def mostrar_teclado(joystick, timeout=120):
    """
    Muestra un teclado en pantalla para ingresar el nombre del jugador.
    """
    letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    filas = 3
    columnas = 9
    teclas = [letras[i:i+columnas] for i in range(0, len(letras), columnas)] + [["OK", "BORRAR"]]
    seleccion = [0, 0]  # Posición inicial en el teclado
    nombre = ""
    tiempo_inicio = pygame.time.get_ticks()

    last_action = Action.NONE
    while True:
        # Dibujar el fondo del teclado
        screen.fill(BLACK)

        # Dibujar las teclas
        for fila_idx, fila in enumerate(teclas):
            for col_idx, tecla in enumerate(fila):
                x = (WIDTH - (80 * (len(teclas[0])-1))) // 2 + col_idx * 80
                y = 200 + fila_idx * 80
                color = YELLOW if [fila_idx, col_idx] == seleccion else WHITE
                texto = font20.render(tecla, True, color)
                screen.blit(texto, (x, y))

        # Dibujar el nombre ingresado
        nombre_texto = font40.render(nombre, True, WHITE)
        screen.blit(nombre_texto, (WIDTH // 2 - nombre_texto.get_width() // 2, 80))

        # Actualizar pantalla
        pygame.transform.scale(screen, (REAL_WIDTH, REAL_HEIGHT), screen_real)
        pygame.display.flip()

        # Capturar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            action = Action.NONE        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    action = Action.MOV_UP
                elif event.key == pygame.K_s:
                    action = Action.MOV_DOWN
                elif event.key == pygame.K_a:
                    action = Action.MOV_LEFT
                elif event.key == pygame.K_d:
                    action = Action.MOV_RIGHT
                elif event.key == pygame.K_SPACE:
                    action = Action.FIRE
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            if joystick and (event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONDOWN):
                axis_x = joystick.get_axis(0)  # Eje horizontal (izquierda/derecha)
                axis_y = joystick.get_axis(1)  # Eje vertical (arriba/abajo)
                
                if abs(axis_y)>abs(axis_x) and abs(axis_y)>0.5:  # Movimiento vertical
                    if axis_y < 0:
                        action = Action.MOV_UP
                    else:   
                        action = Action.MOV_DOWN
                elif abs(axis_x)>abs(axis_y) and abs(axis_x)>0.5:  # Movimiento horizontal
                    if axis_x < 0:
                        action = Action.MOV_LEFT
                    else:
                        action = Action.MOV_RIGHT   
                if joystick.get_button(0):  # Botón "Start" del joystick
                    action = Action.FIRE

            if action != Action.NONE and action != last_action:
                if action == Action.MOV_UP:
                    seleccion[0] = (seleccion[0] - 1) % len(teclas)
                    seleccion[1] = seleccion[1] % len(teclas[seleccion[0]])
                elif action == Action.MOV_DOWN:
                    seleccion[0] = (seleccion[0] + 1) % len(teclas)
                    seleccion[1] = seleccion[1] % len(teclas[seleccion[0]])
                elif action == Action.MOV_LEFT:
                    seleccion[1] = (seleccion[1] - 1) % len(teclas[seleccion[0]])
                elif action == Action.MOV_RIGHT:
                    seleccion[1] = (seleccion[1] + 1) % len(teclas[seleccion[0]])
                elif action == Action.FIRE:
                    tecla_seleccionada = teclas[seleccion[0]][seleccion[1]]
                    if tecla_seleccionada == "OK":
                        return nombre  # Confirmar el nombre
                    elif tecla_seleccionada == "BORRAR":
                        nombre = nombre[:-1]  # Borrar la última letra""  
                    elif len(nombre) < 6:
                        nombre += tecla_seleccionada  # Agregar letra al nombre
            last_action = action

        # Verificar timeout
        tiempo_actual = pygame.time.get_ticks()
        if (tiempo_actual - tiempo_inicio) / 1000 > timeout:
            return nombre  


def actualizar_highscore(highscores, nombre, rondas):
    """
    Actualiza la lista de los 10 mejores puntajes.
    """
    highscores.append({"name": nombre, "rounds": rondas})
    highscores = sorted(highscores, key=lambda x: x["rounds"], reverse=True)[:10]
    return highscores

def guardar_highscores(highscores, archivo="highscores.csv"):
    """
    Guarda los highscores en un archivo CSV.
    """
    with open(archivo, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "rounds"])  # Escribir encabezados
        for score in highscores:
            writer.writerow([score["name"], score["rounds"]])

def cargar_highscores(archivo="highscores.csv"):
    """
    Carga los highscores desde un archivo CSV.
    Si el archivo no existe, devuelve una lista vacía.
    """
    try:
        with open(archivo, mode="r") as file:
            reader = csv.DictReader(file)
            return [{"name": row["name"], "rounds": int(row["rounds"])} for row in reader]
    except FileNotFoundError:
        # Si el archivo no existe, inicializar con una lista vacía
        highscores = [{"name": "PONCHO!", "rounds": i} for i in range(10)]
        guardar_highscores(highscores)
        return highscores


if __name__ == "__main__":

    highscores = cargar_highscores()
    idx_music_track_last = 0

    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)  # Usar el primer joystick conectado
        joystick.init()
        print("Joystick conectado: ", joystick.get_name())
    else:
        joystick = None
        print("No se detectó ningún joystick. Usando teclado como entrada.")

    while True:  # Bucle principal del programa
        # Mostrar la pantalla de inicio
        mostrar_pantalla_inicio(joystick)

        # Inicializar variables del juego
        player_health = max_health
        round_count = 0
        enemies = generate_enemies(round_count)

        # Bucle principal del juego
        running = True
        while running:
            current_time = pygame.time.get_ticks()  # Tiempo actual en milisegundos

            # Dibujar el fondo
            screen.blit(scene["image"][scene["idx_scene"]], (0, 0))  # Dibujar la imagen de fondo en la posición (0, 0)

            if joystick:
                # Usar el joystick si está conectado
                running, action_fire, action_powerup = capturar_eventos_joystick(player, joystick)
            else:
                # Usar el teclado si no hay joystick
                running, action_fire, action_powerup = capturar_eventos_teclado(player)

            aplicar_movimiento(player, power_up)  # Aplicar movimiento al jugador

            # Verificar si se puede disparar  
            if action_fire:
                shoot_ball(player, bullet)  # Disparar            

            # Dibujar y mover enemigos
            if enemies:
                for enemy in enemies[:]:  # Iterar sobre una copia de la lista
                    move_enemy(enemy, player)  # Mover enemigo hacia el jugador
                    screen.blit(enemy_template["images"][enemy["fase"]], (enemy["x"], enemy["y"]))  # Dibujar enemigo con su sprite

                    # Detectar colisión con el jugador
                    if detect_collision(enemy["x"], enemy["y"], player["x"], player["y"]):
                        print("El enemigo tocó al jugador.")
                        player_health -= 20  # Reducir la vida del jugador
                        daño_jugador_sonido.play()  # Reproducir el sonido de daño
                        enemies.remove(enemy)  # Eliminar al enemigo que tocó al jugador

                        # Finalizar el juego si la vida llega a 0
                        if player_health <= 0:
                            print("¡Has perdido!")
                            running = False

                    # Detectar colisión con la bala
                    if bullet["is_fired"] and detect_collision(enemy["x"], enemy["y"], bullet["x"], bullet["y"]):
                        # Agregar una explosión en la posición del enemigo
                        explosions.append({"x": enemy["x"], "y": enemy["y"], "timer": 500})  # 500 ms de duración

                        # Intentar eliminar el enemigo de la lista
                        try:
                            enemies.remove(enemy)  # Eliminar enemigo si es alcanzado por la bala
                        except ValueError:
                            pass  # Ignorar el error si el enemigo ya no está en la lista

                        bullet["is_fired"] = False  # Detener la bala

                        # Reproducir sonido al eliminar un enemigo
                        enemigo_eliminado_sonido.play()

            else:
                # Si no hay enemigos, hacer visible el aro
                aro["visible"] = True

            # Detectar colisión entre el jugador y el aro
            if aro["visible"]:
                screen.blit(aro["image"], (aro["x"], aro["y"]))

                if detect_collision(aro["x"], aro["y"], player["x"], player["y"], size=50):
                    print("¡Tocaste el aro!")
                    aro["visible"] = False  # Hacer que desaparezca

                    # Incrementar el contador de rondas
                    round_count += 1
                    print(f"Ronda {round_count} iniciada")

                    if round_count % scene["change_round"] == 0:
                        scene["idx_scene"] += 1
                        if scene["idx_scene"] >= len(scene["image"]):
                            scene["idx_scene"] = len(scene["image"])-1
                        
                        idx_music_track = (scene["idx_scene"]//3) % len(scene["music"])  # Cambiar la música cada 3 escenas
                        if idx_music_track != idx_music_track_last:
                            idx_music_track_last = idx_music_track
                            # Reproducir la música de fondo
                            pygame.mixer.music.load(scene["music"][scene["idx_scene"]])
                            pygame.mixer.music.play(-1)  # Reproducir en bucle          


                    # Incrementar contador de rondas para el powerup
                    power_up["rounds"] += 1
                    if power_up["rounds"] > power_up["max_rounds"]:
                        power_up["rounds"] = power_up["max_rounds"]

                    # Cambiar el sprite de los enemigos cada 10 rondas
                    if round_count % 10 == 0:
                        # Reproducir el sonido de nivel
                        level_up_sonido.play()                

                    # Reducir el tiempo de espera entre disparos cada 5 rondas
                    if round_count % 5 == 0:
                        bullet["cooldown_time"] -= 100  # Reducir el cooldown en 100 ms
                        if bullet["cooldown_time"] < bullet["min_cooldown_time"]:  # Asegurarse de que no sea menor al mínimo
                            bullet["cooldown_time"] = bullet["min_cooldown_time"]

                    # Generar una nueva tanda de enemigos con velocidad incrementada y enemigos adicionales
                    enemies = generate_enemies(round_count)

                    # Incrementar la vida del jugador al tocar el aro
                    player_health += 20
                    if player_health > max_health:  # Asegurarse de que no supere el máximo
                        player_health = max_health

                    # Reproducir el sonido de vida
                    vida_sonido.play()

            process_power_up(power_up,action_powerup)  # Procesar el power-up

            # Dibujar al jugador
            rotated_image = pygame.transform.rotate(player["image"][1 if power_up["is_active"] else 0], player["angle"])
            rotated_rect = rotated_image.get_rect(center=(player["x"] + 50, player["y"] + 50))
            screen.blit(rotated_image, rotated_rect.topleft)
                    
            refresh_ball_position(bullet)  # Actualizar la posición de la bala

            # Dibujar las explosiones activas
            for explosion in explosions[:]:  # Iterar sobre una copia de la lista
                screen.blit(explosion_image, (explosion["x"], explosion["y"]))  # Dibujar la explosión
                explosion["timer"] -= 20  # Reducir el temporizador de la explosión
                if explosion["timer"] <= 0:
                    explosions.remove(explosion)  # Eliminar la explosión cuando el temporizador llegue a 0

            # Dibujar el contador de rondas
            round_text = font20.render(f"Ronda: {round_count}", True, WHITE)  # Crear el texto principal
            shadow_text = font20.render(f"Ronda: {round_count}", True, DARK_PURPLE)  # Crear el texto sombra
            screen.blit(shadow_text, (8, HEIGHT - 23))  # Mover la sombra un poco más abajo
            screen.blit(round_text, (10, HEIGHT - 25))  # Mover el texto principal un poco más abajo

            # Dibujar la barra de vida como imagen
            health_image = get_health_image(player_health, max_health)
            screen.blit(health_image, (-10, -25))  # Dibujar la barra de vida un poco más arriba

            # Dibujar la barra de progreso por rondas
            screen.blit(power_up["image"][power_up["rounds"]], (WIDTH - 210, 0))  # Mover la barra de progreso un poco más arriba

            # Actualizar pantalla
            # Escalás y mostrás en pantalla
            pygame.transform.scale(screen, (REAL_WIDTH, REAL_HEIGHT), screen_real)
            pygame.display.flip()
            pygame.time.delay(20)  # Pequeño delay para controlar la velocidad

            if player_health <= 0:
                running = False
                nombre = mostrar_teclado(joystick)
                if nombre:
                    highscores = actualizar_highscore(highscores, nombre, round_count)   
                    guardar_highscores(highscores)  # Guardar los highscores en el archivo                
                if not mostrar_pantalla_fin(joystick):  # Si el jugador no quiere reiniciar
                    break  # Salir del bucle principal del programa

    pygame.quit()
