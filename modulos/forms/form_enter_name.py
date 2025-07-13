import pygame as pg
import modulos.forms.base_form as base_form
import modulos.jugador as jugador_mod
import modulos.variables as var
import modulos.auxiliar as aux
from utn_fra.pygame_widgets import (
    Button, Label, TextBox
)
def init_form_enter_name(dict_form_data: dict, jugador: dict) -> dict:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:``
        Crea un formulario, y se le agregan elementos como titulos y botones para
        renderizar la vista del formulario "Start Level"
        Aquí el usuario, luego de finalizar su partida, colocará su nombre para que se guarde
        En el ranking, junto a su puntaje.

    ``¿Qué Devuelve?:`` 
        El diccionario que creó.
    """
    form = base_form.create_base_form(dict_form_data)
    
    #Creamos un form que se activa entre el nivel del juego, y el ranking
    #Para que el usuario pueda elegir el nombre en este momento.
    form['jugador'] = jugador
    form['_last_music_path'] = None
    form['score'] = jugador_mod.get_puntaje_total(form.get('jugador'))
    
    form['confirm_name'] = False
    form['title'] = Label(
        x=var.CENTRO_DIMENSION_X, y=var.CENTRO_DIMENSION_Y - 200, text=var.MAIN_TITLE, 
        screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=75
    )
    form['title_2'] = Label(
        x=var.CENTRO_DIMENSION_X, y= var.CENTRO_DIMENSION_Y - 145, text='Ganaste!', 
        screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=75
    )
    form['subtitle'] = Label(
        x=var.CENTRO_DIMENSION_X, y= var.CENTRO_DIMENSION_Y - 85, text='ESCRIBE TU NOMBRE', 
        screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=50, color=var.COLOR_ROJO
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

def click_confirm_name(form_dict: dict) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:``
        Cambia el valor a True de confirm_name, setea el nombre \n
        Que colocó el usuario y lo escribe en el csv.\n
        Guarda nuevamente el ranking con el nuevo nombre y puntaje.\n
        Para la música que estaba sonando, comienza la nueva, y lo envía al form de "Ranking"

    ``¿Qué Devuelve?:`` 
        None.
    """
    form_dict['confirm_name'] = True
    #Definimos el nombre del usuario
    jugador_mod.set_nombre(
        form_dict.get('jugador'),
        form_dict.get('writing_text').text
    )
    #Guardamos el ranking
    aux.guardar_ranking(form_dict.get('jugador'))
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict['form_ranking'])
    base_form.set_active('form_ranking')

def update_paths(form_dict: dict) -> str:
    """
    Ajusta el background_path y el music_path
    en base a form_dict['jugador']['ganador'].
    """
    ganador = form_dict['jugador'].get('ganador')
    texto_ganador = ''
    if ganador == 'rival':
        form_dict['background_path'] = './modulos/assets/img/forms/img_2.png'
        music_path = var.RUTA_MUSICA_LOSE
        form_dict['music_path']     = var.RUTA_MUSICA_LOSE
        texto_ganador = 'Derrota'
    else:
        form_dict['background_path'] = './modulos/assets/img/forms/img_3.jpg'
        music_path = var.RUTA_MUSICA_WIN
        form_dict['music_path']     = var.RUTA_MUSICA_WIN
        texto_ganador = 'Victoria!'

    # Recargamos la superficie con el nuevo background
    surface = pg.image.load(form_dict['background_path']).convert_alpha()
    form_dict['surface'] = pg.transform.scale(surface, var.DIMENSION_PANTALLA)

    # Si cambió la música, y la global está on, 
    # la reproducimos una sola vez aquí:
    if form_dict.get('_last_music_path') != music_path:
        form_dict['music_path'] = music_path
        # Dispara la música sólo si el usuario no la apagó
        base_form.play_music_if_allowed(form_dict)
        form_dict['_last_music_path'] = music_path
    return texto_ganador
    
def draw(form_dict: dict) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:``
        Dibuja la info que recibe por parámetro, \n
        Incluida la lista de widgets, el "text_box" y dibuja y muestra el "writing_Text". \n
        (Que incluye el nombre que escribe el jugador)

    ``¿Qué Devuelve?:`` 
        None.
    """
    update_paths(form_dict)
    base_form.draw(form_dict)
    base_form.draw_widgets(form_dict)
    form_dict.get('text_box').draw()

    form_dict['writing_text'] = Label(
        x=var.CENTRO_DIMENSION_X, y= var.CENTRO_DIMENSION_Y + 30, text=f'{form_dict.get("text_box").writing.upper()}',
        screen=form_dict.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=30, color=var.COLOR_AMARILLO
    )

    form_dict.get('writing_text').draw()

def update(form_dict: dict, event_list: list) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario, y el listado de eventos.

    ``¿Qué hace?:``
        Actualiza el valor del score, obteniendo el puntaje total. \n
        Luego actualiza el texto y muestra el score actual, y tmb actualiza el textbox.

    ``¿Qué Devuelve?:`` 
        None.
    """

    texto_ganador = update_paths(form_dict)
    #Actualizamos el valor del score
    form_dict['score'] = jugador_mod.get_puntaje_total(form_dict.get('jugador'))
    #Actualizamos el widget para que se actualice también en la vista
    #Usamos update_text de la función Label
    
    form_dict.get('widgets_list')[1].update_text(f'{texto_ganador}', var.COLOR_AMARILLO)
    form_dict.get('widgets_list')[3].update_text(f'{texto_ganador}', var.COLOR_VERDE_OSCURO)
    
    #Le pasamos eventos para que actualice cada vez que el usuario clickee
    form_dict.get('text_box').update(event_list) 

    base_form.update(form_dict)