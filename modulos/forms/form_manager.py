import pygame as pg
import modulos.forms.form_main_menu as form_main_menu
import modulos.variables as var

def create_form_manager(screen: pg.Surface, datos_juego: dict):
    #Idea de crear un diccionario gigante y centralizado
    form = {}
    form['main_screen'] = screen
    form['current_level'] = 1
    form['game_started'] = False
    form['player'] = None
    form['enemy'] = None

    form['player'] = datos_juego.get('player')
    #Listado con los forms/pantallas
    form['form_list'] = [
        form_main_menu.init_form_main_menu(
            dict_form_data={
                "name":'form_main_menu', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "level_num":1, 
                "music_path":var.RUTA_MUSICA

            }
        )
    ]

    return form

def forms_update(form_manager: dict, lista_eventos: pg.event.Event):
    # Preguntar por c/u de los formularios si está activo
    # En caso de estarlo, dibujar y actualizar

    # Form MENU
    if form_manager.get('form_list')[0].get('active'):
        form_main_menu.update(form_manager.get('form_list')[0])
        form_main_menu.draw(form_manager.get('form_list')[0])

    # Form HISTORIA

def update(form_manager: dict, lista_eventos: pg.event.Event):

    forms_update(form_manager, lista_eventos)

