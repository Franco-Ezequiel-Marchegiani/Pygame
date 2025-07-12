import pygame as pg 
import modulos.variables as var
import modulos.auxiliar as aux
import random as rd
import modulos.frases as fra
import modulos.carta as carta
import modulos.jugador as jugador_humano
import modulos.forms.base_form as base_form
def inicializar_nivel_cartas(jugador: dict, pantalla: pg.Surface, nro_nivel: int):
    
    nivel_data = {}
    nivel_data['nro_nivel'] = nro_nivel
    nivel_data['configs'] = {}

    #Estas listas, tendría que pasarla al módulo de "jugador", y pasarlo acá.
    #Guarda por acá los decks generados de la DB del usuario y el rival
    nivel_data['cartas_mazo_juego'] = []
    nivel_data['cartas_mazo_juego_rival'] = []
    #Define ambas rutas
    nivel_data['ruta_mazo'] = ''
    nivel_data['ruta_mazo_rival'] = ''
    nivel_data['screen'] = pantalla
    nivel_data['jugador'] = jugador #Pasar param para generar mazo, junto al listado ya cargado, cartas_mazo_juego
    nivel_data['rival'] = jugador_humano.inicializar_oponente(nivel_data['screen']) #jugador #Pasar param para generar mazo, junto al listado ya cargado, cartas_mazo_juego

    nivel_data['juego_finalizado'] = False
    nivel_data['puntaje_guardado'] = False
    nivel_data['level_timer'] = var.TIMER
    nivel_data['ganador'] = None #Guardar acá quién gane, si el jugador o el enemigo, entre esas 2 opciones
    
    nivel_data['puntaje_nivel'] = 0
    nivel_data['data_cargada'] = False
    
    return nivel_data

#Usarla cada vez que necesitemos cargar toda la data de 0, o al volver al menú inicio para refrescar la partida
def inicializar_data_nivel(nivel_data: dict):
    print('ESTOY GASTANDO RECURSOS Y CARGANDO TODA LA DATA DEL LEVEL')
    cargar_configs_nivel(nivel_data)
    cargar_bd_cartas(nivel_data)
    #asignar_frases(nivel_data)
    generar_mazo(nivel_data['cartas_mazo_juego'], nivel_data['jugador'])
    generar_mazo(nivel_data['cartas_mazo_juego_rival'], nivel_data['rival'])

def cargar_configs_nivel(nivel_data: dict):
    #Si el juego no finalizó, o no se cargó la data...
    if not nivel_data.get('juego_finalizado') and not nivel_data.get('data_cargada'):
        print('=============== CARGANDO CONFIGS INICIALES ===============')
        #Cargamos data del JSON
        configs_globales = aux.cargar_configs(var.RUTA_CONFIGS_JSON)
        #Asigamos estos valores al dict del nivel_data
        nivel_data['configs'] = configs_globales.get(f'nivel_{nivel_data.get("nro_nivel")}')
        print(f"nivel_data['configs']: {nivel_data['configs']}")

        nivel_data['ruta_mazo'] = nivel_data.get('configs').get('ruta_mazo')
        nivel_data['ruta_mazo_rival'] = nivel_data.get('configs').get('ruta_mazo_rival')
        nivel_data.get('jugador')['coords_iniciales'] = nivel_data.get('configs').get('coordenada_mazo_1')
        nivel_data.get('jugador')['coords_finales'] = nivel_data.get('configs').get('coordenada_mazo_2')
        nivel_data.get('rival')['coords_iniciales'] = nivel_data.get('configs').get('coordenada_mazo_rival_1')
        nivel_data.get('rival')['coords_finales'] = nivel_data.get('configs').get('coordenada_mazo_rival_2')

