
import pygame as pg
from forms import form_menu
import Pygame.variables as var
import forms.form_historia as form_historia
import forms.form_juego as form_juego
import Pygame.auxiliar as aux

def pythonisa():
    pg.display.set_caption(var.TITULO_JUEGO)
    pantalla = pg.display.set_mode(var.DIMENSION_PANTALLA)
    corriendo = True
    reloj = pg.time.Clock()
    form_actual = 'menu'
    bandera_juego = False
    datos_juego = {
        "puntuacion": var.PUNTUACION_INICIAL,
        "cantidad_vidas": var.CANTIDAD_VIDAS,
        "nombre": 'Player',
        "volumen_musica": var.VOLUMEN_MUSICA_INICIAL,
    }

    while corriendo:

        cola_eventos = pg.event.get()
        reloj.tick(var.FPS)

        if form_actual == 'menu':
            form_actual = form_menu.mostrar_menu(pantalla, cola_eventos)

        elif form_actual == 'historia':
            if not bandera_juego:
                aux.inicializar_musica(datos_juego)
                bandera_juego = True
            form_actual, bandera_juego = form_historia.mostrar_historia(pantalla, cola_eventos)
        
        elif form_actual == 'juego':
            form_actual = form_juego.mostrar_juego(pantalla, cola_eventos, {})
            
        elif form_actual == 'salir':
            corriendo = False

        pg.display.flip()
    pg.quit()