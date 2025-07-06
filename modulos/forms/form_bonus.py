import modulos.forms.base_form as base_form
import modulos.jugador as jugador_mod
import modulos.variables as var
import pygame as pg
from utn_fra.pygame_widgets import(
    Button, Label, TextBox
)

def init_form_bonus(dict_form_data: dict, jugador: dict):
    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = jugador
    form['bonus_info'] = ''

    form['lbl_titulo'] = Label(x=var.DIMENSION_PANTALLA[0]//2, y=var.DIMENSION_PANTALLA[1] // 2 - 250,text='La PYTHONisa del Tarot', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=75)
    form['lbl_subtitle'] = Label(x=400, y=var.DIMENSION_PANTALLA[1] // 2 - 175,text=form.get('texto'), screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=50)
    form['btn_select'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=var.DIMENSION_PANTALLA[1] // 2 + 175,text='SELECCIONAR', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=22, on_click=click_select_bonus, on_click_param=form)
    form['btn_back'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=var.DIMENSION_PANTALLA[1] // 2 + 250,text='VOLVER AL MENU', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=22, on_click=click_change_form, on_click_param='form_start_level')

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitle'),
        form.get('btn_select'),
        form.get('btn_back'),
    ]

    base_form.forms_dict[form.get('name')] = form

    return form

def click_change_form(param: str):
    base_form.set_active(param)

def click_select_bonus(form_dict: dict):
    option = form_dict.get('bonus_info')

    match option:
        case 'shield': #(Originialmente es un x2 en los puntos)
            jugador_mod.set_puntaje_actual(
                form_dict.get('jugador'),
                jugador_mod.get_puntaje_actual(form_dict.get('jugador')) * 2
            )
        case 'heal': #(Originialmente es un +50 en los puntos)
            jugador_mod.set_puntaje_actual(
                form_dict.get('jugador'),
                jugador_mod.get_puntaje_actual(form_dict.get('jugador')) + 50
            )
    #Sonido de Bonus meanwhile
    pg.time.wait(2000) #Espera 2 segs
    click_change_form('form_start_level') #o form_juego, la idea es volver a la partida

def update_button_bonus(form_dict: dict, new_text: str):
    form_dict['bonus_info'] = new_text

    form_dict.get('widgets_list')[2].update_text(form_dict.get('bonus_info'), var.COLOR_ROJO)

def draw(form_dict: dict):
    base_form.draw(form_dict)

def update(form_dict: dict):
    base_form.update(form_dict)