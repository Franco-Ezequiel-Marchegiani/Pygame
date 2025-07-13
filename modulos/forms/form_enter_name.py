import pygame as pg 
import modulos.forms.base_form as base_form
import modulos.jugador as jugador_mod
import modulos.variables as var
import modulos.auxiliar as aux
from utn_fra.pygame_widgets import (
    Button, Label, TextBox
)
#Centro de las dimensiones horizontales y verticales

def init_form_enter_name(dict_form_data: dict, jugador: dict) -> None:
    """ 
    Parametros:Recibe la data del formulario en formato diccionario.

    ¿Qué hace?:Crea un formulario, y se le agregan elementos como titulos y botones para
    renderizar la vista del formulario "Start Level"
    Aquí el usuario, luego de finalizar su partida, colocará su nombre para que se guarde
    En el ranking, junto a su puntaje.
    
    ¿Qué Devuelve?: None.
    """
    form = base_form.create_base_form(dict_form_data)
    
    #Creamos un form que se activa entre el nivel del juego, y el ranking
    #Para que el usuario pueda elegir el nombre en este momento.
    form['jugador'] = jugador

    form['score'] = jugador_mod.get_puntaje_total(form.get('jugador'))
    
    form['confirm_name'] = False
    form['title'] = Label(
        x=var.CENTRO_DIMENSION_X, y=var.CENTRO_DIMENSION_Y - 200, text=var.MAIN_TITLE, 
        screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=75
    )
    form['title_2'] = Label(
        x=var.CENTRO_DIMENSION_X, y= var.CENTRO_DIMENSION_Y - 150, text='Ganaste!', 
        screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=75
    )
    form['subtitle'] = Label(
        x=var.CENTRO_DIMENSION_X, y= var.CENTRO_DIMENSION_Y - 90, text='ESCRIBE TU NOMBRE', 
        screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=50, color=var.COLOR_NARANJA
    )
    form['subtitle_score'] = Label(
        x=var.CENTRO_DIMENSION_X, y= var.CENTRO_DIMENSION_Y - 20, text=f'Score: {form.get('score')}', 
        screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=30, color=var.COLOR_VERDE_OSCURO
    )

    form['text_box'] = TextBox(
        x=var.CENTRO_DIMENSION_X, y= var.CENTRO_DIMENSION_Y + 40, text='__________', 
        screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=25, color=var.COLOR_VERDE_OSCURO
    )

    form['btn_confirm_name'] = Button(
        x=var.CENTRO_DIMENSION_X, y= var.CENTRO_DIMENSION_Y + 100, text='CONFIRMAR NOMBRE', 
        screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, on_click= click_confirm_name, on_click_param=form
    )
    
    form['widgets_list'] = [
        form.get('title'),
        form.get('title_2'),
        form.get('subtitle'),
        form.get('subtitle_score'),
        form.get('btn_confirm_name'),
    ]

    base_form.forms_dict[dict_form_data.get('name')] = form
    return form


def click_confirm_name(form_dict: dict):
    form_dict['confirm_name'] = True
    #Definimos el nombre del usuario
    jugador_mod.set_nombre(
        form_dict.get('jugador'),
        form_dict.get('writing_text').text
    )
    #Guardamos el ranking
    aux.guardar_ranking(form_dict.get('jugador'))
    #Luego de guardarlo, enviamos al usuario a la vista de ranking
    base_form.stop_music()
    # base_form.play_music(base_form.forms_dict['form_enter_name'])
    aux.inicializar_musica()
    base_form.set_active('form_ranking')

def draw(form_dict: dict):
    base_form.draw(form_dict)
    base_form.draw_widgets(form_dict)
    form_dict.get('text_box').draw()

    form_dict['writing_text'] = Label(
        x=var.CENTRO_DIMENSION_X, y= var.CENTRO_DIMENSION_Y + 30, text=f'{form_dict.get("text_box").writing.upper()}',
        screen=form_dict.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=30, color=var.COLOR_AMARILLO
    )

    form_dict.get('writing_text').draw()

""" def update_paths(form_dict: dict):
    #Actualiza la imagen de fondo con la música, según el ganador
    jugador = form_dict.get('jugador')
    print(f"FONDO ACTUALIZADO")
    print(f"form_dict['background_path']: {form_dict['background_path']}")
    print(f"form_dict['music_path']: {form_dict['music_path']}")
    if jugador.get('ganador') == 'rival':
        form_dict['background_path'] = './modulos/assets/img/forms/img_2.jpg'
        form_dict['music_path'] = var.RUTA_MUSICA_LOSE
        form_dict['surface'] = pg.image.load(form_dict.get('background_path')).convert_alpha()
        form_dict['surface'] = pg.transform.scale(form_dict.get('surface'), form_dict.get('screen_dimentions'))
         """
        

def update(form_dict: dict, event_list: list):
    # update_paths(form_dict)
    #Actualizamos el valor del score
    form_dict['score'] = jugador_mod.get_puntaje_total(form_dict.get('jugador'))
    #Actualizamos el widget para que se actualice también en la vista
    #Usamos update_text de la función Label
    form_dict.get('widgets_list')[3].update_text(f'{form_dict.get('score')}', var.COLOR_VERDE_OSCURO)
    
    #Le pasamos eventos para que actualice cada vez que el usuario clickee
    form_dict.get('text_box').update(event_list) 

    base_form.update(form_dict)