from datetime import datetime
import pygame as pg
import os
import random as rd
import modulos.carta as carta
import modulos.variables as var
import json

def crear_lista_botones(cantidad: int, dimension: tuple, color: str = 'purple'):
    lista_botones = []
    for i in range(cantidad):
        boton = {}
        boton['superficie'] = pg.Surface(dimension)
        boton['rectangulo'] = boton.get('superficie').get_rect()
        boton['superficie'].fill(pg.Color(color))
        lista_botones.append(boton)
    return lista_botones

def mostrar_texto(surface: pg.Surface, texto: str, pos: tuple, font, color = pg.Color('black')):
    words = []

    for word in texto.splitlines():
        words.append(word.split(' '))
    
    space = font.size(' ')[0]
    ancho_max, alto_max = surface.get_size()
    x, y = pos

    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            ancho_palabra, alto_palabra = word_surface.get_size()
            #Si ya no tiene espacio para escribir, sigue abajo en nuevo renglón
            if x + ancho_palabra >= ancho_max:
                x = pos[0]
                y += alto_palabra
            surface.blit(word_surface, (x, y))
            x +=ancho_palabra + space
        x = pos[0]
        y += alto_palabra

def crear_cuadro(dimensiones: tuple, coordenadas: tuple, color: tuple) -> dict:
    cuadro = {}
    cuadro['superficie'] = pg.Surface(dimensiones)
    cuadro['rectangulo'] = cuadro.get('superficie').get_rect()
    cuadro['rectangulo'].topleft = coordenadas
    cuadro['superficie'].fill(pg.Color(color))

    return cuadro


def crear_boton(pantalla: pg.Surface, texto: str, ruta_fuente: str, dimensiones: tuple, coordenadas: tuple, color_fondo: tuple, color_texto: tuple):
    cuadro = crear_cuadro(dimensiones, coordenadas, color_fondo)

    cuadro['texto'] = texto
    cuadro['pantalla'] = pantalla
    cuadro['color_texto'] = color_texto
    cuadro['color_fondo'] = color_fondo
    cuadro['font_path'] = ruta_fuente
    cuadro['padding'] = (10,10)

    return cuadro

def mostrar_boton(boton_dict: dict):
    mostrar_texto(
        boton_dict.get('superficie'),
        boton_dict.get('texto'),
        boton_dict.get('padding'),
        boton_dict.get('font_path'),
        boton_dict.get('color_texto'),
    )
    boton_dict['rectangulo'] = boton_dict.get('pantalla').blit(
        boton_dict.get('superficie'), boton_dict.get("rectangulo").topleft
    )
    pg.draw.rect(boton_dict.get("pantalla"), boton_dict.get("color_fondo"), boton_dict.get("rectangulo"), 2)

    
def generar_bd(root_path_cards: str):

    carta_dict = {
        "cartas": {}
    }

    for root, dir, files in os.walk(root_path_cards, topdown=True):
        reverse_path = ''
        deck_cards = []
        deck_name = root.split('\\')[-1]
        for file in files:
            path_card = os.path.join(root, file)
            
            if "reverse" in path_card:
                reverse_path = path_card
            else:
                file = file.replace('\\', '/')
                filename = file.split('/')[-1]
                datos = filename.split('.')[-2]
                print(f"deck_name: {deck_name}")
                #Tmb se puede optar por esto para el bonus
                #data_bonus = datos[-1] 
                list_data = datos.split('_')
                hp = int(list_data[2])
                atk = int(list_data[4])
                defense = int(list_data[6])
                bonus = int(list_data[7])
                #Definimos los valores ya buffeados
                final_hp = hp + (hp * bonus / 100)
                final_atk = atk + (atk * bonus / 100)
                final_defense = defense + (defense * bonus / 100)
                card = {
                    'id': f'{deck_name}-{list_data[0]}',
                    "hp": hp, #Cambiar luego al final, ya con el bonus potenciado
                    "atk": atk, #Cambiar luego al final, ya con el bonus potenciado
                    "def": defense, #Cambiar luego al final, ya con el bonus potenciado
                    "bonus": int(list_data[7]),
                    "path_imagen_frente": path_card,
                    "path_imagen_reverso": reverse_path, #Este valor puede estar, como no, se agrega más adelante
                }
                deck_cards.append(card)
        
        for index_Card in range(len(deck_cards)):
            deck_cards[index_Card]['path_imagen_reverso'] = reverse_path

        carta_dict['cartas'][deck_name] = deck_cards
    return carta_dict

def asignar_frases(lista_mazo: list[dict], lista_frases: list[dict]) -> list[dict]:

    for index_card in range(len(lista_mazo)):
        frase = rd.choice(lista_frases)
        lista_mazo[index_card]['frase'] = frase.get('frase') #.get("frase") para acceder al objeto del diccionario
        lista_mazo[index_card]['puntaje'] = frase.get('puntaje')
    return lista_mazo

