import pygame as pg
import modulos.variables as var
import sys
import modulos.forms.form_manager as form_manager
import modulos.jugador as jugador_humano
def dragon_ball_tcg() -> None:
    """ 
    ``Parametros:`` 
        None

    ``¿Qué hace?:``
        Levanta el juego, con el título, pantalla, dimensiones. \n
        Define un pequeño dict con la info del jugador \n
        Corre el juego hasta que finalice con .QUIT \n
        Y también actualiza las vistas de cada formulario con f_manager.

    ``¿Qué Devuelve?:`` 
        None
    """
    pg.display.set_caption(var.MAIN_TITLE)
    pantalla = pg.display.set_mode(var.DIMENSION_PANTALLA)
    pg.display.set_icon(pg.image.load(var.RUTA_ICONO))
    corriendo = True
    reloj = pg.time.Clock()
    datos_juego = {
        "tiempo_finalizado": None,
        "jugador": jugador_humano.inicializar_oponente(pantalla),
    }
    f_manager = form_manager.create_form_manager(pantalla, datos_juego)

    while corriendo:
        event_list = pg.event.get()
        reloj.tick(var.FPS)
        for event in event_list:
            if event.type == pg.QUIT:
                corriendo = False
    
        form_manager.update(f_manager, event_list)
        pg.display.flip()

    pg.quit()
    sys.exit()