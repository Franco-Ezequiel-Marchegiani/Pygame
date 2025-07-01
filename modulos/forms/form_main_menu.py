import pygame as pg
import modulos.forms.base_form as base_form
import modulos.variables as var
from utn_fra.pygame_widgets import (
    Button, Label
)

def init_form_main_menu(dict_form_data: dict):
    form = base_form.create_base_form(dict_form_data)
    #Imagen de fondo y sus dimensiones
    form['surface'] = pg.image.load(var.RUTA_FONDO).convert_alpha()
    form['surface'] = pg.transform.scale(form.get('surface'), var.DIMENSION_PANTALLA)

    #Rectángulo de la imagen cargada
    form['rect'] = form.get('surface').get_rect()
    form['rect'].x = dict_form_data.get('coords')[0]
    form['rect'].y = dict_form_data.get('coords')[1] 

    #Características de cada botón
    form['btn_jugar'] = Button(x=var.DIMENSION_BOTON_JUGAR[0], y=var.DIMENSION_BOTON_JUGAR[1], text='JUGAR', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=var.FUENTE_30, on_click=click_start, on_click_param='Boton Start')
    form['btn_historia'] = Button(x=var.DIMENSION_BOTON_HISTORIA[0], y=var.DIMENSION_BOTON_HISTORIA[1], text='HISTORIA', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=var.FUENTE_30, on_click=click_historia, on_click_param='Boton Historia')
    form['btn_salir'] = Button(x=var.DIMENSION_BOTON_SALIR[0], y=var.DIMENSION_BOTON_SALIR[1], text='SALIR', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=var.FUENTE_30, on_click=click_salir, on_click_param='Boton Salir')

    #Listado de las fotos
    form['widgets_list'] = [
        form.get('btn_jugar'), form.get('btn_historia'), form.get('btn_salir')
    ]

    return form

def click_start(parametro: str):
    print(f'Boton start {parametro}')

def click_historia(parametro: str):
    print(f'Boton historia {parametro}')
    
def click_salir(parametro: str):
    print(f'Boton salir {parametro}')

def draw(form_data: dict):
    base_form.draw(form_data)

    for widget in form_data.get('widgets_list'):
        widget.draw()

def update(form_data: dict):
    for widget in form_data.get('widgets_list'):
        widget.update()
