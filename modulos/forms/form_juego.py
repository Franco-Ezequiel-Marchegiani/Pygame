import pygame as pg
import modulos.forms.base_form as base_form
import modulos.variables as var
from utn_fra.pygame_widgets import (Button, Label)
import modulos.auxiliar as aux
import random as rd

#rd.shuffle(fra.lista_frases)

def init_form_juego(dict_form_data: dict):
    # print(f"cartas: {cartas}")
    form = base_form.create_base_form(dict_form_data)
    
    form['ranking_screen'] = []
    form['cards_list_dictionary'] = []
    form['cards_list_vistas'] = []

    form['texto'] = 'HOLA MUNDO - GAMEPLAY'
    form['lbl_titulo'] = Label(x=var.DIMENSION_PANTALLA[0]//2, y=100,text='La PYTHONisa del Tarot', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=50)
    form['lbl_texto'] = Label(x=400, y=200,text=form.get('texto'), screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=22)
    form['btn_volver'] = Button(x=993, y=580, text='VOLVER', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=30, on_click=click_volver, on_click_param='form_main_menu')
    
    
    form['widgets_list'] = [
        form.get('lbl_titulo'), 
        form.get('lbl_texto'), 
        form.get('btn_volver')
    ]
    
    base_form.forms_dict[dict_form_data.get('name')] = form
    
    return form

def click_volver(parametro: str):
    print(parametro)
    base_form.set_active(parametro)

def draw(form_data: dict):
    base_form.draw(form_data)

def init_game(form_data: dict):

    cartas = aux.generar_bd(var.RUTA_MAZO_MAIN)
    #Dentro de todas las cartas, se obtiene por "decks"
    deck_purple_deck_expansion_1 = cartas.get('cartas').get('purple_deck_expansion_1')
    deck_purple_deck_expansion_2 = cartas.get('cartas').get('purple_deck_expansion_2')
    #Acá se agregaban las frases a los decks
        # deck_purple_deck_expansion_1 = aux.asignar_frases(deck_purple_deck_expansion_1, fra.lista_frases)
        # deck_purple_deck_expansion_2 = aux.asignar_frases(deck_purple_deck_expansion_2, fra.lista_frases)

    #Acá genera el mazo y tmb llama al dic "carta"
    lista_cartas_dictionary = aux.generar_mazo(deck_purple_deck_expansion_1)

    #lista_cartas_dictionary.extend(aux.generar_mazo(deck_purple_deck_expansion_2))
    rd.shuffle(lista_cartas_dictionary)

    lista_cartas_dictionary = lista_cartas_dictionary[0:10]
    lista_cartas_vistas = []

    form_data['ranking_screen'] = []
    matrix = form_data.get('cards_list')
    for indice_fila in range(len(matrix)):
        
        fila = matrix[indice_fila]
        
        """
        
        1                   fulano              20
        2                   mengano             15
        
        """
        
        # numero
        form_data['ranking_screen'].append(
            Label(x=var.DIMENSION_PANTALLA[0]//2 - 220, y=var.DIMENSION_PANTALLA[1]//2.9+indice_fila*31,text=f'{indice_fila + 1}', screen=form_data.get('screen'), font_path=var.FUENTE_SAIYAN, color=var.COLOR_NARANJA, font_size=40)
        )
        
        # nombre
        form_data['ranking_screen'].append(
            Label(x=var.DIMENSION_PANTALLA[0]//2, y=var.DIMENSION_PANTALLA[1]//2.9+indice_fila*31,text=f'{fila[0]}', screen=form_data.get('screen'), font_path=var.FUENTE_SAIYAN, color=var.COLOR_NARANJA, font_size=40)
        )
        
        # score
        form_data['ranking_screen'].append(
            Label(x=var.DIMENSION_PANTALLA[0]//2 + 220, y=var.DIMENSION_PANTALLA[1]//2.9+indice_fila*31,text=f'{fila[1]}', screen=form_data.get('screen'), font_path=var.FUENTE_SAIYAN, color=var.COLOR_NARANJA, font_size=40)
        )
    
    

def inicializar_juego(form_data: dict):
    form_data['cards_list'] = aux.cargar_ranking()[:10]
    init_game(form_data)

def update(form_data: dict, event_list: list[pg.event.Event]):
    if form_data.get('active'):
        inicializar_juego(form_data)
    base_form.update(form_data)
    #Pequeño for para obtener coordenadas
    for evento in event_list:
        if evento.type == pg.MOUSEBUTTONDOWN:
            print(f"Coordenada: {evento.pos}")   
        