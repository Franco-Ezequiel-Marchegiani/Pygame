import pygame as pg 
import modulos.variables as var
import modulos.auxiliar as aux
import random as rd
import modulos.frases as fra
import modulos.carta as carta
import modulos.jugador as jugador_humano

def inicializar_nivel_cartas(jugador: dict, pantalla: pg.Surface, nro_nivel: int):
    
    nivel_data = {}
    nivel_data['nro_nivel'] = nro_nivel
    nivel_data['configs'] = {}
    nivel_data['cartas_mazo_juego'] = []
    nivel_data['cartas_mazo_juego_final'] = []
    nivel_data['cartas_mazo_juego_final_vistas'] = []
    nivel_data['ruta_mazo'] = ''
    nivel_data['screen'] = pantalla
    nivel_data['jugador'] = jugador
    
    nivel_data['juego_finalizado'] = False
    nivel_data['puntaje_guardado'] = False
    nivel_data['level_timer'] = var.TIMER
    nivel_data['ganador'] = None
    
    """ nivel_data['surface'] = pg.image.load('./modulos/assets/img/background_cards.png').convert_alpha()
    nivel_data['surface'] = pg.transform.scale(nivel_data.get('surface'), var.DIMENSION_PANTALLA)
    
    nivel_data['rect'] = nivel_data.get('surface').get_rect()
    nivel_data['rect'].topleft = (0,0) """
    
    nivel_data['puntaje_nivel'] = 0
    nivel_data['data_cargada'] = False
    
    return nivel_data

#Usarla cada vez que necesitemos cargar toda la data de 0, o al volver al menú inicio para refrescar la partida
def inicializar_data_nivel(nivel_data: dict):
    print('ESTOY GASTANDO RECURSOS Y CARGANDO TODA LA DATA DEL LEVEL')
    cargar_configs_nivel(nivel_data)
    cargar_bd_cartas(nivel_data)
    #asignar_frases(nivel_data)
    generar_mazo(nivel_data)

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
        nivel_data['coords_iniciales'] = nivel_data.get('configs').get('coordenada_mazo_1')
        nivel_data['coords_finales'] = nivel_data.get('configs').get('coordenada_mazo_2')
        nivel_data['coords_rival_iniciales'] = nivel_data.get('configs').get('coordenada_mazo_rival_1')
        nivel_data['coords_rival_finales'] = nivel_data.get('configs').get('coordenada_mazo_rival_2')

def cargar_bd_cartas(nivel_data: dict):
    if not nivel_data.get('juego_finalizado'):
        print('=============== GENERANDO BD CARTAS INICIALES ===============')
        #Cargamos las cartas en el mazo con la función Generar BD, y devuelve un dict, y obtenemos el listado de cartas
        #Se agrega la ruta del get, ya que devuelve un objeto con la ruta, y de ahí el diccionario
        nivel_data['cartas_mazo_juego'] = aux.generar_bd(nivel_data.get('ruta_mazo')).get('cartas').get('./modulos/assets/img/decks/blue_deck_expansion_1')
        print(f'AFTER Nivel Cartas Mazo Juego: {nivel_data.get('cartas_mazo_juego')}')

#Reciclar esta función por el tema de asignar puntaje
""" def asignar_frases(nivel_data: dict) -> list[dict]:
    print('=============== ASIGNANDO FRASES ALEATORIAS ===============')
    lista_mazo = nivel_data.get('cartas_mazo_juego')
    for index_card in range(len(lista_mazo)):
        frase = rd.choice(fra.lista_frases)
        
        carta.set_frase(lista_mazo[index_card], frase.get('frase'))
        carta.set_puntaje(lista_mazo[index_card], frase.get('puntaje'))
    return lista_mazo """

def generar_mazo(nivel_data: dict):
    print('=============== GENERANDO MAZO FINAL ===============')
    #Para generar el mazo, obtenemos las cartas del mazo del dic, y los recorremos
    lista_mazo_original = nivel_data.get('cartas_mazo_juego')
    nivel_data['cartas_mazo_juego_final'] = []
    print(
        f'Coord iniciales: {nivel_data.get('coords_iniciales')}',
        f'Coord finales: {nivel_data.get('coords_finales')}', sep='\n'
    )
    for card in lista_mazo_original:
        carta_final = carta.inicializar_carta(card, nivel_data.get('coords_iniciales'))
        nivel_data['cartas_mazo_juego_final'].append(carta_final)
    
    #Se definen 10 cartas
    nivel_data['cartas_mazo_juego_final'] = nivel_data['cartas_mazo_juego_final'][:10]
    #Las mezclamos, y creamos en el mismo dict la propiedad para ya utilizar
    rd.shuffle(nivel_data.get('cartas_mazo_juego_final'))

