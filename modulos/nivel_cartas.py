import pygame as pg 
import modulos.variables as var
import modulos.auxiliar as aux
import random as rd
import modulos.carta as carta
import modulos.jugador as jugador_humano
import modulos.forms.base_form as base_form
def inicializar_nivel_cartas(jugador: dict, pantalla: pg.Surface, nro_nivel: int) -> dict:
    """ 
    ``Parametro:`` 
        "jugador" - Recibe la data del formulario en formato diccionario
        "pantalla" - superficie de PG
        "nro_nivel" - Número de nivel actual int

    ``¿Qué hace?:``
        Crea un diccionario y en él agrega los elementos claves para cada nivel
    
    ``¿Qué Devuelve?:`` 
        Un diccionario, con la estructura base ya definida.
    """
    nivel_data = {}
    nivel_data['nro_nivel'] = nro_nivel
    nivel_data['configs'] = {}
    nivel_data['cartas_mazo_juego'] = []
    nivel_data['cartas_mazo_juego_rival'] = []
    nivel_data['cantidades'] = []
    nivel_data['ruta_base'] = ''
    nivel_data['ruta_mazo'] = ''
    nivel_data['ruta_mazo_rival'] = ''
    nivel_data['screen'] = pantalla
    nivel_data['jugador'] = jugador 
    nivel_data['rival'] = jugador_humano.inicializar_oponente(nivel_data['screen']) 
    nivel_data['juego_finalizado'] = False
    nivel_data['puntaje_guardado'] = False
    nivel_data['level_timer'] = var.TIMER
    nivel_data['ganador'] = None
    nivel_data['puntaje_nivel'] = 0
    nivel_data['data_cargada'] = False
    
    return nivel_data

#25% de chance de golpe crítico
crit_list = [1]*25 + [0]*75

#Usarla cada vez que necesitemos cargar toda la data de 0, o al volver al menú inicio para refrescar la partida
def inicializar_data_nivel(nivel_data: dict) -> None:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        Inicializa un conjunto de funciones para levantar el funcionamiento del nivel \n
        Es el corazón de la lógica, utilizando las funciones:
            - cargar_configs_nivel
            - cargar_bd_cartas
            - generar_mazo
            - generar_mazo
    
    ``¿Qué Devuelve?:``
        None
    """
    cargar_configs_nivel(nivel_data)
    cargar_bd_cartas(nivel_data, True)
    generar_mazo(nivel_data['cartas_mazo_juego'], nivel_data['jugador'])
    generar_mazo(nivel_data['cartas_mazo_juego_rival'], nivel_data['rival'])

def cargar_configs_nivel(nivel_data: dict) -> None:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        Si el juego no terminó, y la data no se cargó todavía, carga las configuraciones del nivel \n
        Obtiene la info con ayuda de la función *cargar_configs*, y se la asigna al \n
        diccionario de nivel_data
    
    ``¿Qué Devuelve?:``
        None
    """
    if not nivel_data.get('juego_finalizado') and not nivel_data.get('data_cargada'):
        configs_globales = aux.cargar_configs(var.RUTA_CONFIGS_JSON)
        nivel_data['configs'] = configs_globales.get(f'nivel_{nivel_data.get("nro_nivel")}')

        nivel_data['ruta_base'] = nivel_data.get('configs').get('ruta_base')
        nivel_data['ruta_mazo'] = nivel_data.get('configs').get('ruta_mazo')
        nivel_data['ruta_mazo_rival'] = nivel_data.get('configs').get('ruta_mazo_rival')
        nivel_data['cantidades'] = nivel_data.get('configs').get('cantidades')
        nivel_data.get('jugador')['coords_iniciales'] = nivel_data.get('configs').get('coordenada_mazo_1')
        nivel_data.get('jugador')['coords_finales'] = nivel_data.get('configs').get('coordenada_mazo_2')
        nivel_data.get('rival')['coords_iniciales'] = nivel_data.get('configs').get('coordenada_mazo_rival_1')
        nivel_data.get('rival')['coords_finales'] = nivel_data.get('configs').get('coordenada_mazo_rival_2')

