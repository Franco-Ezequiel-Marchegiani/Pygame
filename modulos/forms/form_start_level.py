import pygame as pg
import modulos.forms.base_form as base_form
import modulos.variables as var
from utn_fra.pygame_widgets import Label
import modulos.nivel_cartas as nivel_cartas
import modulos.forms.form_bonus as form_bonus
from utn_fra.pygame_widgets import(
    Label, TextPoster, ButtonImage
)
def init_form_start_level(dict_form_data: dict, jugador: dict) -> dict:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:``
        Crea un formulario, y se le agregan elementos como titulos y botones para
        renderizar la vista del formulario "Start Level"
        Aquí el usuario estará jugando la partida.

    ``¿Qué Devuelve?:`` 
        El diccionario que creó.
    """
    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = jugador
    form['level'] = nivel_cartas.inicializar_nivel_cartas(form.get('jugador'), form.get('screen'), form.get('level_number'))
    form['clock'] = pg.time.Clock()
    form['bonus_shield_used'] = False
    form['bonus_heal_used'] = False
    form['bonus_shield_active'] = False
    form['bonus_heal_active'] = False
    form['first_last_timer'] = pg.time.get_ticks()
    form['texto'] = f'SCORE: {form.get('jugador').get('puntaje_actual')}'

    form['lbl_hp'] = Label(x=190, y=530,text=f'HP: {form.get('level').get('jugador').get('vida_actual')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=40, color=var.COLOR_AMARILLO)
    form['lbl_atk'] = Label(x=130, y=560,text=f'ATK: {form.get('level').get('jugador').get('atk_total')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=16, color=var.COLOR_AMARILLO)
    form['lbl_def'] = Label(x=245, y=560,text=f'DEF: {form.get('level').get('jugador').get('def_total')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=16, color=var.COLOR_AMARILLO)
    #Stats rival
    form['lbl_hp_rival'] = Label(x=190, y=200,text=f'HP: {form.get('level').get('rival').get('vida_actual')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=40, color=var.COLOR_AMARILLO)
    form['lbl_atk_rival'] = Label(x=130, y=230,text=f'ATK: {form.get('level').get('rival').get('atk_total')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=16, color=var.COLOR_AMARILLO)
    form['lbl_def_rival'] = Label(x=245, y=230,text=f'DEF: {form.get('level').get('rival').get('def_total')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=16, color=var.COLOR_AMARILLO)
    
    form['lbl_clock'] = Label(x=450, y=40,text=f'TIME LEFT: {form.get('level').get('level_timer')}', screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=22)
    form['lbl_score'] = Label(x=150, y=50,text=form.get('texto'), screen=form.get('screen'), font_path=var.FUENTE_ALAGARD, font_size=44)
    
    form['btn_bonus_play_hand'] = ButtonImage(
        x=1200, y=var.CENTRO_DIMENSION_Y + 25, width=126, height=40,
        text='shield', screen=form.get('screen'), image_path='./modulos/assets/img/buttons_image/btn_play_hand.png', 
        on_click=nivel_cartas.jugar_mano, on_click_param= form.get('level')
    )
    form['btn_bonus_shield'] = ButtonImage(
        x=1200, y=var.CENTRO_DIMENSION_Y + 220, width=126, height=40,
        text='shield', screen=form.get('screen'), image_path='./modulos/assets/img/buttons_image/shield.png', 
        on_click=select_bonus, on_click_param='shield'
    )
    form['btn_bonus_heal'] = ButtonImage(
        x=1200, y=var.CENTRO_DIMENSION_Y + 270,width=126, height=40,
        text='heal', screen=form.get('screen'), image_path='./modulos/assets/img/buttons_image/heal.png', 
        on_click=select_bonus, on_click_param='heal'
    )
    
    form['btn_bonus_shield_active'] = ButtonImage(
        x=1170, y=var.CENTRO_DIMENSION_Y - 150, width=50, height=50,
        text='shield', screen=form.get('screen'), image_path='./modulos/assets/img/icons/icon_shield.png', 
    )
    form['btn_bonus_heal_active'] = ButtonImage(
        x=1230, y=var.CENTRO_DIMENSION_Y - 150,width=50, height=50,
        text='heal', screen=form.get('screen'), image_path='./modulos/assets/img/icons/icon_heal.png', 
    )
    
    form['widgets_list'] = [
        form.get('lbl_clock'), 
        form.get('lbl_score'),
        form.get('btn_bonus_play_hand'),
        form.get('lbl_hp'),
        form.get('lbl_atk'),
        form.get('lbl_def'),
        form.get('lbl_hp_rival'),
        form.get('lbl_atk_rival'),
        form.get('lbl_def_rival'),
    ]
    
    base_form.forms_dict[dict_form_data.get('name')] = form
    
    return form

def select_bonus(bonus_name: str) -> None:
    """ 
    ``Parametros:`` 
        Recibe el nombre del bonus en formato str

    ``¿Qué hace?:`` 
        Detiene la música que estaba sonando, y comienza la del formulario "Bonus".
        Luego actualiza el texto para mostrar el nombre del bonus en pantalla.
        Luego activa la vista del form Bonus para continuar ahí.
        Por último inicia el sonido del inicio del bonus y baja su volumen al 20%

    ``¿Qué Devuelve?:`` 
        None.
    """
    base_form.stop_music()
    base_form.play_music(base_form.forms_dict['form_bonus'])
    form_bonus.update_button_bonus(base_form.forms_dict['form_bonus'], bonus_name)

    base_form.set_active('form_bonus')
    
    base_form.play_bonus_music(var.RUTA_SONIDO_BONUS_INICIO)
    pg.mixer.music.set_volume(0.2)

def actualizar_timer(form_data: dict) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:`` 
        Se asegura que el valor level_timer del dict sea mayor a 0, para acto seguido
        restarle 1seg (1000) siempre y cuando al restar este valor, en el tiempo actual sea mayor a 1seg

    ``¿Qué Devuelve?:`` 
        None.
    """
    if form_data.get('level').get('level_timer') > 0:
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - form_data.get('first_last_timer') > 1000:
            form_data.get('level')['level_timer'] -= 1 
            form_data['first_last_timer'] = tiempo_actual

