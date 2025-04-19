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
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movimiento del Personaje")

# Colores
WHITE = (255, 255, 255)

# Configurar personaje
player_x = WIDTH // 2
player_y = HEIGHT // 2
speed = 3  # Velocidad de movimiento

# Configurar personaje-bala
bullet_speed = 7  # Velocidad de movimiento
flag_disparar = False

# Tiempo de espera entre disparos (en milisegundos)
cooldown_time = 1500  # Tiempo inicial de espera (1.5 segundos)
min_cooldown_time = 300  # Tiempo mínimo de espera entre disparos
last_shot_time = 0  # Tiempo del último disparo

# Cargar imagen del personaje
player_image = pygame.image.load("cocoball.png")  # Asegúrate de tener un archivo cocoball.png en tu directorio
player_image = pygame.transform.scale(player_image, (50, 100))  # Escalar la imagen al tamaño deseado
player_image = pygame.transform.rotate(player_image, -90)  # Rotar la imagen 90 grados hacia la izquierda

# Cargar imagen de la bala
bullet_image = pygame.image.load("pelota.png")  # Asegúrate de tener un archivo pelota.png en tu directorio
bullet_image = pygame.transform.scale(bullet_image, (50, 50))  # Escalar la imagen al tamaño deseado

# Cargar imagen del enemigo
enemy_image = pygame.image.load("alien.png")  # Asegúrate de tener un archivo alien.png en tu directorio
enemy_image = pygame.transform.scale(enemy_image, (50, 50))  # Escalar la imagen al tamaño deseado

# Cargar imagen del enemigo fase 2
enemy_image_phase_2 = pygame.image.load("enemigo fase 2.png")  # Asegúrate de tener un archivo enemigo fase 2.png
enemy_image_phase_2 = pygame.transform.scale(enemy_image_phase_2, (50, 50))  # Escalar al tamaño deseado

# Cargar imagen de fondo
background_image = pygame.image.load("luna.png")  # Asegúrate de tener un archivo luna.png en tu directorio
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Escalar al tamaño de la pantalla

# Cargar imagen de inicio
inicio_image = pygame.image.load("inicio.png")  # Asegúrate de tener un archivo inicio.png en tu directorio
inicio_image = pygame.transform.scale(inicio_image, (WIDTH, HEIGHT))  # Escalar al tamaño de la pantalla

# Cargar imagen de la explosión
explosion_image = pygame.image.load("explosion.png")  # Asegúrate de tener un archivo explosion.png
explosion_image = pygame.transform.scale(explosion_image, (50, 50))  # Escalar al tamaño deseado

# Variables adicionales para manejar la rotación
player_angle = 0  # Ángulo inicial del personaje

# Lista de enemigos
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

# Variables para la vida del jugador
max_health = 100  # Vida máxima del jugador
player_health = max_health  # Vida actual del jugador

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
progress_images = [pygame.transform.scale(img, (200, 40)) for img in progress_images]

# Función para obtener la imagen de la barra de progreso según las rondas completadas
def get_progress_image(round_count, max_rounds):
    progress_percentage = (round_count / max_rounds) * 100  # Calcular porcentaje de progreso
    if progress_percentage <= 0:
        return progress_images[0]  # Progreso 0%
    elif progress_percentage <= 10:
        return progress_images[1]  # Progreso 10%
    elif progress_percentage <= 20:
        return progress_images[2]  # Progreso 20%
    elif progress_percentage <= 30:
        return progress_images[3]  # Progreso 30%
    elif progress_percentage <= 40:
        return progress_images[4]  # Progreso 40%
    elif progress_percentage <= 50:
        return progress_images[5]  # Progreso 50%
    elif progress_percentage <= 60:
        return progress_images[6]  # Progreso 60%
    elif progress_percentage <= 70:
        return progress_images[7]  # Progreso 70%
    elif progress_percentage <= 80:
        return progress_images[8]  # Progreso 80%
    elif progress_percentage <= 90:
        return progress_images[9]  # Progreso 90%
    else:
        return progress_images[10]  # Progreso 100%

