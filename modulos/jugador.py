import modulos.carta as carta

def inicializar_oponente(inicializar_screen) -> dict:
    """ 
    Parametro: 
        inicializar_screen, para poder mostrarlo en pantalla

    ¿Qué hace?:
        Crea un diccionario y en él agrega los elementos claves para cada carta
    
    ¿Qué Devuelve?: 
        Un diccionario, con la estructura base ya definida.
    """
    jugador_actual = {}
    jugador_actual['vida_total'] = 0
    jugador_actual['vida_actual'] = 0
    jugador_actual['atk_total'] = 0
    jugador_actual['def_total'] = 0
    jugador_actual['puntaje_actual'] = 0
    jugador_actual['puntaje_total'] = 0
    jugador_actual['ganador'] = ''
    jugador_actual['nombre'] = ''
    jugador_actual['screen'] = inicializar_screen
    jugador_actual['coords_iniciales'] = []
    jugador_actual['coords_finales'] = []
    jugador_actual['cartas_mazo_juego_final'] = []
    jugador_actual['cartas_mazo_juego_final_vistas'] = []

    return jugador_actual

def draw_participante(jugador: dict):
    if jugador.get('cartas_mazo_juego_final'):
        carta.draw_carta(jugador.get('cartas_mazo_juego_final')[-1], jugador.get('screen'))
        
    if jugador.get('cartas_mazo_juego_final_vistas'):
        carta.draw_carta(jugador.get('cartas_mazo_juego_final_vistas')[-1], jugador.get('screen'))

def sumar_puntaje_actual(jugador_actual: dict, nuevo_puntaje: int) -> None:
    """ 
    Parametros: 
        "jugador_actual" - información del jugador en formato dict
        "nuevo_puntaje" - puntaje numérico

    ¿Qué hace?:
        Le asigna el nuevo puntaje al elemento "puntaje_actual" del dict. Jugador \n
        Utilizando para ello el nuevo puntaje que recibe por parametro 
    
    ¿Qué Devuelve?: 
        None
    """
    jugador_actual['puntaje_actual'] += nuevo_puntaje

def actualizar_puntaje_total(jugador_actual: dict) -> None:
    """ 
    Parametros: 
        "jugador_actual" - información del jugador en formato dict
        "nuevo_puntaje" - puntaje numérico

    ¿Qué hace?:
        Le asigna el puntaje actual al elemento "puntaje_total" para que quede guardado
    
    ¿Qué Devuelve?: 
        None
    """
    jugador_actual['puntaje_total'] += jugador_actual.get('puntaje_actual')

def get_puntaje_actual(jugador_actual: dict) -> int:
    """ 
    Parametro: 
        "jugador_actual" - información del jugador en formato dict

    ¿Qué hace?:
        Devuelve el puntaje actual del usuario

    ¿Qué Devuelve?: 
        El puntaje actual en formato int
    """
    return jugador_actual.get('puntaje_actual')

def get_puntaje_total(jugador_actual: dict) -> int:
    """ 
    Parametro: 
        "jugador_actual" - información del jugador en formato dict

    ¿Qué hace?:
        Devuelve el puntaje total del usuario

    ¿Qué Devuelve?: 
        El puntaje total en formato int
    """
    return jugador_actual.get('puntaje_total')

def get_nombre(jugador_actual: dict) -> str:
    """ 
    Parametro: 
        "jugador_actual" - información del jugador en formato dict

    ¿Qué hace?:
        Devuelve el nombre del usuario

    ¿Qué Devuelve?: 
        El nombre en formato str
    """
    return jugador_actual.get('nombre')

def set_puntaje_actual(jugador_actual: dict, nuevo_puntaje: int) -> None:
    """ 
    Parametro: 
        "jugador_actual" - información del jugador en formato dict
        "nuevo_puntaje" - puntaje numérico

    ¿Qué hace?:
        Asigna el nuevo puntaje al elemento "puntaje_actual" del dict. Jugador

    ¿Qué Devuelve?: 
        None
    """
    jugador_actual['puntaje_actual'] = nuevo_puntaje

def set_puntaje_total(jugador_actual: dict, nuevo_puntaje: int) -> None:
    """ 
    Parametro: 
        "jugador_actual" - información del jugador en formato dict
        "nuevo_puntaje" - puntaje numérico

    ¿Qué hace?:
        Asigna el nuevo puntaje al elemento "puntaje_total" del dict. Jugador

    ¿Qué Devuelve?: 
        None
    """
    jugador_actual['puntaje_total'] = nuevo_puntaje

def set_nombre(jugador_actual: dict, nuevo_texto: str) -> None:
    """ 
    Parametro: 
        "jugador_actual" - información del jugador en formato dict
        "nuevo_texto" - nuevo texto str

    ¿Qué hace?:
        Asigna el nuevo nombre al elemento "nombre" del dict. Jugador

    ¿Qué Devuelve?: 
        None
    """
    jugador_actual['nombre'] = nuevo_texto