import pygame as pg
import modulos.forms.base_form as base_form
import modulos.variables as var
from utn_fra.pygame_widgets import (Button, Label)
import modulos.auxiliar as aux
import modulos.nivel_cartas as nivel_cartas
import modulos.forms.form_bonus as form_bonus

import random as rd
from utn_fra.pygame_widgets import(
    Button, Label, TextPoster, ButtonImage, ImageLabel
)
def init_form_start_level(dict_form_data: dict, jugador: dict):
    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = jugador
    form['level'] = nivel_cartas.inicializar_nivel_cartas(form.get('jugador'), form.get('screen'), form.get('level_number'))
    
    form['clock'] = pg.time.Clock()
    form['bonus_shield_used'] = False
    form['bonus_heal_used'] = False
    form['bonus_shield_active'] = False
    form['bonus_heal_active'] = False
    #Acá desarrollamos una función que vaya restando el tiempo
    # form['level_timer'] = var.TIMER #2000 segundos de base, a modificar
    form['first_last_timer'] = pg.time.get_ticks()

    print(f"form Clock: {form.get('clock')}")
    form['texto'] = f'SCORE: {form.get('jugador').get('puntaje_actual')}'

    form['lbl_hp'] = Label(x=190, y=530,text=f'HP: {form.get('level').get('jugador').get('vida_actual')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=40, color=var.COLOR_AMARILLO)
    form['lbl_atk'] = Label(x=130, y=560,text=f'ATK: {form.get('level').get('jugador').get('atk_total')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=16, color=var.COLOR_AMARILLO)
    form['lbl_def'] = Label(x=245, y=560,text=f'DEF: {form.get('level').get('jugador').get('def_total')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=16, color=var.COLOR_AMARILLO)
    #Stats rival
    form['lbl_hp_rival'] = Label(x=190, y=200,text=f'HP: {form.get('level').get('rival').get('vida_actual')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=40, color=var.COLOR_AMARILLO)
    form['lbl_atk_rival'] = Label(x=130, y=230,text=f'ATK: {form.get('level').get('rival').get('atk_total')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=16, color=var.COLOR_AMARILLO)
    form['lbl_def_rival'] = Label(x=245, y=230,text=f'DEF: {form.get('level').get('rival').get('def_total')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=16, color=var.COLOR_AMARILLO)
    
    form['lbl_clock'] = Label(x=450, y=40,text=f'TIME LEFT: {form.get('level').get('level_timer')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=22)
    form['lbl_score'] = Label(x=150, y=50,text=form.get('texto'), screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=44)
    #Text Poster
    form['txp_info_card'] = TextPoster( #Probar volver a instalar pygame_widtget o utn_Fra, no aparece
        text='', screen=form.get('screen'), background_dimentions=(500, 100), background_coords=(390, 584),
        font_path=var.FUENTE_SAIYAN, font_size=25, color=(0,255,0), background_color=(0,0,0)
    )
    # ImageLabel
    form['btn_bonus_play_hand'] = ButtonImage(
        x=1200, y=var.CENTRO_DIMENSION_Y + 25, width=126, height=40,
        text='shield', screen=form.get('screen'), image_path='./modulos/assets/img/buttons_image/btn_play_hand.png', 
        on_click=nivel_cartas.jugar_mano, on_click_param= form.get('level')
    )
    form['btn_bonus_shield'] = ButtonImage(
        x=1200, y=var.CENTRO_DIMENSION_Y + 220, width=126, height=40,
        text='shield', screen=form.get('screen'), image_path='./modulos/assets/img/buttons_image/shield.png', 
        on_click=select_bonus, on_click_param='shield'
    )
    form['btn_bonus_heal'] = ButtonImage(
        x=1200, y=var.CENTRO_DIMENSION_Y + 270,width=126, height=40,
        text='heal', screen=form.get('screen'), image_path='./modulos/assets/img/buttons_image/heal.png', 
        on_click=select_bonus, on_click_param='heal'
    )
    
    form['btn_bonus_shield_active'] = ButtonImage(
        x=1170, y=var.CENTRO_DIMENSION_Y - 150, width=50, height=50,
        text='shield', screen=form.get('screen'), image_path='./modulos/assets/img/icons/icon_shield.png', 
    )
    form['btn_bonus_heal_active'] = ButtonImage(
        x=1230, y=var.CENTRO_DIMENSION_Y - 150,width=50, height=50,
        text='heal', screen=form.get('screen'), image_path='./modulos/assets/img/icons/icon_heal.png', 
    )
    
    form['widgets_list'] = [
        form.get('lbl_clock'), 
        form.get('lbl_score'),
        form.get('btn_bonus_play_hand'),
        form.get('lbl_hp'),
        form.get('lbl_atk'),
        form.get('lbl_def'),
        form.get('lbl_hp_rival'),
        form.get('lbl_atk_rival'),
        form.get('lbl_def_rival'),
    ]
    
    base_form.forms_dict[dict_form_data.get('name')] = form
    
    return form


def select_bonus(bonus_name: str):
    print(f"Print")
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict['form_bonus'])
    #Recibimos un dict, activamos la vista de form_bonus
    #Actualizamos los botones, y también revisamos si ya utilizó
    #Algunos de los bonus, y cambia su valor de Bool
    #Activamos la vista de form_bonus
    form_bonus.update_button_bonus(base_form.forms_dict['form_bonus'], bonus_name)

    #Le pasamos por parámetro el texto del bonus que el usuario seleccionó para mostrar en pantalla
    #Y a la vez, para que se guarde el valor
    base_form.set_active('form_bonus')
    
    base_form.play_bonus_music(var.RUTA_SONIDO_BONUS_INICIO)
    pg.mixer.music.set_volume(0.2)
    

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

    
def condition_btn_draw(form_data: dict, bonus_used: str, btn_active: str, btn_form_active: str, btn_bonus: str):
    if form_data.get(bonus_used):
        pass
    else:
        if form_data.get(btn_active):
            form_data.get(btn_form_active).draw()
        else:
            form_data.get(btn_bonus).draw()
def draw(form_data: dict):
    base_form.draw(form_data)
    
    widgets_list = form_data.get('widgets_list')
    #ESTO HACERLO UNA FUNCIÓN, YA QUE SE REPITE EN EL DRAW Y EL UPDATE
    for widget_index in range(len(widgets_list)):

        form_data.get('widgets_list')[widget_index].draw()
    
    #Hacer acá mismo una condicional con la bandera, y hacer un draw acá, no añadirlo en la lista
    condition_btn_draw(form_data, 
    'bonus_shield_used',
    'bonus_shield_active',
    'btn_bonus_shield_active',
    'btn_bonus_shield'
    )
    condition_btn_draw(form_data, 
    'bonus_heal_used',
    'bonus_heal_active',
    'btn_bonus_heal_active',
    'btn_bonus_heal'
    )


    nivel_cartas.draw(form_data.get('level'))


def inicializar_juego(form_data: dict):
    form_data['level'] = nivel_cartas.reiniciar_nivel(
            form_data.get('level'), form_data.get('jugador'), 
            form_data.get('screen'), form_data.get('level_number')
    )
    nivel_cartas.inicializar_data_nivel(form_data.get('level'))


    form_data.get('widgets_list')[2] = ButtonImage(
        x=1200, y=var.CENTRO_DIMENSION_Y + 25, width=126, height=40,
        text='shield', screen=form_data.get('screen'), image_path='./modulos/assets/img/buttons_image/btn_play_hand.png', 
        on_click=nivel_cartas.jugar_mano, on_click_param= form_data.get('level')
    )

def condition_btn_update(form_data: dict, bonus_used: str, btn_active: str, btn_form_active: str, btn_bonus: str):
    if form_data.get(bonus_used):
        pass
    else:
        if form_data.get(btn_active):
            form_data.get(btn_form_active).update()
        else:
            form_data.get(btn_bonus).update()

def update(form_data: dict, event_list: list[pg.event.Event]):
    # base_form.update(form_data)
    form_data['lbl_clock'].update_text(f'TIME LEFT: {form_data.get('level').get('level_timer')}', (255,0,0)) #Valor actualizado, y color del mismo
    form_data['lbl_score'].update_text(f'SCORE: {form_data.get('jugador').get('puntaje_actual')}', (255,0,0)) #Valor actualizado, y color del mismo
    #Actualiza stats jugador
    form_data['lbl_hp'].update_text(f'HP: {form_data.get('level').get('jugador').get('vida_actual')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    form_data['lbl_atk'].update_text(f'ATK: {form_data.get('level').get('jugador').get('atk_total')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    form_data['lbl_def'].update_text(f'DEF: {form_data.get('level').get('jugador').get('def_total')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    #Actualiza stats rival
    form_data['lbl_hp_rival'].update_text(f'HP: {form_data.get('level').get('rival').get('vida_actual')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    form_data['lbl_atk_rival'].update_text(f'ATK: {form_data.get('level').get('rival').get('atk_total')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    form_data['lbl_def_rival'].update_text(f'DEF: {form_data.get('level').get('rival').get('def_total')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    
    widgets_list = form_data.get('widgets_list')
    

    #Recorre la lista de widgets, si ya está usado el shield o escudo, añade a la lista
    #Otro widget con el ícono ya en uso. Queda agregar que después del próximo ataque se borre 
    # (se puede remover, no deja de ser una lista)
    for widget_index in range(len(widgets_list)):

        widgets_list[widget_index].update()
    
    #Hacer una bandera nueva, y corroborar si está activado, y consumido.

    #En el bonus del shield, rebotar el daño del enemigo, y si pinta tmb el daño del jugador
    #Tmb aplica con críticos.
    #Hacer acá mismo una condicional con la bandera, y hacer un draw acá, no añadirlo en la lista
    condition_btn_update(form_data, 
    'bonus_shield_used',
    'bonus_shield_active',
    'btn_bonus_shield_active',
    'btn_bonus_shield'
    )
    condition_btn_update(form_data, 
    'bonus_heal_used',
    'bonus_heal_active',
    'btn_bonus_heal_active',
    'btn_bonus_heal'
    )
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
    events_handler(event_list)