def cargar_bd_oponente(nivel_data: dict, oponente_name: str, cartas_mazo_juego: str, form_ruta_mazo: str,ruta_mazo: str,):
    #Cargamos las cartas en el mazo con la función Generar BD, y devuelve un dict, y obtenemos el listado de cartas
    #Se agrega la ruta del get, ya que devuelve un objeto con la ruta, y de ahí el diccionario
    dict_mazo = aux.generar_bd(nivel_data.get(form_ruta_mazo))
    nivel_data[cartas_mazo_juego] = dict_mazo.get('cartas').get(ruta_mazo)
    print(f'Oponente ya poblado: {dict_mazo.get('max_stats')}')
    
    #Ya que se recorrió el bucle una vez, aprovechamos y brindamos las max estadísticas a cada oponente
    nivel_data[oponente_name]['vida_total'] = dict_mazo.get('max_stats').get('hp')
    nivel_data[oponente_name]['vida_actual'] = dict_mazo.get('max_stats').get('hp')
    nivel_data[oponente_name]['atk_total'] = dict_mazo.get('max_stats').get('atk')
    nivel_data[oponente_name]['def_total'] = dict_mazo.get('max_stats').get('def')

def cargar_bd_cartas(nivel_data: dict):
    if not nivel_data.get('juego_finalizado'):
        print('=============== GENERANDO BD CARTAS INICIALES ===============')
        cargar_bd_oponente(nivel_data,'jugador', 'cartas_mazo_juego', 'ruta_mazo', './modulos/assets/img/decks/blue_deck_expansion_1')
        cargar_bd_oponente(nivel_data,'rival', 'cartas_mazo_juego_rival', 'ruta_mazo_rival', './modulos/assets/img/decks/blue_deck_expansion_2')
        print(f"Data jugador: {nivel_data['jugador']}")
        

#Crear una sola función, y pasarle los parámetros según sea el deck del jugador, o el rival

#Pasar por segundo param el dic del jugador o enemigo
#Primer param, pasar la lista donde quiero guardarlo.
#Y como segundo param, 
#Al llamar a esta función con el rival, pasarle la lista de cartas que el juego eligió para el rival, y el dict del rival
def generar_mazo(lista_cartas_nivel: list, participante: dict):
    print('=============== GENERANDO MAZO FINAL ===============')
    #Para generar el mazo, obtenemos las cartas del mazo del dic, y los recorremos
    participante['cartas_mazo_juego_final'] = []
    
    for card in lista_cartas_nivel:
        carta_final = carta.inicializar_carta(card, participante.get('coords_iniciales'))
        participante['cartas_mazo_juego_final'].append(carta_final)
    
    print(f"Participante: {len(participante['cartas_mazo_juego_final'])}")
    #Se definen 10 cartas
    participante['cartas_mazo_juego_final'] = participante['cartas_mazo_juego_final']# [:10]
    print(f"Primera carta: {participante['cartas_mazo_juego_final'][0]}")
    #Las mezclamos, y creamos en el mismo dict la propiedad para ya utilizar
    rd.shuffle(participante.get('cartas_mazo_juego_final'))

def calcular_ganador_ronda(nivel_data: dict) -> int:
    #Hace el cálculo del atk y def de cada oponente
    #Para luego hacer la respectiva suma, y retorna el puntaje ganado
    #En la ronda, y a la vez actualiza la barra de vida de cada oponente
    hp_total_jugador = nivel_data.get('jugador').get('vida_total')
    nivel_data['jugador']['vida_actual']
    atk_jugador = nivel_data.get('jugador').get('cartas_mazo_juego_final_vistas')[-1].get('atk')
    def_jugador = nivel_data.get('jugador').get('cartas_mazo_juego_final_vistas')[-1].get('def')

    nivel_data['rival']['vida_actual']
    atk_rival = nivel_data.get('rival').get('cartas_mazo_juego_final_vistas')[-1].get('atk')
    def_rival = nivel_data.get('rival').get('cartas_mazo_juego_final_vistas')[-1].get('def')

    print(f"hp_total_jugador: {hp_total_jugador}")
    print(f"nivel_data['jugador']['vida_actual']: {nivel_data['jugador']['vida_actual']}")
    print(f"atk_jugador: {atk_jugador}")
    print(f"def_jugador: {def_jugador}")

    print(f"nivel_data['rival']['vida_actual']: {nivel_data['rival']['vida_actual']}")
    print(f"atk_rival: {atk_rival}")
    print(f"def_rival: {def_rival}")
    puntaje_ronda = 0
    #Si el ataque del usuario, es mayor al rival, ese será el puntaje
    if atk_jugador > atk_rival:
        puntaje_ronda = atk_jugador - def_rival 
        nivel_data['rival']['vida_actual'] -= puntaje_ronda
    else:
        danio_rival = atk_rival - def_jugador
        nivel_data['jugador']['vida_actual'] -= danio_rival
    return puntaje_ronda