def events_handler(events_list: list[pg.event.Event]) -> None:
    """ 
    ``Parametros:`` 
        Recibe la lista de eventos.

    ``¿Qué hace?:`` 
        Itera dentro de la lista de eventos, y si el usuario presiona una tecla
        Y además, esta de escape, vuelve al formulario de "Menú principal".
        Ahora, si el usuario presiona la barra espaciadora, se inicia el formulario de "Pausa".
        También detiene la música que está sonando, y comienza la música del formulario "Pausa".

    ``¿Qué Devuelve?:`` 
        None.
    """
    for evento in events_list:
            #Si el usuario presiona una tecla
            if evento.type == pg.KEYDOWN:
                #Y si presiona la tecla de escape, lo
                if evento.key == pg.K_ESCAPE:
                    base_form.set_active('form_main_menu')
                elif evento.key == pg.K_SPACE:
                    base_form.set_active('form_pause')
                    base_form.stop_music()
                    base_form.play_music(base_form.forms_dict['form_pause'])

def condition_btn(form_data: dict, bonus_used: str, btn_active: str, btn_form_active: str, btn_bonus: str, accionar: str) -> None:
    """ 
    ``Parametros:`` 
        - La data del formulario 
        - El nombre del bonus usado 
        - Texto del botón activo
        - Widget del botón
        - Widget botón bonus
    
    ``¿Qué hace?:`` 
        Si el "bonus_used" es true, no muestra ningún botón, ya que de ser true, ya se usó el bufo y no se debe mostrar
        En caso contrario, revisa si el btn_Active es true, para mostrar el ícono de que el bonus está activo.
        Y en caso de que no sea así, simplemente muestra el botón para que el usuario pueda activar o usar el bonus.
        A su vez, en caso de que valor tenga el accionar, se encarga de dibujar o actualizar.

    ``¿Qué Devuelve?:`` 
        None.
    """
    if form_data.get(bonus_used):
        pass
    else:
        if form_data.get(btn_active):
            if accionar == 'update':
                form_data.get(btn_form_active).update()
            elif accionar == 'draw':
                form_data.get(btn_form_active).draw()
        else:
            if accionar == 'update':
                form_data.get(btn_bonus).update()
            elif accionar == 'draw':
                form_data.get(btn_bonus).draw()

