import pygame as pg
import modulos.variables as var
import sys
import modulos.auxiliar as aux
import modulos.forms.form_manager as form_manager
def pythonisa():
    pg.init()
    pg.display.set_caption(var.TITULO_JUEGO)
    pantalla = pg.display.set_mode(var.DIMENSION_PANTALLA)
    pg.display.set_icon(pg.image.load(var.RUTA_ICONO))
    corriendo = True
    reloj = pg.time.Clock()
    datos_juego = {
        "tiempo_finalizado": None,
        "player":{
            "name": 'Player',
            "puntaje": var.PUNTUACION_INICIAL, 
            "cantidad_vidas": var.CANTIDAD_VIDAS,
        }
    }

    f_manager = form_manager.create_form_manager(pantalla, datos_juego)

    while corriendo:

        event_list = pg.event.get()
        reloj.tick(var.FPS)

        for event in event_list:
            if event.type == pg.QUIT:
                corriendo = False
            elif event.type == pg.USEREVENT+5:
                print("Terminó la música inicial, comenzando bucle...")
                aux.inicializar_bucle_musica()
        
        #Actualiza las vistas
        form_manager.update(f_manager, event_list)

        pg.display.flip()

    pg.quit()
    sys.exit() #Finaliza cualquier proceso de Python