def jugar_mano(nivel_data: dict):
    if nivel_data.get('jugador').get('cartas_mazo_juego_final') and\
        not nivel_data.get('jugador').get('cartas_mazo_juego_final')[-1].get('visible'):
        
        var.SOUND_CLICK.play()
        carta.asignar_coordenadas_carta(nivel_data.get('jugador').get('cartas_mazo_juego_final')[-1], nivel_data.get('jugador').get('coords_finales'))
        carta.cambiar_visibilidad_carta(nivel_data.get('jugador').get('cartas_mazo_juego_final')[-1])
        #Asignar cartas tmb al rival
        carta.asignar_coordenadas_carta(nivel_data.get('rival').get('cartas_mazo_juego_final')[-1], nivel_data.get('rival').get('coords_finales'))
        carta.cambiar_visibilidad_carta(nivel_data.get('rival').get('cartas_mazo_juego_final')[-1])
        
        #Selecciona una carta random con .pop, y la sumamos a cartas vistas
        carta_vista_jugador = nivel_data.get('jugador').get('cartas_mazo_juego_final').pop()
        nivel_data.get('jugador').get('cartas_mazo_juego_final_vistas').append(carta_vista_jugador)
        
        #Carta rival    
        carta_vista_rival = nivel_data.get('rival').get('cartas_mazo_juego_final').pop()
        nivel_data.get('rival').get('cartas_mazo_juego_final_vistas').append(carta_vista_rival)

        puntaje_ronda = calcular_ganador_ronda(nivel_data)
        print(f"nivel_data.get('jugador').get('cartas_mazo_juego_final_vistas'): {nivel_data.get('jugador').get('cartas_mazo_juego_final_vistas')}")
        
        
        #ESTO HACERLO EN UNA FUNCIÓN APARTE
        
        #Acá revisa si alguno de los bonus está activo.
        #Si alguno de los dos es true, entonces activar el bonus que aplica, y dsp cambiar el valor de active a false
        
        bonus_shield_used = base_form.forms_dict['form_start_level']['bonus_shield_used'] 
        bonus_heal_used = base_form.forms_dict['form_start_level']['bonus_heal_used'] 
        #bonus_shield_used
        #bonus_heal_used
        #Si están activos alguno de los bufos, en el siguiente evento los actualiza el valur de que ya se usó
        if bonus_shield_used:
            base_form.forms_dict['form_start_level']['bonus_shield_active'] = True
        
        if bonus_heal_used:
            base_form.forms_dict['form_start_level']['bonus_heal_active'] = True
        print(f"bonus_shield_active Status: {base_form.forms_dict['form_start_level']['bonus_shield_active']}")
        print(f"bonus_heal_active Status: {base_form.forms_dict['form_start_level']['bonus_heal_active']}")
        #Esto funciona, guarda el puntaje del jugador en base al ataque (dsp analizar bien cómo sumar el puntaje)
        
        #Hacer que el puntaje del jugador, sea el resultado del sobrante de la resta del dato que le hace al rival
        #Ej, si tiene 2000 de defensa, y el usuario 2500 de atque, el puntaje en esa mano es de 500, por ej
        
        #Sumamos los puntos de cada ronda con esta función
        jugador_humano.sumar_puntaje_actual(nivel_data.get('jugador'), puntaje_ronda)
        
        #print(f'Frase actual: {nivel_data.get('cartas_mazo_juego_final_vistas')[-1].get('frase')}')
def eventos(nivel_data: dict, cola_eventos: list[pg.event.Event]):
    
    for evento in cola_eventos:
        #Si damos click, se ejecuta el código
        if evento.type == pg.MOUSEBUTTONDOWN:
            print(f'Coordenada: {evento.pos}')
            

def tiempo_esta_terminado(nivel_data: dict) -> bool:
    #Devuelve true o false, si el tiempo llegó a 0
    return nivel_data.get('level_timer') <= 0

