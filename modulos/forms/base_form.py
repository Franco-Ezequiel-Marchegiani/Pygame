import pygame as pg 

forms_dict = {}

def create_base_form(dict_form_data: dict) -> dict:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:``
        Crea un diccionario y en él agrega los elementos base que cada
        formulario en la aplicación contará.
    
    ``¿Qué Devuelve?:`` 
        Un diccionario, con la estructura base ya definida.
    """
    form = {}
    form['name'] = dict_form_data.get('name')
    form['screen'] = dict_form_data.get('screen')
    form['active'] = dict_form_data.get('active')
    form['x_coord'] = dict_form_data.get('coords')[0]
    form['y_coord'] = dict_form_data.get('coords')[1]
    form['level_number'] = dict_form_data.get('stage_number')
    form['music_path'] = dict_form_data.get('music_path')
    form['music_on'] = True
    form['surface'] = pg.image.load(dict_form_data.get('background_path')).convert_alpha()
    form['surface'] = pg.transform.scale(form.get('surface'), dict_form_data.get('screen_dimentions'))
    
    form['rect'] = form.get('surface').get_rect()
    form['rect'].x = dict_form_data.get('coords')[0]
    form['rect'].y = dict_form_data.get('coords')[1]
    return form

global_music_on = True
def set_global_music(state: bool):
    """
    Activa o desactiva la música globalmente en TODOS los formularios.
    """
    global global_music_on
    global_music_on = state
    # además actualizamos el flag de cada form por si lo usan individualmente:
    for form in forms_dict.values():
        form['music_on'] = state

def play_music_if_allowed(form_dict: dict):
    """
    Reemplaza a play_music; sólo reproduce si la música global está activa.
    """
    if global_music_on and form_dict.get('music_on', True):
        pg.mixer.music.load(form_dict.get('music_path'))
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops=-1, fade_ms=400)

def stop_music() -> None:
    """ 
    ``Parametros:`` 
        None.

    ``¿Qué hace?:`` 
        Detiene la música.

    ``¿Qué Devuelve?:`` 
        None.
    """
    pg.mixer.music.stop()


def play_bonus_music(route: str) -> None:
    """ 
    ``Parametros:`` 
        Recibe la ruta del sonido a reproducir.

    ``¿Qué hace?:`` 
        Inicializa la secuencia de cargar la ruta, definir volumen \n
        Y lo ejecuta una sola vez, con un fade de 200 mili segundos.
    
    ``¿Qué Devuelve?:`` 
        None.
    """
    pg.mixer.music.load(route)
    pg.mixer.music.set_volume(0.2)
    pg.mixer.music.play(loops=1, fade_ms=200)

def play_music(form_dict: dict) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:`` 
        Si music_on es true, inicializa la secuencia de cargar la ruta, \n 
        Definir volumen, y lo ejecuta una sola vez, con un fade de 200 mili segundos.

    ``¿Qué Devuelve?:`` 
        None.
    """
    if form_dict['music_on']:
        pg.mixer.music.load(form_dict.get('music_path'))
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops=-1, fade_ms=400)

def set_active(name: str) -> None:
    """ 
    ``Parametros:`` 
        Nombre del form en str.

    ``¿Qué hace?:`` 
        Funciona como un swich, recorre el listado de form \n
        Y según el nombre del param, activa solo ese, los otros quedan en False

    ``¿Qué Devuelve?:`` 
        None.
    """
    for form in forms_dict.values():
        form['active'] = False
    forms_dict[name]['active'] = True

def update_widgets(form_data: dict) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:`` 
        Itera la lista de widgets y los actualiza.

    ``¿Qué Devuelve?:`` 
        None.
    """
    for widget in form_data.get('widgets_list'):
        widget.update()

def draw_widgets(form_data: dict) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:`` 
        Itera la lista de widgets y los dibuja.

    ``¿Qué Devuelve?:`` 
        None.
    """
    for widget in form_data.get('widgets_list'):
        widget.draw()

def draw(form_data: dict) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:`` 
        Simplemente dibuja la info que recibe por parámetro, \n
        Incluida la lista de widgets.

    ``¿Qué Devuelve?:`` 
        None.
    """
    form_data['screen'].blit(form_data.get('surface'), form_data.get('rect'))

def update(form_data: dict) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:`` 
    Simplemente actualiza la info que recibe por parámetro, \n
    Incluida la lista de widgets.

    ``¿Qué Devuelve?:`` 
        None.
    """
    update_widgets(form_data)