def get_list_deck_name(nivel_data: dict) -> tuple[list, list]:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        Guarda el valor de "cantidades" (que se guardó en el dict desde la configuración) \n
        Luego extrae por un lado las keys del diccionario, y por otro los values \n
    
    ``¿Qué Devuelve?:``
        Una tupla con la lista de las llaves, y los valores
    """
    dict_cantidad_cartas = nivel_data['cantidades']
    keys_dict_cartas = dict_cantidad_cartas.keys()
    list_of_keys = list(keys_dict_cartas)
    values_dict_cartas = dict_cantidad_cartas.values()
    list_of_values = list(values_dict_cartas)
    return (list_of_keys, list_of_values)

def recorrer_deck_individual(deck_completo: list, contenedor_deck: list) -> None:
    """ 
    ``Parametros:``
        *deck_completo* - Listado con los decks completos
        *contenedor_deck* - Listado de contenedor a utilizar

    ``¿Qué hace?:``
        Pequeño for que recorre el deck completo, y añade cada carta al contenedor \n
    
    ``¿Qué Devuelve?:``
        Una tupla con la lista de las llaves, y los valores
    """
    for index in range(len(deck_completo)):
            contenedor_deck.append(deck_completo[index])

def cargar_bd_oponente(nivel_data: dict, oponente_name: str, cartas_mazo_juego: str, nueva_partida: bool) -> None:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario
        *oponente_name* - nombre del oponente (jugador o rival) 
        *cartas_mazo_juego* - Nombre del mazo a poblar el deck (si para el jugador, o rival)
        *nueva_partida* - Booleano para saber si es una partida nueva, o si no hay más cartas en el match actual

    ``¿Qué hace?:``
        Con ayuda de *get_list_deck_name* separamos el diccionario, por un lado las key contiene las rutas \n
        Para obtener las rutas de los decks. Y los values obtiene las cantidades de cartas por deck \n
        Luego crea contenedores de deck, y de las stats (hp, atk y def). \n

        Recorre el listado de decks, invoca a la función *generar_bd* y le pasa por parametro la ruta y cantidad. \n
        De ahí poblamos en el elemento "cartas" del dict nivel_data. Y usamos la función *recorrer_deck_individual* \n
        Para poblar carta por carta en la lista de "contenedor_deck". Y esa lista de diccionarios \n
        Es asignada al valor de *cartas_mazo_juego* recibido por parámetro, para definir a qué oponente corresponde. \n
        Por último, también almacena las estadísticas totales, si la partida continua no refresca la vida.

    ``¿Qué Devuelve?:``
        None
    """
    list_of_decks = get_list_deck_name(nivel_data)
    contenedor_deck = []
    contenedor_max_hp = 0
    contenedor_max_atk = 0
    contenedor_max_def = 0

    for index in range(len(list_of_decks[0])):
        ruta_completa_mazo = nivel_data['ruta_base'] + list_of_decks[0][index]
        cant_carta_mazo = list_of_decks[1][index]
        dict_mazo = aux.generar_bd(ruta_completa_mazo, cant_carta_mazo) 
        deck_completo = dict_mazo.get('cartas').get(ruta_completa_mazo)
        recorrer_deck_individual(deck_completo, contenedor_deck)
        
        contenedor_max_hp += dict_mazo.get('max_stats').get('hp')
        contenedor_max_atk += dict_mazo.get('max_stats').get('atk')
        contenedor_max_def += dict_mazo.get('max_stats').get('def')
    
    nivel_data[cartas_mazo_juego] = contenedor_deck    
    if nueva_partida == True:
        nivel_data[oponente_name]['vida_total'] = contenedor_max_hp
        nivel_data[oponente_name]['vida_actual'] = contenedor_max_hp

    nivel_data[oponente_name]['atk_total'] = contenedor_max_atk
    nivel_data[oponente_name]['def_total'] = contenedor_max_def


