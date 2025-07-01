import pygame as pg
import modulos.forms.base_form as base_form
import modulos.variables as var
from utn_fra.pygame_widgets import (
    Button, Label, TextBox, TextBoxSound
)

def init_form_config(dict_form_data: dict):
    form = base_form.create_base_form(dict_form_data)
    
    form['texto'] = 'HOLA MUNDO'
    form['lbl_titulo'] = Label(x=var.DIMENSION_PANTALLA[0]//2, y=100,text='DRAGON BALL Z TCG', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=50)
    form['lbl_sub_titulo'] = Label(x=var.DIMENSION_PANTALLA[0]//2, y=100,text='Options', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=40)
    form['lbl_music_on'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=350,text='MUSIC ON', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=22, on_click=click_music_on, on_click_param='music_on')
    form['lbl_music_off'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=400,text='MUSIC OFF', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=22, on_click=click_music_off, on_click_param='music_off')
    form['btn_volver'] = Button(x=993, y=580, text='VOLVER', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=30, on_click=click_volver, on_click_param='form_main_menu')
    
    
    form['widgets_list'] = [
        form.get('lbl_titulo'), 
        form.get('lbl_sub_titulo'), 
        form.get('lbl_music_on'), 
        form.get('lbl_music_off'), 
        form.get('btn_volver')
    ]
    
    base_form.forms_dict[dict_form_data.get('name')] = form
    

    return form

def click_volver(parametro: str):
    print(parametro)
    base_form.set_active(parametro)

def click_music_on(parametro: str):
    print(f"PONÉ LA MÚSICA!! {parametro}")
    #base_form.set_active(parametro)

def click_music_off(parametro: str):
    print(f"*Ruido de cd deteniendose {parametro}")
    #base_form.set_active(parametro)

def draw(form_data: dict):
    base_form.draw(form_data)



def update(form_data: dict, event_list: list[pg.event.Event]):
    base_form.update(form_data)
    #Pequeño for para obtener coordenadas
    for evento in event_list:
        if evento.type == pg.MOUSEBUTTONDOWN:
            print(f"Coordenada: {evento.pos}")   

