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
    form['lbl_titulo'] = Label(
        x=var.CENTRO_DIMENSION_X, y=var.CENTRO_DIMENSION_Y - 250,
        text=var.MAIN_TITLE, screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=75)
    form['lbl_subtitle'] = Label(
        x=400, y=var.CENTRO_DIMENSION_Y - 175,
        text=form.get('texto'), screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=50)
    form['btn_select'] = Button(
        x=var.CENTRO_DIMENSION_X, y=var.CENTRO_DIMENSION_Y + 175,
        text='SELECCIONAR', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=22, on_click=click_select_bonus, on_click_param=form)
    form['btn_back'] = Button(
        x=var.CENTRO_DIMENSION_X, y=var.CENTRO_DIMENSION_Y + 250,
        text='VOLVER AL MENU', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=22, on_click=click_change_form, on_click_param='form_start_level')

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
    #Lee la info que esté en bonus_info, y en base a eso selecciona el bonus
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

#Función para actualizar "btn_select" label o Button
def update_button_bonus(form_dict: dict, new_text: str):
    form_dict['bonus_info'] = new_text
    #Actualiza el texto con el bonus que seleccionó el usuario
    form_dict.get('widgets_list')[2].update_text(form_dict.get('bonus_info'), var.COLOR_ROJO)

def draw(form_dict: dict):
    base_form.draw(form_dict)

def update(form_data: dict, event_list: list[pg.event.Event]):
    base_form.update(form_data)
    #Pequeño for para obtener coordenadas
    for evento in event_list:
        if evento.type == pg.MOUSEBUTTONDOWN:
            print(f"Coordenada: {evento.pos}")   