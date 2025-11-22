# Cocodrile Balls

¡Cocoball, el cocodrilo espacial! — un juegazo estilo arcade hecho con Python y Pygame.

**Descripción:**
- Juego de acción donde controlas a "Coco" (un cocodrilo espacial) que dispara pelotas, recoge vidas y enfrenta oleadas de enemigos.
- Soporta teclado y joystick. Incluye efectos de sonido, música de fondo, barras de vida y power-ups.

**Estructura del repositorio**
- `cocoball.py` : Archivo principal del juego.
- `cocoball_base.py` : Código base (auxiliar).
- `imagenes/` : Sprites y fondos (escenas, enemigos, barra de vida, aro, etc.).
- `sonido/` : Efectos y música de fondo (.wav / .mp3).
- `fuentes/` : Tipografías usadas por el juego.
- `highscores.csv` : Archivo CSV con los 10 mejores puntajes (nombre + rondas).
- `LICENSE` : Licencia del proyecto.

**Requisitos**
- Python 3.8+ (probado con entornos con `pygame`).
- Módulo `pygame`.

Instalación rápida (recomendado usar un entorno virtual):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pygame
```

Si usas conda:

```bash
conda create -n cocoball python=3.11
conda activate cocoball
pip install pygame
```

**Ejecutar el juego**

Desde la carpeta del proyecto:

```bash
python cocoball.py
```

(En algunas máquinas puede ser `python3 cocoball.py`.)

**Controles**
- Teclado:
  - Movimiento: `W` / `A` / `S` / `D` (arriba, izquierda, abajo, derecha)
  - Rotar: `K` / `J` (giran la nave/cocodrilo)
  - Disparar: `Espacio`
  - Activar power-up: `T`
  - Pausa/salir en menús: `Esc`
  - Pantalla inicio: `Espacio` para comenzar
- Joystick (si está conectado):
  - Ejes analógicos para movimiento
  - Botón `0` (cruz / A) para disparar
  - Botón `3` (cuadrado / X) para activar power-up
  - Botones `4` y `5` para rotar

**Características principales**
- Oleadas de enemigos con velocidad que aumenta por ronda.
- Power-ups basados en una barra de progreso por rondas.
- Vida del jugador representada por una barra gráfica (sprites en `imagenes/` empezando por `barra_`).
- Sistema de highscores guardado en `highscores.csv` (se guarda automáticamente al finalizar y registrar nombre).
- Pantalla de inicio con alternancia entre splash y highscores.
- Soporte para input por teclado y joystick.

**Personalización / Recursos**
- Cambia fondos en `imagenes/` con prefijo `escena_` para nuevas escenas.
- Enemigos: añade sprites con prefijo `enemigo_` para ampliar variedad.
- Sonidos: reemplaza/añade archivos en `sonido/` (asegúrate de mantener los nombres esperados si quieres evitar cambios en el código).
- Fuentes: la fuente principal se lee desde `fuentes/cocoball_fuente.otf`.

**Notas de desarrollo y debugging**
- Si al ejecutar el juego obtienes errores relacionados con archivos (imágenes, sonidos o fuentes), comprueba que los archivos existan en los directorios `imagenes/`, `sonido/` y `fuentes/`.
- Si quieres ejecutar en modo ventana en lugar de `FULLSCREEN`, edita la línea en `cocoball.py` donde se llama a `pygame.display.set_mode(...)` y quita o cambia la bandera `pygame.FULLSCREEN`.
- Volumen de música y sonidos se controla en el script; ajusta `pygame.mixer.music.set_volume(...)` y/o los volúmenes de los `Sound` si necesitas.

**Contribuciones**
- Mejoras bienvenidas: pulir colisiones, añadir nuevas armas, niveles, enemigos y pantallas.
- Si envías PRs, mantén los cambios aislados y actualiza este README con instrucciones específicas si introduces nuevas dependencias o comandos.

**Problemas conocidos**
- Algunas máquinas pueden requerir ajustar el volumen (el juego actualmente establece un volumen alto en `pygame.mixer.music.set_volume(30)` — puedes reducirlo a `0.3` o similar si el audio suena muy alto).
- Dependiendo de la resolución/escala, algunos sprites pueden necesitar reajuste en `load_images(...)` para verse correctamente.

**Licencia & Créditos**
- Revisa el archivo `LICENSE` incluido en el repositorio para los términos de uso.
- Autor / mantenedor: `ponchogames` (ver historial de commits para más información).

