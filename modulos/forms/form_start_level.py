import pygame as pg
import modulos.forms.base_form as base_form
import modulos.variables as var
from utn_fra.pygame_widgets import (Button, Label)
import modulos.auxiliar as aux
import modulos.nivel_cartas as nivel_cartas
import random as rd
from utn_fra.pygame_widgets import(
    Button, Label, TextPoster, ButtonImage
)
#rd.shuffle(fra.lista_frases)

def init_form_start_level(dict_form_data: dict, jugador: dict):
    # print(f"cartas: {cartas}")
    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = jugador
    form['level'] = nivel_cartas.inicializar_nivel_cartas(form.get('jugador'), form.get('screen'), form.get('level_number'))
    
    form['clock'] = pg.time.Clock()

    #Acá desarrollamos una función que vaya restando el tiempo
    # form['level_timer'] = var.TIMER #2000 segundos de base, a modificar
    form['first_last_timer'] = pg.time.get_ticks()


    form['first_last_timer'] = pg.time.get_ticks()

    print(f"form Clock: {form.get('clock')}")
    form['texto'] = f'SCORE: {form.get('jugador').get('puntaje_actual')}'

    form['lbl_clock'] = Label(x=var.DIMENSION_PANTALLA[0] // 2, y=100,text=f'TIME LEFT: {form.get('level').get('level_timer')}', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=50)
    form['lbl_score'] = Label(x=250, y=50,text=form.get('texto'), screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=22)
    #Text Poster
    form['txp_info_card'] = TextPoster( #Probar volver a instalar pygame_widtget o utn_Fra, no aparece
        text='', screen=form.get('screen'), background_dimentions=(500, 100), background_coords=(390, 584),
        font_path=var.FUENTE_SAIYAN, font_size=25, color=(0,255,0), background_color=(0,0,0)
    )

    form['btn_bonus_1'] = ButtonImage
    
    form['widgets_list'] = [
        form.get('lbl_clock'), 
        form.get('lbl_score'), 
        form.get('txp_info_card')
    ]
    
    base_form.forms_dict[dict_form_data.get('name')] = form
    
    return form


def select_bonus(bonus_name: str):
    pass

def actualizar_timer(form_data: dict):
    if form_data.get('level').get('level_timer') > 0:
        tiempo_actual = pg.time.get_ticks()
        #el first_last_timer, guarda la hora más reciente, la más actual
        #Si el tiempo actual, menos el valor que se actualizó el marcador
        #Superó los 1000 de valor, pasó un segundo, entonces se actualizan los timers
        if tiempo_actual - form_data.get('first_last_timer') > 1000:
            #Restamos 1seg al lever timer, y el first_last_timer
            form_data.get('level')['level_timer'] -= 1 #Este valor es el que se va a mostrar
            form_data['first_last_timer'] = tiempo_actual #Y este el que se toma como referencia para calcular

def click_volver(parametro: str):
    print(parametro)
    base_form.set_active(parametro)

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
    
    
    
def draw(form_data: dict):
    base_form.draw(form_data)
    nivel_cartas.draw(form_data.get('level'))


def inicializar_juego(form_data: dict):
    form_data['cards_list'] = aux.cargar_ranking()[:10]
    init_game(form_data)

def update(form_data: dict, event_list: list[pg.event.Event]):
    #if form_data.get('active'):
    #    inicializar_juego(form_data)
    base_form.update(form_data)
    form_data['lbl_clock'].update_text(f'TIME LEFT: {form_data.get('level').get('level_timer')}', (255,0,0)) #Valor actualizado, y color del mismo
    nivel_cartas.update(form_data.get('level'), event_list)

    form_data['lbl_score'].update_text(f'SCORE: {form_data.get('jugador').get('puntaje_actual')}', (255,0,0)) #Valor actualizado, y color del mismo


    mazo_vistas = form_data.get('level').get('cartas_mazo_juego_final_vistas')
    #
    if mazo_vistas:
        form_data['txp_info_card'].update_text(str(mazo_vistas[-1].get('atk'))) #Escribimos el ataque

    form_data['clock'].tick(var.FPS)
    #Actualizamos el timer
    actualizar_timer(form_data)


    #Pequeño for para obtener coordenadas
    for evento in event_list:
        if evento.type == pg.MOUSEBUTTONDOWN:
            print(f"Coordenada: {evento.pos}")   
        