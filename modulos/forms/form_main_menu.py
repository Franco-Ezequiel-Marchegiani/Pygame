import pygame as pg
import sys
import modulos.forms.base_form as base_form
import modulos.variables as var
import modulos.auxiliar as aux
from utn_fra.pygame_widgets import (
    Button, Label, ButtonImage
)


def init_form_main_menu(dict_form_data: dict):
    form = base_form.create_base_form(dict_form_data)
    
    form['lbl_titulo'] = Label(x=var.DIMENSION_PANTALLA[0]//2, y=100,text='La PYTHONisa del Tarot', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=50)
    
    form['btn_jugar'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=150, text='JUGAR', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=30, on_click=cambiar_formulario_on_click, on_click_param='form_juego')
    form['btn_ranking'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=225, text='RANKING', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=30, on_click=cambiar_formulario_on_click, on_click_param='form_ranking')
    form['btn_historia'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=290, text='HISTORIA', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=30, on_click=cambiar_formulario_on_click, on_click_param='form_historia')
    form['btn_config'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=370, text='CONFIG', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=30, on_click=cambiar_formulario_on_click, on_click_param='form_config')
    form['btn_salir'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=430, text='SALIR', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=30, on_click=click_salir, on_click_param='Boton Salir')
    
    form['widgets_list'] = [
        form.get('lbl_titulo'), 
        form.get('btn_jugar'), 
        form.get('btn_ranking'),
        form.get('btn_historia'), 
        form.get('btn_config'), 
        form.get('btn_salir')
    ]
    
    base_form.forms_dict[dict_form_data.get('name')] = form
    
    return form

def click_start(parametro: str):
    print(parametro)

def cambiar_formulario_on_click(parametro: str):
    print(parametro)
    base_form.set_active(parametro)

def click_salir(parametro: str):
    print(parametro)
    sys.exit()

def draw(form_data: dict):
    base_form.draw(form_data)

def update(form_data: dict, event_list: list[pg.event.Event]):
    base_form.update(form_data)
    #Pequeño for para obtener coordenadas
    for evento in event_list:
        if evento.type == pg.MOUSEBUTTONDOWN:
            print(f"Coordenada: {evento.pos}")   