# Número máximo de rondas para llenar la barra
max_rounds = 10  # Puedes ajustar este valor según el diseño del juego

# Contador de rondas
round_count = 0  # Inicia en 0 para que la primera ronda sea la 1

# Función para generar enemigos con velocidad incrementada y enemigos adicionales
def generate_enemies(num_enemies, round_count):
    base_speed = 2  # Velocidad base de los enemigos
    speed_multiplier = 0.05 * round_count  # Incremento de velocidad por ronda
    additional_enemies = round_count // 20  # Un alien adicional cada 20 rondas
    total_enemies = num_enemies + additional_enemies  # Total de enemigos a generar
    return [
        {"x": random.randint(50, WIDTH - 50), "y": random.randint(50, HEIGHT - 50), "speed": base_speed + speed_multiplier}
        for _ in range(total_enemies)
    ]

# Función para mover enemigos hacia el jugador
def move_enemy(enemy, player_x, player_y):
    # Calcular la dirección hacia el jugador
    dx = player_x - enemy["x"]
    dy = player_y - enemy["y"]
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
        pygame.display.flip()  # Actualizar la pantalla

        # Capturar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # Salir de la pantalla de inicio y comenzar el juego

# Mostrar la pantalla de inicio
mostrar_pantalla_inicio()

# Registrar el tiempo de inicio del juego después de la pantalla de inicio
start_time = pygame.time.get_ticks()  # Tiempo en milisegundos desde que se inició el juego

# Generar la primera tanda de enemigos
enemies = generate_enemies(3, round_count + 1)  # Generar enemigos para la primera ronda

# Variables para el efecto de power-up
power_up_active = False
power_up_start_time = 0
power_up_duration = 10000  # Duración del power-up en milisegundos (10 segundos)

