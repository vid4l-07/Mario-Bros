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

class Posicion:
    imagen: Imagen
    posicion: tuple[int, int]
    def __init__(self, imagen: Imagen, posicion: tuple[int, int]):
        self.imagen = imagen
        self.posicion = posicion

    def draw(self):
        self.imagen.draw(self.posicion)

class Cinta:
    # TODO: Hay que simplificar mucho esta clase. No es necesario pero renta

    paquetes: list[int]
    estados: list[Posicion]
    velocidad: float
    frame: int

    def __init__(self, paquete: Imagen, paquete_caida: Imagen | None, referencia: tuple[int, int], numero: int, direccion: bool, factor: float = 1):
        self.paquetes = []
        self.velocidad = 20 / factor
        self.estados = [Posicion(paquete, referencia)]
        self.frame = 0

        if paquete_caida != None:
            numero -= 1

        desplazamiento = 11 if direccion else -11
        for _ in range(numero - 1):
            x, y = self.estados[-1].posicion
            self.estados.append(Posicion(paquete, (x + desplazamiento, y)))

        if paquete_caida != None:
            x, y = self.estados[-1].posicion
            self.estados.append(Posicion(paquete_caida, (x + desplazamiento, y)))

    def añadir_paquete(self):
        self.paquetes.append(0)
        print(self.velocidad)

    def eliminar_paquetes(self):
        self.paquetes.clear()

    def actualizar_velocidad(self, factor: float):
        self.velocidad = 20 / factor

    def draw(self):
        for paquete in self.paquetes:
            if paquete < len(self.estados):
                self.estados[paquete].draw()

    def caida(self):
        if len(self.paquetes) > 0 and self.paquetes[0] == len(self.estados) - 1:
            return True
        return False

    def avanzar(self):
        self.frame += 1
        if self.frame < self.velocidad:
            return False
        self.frame = 0

        salida = False
        nuevos: list[int] = []

        for paquete in self.paquetes:
            nuevo = paquete + 1
            if nuevo < len(self.estados):
                nuevos.append(nuevo)
            else:
                salida = True

        self.paquetes = nuevos
        return salida

MARIO_1_1 = Imagen(2, (18, 152), (27, 26))
MARIO_1_2 = Imagen(2, (44, 152), (27, 26))

PAQUETE_1 = Imagen(2, (135, 116), (9, 4))
PAQUETE_1_CAIDA = Imagen(2, (9, 152), (9, 9))

PAQUETE_2 = Imagen(2, (109, 113), (9, 7))
PAQUETE_2_CAIDA = Imagen(2, (75, 114), (10, 10))

PAQUETE_3 = Imagen(2, (151, 94), (9, 7))
PAQUETE_3_CAIDA = Imagen(2, (162, 94), (10, 11))

PAQUETE_4 = Imagen(2, (109, 73), (9, 9))
PAQUETE_4_CAIDA = Imagen(2, (0, 164), (11, 12))

PAQUETE_5 = Imagen(2, (136, 36), (9, 9))
PAQUETE_5_CAIDA = Imagen(2, (0, 184), (12, 12))

PAQUETE_6 = Imagen(2, (109, 36), (9, 9))
PAQUETE_6_CAIDA = Imagen(2, (16, 184), (13, 13))

# Esto es una porquería
cinta10 = Cinta(paquete=PAQUETE_6, paquete_caida=PAQUETE_6_CAIDA,referencia=(106, 28),  numero=4, direccion=False)
cinta9 = Cinta(paquete=PAQUETE_5, paquete_caida=None,            referencia=(155, 28),  numero=4, direccion=False)
cinta8 = Cinta(paquete=PAQUETE_5, paquete_caida=PAQUETE_5_CAIDA, referencia=(126, 47),  numero=4, direccion=True)
cinta7 = Cinta(paquete=PAQUETE_4, paquete_caida=None,            referencia=(77,  46),  numero=4, direccion=True)
cinta6 = Cinta(paquete=PAQUETE_4, paquete_caida=PAQUETE_4_CAIDA, referencia=(106, 65),  numero=4, direccion=False)
cinta5 = Cinta(paquete=PAQUETE_3, paquete_caida=None,            referencia=(155, 67),  numero=4, direccion=False)
cinta4 = Cinta(paquete=PAQUETE_3, paquete_caida=PAQUETE_3_CAIDA, referencia=(126, 86),  numero=4, direccion=True)
cinta3 = Cinta(paquete=PAQUETE_2, paquete_caida=None,            referencia=(77,  86),  numero=4, direccion=True)
cinta2 = Cinta(paquete=PAQUETE_2, paquete_caida=PAQUETE_2_CAIDA, referencia=(106, 105), numero=4, direccion=False)
cinta1 = Cinta(paquete=PAQUETE_1, paquete_caida=None,            referencia=(154, 108), numero=4, direccion=False, factor=2)
cinta0 = Cinta(paquete=PAQUETE_1, paquete_caida=PAQUETE_1_CAIDA, referencia=(217, 108), numero=3, direccion=False)

cintas = [cinta0, cinta1, cinta2, cinta3, cinta4, cinta5, cinta6, cinta7, cinta8, cinta9, cinta10]

# TODO: Podríamos hacer que la clase Menu sea capaz de crear partidas?
class Partida:
    mapa: Imagen
    mario: Jugador
    luigi: Jugador

    def __init__(self, dificultad: int):
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
        for numero_cinta, cinta in enumerate(cintas):
            salida = cinta.avanzar()
            if salida:
                salidas.append(numero_cinta)
                self.fall_handler(numero_cinta)

        # Se mueven los paquetes de una cinta a otra
        for numero_cinta in salidas:
            if numero_cinta + 1 < len(cintas):
                cintas[numero_cinta + 1].añadir_paquete()

    def draw(self):
        # El orden es importante
        for cinta in cintas:
            cinta.draw()
        self.mapa.draw((0, 0))
        self.mario.draw()
        self.luigi.draw()


# TODO: El tamaño del mapa tiene que ser una constante
class Juego:
    menu: Menu
    partida: None | Partida

    def __init__(self):
        self.menu = Menu(['Facil', 'Normal', 'Dificil', 'Crazy'])

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
    # _ = Partida()
    _ = Juego()
