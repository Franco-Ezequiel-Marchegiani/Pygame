from datetime import datetime
import pygame as pg
import os
import random as rd
import modulos.carta as carta
import modulos.variables as var
import json

def generar_bd(root_path_cards: str, cantidad_cartas: int):

    contenedor_hp = 0
    contenedor_atk = 0
    contenedor_def = 0
    
    carta_dict = {
        "cartas": {},
        "max_stats": {
            "hp": 0,
            "atk": 0,
            "def": 0,
        },
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
                #HACER EL FOR, O EL RANDOM ACÁ

                file = file.replace('\\', '/')
                filename = file.split('/')[-1]
                datos = filename.split('.')[-2]
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

                #Redondear para arriba
                final_hp = round(final_hp) #Retorna tipo float, se puede parsear a entero. Redondea para arriba
                final_atk = round(final_atk) #Retorna tipo float, se puede parsear a entero. Redondea para arriba
                final_defense = round(final_defense) #Retorna tipo float, se puede parsear a entero. Redondea para arriba
                
                card = {
                    'id': f'{deck_name}-{list_data[0]}',
                    "hp": final_hp, #Cambiar luego al final, ya con el bonus potenciado
                    "atk": final_atk, #Cambiar luego al final, ya con el bonus potenciado
                    "def": final_defense, #Cambiar luego al final, ya con el bonus potenciado
                    "bonus": int(list_data[7]),
                    "path_imagen_frente": path_card,
                    "path_imagen_reverso": reverse_path, #Este valor puede estar, como no, se agrega más adelante
                }
                #Agregamos la carta al listado
                deck_cards.append(card)
                #Sumamos cada estadística de cada carta para obtener el total:
                

    deck_cards_filtrado = rd.sample(deck_cards, cantidad_cartas)

    for index in range(len(deck_cards_filtrado)):
        deck_cards_filtrado[index]['path_imagen_reverso'] = reverse_path
        
        filter_hp = deck_cards_filtrado[index].get('hp')
        filter_atk = deck_cards_filtrado[index].get('atk')
        filter_defense = deck_cards_filtrado[index].get('def')

        contenedor_hp += filter_hp
        contenedor_atk += filter_atk
        contenedor_def += filter_defense
        #Actualizo los valores habiendo acumulado
        carta_dict["max_stats"]["hp"] = contenedor_hp
        carta_dict["max_stats"]["atk"] = contenedor_atk
        carta_dict["max_stats"]["def"] = contenedor_def
    
    carta_dict['cartas'][deck_name] = deck_cards_filtrado
    
    return carta_dict


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



def inicializar_musica():
    #Calculamos cuanto dura la primera canción, para que se ejecute una vez
    sound = pg.mixer.Sound(var.RUTA_MUSICA)
    dur_ms = int(sound.get_length() * 1000)
    #Indicamos un evento para que se inicie el loop una vez terminado
    pg.time.set_timer(pg.USEREVENT+5, dur_ms, loops=1) 

    #Musica inicial
    pg.mixer.music.load(var.RUTA_MUSICA)
    pg.mixer.music.play() #Suena una sola vez



def inicializar_bucle_musica():
    #Musica en bucle dsp de la primera
    pg.mixer.music.load(var.RUTA_MUSICA_BUCLE)
    pg.mixer.music.set_volume(100)
    pg.mixer.music.play(-1) #-1 para que suene en bucle infinito


def terminar_musica(dict_juego: dict):
    dict_juego["musica_bucle_iniciada"] = True
    pg.mixer.music.stop()



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
    print(f"Ranking BEFORE: {ranking}")
    #Este ordena
    #En caso de querer que sea ASC, cambiar valor del Reverse
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