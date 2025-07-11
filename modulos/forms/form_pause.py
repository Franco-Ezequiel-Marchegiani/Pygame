import pygame as pg
import modulos.forms.base_form as base_form
import modulos.variables as var
from utn_fra.pygame_widgets import (
    Button, Label
)

def init_form_pause(dict_form_data: dict):
    form = base_form.create_base_form(dict_form_data)
    
    form['title'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=var.DIMENSION_PANTALLA[1] // 2 - 250,
        text=var.MAIN_TITLE, screen=form.get('screen'), 
        font_path=var.FUENTE_SAIYAN, font_size=75, color=var.COLOR_NEGRO
    )
    form['subtitle'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=var.DIMENSION_PANTALLA[1] // 2 - 175,
        text='PAUSE', screen=form.get('screen'), 
        font_path=var.FUENTE_SAIYAN, font_size=50, color=var.COLOR_NEGRO
    )
    
    form['btn_back'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=var.DIMENSION_PANTALLA[1] // 2 + 175,
        text="BACK TO THE MENU", screen=form.get('screen'), 
        font_path=var.FUENTE_SAIYAN, color=var.COLOR_NEGRO,
        on_click=click_change_form, on_click_param='form_main_menu'
    )
    
    form['btn_resume'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=var.DIMENSION_PANTALLA[1] // 2 + 250,
        text="BACK TO THE GAME", screen=form.get('screen'), 
        font_path=var.FUENTE_SAIYAN, color=var.COLOR_NEGRO,
        on_click=click_change_form, on_click_param='form_start_level'
    )
    
    form['widgets_list'] = [
        form.get('title'), form.get('subtitle'),
        form.get('btn_back'), form.get('btn_resume')
    ]
    
    base_form.forms_dict[form.get('name')] = form
    
    return form

def click_change_form(param: str):
    var.SOUND_CLICK.play()
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict[param])
    base_form.set_active(param)

def draw(form_dict: dict):
    base_form.draw(form_dict)
    base_form.draw_widgets(form_dict)

def update(form_dict: dict):
    base_form.update(form_dict)
    base_form.draw_widgets(form_dict)

#Ver si puedo globalizar este draw y update, y llamarlo en cada función, ya que se repiten mucho
def update(form_data: dict, event_list: list[pg.event.Event]):
    base_form.update(form_data)
    #Pequeño for para obtener coordenadas
    for evento in event_list:
        if evento.type == pg.MOUSEBUTTONDOWN:
            print(f"Coordenada: {evento.pos}")   