import pygame as pg
import sys
import modulos.forms.base_form as base_form
import modulos.variables as var
import modulos.auxiliar as aux
import modulos.nivel_cartas as nivel_cartas
import modulos.forms.form_start_level as form_start_level_module
from utn_fra.pygame_widgets import (
    Button, Label, ButtonImage
)


def init_form_main_menu(dict_form_data: dict):
    form = base_form.create_base_form(dict_form_data)
    
    form['lbl_titulo'] = Label(x=var.DIMENSION_PANTALLA[0]//2, y=100,text=var.MAIN_TITLE, screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=50)
    form['lbl_sub_titulo'] = Label(x=var.DIMENSION_PANTALLA[0]//2, y=175,text='MAIN MENU', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=50)
    
    form['btn_jugar'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=375, text='JUGAR', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=30, on_click=cambiar_formulario_on_click, on_click_param='form_start_level')
    form['btn_ranking'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=445, text='RANKING', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=30, on_click=cambiar_formulario_on_click, on_click_param='form_ranking')
    form['btn_config'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=515, text='CONFIG', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=30, on_click=cambiar_formulario_on_click, on_click_param='form_config')
    form['btn_salir'] = Button(x=var.DIMENSION_PANTALLA[0]//2, y=580, text='SALIR', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=30, on_click=click_salir, on_click_param='Boton Salir')
    
    form['widgets_list'] = [
        form.get('lbl_titulo'), 
        form.get('lbl_sub_titulo'), 
        form.get('btn_jugar'), 
        form.get('btn_ranking'), 
        form.get('btn_config'), 
        form.get('btn_salir')
    ]
    
    base_form.forms_dict[dict_form_data.get('name')] = form
    
    return form

def click_start(parametro: str):
    print(parametro)

def cambiar_formulario_on_click(parametro: str):
    #Recibe por parámetro un string, con el nombre del form 
    #Para poder activar y mostrar el mismo en pantalla
    print(parametro)
    

    #Si vamos al form de start_level, recién ahí iniciamos y cargamos la data
    #Esto con la finalidad de administrar recursos
    if parametro == 'form_start_level':
        form_start_level = base_form.forms_dict[parametro]
        #Antes de iniciar el juego con su data, reiniciamos el puntaje y todo
        form_start_level_module.inicializar_juego(form_start_level)
        
    base_form.set_active(parametro)
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict[parametro])


def click_salir(parametro: str):
    print(parametro)
    sys.exit()

def draw(form_data: dict):
    base_form.draw(form_data)
    base_form.draw_widgets(form_data)

def update(form_data: dict, event_list: list[pg.event.Event]):
    base_form.update(form_data)
    #Pequeño for para obtener coordenadas
    for evento in event_list:
        if evento.type == pg.MOUSEBUTTONDOWN:
            print(f"Coordenada: {evento.pos}")   