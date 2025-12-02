import random
import pyxel

class Imagen:
    x: int
    y: int
    ancho: int
    alto: int
    imagen: int
    def __init__(self, imagen: int, posicion: tuple[int, int], tamano: tuple[int, int]):
        self.x, self.y = posicion
        self.ancho, self.alto = tamano
        self.imagen = imagen

    def draw(self, posicion: tuple[int, int]):
        x, y = posicion
        pyxel.blt(x, y, self.imagen, self.x, self.y, self.ancho, self.alto, colkey=7)

class Menu:
    opciones: list[str]
    seleccion: int
    visible: bool

    def __init__(self, opciones: list[str]):
        self.opciones = opciones
        self.seleccion = 0
        self.visible = True

    def update(self) -> int | None:
        if pyxel.btnp(pyxel.KEY_M):
            self.visible = not self.visible

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.seleccion = min(self.seleccion + 1, len(self.opciones) - 1)

        if pyxel.btnp(pyxel.KEY_UP):
            self.seleccion = max(self.seleccion - 1, 0)

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.visible = False
            return self.seleccion

        return None

    def draw(self):
        if not self.visible:
            return

        pyxel.cls(0)

        for i, opcion in enumerate(self.opciones):
            pyxel.text(10, 10 + (10 * i), opcion, 1 if i == self.seleccion else 7)

        pyxel.text(50, 10 + (10 * self.seleccion), '<', 1)

class Jugador:
    posiciones: list[tuple[int, int]]
    posicion: int
    imagen: Imagen
    def __init__(self, posiciones: list[tuple[int, int]], imagen: Imagen, teclas) -> None:
        self.posiciones = posiciones
        self.posicion = 0
        self.imagen = imagen
        self.arriba, self.abajo = teclas

    def update(self) -> None:
        if pyxel.btnp(self.arriba):
            self.posicion = min(self.posicion + 1, len(self.posiciones) - 1)

        elif pyxel.btnp(self.abajo):
            self.posicion = max(self.posicion - 1, 0)

    def draw(self) -> None:
        x, y = self.posiciones[self.posicion]
        self.imagen.draw((x, y))

# TODO: Imagen de caida
class Cinta:
    imagen_paquete: Imagen
    paquetes: list[int]
    inicio: tuple[int, int]
    velocidad: float
    frame: int
    direccion: int
    pasos: int

    def __init__(self, imagen_paquete: Imagen, inicio: tuple[int, int], pasos: int, direccion: int, factor_velocidad: float = 1):
        self.imagen_paquete = imagen_paquete
        self.paquetes = []
        self.inicio = inicio
        self.direccion = direccion
        self.pasos = pasos
        self.velocidad = 20 / factor_velocidad
        self.frame = 0

    def añadir_paquete(self):
        self.paquetes.append(0)

    def eliminar_paquetes(self):
        self.paquetes.clear()

    def actualizar_velocidad(self, factor: float):
        self.velocidad = 20 / factor

    def draw(self):
        x, y = self.inicio
        for paquete in self.paquetes:
            self.imagen_paquete.draw((x + (paquete * 11 * self.direccion), y))

    def caida(self) -> bool:
        return any(paso >= self.pasos for paso in self.paquetes)

    def avanzar(self):
        self.frame += 1
        if self.frame < self.velocidad:
            return False
        self.frame = 0

        salida = False
        nuevos: list[int] = []

        for paquete in self.paquetes:
            nuevo = paquete + 1
            if nuevo < self.pasos:
                nuevos.append(nuevo)
            else:
                salida = True

        self.paquetes = nuevos
        return salida

MARIO_1_1 = Imagen(2, (18, 152), (27, 26))
MARIO_1_2 = Imagen(2, (44, 152), (27, 26))

PAQUETE_1 = Imagen(2, (135, 116), (9, 4))
PAQUETE_2 = Imagen(2, (109, 113), (9, 7))
PAQUETE_3 = Imagen(2, (151, 94), (9, 7))
PAQUETE_4 = Imagen(2, (109, 73), (9, 9))
PAQUETE_5 = Imagen(2, (136, 36), (9, 9))
PAQUETE_6 = Imagen(2, (109, 36), (9, 9))

# PAQUETE_1_CAIDA = Imagen(2, (9, 152), (9, 9))
# PAQUETE_2_CAIDA = Imagen(2, (75, 114), (10, 10))
# PAQUETE_3_CAIDA = Imagen(2, (162, 94), (10, 11))
# PAQUETE_4_CAIDA = Imagen(2, (0, 164), (11, 12))
# PAQUETE_5_CAIDA = Imagen(2, (0, 184), (12, 12))
# PAQUETE_6_CAIDA = Imagen(2, (16, 184), (13, 13))

