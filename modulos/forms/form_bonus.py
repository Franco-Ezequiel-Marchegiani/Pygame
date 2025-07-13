import modulos.forms.base_form as base_form
import modulos.variables as var
import pygame as pg
from utn_fra.pygame_widgets import(
    Button, Label
)
def init_form_bonus(dict_form_data: dict, jugador: dict) -> dict:
    """ 
    Parametros: Recibe la data del formulario en formato diccionario.

    ¿Qué hace?:Crea un formulario, y se le agregan elementos como titulos y botones para
    renderizar la vista del formulario "Bonus"
    Aquí el usuario podrá elegir en activar el bonus, o volver a la partida
    ¿Qué Devuelve?: El diccionario que creó.
    """
    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = jugador
    form['bonus_info'] = ''
    form['confirm_bonus'] = False
    
    form['lbl_titulo'] = Label(
        x=var.CENTRO_DIMENSION_X, y=var.CENTRO_DIMENSION_Y - 250,
        text=var.MAIN_TITLE, screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=75)
    form['lbl_subtitle'] = Label(
        x=400, y=var.CENTRO_DIMENSION_Y - 175,
        text=form.get('texto'), screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=50)
    form['btn_select'] = Button(
        x=var.CENTRO_DIMENSION_X - 200, y=var.CENTRO_DIMENSION_Y + 75,
        text='SELECCIONAR', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=34, on_click=click_select_bonus, on_click_param=form)
    form['btn_back'] = Button(
        x=var.CENTRO_DIMENSION_X + 200, y=var.CENTRO_DIMENSION_Y + 75,
        text='CANCELAR', screen=form.get('screen'), font_path=var.FUENTE_SAIYAN, font_size=34, color=var.COLOR_NARANJA, on_click=click_change_form, on_click_param='form_start_level')

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitle'),
        form.get('btn_select'),
        form.get('btn_back'),
    ]
    base_form.forms_dict[form.get('name')] = form
    
    return form

def click_change_form(param: str) -> None:
    """ 
    Parametros: Recibe el string del formulario.

    ¿Qué hace?: Envía al usuario al juego nuevamente sin hacer nada más. \n
    Comienza la música y activa el valor recibido por param.

    ¿Qué Devuelve?: None.
    """
    var.SOUND_CLICK.play()
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict[param])
    base_form.set_active(param)

def click_select_bonus(form_dict: dict) -> None:
    """ 
    Parametros: Recibe la data del formulario en formato diccionario.

    ¿Qué hace?: Según la info de bonus info, actualiza con valor True el \n
    Valor de bonus activo del dict que recibió por params. \n
    Sumado a eso inicializa un sonido, espera 6segs y envía al form "Start Level"

    ¿Qué Devuelve?: None.
    """
    #Lee la info que esté en bonus_info, y en base a eso selecciona el bonus
    option = form_dict.get('bonus_info')
    match option:
        case 'shield': #(Originialmente es un x2 en los puntos)
            #Indica que ya fue usado, y cambia el valor
            base_form.forms_dict['form_start_level']['bonus_shield_active'] = True
            
        case 'heal': #(Originialmente es un +50 en los puntos)
            #Indica que ya fue usado, y cambia el valor
            base_form.forms_dict['form_start_level']['bonus_heal_active'] = True

    base_form.play_bonus_music(var.RUTA_SONIDO_BONUS_FIN)
    pg.time.wait(6000)
    click_change_form('form_start_level') 
    
#Función para actualizar "btn_select" label o Button
def update_button_bonus(form_dict: dict, new_text: str) -> None:
    """ 
    Parametros: Recibe la data del formulario en formato diccionario, y el texto.

    ¿Qué hace?: Actualiza el texto del "Bonus Info", para mostrar en pantalla.

    ¿Qué Devuelve?: None.
    """
    #Meter acá un "confirm", si se clickea "click_select_bonus", sino siempre será False
    form_dict['bonus_info'] = new_text
    #Actualiza el texto con el bonus que seleccionó el usuario
    form_dict.get('widgets_list')[2].update_text(form_dict.get('bonus_info'), var.COLOR_NARANJA)

def draw(form_dict: dict) -> None:
    """ 
    Parametros: Recibe la data del formulario en formato diccionario.

    ¿Qué hace?: Simplemente dibuja la info que recibe por parámetro, \n
    Incluida la lista de widgets.

    ¿Qué Devuelve?: None.
    """
    base_form.draw(form_dict)
    base_form.draw_widgets(form_dict)

def update(form_data: dict) -> None:
    """ 
    Parametros: Recibe la data del formulario en formato diccionario.

    ¿Qué hace?: Simplemente actualiza la info que recibe por parámetro, \n
    Incluida la lista de widgets.

    ¿Qué Devuelve?: None.
    """
    base_form.update(form_data)