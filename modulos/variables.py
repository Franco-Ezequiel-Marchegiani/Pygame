import pygame as pg

# ======= PANTALLA ===========

RATIO_SD = (854, 480)
RATIO_SDP = (800, 600)
RATIO_HD = (1280, 720)
RATIO_FHD = (1920, 1080)
RATIO_UHD = (3840, 2160)

DIMENSION_PANTALLA = RATIO_HD


FPS = 60
# ======= BOTONES ===========

BOTON_X = 125
BOTON_Y = 275

BOTON_JUGAR = 0
BOTON_AJUSTES = 1
BOTON_HISTORIA = 2
BOTON_SALIR = 3

MAIN_TITLE = 'DRAGON BALL Z TCG'
SUB_TITLE_MENU = ''
SUB_TITLE_GAME = ''
SUB_TITLE_RANKING = ''
SUB_TITLE_OPTIONS = ''
SUB_TITLE_ = ''
# ======= FUENTES ===========

FUENTE_ALAGARD = './modulos/assets/fonts/alagard.ttf'
FUENTE_SAIYAN = './modulos/assets/fonts/saiyan_sans.ttf'

# FUENTE_20 = pg.font.SysFont("Arial",20)
FUENTE_22 = 22
FUENTE_25 = 25
FUENTE_27 = 27
FUENTE_30 = 30
FUENTE_32 = 32
FUENTE_50 = 50

# ======= DIMENSIONES ===========

#Define la caja que ocupará
#Centro de las dimensiones horizontales y verticales
CENTRO_DIMENSION_X = DIMENSION_PANTALLA[0] // 2
CENTRO_DIMENSION_Y = DIMENSION_PANTALLA[1] // 2 
#Largo x alto
DIMENSION_BOTON_JUGAR = (125, 115)
DIMENSION_BOTON_HISTORIA = (125,275)
DIMENSION_BOTON_SALIR = (125,355)
DIMENSION_TITULO = (600, 80)
DIMENSION_PUNTAJE = (200, 60)
DIMENSION_PREGUNTA = (500,100)
DIMENSION_FRASE = (500,100)
DIMENSION_HISTORIA = (1200, 450)
DIMENSION_RESPUESTA = (250,60)
DIMENSION_BOTON = (250,60)
DIMENSION_BOTON_BACK = (200, 60)
CUADRO_TEXTO = (250,50)
DIMENSION_BOTON_VOLUMEN = (60,60)
DIMENSION_BOTON_VOLVER = (100,40)
DIMENSION_CAJA_TEXTO = (1200, 450)

# ======= RUTA ===========

""" RUTA_MAZO_MAIN = './assets/decks'
RUTA_FONDO = './assets/background/fondo_tablero.png'
RUTA_SONIDO_CLICK = './assets/sound/click.mp3'
RUTA_MUSICA = './assets/sound/music.ogg'
RUTA_ICONO = './assets/icon_4_star.png' """

# ======= CONFIGS ===========

CANTIDAD_VIDAS = 3
PUNTUACION_INICIAL = 0
VOLUMEN_MUSICA_INICIAL = 20
PUNTUACION_ACIERTO = 100
PUNTUACION_ERROR = 25

# ======= COORDENADAS ===========

