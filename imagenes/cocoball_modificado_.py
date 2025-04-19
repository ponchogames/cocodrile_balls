import math
import pygame
import random  # Importar para generar posiciones aleatorias

# Inicializar pygame
pygame.init()

# Inicializar el módulo de sonido
pygame.mixer.init()

# Cargar efectos de sonido
disparo_sonido = pygame.mixer.Sound("disparo.wav")  # Sonido de disparo
enemigo_eliminado_sonido = pygame.mixer.Sound("enemigo_eliminado.wav")  # Sonido al eliminar un enemigo
vida_sonido = pygame.mixer.Sound("vida.wav")  # Sonido al tocar la canasta
level_up_sonido = pygame.mixer.Sound("level up.wav")  # Sonido al cambiar de sprite en la ronda 10

# Cargar música de fondo
pygame.mixer.music.load("cocosong.mp3")  # Asegúrate de tener un archivo musica_fondo.mp3 en tu directorio
pygame.mixer.music.set_volume(0.5)  # Ajustar el volumen de la música (0.0 a 1.0)
pygame.mixer.music.play(-1)  # Reproducir la música en bucle (-1 significa infinito)

# Configurar pantalla
WIDTH, HEIGHT = 960, 540  # Dimensiones de la pantalla
screen = pygame.Surface((WIDTH, HEIGHT))
REAL_WIDTH, REAL_HEIGHT = 1920, 1080
screen_real = pygame.display.set_mode((REAL_WIDTH, REAL_HEIGHT))
pygame.display.set_caption("Cocoball, el cocodrilo espacial!")

# Colores
WHITE = (255, 255, 255)

# Configurar personaje
max_health = 100  # Vida máxima del jugador
player = {
    "x": WIDTH // 2,  # Posición inicial X del jugador
    "y": HEIGHT // 2,  # Posición inicial Y del jugador
    "angle": 0,  # Ángulo inicial del jugador
    "speed": 3,  # Velocidad de movimiento
    "image": None  # Imagen del jugador (se cargará más adelante)
}
# Cargar imagen del personaje
player_image_1 = pygame.image.load("imagenes/coco_1.png")  # Asegúrate de tener un archivo cocoball.png en tu directorio
player_image_1 = pygame.transform.scale(player_image_1, (50, 100))  # Escalar la imagen al tamaño deseado
player_image_1 = pygame.transform.rotate(player_image_1, -90)  # Rotar la imagen 90 grados hacia la izquierda
player_image_2 = pygame.image.load("imagenes/coco_2.png")  # Asegúrate de tener un archivo cocoball.png en tu directorio
player_image_2 = pygame.transform.scale(player_image_2, (50, 100))  # Escalar la imagen al tamaño deseado
player_image_2 = pygame.transform.rotate(player_image_2, -90)  # Rotar la imagen 90 grados hacia la izquierda
player["image"] = [player_image_1, player_image_2]  # Asignar la imagen al diccionario del jugador


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

power_up = {
    "is_active": False,  # Estado de power-up
    "start_time": 0,  # Tiempo de inicio del power-up
    "duration": 10000,  # Duración del power-up en milisegundos (10 segundos)
    "rounds": 0,  # Contador de rondas para el power-up
    "max_rounds": 10, # Número máximo de rondas para llenar la barra 
    "image": None,  # Imagen de la barra de progreso (se cargará más adelante) 
}
# Cargar imágenes de la barra de progreso por rondas
progress_images = [
    pygame.image.load("progreso_100.png"), 
    pygame.image.load("progreso_90.png"),  
    pygame.image.load("progreso_80.png"), 
    pygame.image.load("progreso_70.png"), 
    pygame.image.load("progreso_60.png"), 
    pygame.image.load("progreso_50.png"),   
    pygame.image.load("progreso_40.png"), 
    pygame.image.load("progreso_30.png"), 
    pygame.image.load("progreso_20.png"),
    pygame.image.load("progreso_10.png"), 
    pygame.image.load("progreso_0.png"),     
]
# Escalar las imágenes al tamaño deseado (opcional)
power_up["image"] = [pygame.transform.scale(img, (200, 40)) for img in progress_images]

# Cargar imagen de la bala
bullet_image = pygame.image.load("pelota.png")  # Asegúrate de tener un archivo pelota.png en tu directorio
bullet_image = pygame.transform.scale(bullet_image, (50, 50))  # Escalar la imagen al tamaño deseado
bullet_image_large = pygame.transform.scale(bullet_image, (70, 70))  # Incrementar el tamaño de la pelota
bullet["image"] = [bullet_image, bullet_image_large]  # Asignar la imagen al diccionario de la bala


