import pygame as pg
import variables as var
import auxiliar as aux
import frases as fra
cuadro_frase = aux.crear_cuadro(var.DIMENSION_CAJA_TEXTO, var.COORDENADA_CAJA_HISTORIA, (0,0,0))

def mostrar_historia(pantalla: pg.Surface, cola_eventos: list[pg.event.Event]) -> tuple:
    retorno = 'historia'
    bandera_juego = True
    pg.display.set_caption('HISTORIA')

    boton_volver = aux.crear_boton(pantalla, 'VOLVER', var.FUENTE_30, var.DIMENSION_BOTON, (993, 580), var.COLOR_NEGRO, var.COLOR_ROJO)

    for evento in cola_eventos:
        if evento.type == pg.QUIT:
            retorno = 'salir'
        elif evento.type == pg.MOUSEBUTTONDOWN:
            print(f"Coordenada: {evento.pos}")  
            if boton_volver.get('rectangulo').collidepoint(evento.pos):
                var.CLICK_SONIDO.play()
                retorno = 'menu'
                bandera_juego = False
                aux.terminar_musica()
    
    pantalla.fill(var.COLOR_BLANCO)
    pantalla.blit(var.FONDO, var.FONDO.get_rect())

    aux.mostrar_boton(boton_volver)

    aux.mostrar_texto(cuadro_frase['superficie'], fra.historia, (20,20), var.FUENTE_22, (0, 255, 0))
    cuadro_frase['rectangulo'] = pantalla.blit(cuadro_frase["superficie"], cuadro_frase['rectangulo'].topleft)
    pg.draw.rect(pantalla, (0,0,0), cuadro_frase['rectangulo'], 2)

    return retorno, bandera_juego