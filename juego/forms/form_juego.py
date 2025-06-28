import pygame as pg
import Pygame.variables as var
import Pygame.juego.auxiliar as aux
import Pygame.juego.frases as fra
import random as rd
import Pygame.juego.carta as carta

cuadro_titulo = aux.crear_cuadro(var.DIMENSION_TITULO, var.COORDENADA_CAJA_HISTORIA, var.COLOR_BLANCO)
cuadro_frase = aux.crear_cuadro(var.DIMENSION_FRASE, var.COORDENADA_CAJA_HISTORIA, var.COLOR_BLANCO)

rd.shuffle(fra.lista_frases)

cartas = aux.generar_bd(var.RUTA_MAZO_MAIN)
raider_waite = cartas.get('cartas').get('raider_waite')
senkai_yami = cartas.get('cartas').get('senkai_yami')

raider_waite = aux.asignar_frases(raider_waite, fra.lista_frases)
senkai_yami = aux.asignar_frases(senkai_yami, fra.lista_frases)

lista_cartas_dictionary = aux.generar_mazo(raider_waite)

lista_cartas_dictionary.extend(aux.generar_mazo(senkai_yami))
rd.shuffle(lista_cartas_dictionary)

lista_cartas_vistas = []

def mostrar_juego(pantalla: pg.Surface, cola_eventos: list[pg.event.Event], datos_juego: dict) -> tuple:

    boton_volver = aux.crear_boton(pantalla, 'VOLVER', var.FUENTE_30, var.DIMENSION_BOTON, (993, 580), (0,0,0), (255,0,0))
    bandera_juego = True

    retorno = 'juego'

    for evento in cola_eventos:
        if evento.type == pg.QUIT:
            retorno = 'salir'
        elif evento.type == pg.MOUSEBUTTONDOWN:
            print(f"Coordenada: {evento.pos}")  
            if boton_volver.get('rectangulo').collidepoint(evento.pos):
                retorno = 'menu'
            
            #Si todavía tengo cartas en el mazo original, y en donde dí click corresponde al area del mazo
            #Y además esa última carta que le di click, no está visible, entonces...
            if lista_cartas_dictionary and\
                lista_cartas_dictionary[-1].get('rect').collidepoint(evento.pos) and\
                not lista_cartas_dictionary[-1].get('visible'):
                    carta.asignar_coordenadas_carta(lista_cartas_dictionary[-1], var.COORDENADA_CARTA_VISTA)
                    carta.cambiar_visibilidad_carta(lista_cartas_dictionary[-1])

                    #Sacamos el último elemento, y lo guardamos en la lista de cartas vistas
                    carta_vista = lista_cartas_dictionary.pop()
                    lista_cartas_vistas.append(carta_vista)

                    print(f"Frase actual: {lista_cartas_vistas[-1].get('frase')}")
                    

    pantalla.fill(var.COLOR_VIOLETA)
    pantalla.blit(var.FONDO, var.FONDO.get_rect())

    aux.mostrar_texto(cuadro_titulo['superficie'], 'La PYTHONisa del Tarot', (20,20), var.FUENTE_30, var.COLOR_VERDE)
    aux.mostrar_boton(boton_volver)


    if lista_cartas_dictionary:
        carta.draw_carta(lista_cartas_dictionary[-1], pantalla)
        
    if lista_cartas_vistas:
        carta.draw_carta(lista_cartas_vistas[-1], pantalla)
        #Gestionar mensaje texto
        aux.mostrar_texto(cuadro_frase.get('superficie', f'{lista_cartas_vistas[-1].get("frase")}', (20, 20), var.FUENTE_22, var.COLOR_BLANCO))
        cuadro_frase['rectangulo'] = pantalla.blit(cuadro_frase['superficie'], cuadro_frase['rectangulo'].topleft)

    cuadro_titulo['rectangulo'] = pantalla.blit(cuadro_titulo['superficie'], cuadro_titulo['rectangulo'].topleft)

    """ for carta in lista_cartas_dictionary:
        carta.draw_carta(carta, pantalla)

    for carta_v in lista_cartas_vistas:
        carta.draw_carta(carta, pantalla) """

    if not lista_cartas_dictionary and not datos_juego.get('tiempo_finalizado'):
        datos_juego['tiempo_finalizado'] = pg.time.get_ticks()
    
    if not lista_cartas_dictionary:
        retorno = aux.verificar_tiempo_cumplido(datos_juego.get('tiempo_finalizado'), ('menu', 'juego'))

    # cuadro_frase['rectangulo'] = pantalla.blit(cuadro_frase["superficie"], cuadro_frase['rectangulo'].topleft)

    return retorno, bandera_juego