def cargar_bd_cartas(nivel_data: dict, nueva_partida: bool) -> None:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario
        *nueva_partida* - Booleano para saber si es una partida nueva, o si no hay más cartas en el match actual

    ``¿Qué hace?:``
        Genera el deck para cada oponente, para el jugador y el rival con ayuda de la función *cargar_bd_oponente* \n
        
    ``¿Qué Devuelve?:``
        None
    """
    if not nivel_data.get('juego_finalizado'):
        print('=============== GENERANDO BD CARTAS INICIALES ===============')
        cargar_bd_oponente(nivel_data,'jugador', 'cartas_mazo_juego', nueva_partida)
        cargar_bd_oponente(nivel_data,'rival', 'cartas_mazo_juego_rival', nueva_partida)

def generar_mazo(lista_cartas_nivel: list, participante: dict) -> None:
    """ 
    ``Parametros:``
        *lista_cartas_nivel* - Listado de las cartas del nivel
        *participante* - Diccionario indicando si el oponente es el jugador, o el rival

    ``¿Qué hace?:``
        Creamos primero una lista vacía para almacenar allí las cartas inicializadas. \n
        En esta instancia se ordena en una lista cada carta inicializada con ayuda de *inicializar_carta* \n
        Para luego poblarla en la lista del diccionario "cartas_mazo_juego_final". \n
        Luego mezcla la lista, y ya el deck está listo para utilizar.

    ``¿Qué Devuelve?:``
        None
    """
    participante['cartas_mazo_juego_final'] = []
    
    for card in lista_cartas_nivel:
        carta_final = carta.inicializar_carta(card, participante.get('coords_iniciales'))
        participante['cartas_mazo_juego_final'].append(carta_final)
    
    participante['cartas_mazo_juego_final'] = participante['cartas_mazo_juego_final']
    rd.shuffle(participante.get('cartas_mazo_juego_final'))

def calcular_ganador_ronda(nivel_data: dict, golpe_critico: bool) -> dict:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario
        *golpe_critico* - Valor bool para definir el daño crítico

    ``¿Qué hace?:``
        Calcula el atk y def de cada oponente. Si el ataque del jugador es mayor,\n
        Se reduce la vida del rival con el 100% del ataque de la carta que hizo el jugador. \n
        Si el ataque del rival fue mayor, ocurre lo opuesto. \n
        También se registra el ganador de la ronda, y se suma puntaje según el daño que \n
        El jugador realice al rival (no se resta por el daño recibido).
    
    ``¿Qué Devuelve?:``
        Un diccionario con el string del ganador, y el puntaje hasta el momento.
    """
    nivel_data['jugador']['vida_actual']
    atk_jugador = nivel_data.get('jugador').get('cartas_mazo_juego_final_vistas')[-1].get('atk')

    nivel_data['rival']['vida_actual']
    atk_rival = nivel_data.get('rival').get('cartas_mazo_juego_final_vistas')[-1].get('atk')

    puntaje_ronda = 0
    ganador_ronda = ''
    multiplicador_golpe = 1
    if golpe_critico:
        multiplicador_golpe = 3
    #Si el ataque del usuario, es mayor al rival, ese será el puntaje
    if atk_jugador > atk_rival:
        puntaje_ronda = atk_jugador * multiplicador_golpe
        nivel_data['rival']['vida_actual'] -= puntaje_ronda
        ganador_ronda = 'jugador'
    else:
        nivel_data['jugador']['vida_actual'] -= atk_rival * multiplicador_golpe
        ganador_ronda = 'rival'

    return {'ganador_ronda': ganador_ronda, 'puntaje_ronda': puntaje_ronda}

def validacion_uso_bonus() -> str:
    """ 
    ``Parametros:``
        None

    ``¿Qué hace?:``
        Revisa y remueve la vista de los íconos del form start_level, y devuelve en formato str\n
        El bonus activo en esta ronda para que jugar_mano haga la lógica.
    
    ``¿Qué Devuelve?:``
        String indicando el bonus activo
    """

    bonus_shield_active = base_form.forms_dict['form_start_level']['bonus_shield_active'] 
    bonus_heal_active = base_form.forms_dict['form_start_level']['bonus_heal_active'] 
    bonus_name = ''

    if bonus_shield_active:
        bonus_name = 'shield'
    
    if bonus_heal_active:
        base_form.forms_dict['form_start_level']['bonus_heal_used'] = True
        bonus_name = 'heal'
    if bonus_shield_active and bonus_heal_active:
        bonus_name = 'ambos'
    return bonus_name

def bonus_heal(nivel_data: dict) -> None:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        Restaura la vida actual del jugador, y la reestablece al valor original al 100%\n
        Utilizando para esto el elemento 'vida_total', igualando su valor a 'vida_actual'.

    ``¿Qué Devuelve?:``
        None
    """
    nivel_data['jugador']['vida_actual'] = nivel_data['jugador']['vida_total']

def bonus_shield(nivel_data: dict, resultado_ronda: dict) -> None:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        SOLO SE ACTIVA si la mano la gana el rival, una vez aplicado ese caso,\n
        El daño que iba a recibir el jugador, es reflejado al rival, recibiendo el daño al 100%.\n
        Se remueve el ícono una vez que el rival gane la ronda, ya que ahí se refleja el daño.
        
    ``¿Qué Devuelve?:``
        None
    """
    if resultado_ronda.get('ganador_ronda') == 'rival':
        atk_rival = nivel_data.get('rival').get('cartas_mazo_juego_final_vistas')[-1].get('atk')
        nivel_data['rival']['vida_actual'] -= atk_rival
        base_form.forms_dict['form_start_level']['bonus_shield_used'] = True
        resultado_ronda['puntaje_ronda'] = atk_rival

