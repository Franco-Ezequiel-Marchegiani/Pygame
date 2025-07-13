import pygame as pg
import os
import random as rd
import modulos.carta as carta
import modulos.variables as var
import json

def recorrer_archivo(files: list[str], root: str, deck_name: str, deck_cards: list) -> str:
    """ 
    Parametros: Recibe:\n
    -"Files" que sería una lista de strings, representando el listado de rutas \n
    -"Root" indicando la ruta base a buscar.\n
    -"deck_name" para poder identificar el dict con el ID.\n
    -"deck_cards" una lista, inicialmente vacía, que se le irán poblando los objetos.\n

    ¿Qué hace?: Itera sobre el listado de rutas, obtiene la información de la ruta y...\n
    Si es "reverse", guarda el valor en la variable "reverse_path". \n
    En caso contrario, puebla un objeto con la información de cada ruta con la imagen.

    ¿Qué Devuelve?: El reverse_path en formato string.
    """
    reverse_path = ''
    for file in files:
        path_card = os.path.join(root, file)
        
        if "reverse" in path_card:
            reverse_path = path_card
            print(f"REVERSE_PATH SAVED!: {reverse_path}")
        else:
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
    print(f"INDIVIDUAL CARD VALUE: {card}")
    return reverse_path

def generar_bd(root_path_cards: str, cantidad_cartas: int) -> dict:
    """ 
    Parametros: Recibe:\n
    -"root_path_cards" que es la ruta completa del deck a trabajar \n
    -"cantidad_cartas" indicando el límite de cartas por mazo. \n

    ¿Qué hace?: Inicializa con contenedores y un dict vacío, para acto seguido\n
    Recorrer según la ruta recibida, crear una lista vacía para contener la info del deck \n
    Recorrerlo y crea los dict de cada carta con ayuda de "recorrer_archivo". \n
    Luego mezcla todas las cartas del deck, las filtra según la cantidad indicada en param \n
    Y le asigna la imagen del reverse_path, junto al promedio de estadísticas a las variables \n
    Que se crearon al inicio.

    ¿Qué Devuelve?: El diccionario con la información poblada.
    """
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
        deck_cards = []
        deck_name = root.split('\\')[-1]
        reverse_path = recorrer_archivo(files, root, deck_name, deck_cards)

    deck_cards_filtrado = rd.sample(deck_cards, cantidad_cartas)

    for index in range(len(deck_cards_filtrado)):
        deck_cards_filtrado[index]['path_imagen_reverso'] = reverse_path
        
        filter_hp = deck_cards_filtrado[index].get('hp')
        filter_atk = deck_cards_filtrado[index].get('atk')
        filter_defense = deck_cards_filtrado[index].get('def')

        contenedor_hp += filter_hp
        contenedor_atk += filter_atk
        contenedor_def += filter_defense

        carta_dict["max_stats"]["hp"] = contenedor_hp
        carta_dict["max_stats"]["atk"] = contenedor_atk
        carta_dict["max_stats"]["def"] = contenedor_def
    
    carta_dict['cartas'][deck_name] = deck_cards_filtrado
    
    return carta_dict

def achicar_imagen_card(path_imagen: str, porcentaje: int) -> pg.Surface:
    """ 
    Parametros: Recibe:\n
    -"path_imagen" Ruta de la imagen a trabajar \n
    -"porcentaje" Porcentaje a modificar.

    ¿Qué hace?: Recibe la imagen y lo primero que hace es cargarla.\n
    Acto seguido procede a definir el alto y el ancho con los valores del parámetro. \n
    Lo transforma en escala, y devuelve la imagen con las nuevas medidas.

    ¿Qué Devuelve?: Una superficie de PG
    """
    imagen_raw = pg.image.load(path_imagen)
    alto = int(imagen_raw.get_height() * float(f'0.{porcentaje}'))
    ancho = int(imagen_raw.get_width() * float(f'0.{porcentaje}'))
    imagen_final = pg.transform.scale(imagen_raw, (ancho, alto))
    return imagen_final