def draw(form_data: dict) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:`` 
        Se encarga de dibujar/mostrar todo el listado de widgets para que
        se vea en pantalla.\n
        A su vez revisa la condición de los bonus de heal y shild.

    ``¿Qué Devuelve?:`` 
        None.
    """
    base_form.draw(form_data)
    
    widgets_list = form_data.get('widgets_list')
    for widget_index in range(len(widgets_list)):

        form_data.get('widgets_list')[widget_index].draw()
    
    #Hacer acá mismo una condicional con la bandera, y hacer un draw acá, no añadirlo en la lista
    condition_btn(form_data, 
    'bonus_shield_used',
    'bonus_shield_active',
    'btn_bonus_shield_active',
    'btn_bonus_shield',
    'draw'
    )
    condition_btn(form_data, 
    'bonus_heal_used',
    'bonus_heal_active',
    'btn_bonus_heal_active',
    'btn_bonus_heal',
    'draw'
    )


    nivel_cartas.draw(form_data.get('level'))

def inicializar_juego(form_data: dict) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:`` 
        Inicializa el juego, o en su defecto lo "reinicia de 0".
        Carga en el elemento 'level' del form data, toda la información necesaria
        Para que el usuario pueda iniciar una partida sin problema. \n

    ``¿Qué Devuelve?:`` 
        None.
    """
    form_data['level'] = nivel_cartas.reiniciar_nivel(
            form_data.get('level'), form_data.get('jugador'), 
            form_data.get('screen'), form_data.get('level_number')
    )
    nivel_cartas.inicializar_data_nivel(form_data.get('level'))

    form_data.get('widgets_list')[2] = ButtonImage(
        x=1200, y=var.CENTRO_DIMENSION_Y + 25, width=126, height=40,
        text='shield', screen=form_data.get('screen'), image_path='./modulos/assets/img/buttons_image/btn_play_hand.png', 
        on_click=nivel_cartas.jugar_mano, on_click_param= form_data.get('level')
    )

def check_juego_terminado(form_data: dict) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario.

    ``¿Qué hace?:`` 
        Revisa si el juego está terminado, de ser así detiene la música
        Inicia la música del form "Enter name", y tmb activa dicho form.

    ``¿Qué Devuelve?:`` 
        None.
    """
    if nivel_cartas.juego_terminado(form_data.get('level')):
        base_form.stop_music()
        base_form.play_music(base_form.forms_dict['form_enter_name'])
        base_form.set_active('form_enter_name')

def update(form_data: dict, event_list: list[pg.event.Event]) -> None:
    """ 
    ``Parametros:`` 
        Recibe la data del formulario en formato diccionario, y la lista de eventos

    ``¿Qué hace?:`` 
        Se encarga de actualizar todo el listado de widgets, incluyendo labels.\n
        A su vez revisa la condición de los bonus de heal y shild.

    ``¿Qué Devuelve?:`` 
        None.
    """
    # base_form.update(form_data)
    form_data['lbl_clock'].update_text(f'TIME LEFT: {form_data.get('level').get('level_timer')}', (255,0,0)) #Valor actualizado, y color del mismo
    form_data['lbl_score'].update_text(f'SCORE: {form_data.get('jugador').get('puntaje_actual')}', (255,0,0)) #Valor actualizado, y color del mismo
    #Actualiza stats jugador
    form_data['lbl_hp'].update_text(f'HP: {form_data.get('level').get('jugador').get('vida_actual')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    form_data['lbl_atk'].update_text(f'ATK: {form_data.get('level').get('jugador').get('atk_total')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    form_data['lbl_def'].update_text(f'DEF: {form_data.get('level').get('jugador').get('def_total')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    #Actualiza stats rival
    form_data['lbl_hp_rival'].update_text(f'HP: {form_data.get('level').get('rival').get('vida_actual')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    form_data['lbl_atk_rival'].update_text(f'ATK: {form_data.get('level').get('rival').get('atk_total')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    form_data['lbl_def_rival'].update_text(f'DEF: {form_data.get('level').get('rival').get('def_total')}', var.COLOR_AMARILLO) #Valor actualizado, y color del mismo
    
    widgets_list = form_data.get('widgets_list')
    
    for widget_index in range(len(widgets_list)):

        widgets_list[widget_index].update()
    
    condition_btn(form_data, 
    'bonus_shield_used',
    'bonus_shield_active',
    'btn_bonus_shield_active',
    'btn_bonus_shield',
    'update'
    )
    condition_btn(form_data, 
    'bonus_heal_used',
    'bonus_heal_active',
    'btn_bonus_heal_active',
    'btn_bonus_heal',
    'update'
    )
    nivel_cartas.update(form_data.get('level'), event_list)
    
    form_data['clock'].tick(var.FPS)
    actualizar_timer(form_data)
    check_juego_terminado(form_data)
    events_handler(event_list)