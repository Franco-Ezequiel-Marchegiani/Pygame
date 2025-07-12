import pygame as pg 
import modulos.variables as var
import modulos.auxiliar as aux
import random as rd
import modulos.carta as carta
import modulos.jugador as jugador_humano
import modulos.forms.base_form as base_form
def inicializar_nivel_cartas(jugador: dict, pantalla: pg.Surface, nro_nivel: int):
    
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

#Usarla cada vez que necesitemos cargar toda la data de 0, o al volver al menú inicio para refrescar la partida
def inicializar_data_nivel(nivel_data: dict):
    print('ESTOY GASTANDO RECURSOS Y CARGANDO TODA LA DATA DEL LEVEL')
    cargar_configs_nivel(nivel_data)
    cargar_bd_cartas(nivel_data, True)
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

        nivel_data['ruta_base'] = nivel_data.get('configs').get('ruta_base')
        nivel_data['ruta_mazo'] = nivel_data.get('configs').get('ruta_mazo')
        nivel_data['ruta_mazo_rival'] = nivel_data.get('configs').get('ruta_mazo_rival')
        nivel_data['cantidades'] = nivel_data.get('configs').get('cantidades')
        nivel_data.get('jugador')['coords_iniciales'] = nivel_data.get('configs').get('coordenada_mazo_1')
        nivel_data.get('jugador')['coords_finales'] = nivel_data.get('configs').get('coordenada_mazo_2')
        nivel_data.get('rival')['coords_iniciales'] = nivel_data.get('configs').get('coordenada_mazo_rival_1')
        nivel_data.get('rival')['coords_finales'] = nivel_data.get('configs').get('coordenada_mazo_rival_2')

def get_list_deck_name(nivel_data: dict) -> tuple[list, list]:
    # Obtenemos el dict de "cantidades" de nivel_data
    # Para luego obtener sus keys (que en ellas contiene el final del nombre de la ruta)
    # Lo transformamos en una lista y la retornamos, para luego poder iterarlo en cargar_bd_oponente
    dict_cantidad_cartas = nivel_data['cantidades']
    keys_dict_cartas = dict_cantidad_cartas.keys()
    list_of_keys = list(keys_dict_cartas)
    values_dict_cartas = dict_cantidad_cartas.values()
    list_of_values = list(values_dict_cartas)
    return (list_of_keys, list_of_values)

def recorrer_deck_individual(deck_completo: list, contenedor_deck: list) -> None:
    #Sumamos cada carta individual, en el contenedor deck
    for index in range(len(deck_completo)):
            contenedor_deck.append(deck_completo[index])


def cargar_bd_oponente(nivel_data: dict, oponente_name: str, cartas_mazo_juego: str, nueva_partida: bool):
    #Cargamos las cartas en el mazo con la función Generar BD, y devuelve un dict, y obtenemos el listado de cartas
    #Se agrega la ruta del get, ya que devuelve un objeto con la ruta, y de ahí el diccionario
    #Si contador es igual o más que 3, no actualiza la vida, ya que sigue la misma partida solo que se quedaron sin cartas

    list_of_decks = get_list_deck_name(nivel_data)
    contenedor_deck = []
    contenedor_max_hp = 0
    contenedor_max_atk = 0
    contenedor_max_def = 0

    for index in range(len(list_of_decks[0])):
        #De la tupla, obtenemos la ruta completa, y la cantidad de cartas x mazo
        ruta_completa_mazo = nivel_data['ruta_base'] + list_of_decks[0][index]
        cant_carta_mazo = list_of_decks[1][index]
        #Obtenemos un mazo completo (ej deck_rojo)
        #Y luego recorremos carta por carta
        dict_mazo = aux.generar_bd(ruta_completa_mazo, cant_carta_mazo) #Cargar todas las cartas primero, dsp anadirle tope: cant_carta_mazo
        
        #For para recorrer cada deck con el largo completo
        deck_completo = dict_mazo.get('cartas').get(ruta_completa_mazo)
        recorrer_deck_individual(deck_completo, contenedor_deck)
        
        #Por último, en cada vuelta de cada tipo de deck, se le sumará las estadísticas máximas
        contenedor_max_hp += dict_mazo.get('max_stats').get('hp')
        contenedor_max_atk += dict_mazo.get('max_stats').get('atk')
        contenedor_max_def += dict_mazo.get('max_stats').get('def')
    
    #Asignamos los nuevos valores a nuestros diccionarios
    nivel_data[cartas_mazo_juego] = contenedor_deck    
    if nueva_partida == True:
        nivel_data[oponente_name]['vida_total'] = contenedor_max_hp
        nivel_data[oponente_name]['vida_actual'] = contenedor_max_hp

    nivel_data[oponente_name]['atk_total'] = contenedor_max_atk
    nivel_data[oponente_name]['def_total'] = contenedor_max_def