# Cargar imagen del enemigo
enemy_image = pygame.image.load("alien.png")  # Asegúrate de tener un archivo alien.png en tu directorio
enemy_image = pygame.transform.scale(enemy_image, (50, 50))  # Escalar la imagen al tamaño deseado

# Cargar imagen del enemigo fase 2
enemy_image_phase_2 = pygame.image.load("enemigo fase 2.png")  # Asegúrate de tener un archivo enemigo fase 2.png
enemy_image_phase_2 = pygame.transform.scale(enemy_image_phase_2, (50, 50))  # Escalar al tamaño deseado

# Cargar imagen de fondo
background_image = pygame.image.load("imagenes/fondo_1.png")  # Asegúrate de tener un archivo luna.png en tu directorio
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Escalar al tamaño de la pantalla

# Cargar imagen de inicio
inicio_image = pygame.image.load("inicio.png")  # Asegúrate de tener un archivo inicio.png en tu directorio
inicio_image = pygame.transform.scale(inicio_image, (WIDTH, HEIGHT))  # Escalar al tamaño de la pantalla

# Cargar imagen de la explosión
explosion_image = pygame.image.load("explosion.png")  # Asegúrate de tener un archivo explosion.png
explosion_image = pygame.transform.scale(explosion_image, (50, 50))  # Escalar al tamaño deseado


# Configurar enemigos
num_base_enemigos = 3 # Número de enemigos al arrancar el juego
base_speed = 2  # Velocidad base de los enemigos
enemies = []

# Lista de explosiones activas
explosions = []

