import sys
import modulos.forms.base_form as base_form
import modulos.variables as var
import modulos.forms.form_start_level as form_start_level_module
from utn_fra.pygame_widgets import (
    Button, Label
)

def init_form_main_menu(dict_form_data: dict) -> dict:
    """ 
    Parametros: Recibe la data del formulario en formato diccionario.

    ¿Qué hace?:Crea un formulario, y se le agregan elementos como titulos y botones para
    renderizar la vista del formulario "Start Level"
    Aquí el usuario puede navegar entre cada formulario.

    ¿Qué Devuelve?: El diccionario que creó.
    """
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
    dict_name = dict_form_data.get('name')
    base_form.forms_dict[dict_name] = form
    base_form.play_music(base_form.forms_dict[dict_name])

    return form

def cambiar_formulario_on_click(parametro: str) -> None:
    """ 
    Parametros: Recibe el string del formulario.

    ¿Qué hace?: Direcciona al usuario según el valor que reciba por param \n
    Si comienza la partida, inicializa la función para arrancar el juego.

    ¿Qué Devuelve?: None.
    """
    #Recibe por parámetro un string, con el nombre del form 
    #Para poder activar y mostrar el mismo en pantalla
    print(parametro)
    var.SOUND_CLICK.play()

    #Si vamos al form de start_level, recién ahí iniciamos y cargamos la data
    #Esto con la finalidad de administrar recursos
    if parametro == 'form_start_level':
        form_start_level = base_form.forms_dict[parametro]
        #Antes de iniciar el juego con su data, reiniciamos el puntaje y todo
        form_start_level_module.inicializar_juego(form_start_level)
        
    base_form.set_active(parametro)
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict[parametro])


def click_salir() -> None:
    """ 
    Parametros: None.

    ¿Qué hace?: Saca al usuario de la app, cierra y finaliza el proceso.

    ¿Qué Devuelve?: None.
    """
    sys.exit()

def draw(form_data: dict):
    """ 
    Parametros: Recibe la data del formulario en formato diccionario.

    ¿Qué hace?: Simplemente dibuja la info que recibe por parámetro, \n
    Incluida la lista de widgets.

    ¿Qué Devuelve?: None.
    """
    base_form.draw(form_data)
    base_form.draw_widgets(form_data)

def update(form_data: dict):
    """ 
    Parametros: Recibe la data del formulario en formato diccionario.

    ¿Qué hace?: Simplemente actualiza la info que recibe por parámetro, \n
    Incluida la lista de widgets.

    ¿Qué Devuelve?: None.
    """
    base_form.update(form_data)