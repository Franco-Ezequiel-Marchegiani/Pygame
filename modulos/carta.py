import pygame as pg
import modulos.auxiliar as aux

def inicializar_carta(carta_dict: dict, coordenadas: tuple[int, int]) -> dict:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario y coordenadas

    ``¿Qué hace?:``
        Crea un diccionario y en él agrega los elementos claves para cada carta
    
    ``¿Qué Devuelve?:`` 
        Un diccionario, con la estructura base ya definida.
    """
    carta_dict_final = {}
    carta_dict_final['id'] = carta_dict.get('id')
    carta_dict_final['hp'] = carta_dict.get('hp')
    carta_dict_final['atk'] = carta_dict.get('atk')
    carta_dict_final['def'] = carta_dict.get('def')
    carta_dict_final['bonus'] = carta_dict.get('bonus')
    carta_dict_final['path_imagen_frente'] = carta_dict.get('path_imagen_frente')
    carta_dict_final['path_imagen_reverso'] = carta_dict.get('path_imagen_reverso')

    carta_dict_final['visible'] = False
    carta_dict_final['imagen'] = aux.achicar_imagen_card(carta_dict_final.get('path_imagen_frente'), 40)
    carta_dict_final['imagen_reverso'] = aux.achicar_imagen_card(carta_dict_final.get('path_imagen_reverso'), 40)

    carta_dict_final['rect'] = carta_dict_final.get('imagen').get_rect(topleft = coordenadas)
    carta_dict_final['rect'].x = coordenadas[0]
    carta_dict_final['rect'].y = coordenadas[1]

    carta_dict_final['rect_reverso'] = carta_dict_final.get('imagen_reverso').get_rect(topleft = coordenadas)
    carta_dict_final['rect_reverso'].x = coordenadas[0]
    carta_dict_final['rect_reverso'].y = coordenadas[1]

    return carta_dict_final

def set_puntaje(card_dict: dict, puntaje: int) -> None:
    """ 
    ``Parametros:`` 
        "card_dict" - información de la carta en formato dict
        "puntaje" - puntaje numérico

    ``¿Qué hace?:``
        Le asigna un valor de la variable "puntaje" recibido por params, al diccionario de carta
    
    ``¿Qué Devuelve?:`` 
        None
    """
    #Setea el puntaje
    card_dict['puntaje'] = puntaje

def draw_carta(card_data: dict, screen: pg.Surface) -> None:
    """ 
    ``Parametros:`` 
        - "card_dict" - información de la carta en formato dict
        - "screen" - superficie de PG

    ``¿Qué hace?:``
        Simula el evento de tirar una carta, revisa si es visible o no para mostrar el frente o dorso

    ``¿Qué Devuelve?:`` 
        None
    """
    if card_data.get('visible'):
        screen.blit(card_data.get('imagen'), card_data.get('rect'))
    else:
        screen.blit(card_data.get('imagen_reverso'), card_data.get('rect'))

def asignar_coordenadas_carta(carta_dict: dict, nueva_coordenada: tuple[int,int]) -> None:
    """ 
    ``Parametros:`` 
        "card_dict" - información de la carta en formato dict
        "nueva_coordenada" - Tupla de 2 ints con las nuevas coordenadas

    ``¿Qué hace?:``
        Asigna el valor de las nuevas coordenadas

    ``¿Qué Devuelve?:`` 
        None
    """
    carta_dict['rect'].topleft = nueva_coordenada
    carta_dict['rect'].topleft = nueva_coordenada

def cambiar_visibilidad_carta(carta_dict: dict) -> None:
    """ 
    ``Parametros:`` 
        - "card_dict" - información de la carta en formato dict
        - "screen" - superficie de PG

    ``¿Qué hace?:``
        Cambia el valor del elemento 'visible' a True, \n
        Para cambiar la visibilidad de la carta
    
    ``¿Qué Devuelve?:`` 
        None
    """
    carta_dict['visible'] = True