def generar_mazo(mazo_dict_original: list[dict]) -> list[dict]:
    """ 
    Parametros: Recibe:mazo_dict_original que es un listado de diccionarios.

    ¿Qué hace?: Inicializa una lista vacía, recorre el mazo que recibe por params\n
    Acto seguido inicializa las cartas con ayuda de "inicializar_carta", y una vez creada. \n
    Se agrega al listado, se mezcla y devuelve una lista de mazo mezclada y lista para usar

    ¿Qué Devuelve?: una lista de diccionarios
    """
    lista_mazo_resultado = []
    for card in mazo_dict_original:
        carta_final = carta.inicializar_carta(card, var.COORDENADA_CARTA_MAZO)
        lista_mazo_resultado.append(carta_final)
    rd.shuffle(lista_mazo_resultado)

    return lista_mazo_resultado

def parsear_entero(valor: str) -> int | str:
    """ 
    Parametros: Valor en string a parsear.

    ¿Qué hace?: Recibe un valor en string, aplica isdigit para devolverlo en numérico\n
    Con la finalidad de asegurarse que sea un valor entero.

    ¿Qué Devuelve?: Un string o int pero en entero
    """
    if valor.isdigit():
        return int(valor)
    return valor

def mapear_valores(matriz: list[list], indice_a_aplicar: int, callback) -> None:
    """ 
    Parametros:\n
        -"matriz" lista de lista para recorrer su largo \n
        -"indice_a_aplicar" número para posicionar. \n
        -"callback" función "parsear_entero" \n

    ¿Qué hace?: 
        Recorre la matriz recibida por params para almacenar su valor\n
        Para luego usar el callback para pasarlo a entero.

    ¿Qué Devuelve?:
        None
    """
    for indice_fila in range(len(matriz)):
        valor = matriz[indice_fila][indice_a_aplicar]
        matriz[indice_fila][indice_a_aplicar] = callback(valor)

def cargar_ranking() -> list:
    """ 
    Parametros:\n
        None

    ¿Qué hace?: 
        Inicializa una lista vacía, abre el archivo CSV solo para leer\n
        Lo recorre separando linea por linea con "split", para luego \n
        Agregar información a la lista de ranking. Luego de eso mapea \n
        Los valores, y se define de qué manera mostrarlo, por short, \n
        En qué fila, etc.

    ¿Qué Devuelve?:
        Listado de ranking
    """
    ranking = []
    with open(var.RUTA_RANKING_CSV, 'r', encoding='utf-8') as file:
        lineas = file.read()
        for linea in lineas.split('\n'):
            if linea:
                ranking.append(linea.split(','))
    mapear_valores(ranking, 1, parsear_entero)
    ranking.sort(key=lambda fila: fila[1], reverse=True)
    
    return ranking

def guardar_ranking(jugador_dict: dict) -> None:
    """ 
    Parametros:\n
        jugador_dict: Diccionario de jugador

    ¿Qué hace?: 
        Abre el archivo CSV en "append", para agregar información sin borrar.\n
        Define la información para agregar, que sería el nombre del usuario y puntaje \n
        Y por último lo escribe en el archivo \n

    ¿Qué Devuelve?:
        None
    """
    with open(var.RUTA_RANKING_CSV, 'a', encoding='utf-8') as file:
        #Mensaje con la data del nombre y puntaje
        data = f'{jugador_dict.get('nombre')},{jugador_dict.get('puntaje_actual')}\n'
        file.write(data)
        print(f'Datos guardados con éxito! -> {data}')

def cargar_configs(path: str) -> dict:
    """ 
    Parametros:\n
        path: Recibe la ruta del archivo con las configuraciones

    ¿Qué hace?: 
        Crea un dict vacío, luego abre el archivo (de la ruta de params) en formato lectura \n
        Se carga ese archivo JSON al dict creado previamente, y retorna el dict

    ¿Qué Devuelve?:
        Diccionario con las configuraciones en formato JSON
    """
    configuraciones = {}
    #Leemos "r" en la ruta pasada en param
    with open(path, 'r', encoding='utf-8') as file:
        configuraciones = json.load(file)
    #Cargamos la info del json, y lo devolvemos
    return configuraciones