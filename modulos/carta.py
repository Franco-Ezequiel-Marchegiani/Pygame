import pygame as pg
import modulos.auxiliar as aux


def inicializar_carta(carta_dict: dict, coordenadas: tuple[int, int]) -> dict:
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
    #Setea el puntaje
    card_dict['puntaje'] = puntaje

def draw_carta(card_data: dict, screen: pg.Surface):
    #Función que simula el evento de tirar una carta, revisa si es visible o no para mostrar el frente o dorso
    if card_data.get('visible'):
        screen.blit(card_data.get('imagen'), card_data.get('rect'))
    else:
        screen.blit(card_data.get('imagen_reverso'), card_data.get('rect'))

def asignar_coordenadas_carta(carta_dict: dict, nueva_coordenada: tuple[int,int]):
    carta_dict['rect'].topleft = nueva_coordenada
    carta_dict['rect'].topleft = nueva_coordenada

def cambiar_visibilidad_carta(carta_dict: dict):
    carta_dict['visible'] = True