def mazo_esta_vacio(nivel_data: dict) -> bool:
    #Revisa cuando se terminaron las cartas para jugar
    return len(nivel_data.get('jugador').get('cartas_mazo_juego_final')) == 0
    #Tmb válido:
    # return not nivel_data.get('cartas_mazo_juego_final')

def definicion_ganador(nivel_data: dict) -> str:
    if nivel_data['jugador']['vida_actual'] > nivel_data['rival']['vida_actual']:
        return 'jugador'
    else:
        return 'rival'

def check_juego_terminado(nivel_data: dict):
    # Si se termina el mazo, o el tiempo, finaliza el juego
    # Para eso, cambia el valor bool de "juego_finalizado"
    if nivel_data['jugador']['vida_actual'] <= 0 or nivel_data['rival']['vida_actual'] <= 0:
            nivel_data['juego_finalizado'] = True
            #Ganador:
            nivel_data['jugador']['ganador'] = definicion_ganador(nivel_data)
    
    if mazo_esta_vacio(nivel_data) or\
        tiempo_esta_terminado(nivel_data):
            nivel_data['juego_finalizado'] = True
    

def juego_terminado(nivel_data: dict) -> bool:
    #Nos devuelve el valor bool que tenemos en 'juego_finalizado'
    return nivel_data.get('juego_finalizado') 

#Asegurarse de reiniciar tmb el deck rival, así no se duplica
def reiniciar_nivel(nivel_cartas: dict, jugador: dict, pantalla: pg.Surface, nro_nivel: int):
    print('=============== REINICIANDO NIVEL ===============')
    #Obtenemos los valores de si ya se usó el bono, y los refrescamos
    base_form.forms_dict['form_start_level']['bonus_shield_used'] = False
    base_form.forms_dict['form_start_level']['bonus_shield_used'] = False
    base_form.forms_dict['form_start_level']['bonus_heal_active'] = False
    base_form.forms_dict['form_start_level']['bonus_heal_active'] = False
    #Reiniciamos para evitar que se muestren cartas
    jugador['cartas_mazo_juego_final_vistas'] = []
    #Llama a la función para setear el puntaje y reiniciarlo pasandole el valor de 0
    jugador_humano.set_puntaje_actual(jugador, 0)
    #Reiniciamos los valores de "inicializar_nivel_Cartas" para que pueda jugar nuevamente

    
    nivel_cartas = inicializar_nivel_cartas(jugador, pantalla, nro_nivel)

    #Al pasarle los valores y ejecutar la función, lo que hacemos es pisar los valores del dict e inicia de nuevo
    return nivel_cartas


def draw(nivel_data: dict):
    #Dibuja cada deck, del jugador y el rival
    #En una función optimizada, y por parámetro se le pasa el dict de cada uno
    jugador_humano.draw_participante(nivel_data.get('jugador'))
    jugador_humano.draw_participante(nivel_data.get('rival'))

def update(nivel_data: dict, cola_eventos: list[pg.event.Event]):
    #Manejar acá todo lo que se tenga que actualizar, ya sea la vida, barrera, etc.
    eventos(nivel_data, cola_eventos)
    #Revisa si la partida/juego ya terminó
    check_juego_terminado(nivel_data)
    #Si el juego terminó, y NO se guardó el puntaje...
    if juego_terminado(nivel_data) and not nivel_data.get('puntaje_guardado'):
        #Actualiza el puntaje del jugador
        jugador_humano.actualizar_puntaje_total(nivel_data.get("jugador"))
        
        #Guardamos una sola vez el puntaje guardado.
        nivel_data['puntaje_guardado'] = True 
        print(f'Puntaje final alcanzado: {jugador_humano.get_puntaje_total(nivel_data.get("jugador"))}')
        print(f'GANADOR VIEJO : {nivel_data['ganador']}')
        print(f'Y EL GANADOR ES... : {nivel_data['jugador']['ganador']}')

#Manejar acá la lógica de definir ganador, y demás, en los forms va solo info que se muestre, acá va toda la lógica pesada

#Crear la clave de "mazo" para el usuario y el enemigo, crear un dic para el enemigo tmb

#Que recorra todo el dict de cartas, y que a medida que levante una carta, se arme un dict.

#Probar tmb usando rd.sample para mezclar y distribuir las cartas seleccionadas