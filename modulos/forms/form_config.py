import pygame as pg
import modulos.forms.base_form as base_form
import modulos.variables as var
import modulos.auxiliar as aux
from utn_fra.pygame_widgets import (
    Button, Label, TextBox, TextBoxSound
)

def init_form_config(dict_form_data: dict):
    form = base_form.create_base_form(dict_form_data)
    
    form['texto'] = 'HOLA MUNDO'
    form['lbl_titulo'] = Label(x=var.DIMENSION_PANTALLA[0]//2, y=100,text='DRAGON BALL Z TCG', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=50)
    form['lbl_sub_titulo'] = Label(x=var.DIMENSION_PANTALLA[0]//2, y=175,text='Options', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=40)
    form['lbl_music_on'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=325,text='MUSIC ON', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=22, on_click=click_music_on, on_click_param = dict_form_data)
    form['lbl_music_off'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=375,text='MUSIC OFF', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=22, on_click=click_music_off, on_click_param=dict_form_data)
    form['btn_volver'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=580, text='BACK TO MENU', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=30, on_click=click_volver, on_click_param='form_main_menu')
    
    
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
    var.SOUND_CLICK.play()
    base_form.set_active(parametro)

def click_music_on(dict_form_data: dict):
    #aux.inicializar_musica(dict_form_data)
    base_form.active_music(base_form.forms_dict[dict_form_data.get('name')])
    base_form.play_music(base_form.forms_dict[dict_form_data.get('name')])

def click_music_off(dict_form_data: dict):
    base_form.cancel_music(dict_form_data)
    #aux.terminar_musica(parametro)
    #base_form.set_active(dict_form_data)

def draw(form_data: dict):
    base_form.draw(form_data)
    base_form.draw_widgets(form_data)


def update(form_data: dict, event_list: list[pg.event.Event]):
    base_form.update(form_data)
    #Pequeño for para obtener coordenadas
    for evento in event_list:
        if evento.type == pg.MOUSEBUTTONDOWN:
            print(f"Coordenada: {evento.pos}")   