# Bucle principal del juego
running = True
while running:
    # Dibujar el fondo
    screen.blit(background_image, (0, 0))  # Dibujar la imagen de fondo en la posición (0, 0)

    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capturar teclas presionadas (continuamente)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= speed
    if keys[pygame.K_d]:
        player_x += speed
    if keys[pygame.K_w]:
        player_y -= speed
    if keys[pygame.K_s]:
        player_y += speed
    if keys[pygame.K_k]:
        player_angle += 5
    if keys[pygame.K_j]:
        player_angle -= 5

    # Verificar si se puede disparar
    current_time = pygame.time.get_ticks()  # Tiempo actual en milisegundos
    if keys[pygame.K_SPACE] and current_time - last_shot_time >= cooldown_time:
        # Disparar
        bullet_x = player_x + 50 + 45 * math.cos(math.radians(player_angle))
        bullet_y = player_y + 45 - 45 * math.sin(math.radians(player_angle))
        bullet_angle = player_angle
        flag_disparar = True
        last_shot_time = current_time  # Actualizar el tiempo del último disparo

        # Reproducir sonido de disparo
        disparo_sonido.play()

    # Dibujar y mover enemigos
    if enemies:
        for enemy in enemies[:]:  # Iterar sobre una copia de la lista
            move_enemy(enemy, player_x, player_y)  # Mover enemigo hacia el jugador
            screen.blit(enemy_image, (enemy["x"], enemy["y"]))  # Dibujar enemigo con su sprite

            # Detectar colisión con el jugador
            if detect_collision(enemy["x"], enemy["y"], player_x, player_y):
                print("El enemigo tocó al jugador.")
                player_health -= 20  # Reducir la vida del jugador
                enemies.remove(enemy)  # Eliminar al enemigo que tocó al jugador

                # Finalizar el juego si la vida llega a 0
                if player_health <= 0:
                    print("¡Has perdido!")
                    running = False

            # Detectar colisión con la bala
            if flag_disparar and detect_collision(enemy["x"], enemy["y"], bullet_x, bullet_y):
                # Agregar una explosión en la posición del enemigo
                explosions.append({"x": enemy["x"], "y": enemy["y"], "timer": 500})  # 500 ms de duración

                # Intentar eliminar el enemigo de la lista
                try:
                    enemies.remove(enemy)  # Eliminar enemigo si es alcanzado por la bala
                except ValueError:
                    pass  # Ignorar el error si el enemigo ya no está en la lista

                flag_disparar = False  # Detener la bala

                # Reproducir sonido al eliminar un enemigo
                enemigo_eliminado_sonido.play()

    else:
        # Si no hay enemigos, hacer visible el aro
        aro["visible"] = True

    # Detectar colisión entre el jugador y el aro
    if aro["visible"]:
        screen.blit(aro_image, (aro["x"], aro["y"]))

        if detect_collision(aro["x"], aro["y"], player_x, player_y, size=50):
            print("¡Tocaste el aro!")
            aro["visible"] = False  # Hacer que desaparezca

            # Incrementar el contador de rondas
            round_count += 1
            print(f"Ronda {round_count} iniciada")

            # Cambiar el sprite de los enemigos cada 10 rondas
            if round_count % 10 == 0:
                enemy_image = enemy_image_phase_2
                print("¡Los enemigos han cambiado a la fase 2!")
                # Reproducir el sonido de nivel
                level_up_sonido.play()

            # Reducir el tiempo de espera entre disparos cada 5 rondas
            if round_count % 5 == 0:
                cooldown_time -= 100  # Reducir el cooldown en 100 ms
                if cooldown_time < min_cooldown_time:  # Asegurarse de que no sea menor al mínimo
                    cooldown_time = min_cooldown_time
                print(f"Tiempo de espera entre disparos reducido a {cooldown_time} ms")

            # Generar una nueva tanda de enemigos con velocidad incrementada y enemigos adicionales
            enemies = generate_enemies(3, round_count)

            # Incrementar la vida del jugador al tocar el aro
            player_health += 20
            if player_health > max_health:  # Asegurarse de que no supere el máximo
                player_health = max_health

            # Reproducir el sonido de vida
            vida_sonido.play()

    # Detectar si la barra de progreso está llena y si se presiona la tecla T
    if round_count >= max_rounds and not power_up_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_t]:
            print("¡Power-up activado!")
            power_up_active = True
            power_up_start_time = pygame.time.get_ticks()  # Registrar el tiempo de inicio del power-up

            # Aumentar el tamaño de la pelota
            bullet_image = pygame.transform.scale(bullet_image, (70, 70))  # Incrementar el tamaño de la pelota

            # Aumentar la velocidad del cocodrilo
            speed *= 2

            # Reiniciar la barra de progreso
            round_count = 0

    # Verificar si el efecto de power-up ha terminado
    if power_up_active:
        current_time = pygame.time.get_ticks()
        if current_time - power_up_start_time >= power_up_duration:
            print("¡Power-up terminado!")
            power_up_active = False

            # Restaurar el tamaño de la pelota
            bullet_image = pygame.transform.scale(bullet_image, (50, 50))  # Restaurar el tamaño original de la pelota

            # Restaurar la velocidad del cocodrilo
            speed //= 2

    # Dibujar al jugador
    rotated_image = pygame.transform.rotate(player_image, player_angle)
    rotated_rect = rotated_image.get_rect(center=(player_x + 50, player_y + 50))
    screen.blit(rotated_image, rotated_rect.topleft)

    if flag_disparar:
        # Calcular la nueva posición de la bala
        bullet_x += bullet_speed * math.cos(math.radians(bullet_angle))
        bullet_y -= bullet_speed * math.sin(math.radians(bullet_angle))
        # Dibujar la bala
        rotated_bullet_image = pygame.transform.rotate(bullet_image, bullet_angle)
        bullet_rect = rotated_bullet_image.get_rect(center=(bullet_x, bullet_y))
        screen.blit(rotated_bullet_image, bullet_rect.topleft)

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
    progress_image = get_progress_image(round_count, max_rounds)
    screen.blit(progress_image, (500, 0))  # Dibujar la barra de progreso debajo de la barra de vida

    # Actualizar pantalla
    pygame.display.flip()
    pygame.time.delay(20)  # Pequeño delay para controlar la velocidad

pygame.quit()