cinta10 = Cinta(PAQUETE_6, (106, 28), 4, -1)
cinta9 = Cinta(PAQUETE_5, (155, 28),  4, -1)
cinta8 = Cinta(PAQUETE_5, (126, 47),  4, 1)
cinta7 = Cinta(PAQUETE_4, (77,  46),  4, 1)
cinta6 = Cinta(PAQUETE_4, (106, 65),  4, -1)
cinta5 = Cinta(PAQUETE_3, (155, 67),  4, -1)
cinta4 = Cinta(PAQUETE_3, (126, 86),  4, 1)
cinta3 = Cinta(PAQUETE_2, (77,  86),  4, 1)
cinta2 = Cinta(PAQUETE_2, (106, 105), 4, -1)
cinta1 = Cinta(PAQUETE_1, (154, 108), 4, -1, 2)
cinta0 = Cinta(PAQUETE_1, (217, 108), 3, -1)

cinta0.añadir_paquete()
cintas = [cinta0, cinta1, cinta2, cinta3, cinta4, cinta5, cinta6, cinta7, cinta8, cinta9, cinta10]

class Partida:
    mapa: Imagen
    mario: Jugador
    luigi: Jugador
    cintas: list[Cinta]

    def __init__(self, dificultad: int):
        # TODO: Hay que aplicar la dificultad aquí. Cuando se crea la partida,
        # se configura todo según la dificultad. Es por eso que las cintas
        # deben crearse aquí también.

        # No se a qué se refiere el documento con cintas 0-7 porque la siete
        # acaba en el lado de Mario.

        if dificultad == 0:
            self.cintas = cintas[:7]

        MARIO_POSICIONES = [(173,103), (173, 68), (173, 28)]
        LUIGI_POSICIONES = [(55,86), (55,50), (55,12)]

        self.mapa = Imagen(1, (0, 0), (240, 136))
        self.mario = Jugador(MARIO_POSICIONES, MARIO_1_1, (pyxel.KEY_UP, pyxel.KEY_DOWN))
        self.luigi = Jugador(LUIGI_POSICIONES, MARIO_1_1, (pyxel.KEY_W, pyxel.KEY_S))

    # Esto comprueba si se cae un paquete
    def fall_handler(self, numero_cinta: int):
        resto = numero_cinta % 4
        posicion = None

        if resto == 0:
            posicion = numero_cinta % 3
        elif resto == 2:
            posicion = (numero_cinta + 1) % 3

        if posicion is not None:
            jugador = self.mario if resto == 0 else self.luigi
            if jugador.posicion != posicion:
                pyxel.quit()

    def update(self):
        # Actualizamos el estado de los jugadores
        self.mario.update()
        self.luigi.update()

        # Las cintas avanzan
        salidas: list[int] = []
        for numero_cinta, cinta in enumerate(self.cintas):
            salida = cinta.avanzar()
            if salida:
                salidas.append(numero_cinta)
                self.fall_handler(numero_cinta)

        # Se mueven los paquetes de una cinta a otra
        for numero_cinta in salidas:
            if numero_cinta + 1 < len(self.cintas):
                self.cintas[numero_cinta + 1].añadir_paquete()

    def draw(self):
        # El orden es importante
        for cinta in self.cintas:
            cinta.draw()
        self.mapa.draw((0, 0))
        self.mario.draw()
        self.luigi.draw()


# TODO: El tamaño del mapa debería ser una constante
class Juego:
    menu: Menu
    partida: None | Partida

    def __init__(self):
        self.menu = Menu(['Facil', 'Medio', 'Extremo', 'Crazy'])

        self.partida = None

        pyxel.init(240, 136)
        pyxel.load('my_resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        # Se puede cerrar el juego en cualquier momento
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Si se está usando el menú no se actualiza el estado del resto del juego
        seleccion = self.menu.update()
        if seleccion != None:
            # Se crea una nueva partida con los valores de la nueva dificultad
            self.partida = Partida(seleccion)
        if self.menu.visible:
            return

        if self.partida != None:
            self.partida.update()

    def draw(self):
        pyxel.cls(7)
        if self.partida != None:
            self.partida.draw()
        self.menu.draw()

if __name__ == '__main__':
    _ = Juego()