def eventos(nivel_data: dict, cola_eventos: list[pg.event.Event]):
    
    for evento in cola_eventos:
        #Si damos click, se ejecuta el código
        if evento.type == pg.MOUSEBUTTONDOWN:
            print(f'Coordenada: {evento.pos}')
            # verificar la colision con el boton
            #Si hay cartas, y el usuario hace click se ejecuta esto:
            #cartas_mazo_juego_final = Mazo mezclado listo para jugar
            #cartas_mazo_juego_final_vistas = Cartas ya mostradas
            if nivel_data.get('cartas_mazo_juego_final') and\
                nivel_data.get('cartas_mazo_juego_final')[-1].get('rect').collidepoint(evento.pos) and\
                not nivel_data.get('cartas_mazo_juego_final')[-1].get('visible'):
                # var.CLICK_SONIDO.play()
                carta.asignar_coordenadas_carta(nivel_data.get('cartas_mazo_juego_final')[-1], nivel_data.get('coords_finales'))
                carta.cambiar_visibilidad_carta(nivel_data.get('cartas_mazo_juego_final')[-1])
                
                #Selecciona una carta random con .pop, y la sumamos a cartas vistas
                carta_vista = nivel_data.get('cartas_mazo_juego_final').pop()
                nivel_data.get('cartas_mazo_juego_final_vistas').append(carta_vista)
                nivel_data['jugador']['puntaje_actual'] += nivel_data.get('cartas_mazo_juego_final_vistas')[-1].get('atk')
                #Hacer que el puntaje del jugador, sea el resultado del sobrante de la resta del dato que le hace al rival
                #Ej, si tiene 2000 de defensa, y el usuario 2500 de atque, el puntaje en esa mano es de 500, por ej
                carta_actual = nivel_data.get('cartas_mazo_juego_final_vistas')[-1]
                print(f"Puntaje Actual: {nivel_data['jugador']['puntaje_actual']}")

                #jugador_humano.sumar_puntaje_carta_actual(nivel_data.get('jugador'), carta_actual)
                #
                #print(f'Puntaje Actual: {jugador_humano.get_puntaje_actual(nivel_data["jugador"])}')
                #
                #print(f'Frase actual: {nivel_data.get('cartas_mazo_juego_final_vistas')[-1].get('frase')}')

def tiempo_esta_terminado(nivel_data: dict) -> bool:
    #Devuelve true o false, si el tiempo llegó a 0
    return nivel_data.get('level_timer') <= 0

def mazo_esta_vacio(nivel_data: dict) -> bool:
    #Revisa cuando se terminaron las cartas para jugar
    return len(nivel_data.get('cartas_mazo_juego_final')) == 0
    #Tmb válido:
    # return not nivel_data.get('cartas_mazo_juego_final')

def check_juego_terminado(nivel_data: dict):
    # Si se termina el mazo, o el tiempo, finaliza el juego
    # Para eso, cambia el valor bool de "juego_finalizado"
    if mazo_esta_vacio(nivel_data) or\
        tiempo_esta_terminado(nivel_data):
            nivel_data['juego_finalizado'] = True

def juego_terminado(nivel_data: dict):
    return nivel_data.get('juego_finalizado')

def reiniciar_nivel(nivel_cartas: dict, jugador: dict, pantalla: pg.Surface, nro_nivel: int):
    print('=============== REINICIANDO NIVEL ===============')
    jugador_humano.set_puntaje_actual(jugador, 0)
    nivel_cartas = inicializar_nivel_cartas(jugador, pantalla, nro_nivel)
    return nivel_cartas

def draw(nivel_data: dict):
    #Llama a la función "draw_carta" y le pasa la última de cada mazo
    if nivel_data.get('cartas_mazo_juego_final'):
        carta.draw_carta(nivel_data.get('cartas_mazo_juego_final')[-1], nivel_data.get('screen'))
        
    if nivel_data.get('cartas_mazo_juego_final_vistas'):
        carta.draw_carta(nivel_data.get('cartas_mazo_juego_final_vistas')[-1], nivel_data.get('screen'))

def update(nivel_data: dict, cola_eventos: list[pg.event.Event]):
    eventos(nivel_data, cola_eventos)
    check_juego_terminado(nivel_data)
    if juego_terminado(nivel_data) and not nivel_data.get('puntaje_guardado'):
        jugador_humano.actualizar_puntaje_total(nivel_data.get("jugador"))
        nombre_elegido = rd.choice(var.nombres)
        jugador_humano.set_nombre(nivel_data.get("jugador"), nombre_elegido)
        aux.guardar_ranking(nivel_data.get('jugador'))
        nivel_data['puntaje_guardado'] = True
        print(f'Puntaje acumulado: {jugador_humano.get_puntaje_total(nivel_data.get("jugador"))}')