# Variables para el aro de básquet
aro = {
    "x": (WIDTH // 2) - 25,  # Centrar el aro horizontalmente (ajustar por el tamaño del sprite)
    "y": (HEIGHT // 2) - 25,  # Centrar el aro verticalmente (ajustar por el tamaño del sprite)
    "visible": True  # El aro es visible al inicio
}
aro_image = pygame.image.load("aro.png")  # Asegúrate de tener un archivo aro.png
aro_image = pygame.transform.scale(aro_image, (50, 50))  # Escalar al tamaño deseado


# Cargar imágenes de la barra de vida
health_images = [
    pygame.image.load("barra 0 puntos.png"),   # Vida 0%
    pygame.image.load("barra 1 punto.png"), # Vida 20%
    pygame.image.load("barra 2 puntos.png"), # Vida 40%
    pygame.image.load("barra 3 puntos.png"), # Vida 60%
    pygame.image.load("barra 4 puntos.png"), # Vida 80%
    pygame.image.load("barra llena.png") # Vida 100%
]

# Escalar las imágenes al tamaño deseado (opcional)
health_images = [pygame.transform.scale(img, (200, 80)) for img in health_images]

# Lista de fondos con sus características
fondos = [
    {"imagen": "imagenes/fondo_1.png", "rondas": 1, "musica": "musica_1.mp3"},
    {"imagen": "imagenes/fondo_2.png", "rondas": 5, "musica": "musica_2.mp3"},
    {"imagen": "imagenes/fondo_3.png", "rondas": 10, "musica": "musica_3.mp3"}
]

# Función para obtener la imagen de la barra de vida según la vida actual
def get_health_image(player_health, max_health):
    health_percentage = (player_health / max_health) * 100  # Calcular porcentaje de vida
    if health_percentage <= 0:
        return health_images[0]  # Vida 0%
    elif health_percentage <= 20:
        return health_images[1]  # Vida 20%
    elif health_percentage <= 40:
        return health_images[2]  # Vida 40%
    elif health_percentage <= 60:
        return health_images[3]  # Vida 60%
    elif health_percentage <= 80:
        return health_images[4]  # Vida 80%
    else:
        return health_images[5]  # Vida 100%

# Función para generar enemigos con velocidad incrementada y enemigos adicionales
def generate_enemies(round_count):
    speed_multiplier = 0.05 * round_count  # Incremento de velocidad por ronda
    additional_enemies = (round_count+1) // 20  # Un alien adicional cada 20 rondas
    total_enemies = num_base_enemigos + additional_enemies  # Total de enemigos a generar
    return [
        {"x": random.randint(50, WIDTH - 50), "y": random.randint(50, HEIGHT - 50), "speed": base_speed + speed_multiplier}
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

# Función para detectar colisiones
def detect_collision(x1, y1, x2, y2, size=50):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) < size

# Pantalla de inicio
def mostrar_pantalla_inicio():
    while True:
        screen.blit(inicio_image, (0, 0))  # Dibujar la imagen de inicio
        pygame.transform.scale(screen, (REAL_WIDTH, REAL_HEIGHT), screen_real)
        pygame.display.flip()  # Actualizar la pantalla

        # Capturar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # Salir de la pantalla de inicio y comenzar el juego


def capturar_eventos_teclado(player,power_up):
    running = True
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capturar teclas presionadas (continuamente)
    power_up_multiplier = (2 if power_up["is_active"] else 1)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player["x"] -= player["speed"]*power_up_multiplier
    if keys[pygame.K_d]:
        player["x"] += player["speed"]*power_up_multiplier
    if keys[pygame.K_w]:
        player["y"] -= player["speed"]*power_up_multiplier
    if keys[pygame.K_s]:
        player["y"] += player["speed"]*power_up_multiplier
    
    if player["x"] < 0:
        player["x"] = 0
    if player["x"] > WIDTH - 100:  # Ajustar por el tamaño del sprite
        player["x"] = WIDTH - 100
    if player["y"] < 0:
        player["y"] = 0
    if player["y"] > HEIGHT - 100:  # Ajustar por el tamaño del sprite
        player["y"] = HEIGHT - 100

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


if __name__ == "__main__":
    # Mostrar la pantalla de inicio
    mostrar_pantalla_inicio()

    # Registrar el tiempo de inicio del juego después de la pantalla de inicio
    start_time = pygame.time.get_ticks()  # Tiempo en milisegundos desde que se inició el juego

    # Contador de rondas
    round_count = 0  # Inicia en 0 para que la primera ronda sea la 1

    # Generar la primera tanda de enemigos
    enemies = generate_enemies(round_count)  # Generar enemigos para la primera ronda

    # Bucle principal del juego
    running = True

    player_health = max_health  # Vida actual del jugador
    while running:
        current_time = pygame.time.get_ticks()  # Tiempo actual en milisegundos

        # Dibujar el fondo
        screen.blit(background_image, (0, 0))  # Dibujar la imagen de fondo en la posición (0, 0)

        running, action_fire, action_powerup = capturar_eventos_teclado(player,power_up)  # Capturar eventos de teclado

        # Verificar si se puede disparar
        if action_fire:
            shoot_ball(player, bullet)  # Disparar            

        # Dibujar y mover enemigos
        if enemies:
            for enemy in enemies[:]:  # Iterar sobre una copia de la lista
                move_enemy(enemy, player)  # Mover enemigo hacia el jugador
                screen.blit(enemy_image, (enemy["x"], enemy["y"]))  # Dibujar enemigo con su sprite

                # Detectar colisión con el jugador
                if detect_collision(enemy["x"], enemy["y"], player["x"], player["y"]):
                    print("El enemigo tocó al jugador.")
                    player_health -= 20  # Reducir la vida del jugador
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
            screen.blit(aro_image, (aro["x"], aro["y"]))

            if detect_collision(aro["x"], aro["y"], player["x"], player["y"], size=50):
                print("¡Tocaste el aro!")
                aro["visible"] = False  # Hacer que desaparezca

                # Incrementar el contador de rondas
                round_count += 1
                print(f"Ronda {round_count} iniciada")

                # Incrementar contador de rondas para el powerup
                power_up["rounds"] += 1
                if power_up["rounds"] > power_up["max_rounds"]:
                    power_up["rounds"] = power_up["max_rounds"]

                # Cambiar el sprite de los enemigos cada 10 rondas
                if round_count % 10 == 0:
                    enemy_image = enemy_image_phase_2
                    print("¡Los enemigos han cambiado a la fase 2!")
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

        # Cambiar fondo y música según el número de rondas
        for fondo in fondos:
            if round_count >= fondo["rondas"]:
                background_image = pygame.image.load(fondo["imagen"])
                pygame.mixer.music.load(fondo["musica"])
                pygame.mixer.music.play(-1)  # Reproducir en bucle

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

        # Dibujar la barra de vida como imagen
        health_image = get_health_image(player_health, max_health)
        screen.blit(health_image, (10, -20))  # Dibujar la barra de vida en la esquina superior izquierda

        # Dibujar la barra de progreso por rondas
        screen.blit(power_up["image"][power_up["rounds"]], (500, 0))  # Dibujar la barra de progreso debajo de la barra de vida

        # Actualizar pantalla
        # Escalás y mostrás en pantalla
        pygame.transform.scale(screen, (REAL_WIDTH, REAL_HEIGHT), screen_real)
        pygame.display.flip()
        pygame.time.delay(20)  # Pequeño delay para controlar la velocidad

    pygame.quit()