#Define la posición de las coordenadas en donde se posicionará 
COORDENADA_LABEL_TITULO = (340, 10)
DIMENSION_BOTON_VOLVER = (993,580)
COORDENADA_LABEL_TEXTO_HISTORIA = (37, 115)
COORDENADA_CAJA_FRASE = (390,584)
COORDENADA_CARTA_VISTA = (690,106)
COORDENADA_CAJA_TITULO = (DIMENSION_PANTALLA[0]//2 - DIMENSION_TITULO[0] // 2,10)
COORDENADA_PUNTAJE = (50, COORDENADA_CAJA_TITULO[1])
COORDENADA_CAJA_HISTORIA = (37, 115)



# ======= COLORES ===========

COLOR_BLANCO = (255,255,255)
COLOR_NEGRO = (0,0,0)
COLOR_VERDE = (0,255,0)
COLOR_ROJO = (255,0,0)
COLOR_AZUL = (0,0,255)
COLOR_VIOLETA = (134,23,219)
COLOR_AMARILLO = (239,255,0)
COLOR_VERDE_OSCURO = "#0B9827"
COLOR_NARANJA = (255, 87, 20)


# ======= FUENTES ===========
""" 
FUENTE_ALAGARD = './modulos/assets/fonts/alagard.ttf'

FUENTE_20 = pg.font.SysFont("Arial",20)
FUENTE_22 = pg.font.Font(FUENTE_ALAGARD, 22)
FUENTE_25 = pg.font.Font(FUENTE_ALAGARD, 25)
FUENTE_27 = pg.font.Font(FUENTE_ALAGARD, 27)
FUENTE_30 = pg.font.Font(FUENTE_ALAGARD, 30)
FUENTE_32 = pg.font.Font(FUENTE_ALAGARD, 32)
FUENTE_50 = pg.font.Font(FUENTE_ALAGARD, 50) """

# ======= RUTA ===========

RUTA_MAZO_MAIN = './modulos/assets/img/decks'
RUTA_FONDO = './modulos/assets/background/fondo_tablero.png'
RUTA_SONIDO_CLICK = './modulos/assets/sound/click.mp3'
RUTA_MUSICA_MAIN_MENU = './modulos/assets/audio/music/form_main_menu.ogg'
RUTA_MUSICA_RANKING = './modulos/assets/audio/music/form_ranking.ogg' 
RUTA_MUSICA_WIN = './modulos/assets/audio/music/music_dragon_ball_1.mp3'
RUTA_MUSICA_LOSE = './modulos/assets/audio/music/lose_music.ogg'
RUTA_MUSICA_BONUS = './modulos/assets/audio/music/form_wish_select.ogg'
RUTA_MUSICA_BATALLA = './modulos/assets/audio/music/level_01.ogg'
RUTA_MUSICA_BUCLE = './modulos/assets/sound/music_dragon_ball_bucle.mp3'
RUTA_MUSICA_PAUSA = './modulos/assets/audio/music/form_pausa.ogg'
RUTA_MUSICA = './modulos/assets/audio/music/music_dragon_ball_1.mp3'
RUTA_ICONO = './modulos/assets/icon_4_star.png'

SOUND_CLICK = pg.mixer.Sound(RUTA_SONIDO_CLICK)

# ======= CONFIGS ===========

CANTIDAD_VIDAS = 3
PUNTUACION_INICIAL = 0
VOLUMEN_MUSICA_INICIAL = 100
PUNTUACION_ACIERTO = 100
PUNTUACION_ERROR = 25
TIMER = 3000

# ======= COORDENADAS ===========

#Define la posición de las coordenadas en donde se posicionará 
COORDENADA_CAJA_FRASE = (390,584)
COORDENADA_CAJA_FRASE = (993, 580)
COORDENADA_CARTA_MAZO = (440,206)
COORDENADA_CARTA_VISTA = (790,206)
COORDENADA_CAJA_TITULO = (DIMENSION_PANTALLA[0]//2 - DIMENSION_TITULO[0] // 2,10)
COORDENADA_PUNTAJE = (50, COORDENADA_CAJA_TITULO[1])
COORDENADA_CAJA_HISTORIA = (37, 115)

# ======= ARCHIVOS ===========
RUTA_RANKING = './ranking_usuario.csv'
RUTA_RANKING_CSV = './ranking.csv'
RUTA_CONFIGS_JSON = './config.json'

# ======= OBJETOS ===========

FONDO = pg.image.load(RUTA_FONDO)
CLICK_SONIDO = pg.mixer.Sound(RUTA_SONIDO_CLICK)


nombres = [
    "Pepe", "Moni", "Fatiga", "Dardo", "Guarani"
]