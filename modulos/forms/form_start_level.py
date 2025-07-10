import pygame as pg
import modulos.forms.base_form as base_form
import modulos.variables as var
from utn_fra.pygame_widgets import (Button, Label)
import modulos.auxiliar as aux
import modulos.nivel_cartas as nivel_cartas
import modulos.forms.form_bonus as form_bonus
import random as rd
from utn_fra.pygame_widgets import(
    Button, Label, TextPoster, ButtonImage
)
def init_form_start_level(dict_form_data: dict, jugador: dict):
    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = jugador
    form['level'] = nivel_cartas.inicializar_nivel_cartas(form.get('jugador'), form.get('screen'), form.get('level_number'))
    
    form['clock'] = pg.time.Clock()
    form['bonus_shield_used'] = False
    form['bonus_heal_used'] = False
    #Acá desarrollamos una función que vaya restando el tiempo
    # form['level_timer'] = var.TIMER #2000 segundos de base, a modificar
    form['first_last_timer'] = pg.time.get_ticks()

    print(f"form Clock: {form.get('clock')}")
    form['texto'] = f'SCORE: {form.get('jugador').get('puntaje_actual')}'

    contenedor_max_hp_jugador = form.get('level').get('jugador').get('vida_total')
    print(f"contenedor_max_hp_jugador: {contenedor_max_hp_jugador}")
    form['lbl_hp'] = Label(x=200, y=500,text=f'HP: {form.get('level').get('jugador').get('vida_total')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=22)
    form['lbl_clock'] = Label(x=950, y=50,text=f'TIME LEFT: {form.get('level').get('level_timer')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=22)
    form['lbl_score'] = Label(x=150, y=50,text=form.get('texto'), screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=22)
    #Text Poster
    form['txp_info_card'] = TextPoster( #Probar volver a instalar pygame_widtget o utn_Fra, no aparece
        text='', screen=form.get('screen'), background_dimentions=(500, 100), background_coords=(390, 584),
        font_path=var.FUENTE_SAIYAN, font_size=25, color=(0,255,0), background_color=(0,0,0)
    )

    form['btn_bonus_play_hand'] = ButtonImage(
        x=1200, y=var.CENTRO_DIMENSION_Y + 25, width=126, height=40,
        text='shield', screen=form.get('screen'), image_path='./modulos/assets/img/buttons_image/btn_play_hand.png', 
        on_click=select_bonus, on_click_param={'form': form, 'bonus': 'shield'}
    )
    form['btn_bonus_shield'] = ButtonImage(
        x=1200, y=var.CENTRO_DIMENSION_Y + 220, width=126, height=40,
        text='shield', screen=form.get('screen'), image_path='./modulos/assets/img/buttons_image/shield.png', 
        on_click=select_bonus, on_click_param={'form': form, 'bonus': 'shield'}
    )
    form['btn_bonus_heal'] = ButtonImage(
        x=1200, y=var.CENTRO_DIMENSION_Y + 270,width=126, height=40,
        text='heal', screen=form.get('screen'), image_path='./modulos/assets/img/buttons_image/heal.png', 
        on_click=select_bonus, on_click_param={'form': form, 'bonus': 'heal'}
    )
    
    form['btn_bonus_shield_used'] = ButtonImage(
        x=1170, y=var.CENTRO_DIMENSION_Y - 150, width=50, height=50,
        text='shield', screen=form.get('screen'), image_path='./modulos/assets/img/icons/icon_shield.png', 
    )
    form['btn_bonus_heal_used'] = ButtonImage(
        x=1230, y=var.CENTRO_DIMENSION_Y - 150,width=50, height=50,
        text='heal', screen=form.get('screen'), image_path='./modulos/assets/img/icons/icon_heal.png', 
    )
    
    form['widgets_list'] = [
        form.get('lbl_clock'), 
        form.get('lbl_score'),
        form.get('btn_bonus_shield'),
        form.get('btn_bonus_heal'),
        form.get('btn_bonus_play_hand'),
        form.get('lbl_hp'),
    ]
    
    base_form.forms_dict[dict_form_data.get('name')] = form
    
    return form


def select_bonus(form_y_bonus_name: dict):
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict['form_bonus'])
    #Recibimos un dict, activamos la vista de form_bonus
    #Actualizamos los botones, y también revisamos si ya utilizó
    #Algunos de los bonus, y cambia su valor de Bool
    #Activamos la vista de form_bonus
    base_form.set_active('form_bonus')

    #Le pasamos por parámetro el texto del bonus que el usuario seleccionó para mostrar en pantalla
    #Y a la vez, para que se guarde el valor
    form_bonus.update_button_bonus(base_form.forms_dict['form_bonus'], form_y_bonus_name.get('bonus'))
    

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

def events_handler(events_list: list[pg.event.Event]):
    for evento in events_list:
            #Si el usuario presiona una tecla
            if evento.type == pg.KEYDOWN:
                #Y si presiona la tecla de escape, lo
                if evento.key == pg.K_ESCAPE:
                    base_form.set_active('form_main_menu')
                elif evento.key == pg.K_SPACE:
                    base_form.set_active('form_pause')
                    base_form.stop_music()
                    base_form.play_music(base_form.forms_dict['form_pause'])

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

    widgets_list = form_data.get('widgets_list')
    #ESTO HACERLO UNA FUNCIÓN, YA QUE SE REPITE EN EL DRAW Y EL UPDATE
    for widget_index in range(len(form_data.get('widgets_list'))):
        #Si está en true, ya se usó
        #LLAMAR ACÁ AL DICT DE FORM_BONUS Y QUE LEAN DE AHÍ PARA MOSTRARLOS O NO
        if widget_index == 2 and form_data.get('bonus_shield_used'):
            #Si es true y ya se usó, no hace nada, continúa
            widgets_list.append(form_data.get('btn_bonus_shield_used'))
            continue
        if widget_index == 3 and form_data.get('bonus_heal_used'):
            widgets_list.append(form_data.get('btn_bonus_heal_used'))
            continue
        form_data.get('widgets_list')[widget_index].draw()

    nivel_cartas.draw(form_data.get('level'))


def inicializar_juego(form_data: dict):
    form_data['cards_list'] = aux.cargar_ranking()[:10]
    init_game(form_data)

def update(form_data: dict, event_list: list[pg.event.Event]):
    # base_form.update(form_data)
    form_data['lbl_clock'].update_text(f'TIME LEFT: {form_data.get('level').get('level_timer')}', (255,0,0)) #Valor actualizado, y color del mismo
    form_data['lbl_score'].update_text(f'SCORE: {form_data.get('jugador').get('puntaje_actual')}', (255,0,0)) #Valor actualizado, y color del mismo
    form_data['lbl_hp'].update_text(f'HP: {form_data.get('level').get('jugador').get('vida_total')}', (255,0,0)) #Valor actualizado, y color del mismo
    
    widgets_list = form_data.get('widgets_list')
    #Recorre la lista de widgets, si ya está usado el shield o escudo, añade a la lista
    #Otro widget con el ícono ya en uso. Queda agregar que después del próximo ataque se borre 
    # (se puede remover, no deja de ser una lista)
    for widget_index in range(len(widgets_list)):
        #Si está en true, ya se usó
        if widget_index == 2 and form_data.get('bonus_shield_used'):
            #Si es true y ya se usó, no hace nada, continúa
            widgets_list.append(form_data.get('btn_bonus_shield_used'))
            continue
        if widget_index == 3 and form_data.get('bonus_heal_used'):
            widgets_list.append(form_data.get('btn_bonus_heal_used'))
            continue
        widgets_list[widget_index].update()
    
    nivel_cartas.update(form_data.get('level'), event_list)
    

    mazo_vistas = form_data.get('level').get('cartas_mazo_juego_final_vistas')
    #
    if mazo_vistas:
        form_data['txp_info_card'].update_text(str(mazo_vistas[-1].get('atk'))) #Escribimos el ataque

    form_data['clock'].tick(var.FPS)
    #Actualizamos el timer
    actualizar_timer(form_data)

    if nivel_cartas.juego_terminado(form_data.get('level')):
        base_form.stop_music()
        base_form.play_music(base_form.forms_dict['form_enter_name'])
        base_form.set_active('form_enter_name')
    #Pequeño for para obtener coordenadas
    for evento in event_list:
        if evento.type == pg.MOUSEBUTTONDOWN:
            print(f"Coordenada: {evento.pos}")   
    events_handler(event_list)