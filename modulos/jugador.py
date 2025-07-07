import modulos.carta as carta

def inicializar_jugador():
    jugador_actual = {}
    jugador_actual['puntaje_actual'] = 0
    jugador_actual['puntaje_total'] = 0
    jugador_actual['nombre'] = 'jugador'
    
    return jugador_actual

#De acá, se puede añadir tmb de asignarle al usuario un mazo de cartas, y hacer una función que haga un get sobre eso

def sumar_puntaje_actual(jugador_actual: dict, nuevo_puntaje: int) -> None:
    jugador_actual['puntaje_actual'] += nuevo_puntaje
    print(f"Puntaje por params: {nuevo_puntaje}")
    print(f"Puntaje actual, función: {jugador_actual['puntaje_actual']}")

def sumar_puntaje_carta_actual(jugador_actual: dict, carta_actual: dict) -> None:
    jugador_actual['puntaje_actual'] += carta.get_puntaje_carta(carta_actual)

def actualizar_puntaje_total(jugador_actual: dict) -> None:
    jugador_actual['puntaje_total'] += jugador_actual.get('puntaje_actual')

# Getters
def get_puntaje_actual(jugador_actual: dict) -> int:
    #Devuelve el puntaje actual del usuario
    return jugador_actual.get('puntaje_actual')

def get_puntaje_total(jugador_actual: dict) -> int:
    #Devuelve el puntaje total del usuario
    return jugador_actual.get('puntaje_total')

def get_nombre(jugador_actual: dict) -> str:
    #Devuelve el nombre del usuario
    return jugador_actual.get('nombre')

# Setters
def set_puntaje_actual(jugador_actual: dict, nuevo_puntaje: int):
    #Define o setea el puntaje actual del usuario
    jugador_actual['puntaje_actual'] = nuevo_puntaje

def set_puntaje_total(jugador_actual: dict, nuevo_puntaje: int):
    jugador_actual['puntaje_total'] = nuevo_puntaje

def set_nombre(jugador_actual: dict, nuevo_puntaje: int):
    jugador_actual['nombre'] = nuevo_puntaje