def calculo_critico() -> bool:
    """ 
    ``Parametros:``
        None

    ``¿Qué hace?:``
        Selecciona un número random desde la lista de crit_list, en caso que sea 1\n
        Devuelve True haciendo un golpe crítico, caso contrario sigue todo normal.
    
    ``¿Qué Devuelve?:``
        Booleano
    """
    return rd.choice(crit_list) == 1

def sonido_golpe(golpe_critico: bool) -> None:
    """ 
    ``Parametros:``
        Booleano

    ``¿Qué hace?:``
        Si el valor de param es True, realiza un sonido, caso contrario reproduceotro\n
    
    ``¿Qué Devuelve?:``
        None
    """
    var.SOUND_CLICK_CRITICO.set_volume(0.15)
    if golpe_critico:
            var.SOUND_CLICK_CRITICO.play()
    else:
        var.SOUND_CLICK.play()

def jugar_mano(nivel_data: dict) -> None:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        Revisa que el jugador tenga cartas, y que la última carta NO sea visible\n
        Una vez revisado eso, le asigna las coordenadas a la carta, cambia su visibilidad \n
        Y se coloca en donde se indicaron las coordenadas. \n
        Luego va eliminando de a uno las cartas del mazo, y las agrega en *cartas_mazo_juego_final_vistas \n
        Indicando que ya fueron manos jugadas, tanto para el jugador como para el rival. \n
        Luego revisa si se activó algún bonus, y en base a eso llama a sus respectivas funciones \n
        Para activar los bufos, y suma el puntaje de la ronda.
    
    ``¿Qué Devuelve?:``
        None
    """
    if nivel_data.get('jugador').get('cartas_mazo_juego_final') and\
        not nivel_data.get('jugador').get('cartas_mazo_juego_final')[-1].get('visible'):
        
        golpe_critico = calculo_critico()
        sonido_golpe(golpe_critico)
        
        carta.asignar_coordenadas_carta(nivel_data.get('jugador').get('cartas_mazo_juego_final')[-1], nivel_data.get('jugador').get('coords_finales'))
        carta.cambiar_visibilidad_carta(nivel_data.get('jugador').get('cartas_mazo_juego_final')[-1])
        carta.asignar_coordenadas_carta(nivel_data.get('rival').get('cartas_mazo_juego_final')[-1], nivel_data.get('rival').get('coords_finales'))
        carta.cambiar_visibilidad_carta(nivel_data.get('rival').get('cartas_mazo_juego_final')[-1])
        
        carta_vista_jugador = nivel_data.get('jugador').get('cartas_mazo_juego_final').pop()
        nivel_data.get('jugador').get('cartas_mazo_juego_final_vistas').append(carta_vista_jugador)
        carta_vista_rival = nivel_data.get('rival').get('cartas_mazo_juego_final').pop()
        nivel_data.get('rival').get('cartas_mazo_juego_final_vistas').append(carta_vista_rival)


        bonus_value = validacion_uso_bonus()
        resultado_ronda = calcular_ganador_ronda(nivel_data, golpe_critico)
        if bonus_value == 'shield':
            bonus_shield(nivel_data, resultado_ronda)
        elif bonus_value == 'heal':
            bonus_heal(nivel_data)
        elif bonus_value == 'ambos':
            bonus_shield(nivel_data, resultado_ronda)
            bonus_heal(nivel_data)

        jugador_humano.sumar_puntaje_actual(nivel_data.get('jugador'), resultado_ronda.get('puntaje_ronda'))
        
def tiempo_esta_terminado(nivel_data: dict) -> bool:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        #Devuelve true o false, si el tiempo llegó a 0
    
    ``¿Qué Devuelve?:``
        Booleano
    """
    
    return nivel_data.get('level_timer') <= 0

def mazo_esta_vacio(nivel_data: dict) -> bool:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        Revisa cuando se terminaron las cartas para jugar

    ``¿Qué Devuelve?:``
        Booleano
    """
    return len(nivel_data.get('jugador').get('cartas_mazo_juego_final')) == 0

def definicion_ganador(nivel_data: dict) -> str:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        Calcula quién tiene más vida entre el jugador y el oponente, y define al ganador\n
        
    
    ``¿Qué Devuelve?:``
        String indicando al ganador
    """
    if nivel_data['jugador']['vida_actual'] > nivel_data['rival']['vida_actual']:
        return 'jugador'
    else:
        return 'rival'