def cargar_bd_cartas(nivel_data: dict, nueva_partida: bool):
    if not nivel_data.get('juego_finalizado'):
        print('=============== GENERANDO BD CARTAS INICIALES ===============')
        cargar_bd_oponente(nivel_data,'jugador', 'cartas_mazo_juego', nueva_partida)
        cargar_bd_oponente(nivel_data,'rival', 'cartas_mazo_juego_rival', nueva_partida)


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
    #Las mezclamos, y creamos en el mismo dict la propiedad para ya utilizar
    rd.shuffle(participante.get('cartas_mazo_juego_final'))

def calcular_ganador_ronda(nivel_data: dict) -> dict:
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

    puntaje_ronda = 0
    ganador_ronda = ''
    #Si el ataque del usuario, es mayor al rival, ese será el puntaje
    if atk_jugador > atk_rival:
        puntaje_ronda = atk_jugador 
        nivel_data['rival']['vida_actual'] -= puntaje_ronda
        ganador_ronda = 'jugador'
    else:
        nivel_data['jugador']['vida_actual'] -= atk_rival
        ganador_ronda = 'rival'
    return {'ganador_ronda': ganador_ronda, 'puntaje_ronda': puntaje_ronda}

def validacion_uso_bonus() -> str:
    #Revisa y remueve la vista de los íconos del form start_level, y devuelve en formato str
    #El bonus activo en esta ronda para que jugar_mano haga la lógica

    bonus_shield_active = base_form.forms_dict['form_start_level']['bonus_shield_active'] 
    bonus_heal_active = base_form.forms_dict['form_start_level']['bonus_heal_active'] 

    #Si están activos alguno de los bufos, en el siguiente evento los actualiza el valur de que ya se usó
    if bonus_shield_active:
        #El escudo se activa recién cuando el rival gane la ronda, no es instantaneo
        return 'shield'
    
    if bonus_heal_active:
        base_form.forms_dict['form_start_level']['bonus_heal_used'] = True
        return 'heal'
    return ''

def bonus_heal(nivel_data: dict):
    nivel_data['jugador']['vida_actual'] = nivel_data['jugador']['vida_total']

def bonus_shield(nivel_data: dict, resultado_ronda: dict):
    if resultado_ronda.get('ganador_ronda') == 'rival':
        #Si la mano la gana el rival, entonces recién ahí se consume el buff y rebota el daño del enemigo
        atk_rival = nivel_data.get('rival').get('cartas_mazo_juego_final_vistas')[-1].get('atk')
        nivel_data['rival']['vida_actual'] -= atk_rival
        #Y recién ahora utiliza el bonus, y se elimina de la vista
        base_form.forms_dict['form_start_level']['bonus_shield_used'] = True
        #Le sumamos el puntaje el daño hecho por el enemigo a sí mismo:
        resultado_ronda['puntaje_ronda'] = atk_rival
contador_clicks = 0

def jugar_mano(nivel_data: dict):
    if nivel_data.get('jugador').get('cartas_mazo_juego_final') and\
        not nivel_data.get('jugador').get('cartas_mazo_juego_final')[-1].get('visible'):
        
        print(f"contador_clicks: {contador_clicks}")
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


        bonus_value = validacion_uso_bonus()

        resultado_ronda = calcular_ganador_ronda(nivel_data)
        
        #Según el valor que retorne, activa un bonus o el otro
        if bonus_value == 'shield':
            bonus_shield(nivel_data, resultado_ronda)
        elif bonus_value == 'heal':
            bonus_heal(nivel_data)
        #Sumamos los puntos de cada ronda con esta función
        jugador_humano.sumar_puntaje_actual(nivel_data.get('jugador'), resultado_ronda.get('puntaje_ronda'))
        

def eventos(cola_eventos: list[pg.event.Event]):
    
    for evento in cola_eventos:
        #Si damos click, se ejecuta el código
        if evento.type == pg.MOUSEBUTTONDOWN:
            pass
            # print(f'Coordenada: {evento.pos}')
            

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
    

def juego_terminado(nivel_data: dict) -> bool:
    #Nos devuelve el valor bool que tenemos en 'juego_finalizado'
    return nivel_data.get('juego_finalizado') 

#Asegurarse de reiniciar tmb el deck rival, así no se duplica
def reiniciar_nivel(nivel_cartas: dict, jugador: dict, pantalla: pg.Surface, nro_nivel: int):
    print('=============== REINICIANDO NIVEL ===============')
    #Obtenemos los valores de si ya se usó el bono, y los refrescamos
    base_form.forms_dict['form_start_level']['bonus_shield_used'] = False
    base_form.forms_dict['form_start_level']['bonus_heal_used'] = False
    base_form.forms_dict['form_start_level']['bonus_shield_active'] = False
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
    eventos(cola_eventos)
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