def achicar_imagen_card(path_imagen: str, porcentaje: int):
    imagen_raw = pg.image.load(path_imagen)
    alto = int(imagen_raw.get_height() * float(f'0.{porcentaje}'))
    ancho = int(imagen_raw.get_width() * float(f'0.{porcentaje}'))
    imagen_final = pg.transform.scale(imagen_raw, (ancho, alto))
    return imagen_final


def generar_mazo(mazo_dict_original: list[dict]):
    lista_mazo_resultado = []
    for card in mazo_dict_original:
        carta_final = carta.inicializar_carta(card, var.COORDENADA_CARTA_MAZO)
        lista_mazo_resultado.append(carta_final)

    rd.shuffle(lista_mazo_resultado)

    return lista_mazo_resultado


def actualizar_puntaje(dict_juego: dict, puntaje: int):
    dict_juego['puntaje'] += puntaje

def verificar_tiempo_cumplido(tiempo_finalizado: int, retorno: tuple[str, str]):
    tiempo_actual = pg.time.get_ticks()
    if tiempo_actual - tiempo_finalizado >= 2000:
        return retorno[0]
    return retorno[1]

def datos_player_to_csv(dict_juego: dict):
    data = f'{datetime.now()},{dict_juego.get('nombre')},{dict_juego.get("puntaje")}\n'
    return data

def grabar_puntaje(dict_juego: dict):
    with open(var.RUTA_RANKING, '+a', encoding='utf-8') as file:
        data = datos_player_to_csv(dict_juego)
        file.write(data)

def inicializar_musica(dict_juego: dict):
    porcentaje_coma = dict_juego.get('volumen_musica') / 50
    #Calculamos cuanto dura la primera canción, para que se ejecute una vez
    sound = pg.mixer.Sound(var.RUTA_MUSICA)
    dur_ms = int(sound.get_length() * 1000)
    #Indicamos un evento para que se inicie el loop una vez terminado
    pg.time.set_timer(pg.USEREVENT+5, dur_ms, loops=1) 

    #Musica inicial
    pg.mixer.music.load(var.RUTA_MUSICA)
    pg.mixer.music.set_volume(porcentaje_coma)
    pg.mixer.music.play() #Suena una sola vez



def inicializar_bucle_musica():
    #Musica en bucle dsp de la primera
    pg.mixer.music.load(var.RUTA_MUSICA_BUCLE)
    pg.mixer.music.set_volume(100)
    pg.mixer.music.play(-1) #-1 para que suene en bucle infinito


def terminar_musica(dict_juego: dict):
    dict_juego["musica_bucle_iniciada"] = True
    pg.mixer.music.stop()




def crear_cuadro(dimensiones: tuple, coordenadas: tuple, color: tuple) -> dict:
    cuadro = {}
    cuadro['superficie'] = pg.Surface(dimensiones)
    cuadro['rectangulo'] = cuadro.get('superficie').get_rect()
    cuadro['rectangulo'].topleft = coordenadas
    cuadro['superficie'].fill(pg.Color(color))
    return cuadro

def parsear_entero(valor: str):
    if valor.isdigit():
        return int(valor)
    return valor

def mapear_valores(matriz: list[list], indice_a_aplicar: int, callback):
    
    for indice_fila in range(len(matriz)):
        valor = matriz[indice_fila][indice_a_aplicar]
        matriz[indice_fila][indice_a_aplicar] = callback(valor)

def cargar_ranking():
    ranking = []
    with open(var.RUTA_RANKING_CSV, 'r', encoding='utf-8') as file:
        lineas = file.read()
        for linea in lineas.split('\n'):
            if linea:
                ranking.append(linea.split(','))
    mapear_valores(ranking, 1, parsear_entero)
    ranking.sort(key=lambda fila: fila[1], reverse=True)
    
    return ranking

def guardar_ranking(jugador_dict: dict):
    #Por parámetro recibe el dict del jugador para que guarde la info
    #w es para escribir pero borra todo
    #Para eso, usar append para añadir 'a'
    with open(var.RUTA_RANKING_CSV, 'a', encoding='utf-8') as file:
        #Mensaje con la data del nombre y puntaje
        data = f'{jugador_dict.get('nombre')},{jugador_dict.get('puntaje_actual')}\n'
        file.write(data)
        print(f'Datos guardados con éxito! -> {data}')
        #Por ahora, solo guardar nombre y puntaje
def cargar_configs(path: str) -> dict:
    configuraciones = {}
    print(f"path: {path}")
    #Leemos "r" en la ruta pasada en param
    with open(path, 'r', encoding='utf-8') as file:
        print(f"File: {file}")
        configuraciones = json.load(file)
    #Cargamos la info del json, y lo devolvemos
    return configuraciones