def check_juego_terminado(nivel_data: dict) -> None:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        Revisa si la vida de alguno de los oponentes llegó a 0\n
        De ser así, cambia el valor del elemento *juego_finalizado* a true, y se asigna \n
        El ganador de la partida en *[jugador][ganador]*\n
        También valida si el mazo está vacío, de ser así, vacía las cartas vistas de ambos \n
        Oponentes, y les genera un nuevo mazo. \n
        También revisa si el tiempo terminó, gana el que tiene más vida en el momento
    
    ``¿Qué Devuelve?:``
        None
    """
    # Si se termina el mazo, o el tiempo, finaliza el juego
    # Para eso, cambia el valor bool de "juego_finalizado"
    vida_actual_jugador = nivel_data['jugador']['vida_actual']
    vida_actual_rival = nivel_data['rival']['vida_actual']
    if vida_actual_jugador <= 0 or vida_actual_rival <= 0:
            nivel_data['juego_finalizado'] = True
            nivel_data['jugador']['ganador'] = definicion_ganador(nivel_data)
    
    #Si no hay más cartas, se renuevan:
    if mazo_esta_vacio(nivel_data):
            #Poner acá un video o una animación o algo indicando que se está mezclando el mazo nuevamente.
            #La vida permanece, así que todo ok
            #Generando un nuevo mazo
            nivel_data.get('jugador')['cartas_mazo_juego_final_vistas'] = []
            nivel_data.get('rival')['cartas_mazo_juego_final_vistas'] = []
            #Generamos un nuevo mazo, sin perder el dato de la vida que se venía jugando
            cargar_bd_cartas(nivel_data, False)
            generar_mazo(nivel_data['cartas_mazo_juego'], nivel_data['jugador'])
            generar_mazo(nivel_data['cartas_mazo_juego_rival'], nivel_data['rival'])
            
    if tiempo_esta_terminado(nivel_data):
            nivel_data['juego_finalizado'] = True
            if vida_actual_jugador < vida_actual_rival:
                nivel_data['jugador']['ganador'] = 'rival'
            else:
                nivel_data['jugador']['ganador'] = 'jugador'


def juego_terminado(nivel_data: dict) -> bool:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        Nos devuelve el valor bool que tenemos en 'juego_finalizado'

    ``¿Qué Devuelve?:``
        Bool
    """
    return nivel_data.get('juego_finalizado') 

#Asegurarse de reiniciar tmb el deck rival, así no se duplica
def reiniciar_nivel(nivel_cartas: dict, jugador: dict, pantalla: pg.Surface, nro_nivel: int) -> dict:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario
        *jugador* - Recibe la data del formulario jugador en formato diccionario
        "pantalla" - superficie de PG
        "nro_nivel" - Número de nivel actual int

    ``¿Qué hace?:``
        Formatea todo de 0, más puntualmente:\n
        *bonus_shield_used*
        *bonus_heal_used*
        *bonus_shield_active*
        *bonus_heal_active*
        Como así también el puntaje del jugador, y las cartas vistas.\n
        Luego corre la función *inicializar_nivel_cartas* para arrancar nuevamente

    ``¿Qué Devuelve?:``
        Diccionario inicializando el nivel de cartas
    """
    base_form.forms_dict['form_start_level']['bonus_shield_used'] = False
    base_form.forms_dict['form_start_level']['bonus_heal_used'] = False
    base_form.forms_dict['form_start_level']['bonus_shield_active'] = False
    base_form.forms_dict['form_start_level']['bonus_heal_active'] = False
    jugador['cartas_mazo_juego_final_vistas'] = []
    jugador_humano.set_puntaje_actual(jugador, 0)
    nivel_cartas = inicializar_nivel_cartas(jugador, pantalla, nro_nivel)

    return nivel_cartas


def draw(nivel_data: dict) -> None:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        Dibuja cada deck, del jugador y el rival\n
        En una función optimizada *draw_participante*, y por parámetro se le pasa el dict de cada uno
    
    ``¿Qué Devuelve?:``
        None
    """
    jugador_humano.draw_participante(nivel_data.get('jugador'))
    jugador_humano.draw_participante(nivel_data.get('rival'))

def update(nivel_data: dict, cola_eventos: list[pg.event.Event]) -> None:
    """ 
    ``Parametros:``
        *nivel_data* - Recibe la data del formulario nivel_data en formato diccionario

    ``¿Qué hace?:``
        Manejar acá todo lo que se tenga que actualizar, ya sea la vida, barrera, etc.\n
        Revisa si la partida/juego ya terminó. En caso de haber terminado, actualiza el puntaje \n
        Y levanta la bandera en *puntaje_guardado*
    
    ``¿Qué Devuelve?:``
        None
    """
    check_juego_terminado(nivel_data)
    if juego_terminado(nivel_data) and not nivel_data.get('puntaje_guardado'):
        jugador_humano.actualizar_puntaje_total(nivel_data.get("jugador"))

        nivel_data['puntaje_guardado'] = True 
