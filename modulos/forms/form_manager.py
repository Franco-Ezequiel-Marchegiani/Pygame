import pygame as pg
import modulos.variables as var
import modulos.forms.form_main_menu as form_main_menu
import modulos.forms.form_start_level as form_start_level
import modulos.forms.form_config as form_config
import modulos.forms.form_ranking as form_ranking
import modulos.forms.form_bonus as form_bonus
import modulos.forms.form_enter_name as form_enter_name
import modulos.forms.form_pause as form_pause

def create_form_manager(screen: pg.Surface, datos_juego: dict):
    form = {}
    form['main_screen'] = screen
    form['current_level'] = 1
    form['game_started'] = False
    form['jugador'] = None
    form['enemy'] = None
    
    form['jugador'] = datos_juego.get('jugador')
    form['form_list'] = [
        form_main_menu.init_form_main_menu(
            dict_form_data={
                "name":'form_main_menu', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "stage_number":1, 
                "music_path":var.RUTA_MUSICA_MAIN_MENU, #Cambiar acá la ruta de la música que se quiera que suene
                "background_path": './modulos/assets/img/forms/img_5.png',
                "screen_dimentions": var.DIMENSION_PANTALLA
            }
        ),
        form_start_level.init_form_start_level (
            dict_form_data={
                "name":'form_start_level', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "stage_number":1, 
                "music_path":var.RUTA_MUSICA_BATALLA,
                "background_path": './modulos/assets/img/background_cards.png',
                "screen_dimentions": var.DIMENSION_PANTALLA
            }, jugador = form.get('jugador')
        ),
        form_config.init_form_config(
            dict_form_data={
                "name":'form_config', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "stage_number":1, 
                "music_path":var.RUTA_MUSICA_MAIN_MENU,
                "volumen_musica": var.VOLUMEN_MUSICA_INICIAL,
                "musica_bucle_iniciada": False,
                "background_path": './modulos/assets/img/forms/img_6.png',
                "screen_dimentions": var.DIMENSION_PANTALLA
            }
        ),
        form_ranking.init_form_ranking(
            dict_form_data={
                "name":'form_ranking', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "stage_number":1, 
                "music_path":var.RUTA_MUSICA_RANKING,
                "background_path": './modulos/assets/img/forms/img_8.png',
                "screen_dimentions": var.DIMENSION_PANTALLA
            }, jugador=form.get('jugador')
        ),
        form_bonus.init_form_bonus(
            dict_form_data={
                "name":'form_bonus', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "stage_number":1, 
                "music_path":var.RUTA_MUSICA_BONUS,
                "background_path": './modulos/assets/img/forms/img_9.png',
                "screen_dimentions": var.DIMENSION_PANTALLA
            }, jugador=form.get('jugador')
        ),
        form_enter_name.init_form_enter_name(
            dict_form_data={
                "name":'form_enter_name', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "stage_number":1, 
                "music_path":var.RUTA_MUSICA_WIN, #Hacer un IF, de que si jugador ganó, ponga una música, u otra
                "background_path": './modulos/assets/img/forms/img_3.jpg',
                "screen_dimentions": var.DIMENSION_PANTALLA
            }, jugador=form.get('jugador')
        ),
        form_pause.init_form_pause(
            dict_form_data={
                "name":'form_pause', 
                "screen":form.get('main_screen'), 
                "active":True, 
                "coords":(0,0), 
                "stage_number":1, 
                "music_path":var.RUTA_MUSICA_PAUSA,
                "background_path": './modulos/assets/img/forms/img_20.jpg',
                "screen_dimentions": var.DIMENSION_PANTALLA
            }
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
    
    # FORM JUEGO / START LEVEL
    elif form_manager.get('form_list')[1].get('active'):
        form_start_level.update(form_manager.get('form_list')[1], event_list)
        form_start_level.draw(form_manager.get('form_list')[1],)

    # FORM CONFIG
    elif form_manager.get('form_list')[2].get('active'):
        form_config.update(form_manager.get('form_list')[2], event_list)
        form_config.draw(form_manager.get('form_list')[2])
    
    # FORM RANKING
    elif form_manager.get('form_list')[3].get('active'):
        form_ranking.update(form_manager.get('form_list')[3], event_list)
        form_ranking.draw(form_manager.get('form_list')[3],)

    # FORM BONUS
    elif form_manager.get('form_list')[4].get('active'):
        form_bonus.update(form_manager.get('form_list')[4], event_list)
        form_bonus.draw(form_manager.get('form_list')[4],)

    # FORM ENTER NAME
    elif form_manager.get('form_list')[5].get('active'):
        form_enter_name.update(form_manager.get('form_list')[5], event_list)
        form_enter_name.draw(form_manager.get('form_list')[5],)

    # FORM PAUSE
    elif form_manager.get('form_list')[6].get('active'):
        form_pause.update(form_manager.get('form_list')[6], event_list)
        form_pause.draw(form_manager.get('form_list')[6],)


def update(form_manager: dict, event_list: pg.event.Event):
    forms_update(form_manager, event_list)
    