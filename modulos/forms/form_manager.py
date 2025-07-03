import pygame as pg
import modulos.variables as var
import modulos.forms.form_main_menu as form_main_menu
import modulos.forms.form_historia as form_historia
import modulos.forms.form_config as form_config
import modulos.forms.form_ranking as form_ranking


def create_form_manager(screen: pg.Surface, datos_juego: dict):
    form = {}
    form['main_screen'] = screen
    form['current_level'] = 1
    form['game_started'] = False
    form['player'] = None
    form['enemy'] = None
    
    form['jugador'] = datos_juego.get('jugador')
    
    form['form_list'] = [
        form_main_menu.init_form_main_menu(
            dict_form_data={
                "name":'form_main_menu', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "level_num":1, 
                "music_path":var.RUTA_MUSICA,
                "background_path": './modulos/assets/background/fondo_3.png',
                "screen_dimentions": var.DIMENSION_PANTALLA
            }
        ),
        form_historia.init_form_historia(
            dict_form_data={
                "name":'form_historia', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "level_num":1, 
                "music_path":var.RUTA_MUSICA,
                "background_path": './modulos/assets/background/fondo_tablero.png',
                "screen_dimentions": var.DIMENSION_PANTALLA
            }
        ),
        form_config.init_form_config(
            dict_form_data={
                "name":'form_config', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "level_num":1, 
                "music_path":var.RUTA_MUSICA,
                "volumen_musica": var.VOLUMEN_MUSICA_INICIAL,
                "musica_bucle_iniciada": False,
                "background_path": './modulos/assets/background/fondo_tablero.png',
                "screen_dimentions": var.DIMENSION_PANTALLA
            }
        ),
        form_ranking.init_form_ranking(
            dict_form_data={
                "name":'form_ranking', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "level_num":1, 
                "music_path":var.RUTA_MUSICA,
                "background_path": './modulos/assets/background/fondo_4.png',
                "screen_dimentions": var.DIMENSION_PANTALLA
            }, jugador=form.get('jugador')
        )
    ]
    
    return form


def forms_update(form_manager: dict, event_list: pg.event.Event):
    # Preguntar por cada uno de los formularios si esta activo
    # en caso de estarlo, dibujar y actualizar
    
    # FORM MENU
    if form_manager.get('form_list')[0].get('active'):
        form_main_menu.update(form_manager.get('form_list')[0], event_list)
        form_main_menu.draw(form_manager.get('form_list')[0],)
    
    # FORM HISTORIA
    elif form_manager.get('form_list')[1].get('active'):
        form_historia.update(form_manager.get('form_list')[1], event_list)
        form_historia.draw(form_manager.get('form_list')[1],)
    
    # FORM CONFIG
    elif form_manager.get('form_list')[2].get('active'):
        form_config.update(form_manager.get('form_list')[2], event_list)
        form_config.draw(form_manager.get('form_list')[2])
    
    # FORM RANKING
    elif form_manager.get('form_list')[3].get('active'):
        form_ranking.update(form_manager.get('form_list')[3], event_list)
        form_ranking.draw(form_manager.get('form_list')[3],)


def update(form_manager: dict, event_list: pg.event.Event):
    forms_update(form_manager, event_list)
    