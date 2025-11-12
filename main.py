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

PAQUETE_1_1 = Imagen(2, (0, 152), (9, 4))
PAQUETE_1_2 = Imagen(2, (0, 152), (3, 4))
PAQUETE_1_3 = Imagen(2, (9, 152), (9, 9))

MARIO_1_1 = Imagen(2, (18, 152), (27, 26))
MARIO_1_2 = Imagen(2, (45, 152), (27, 26))

class Paquete:
    def __init__(self, imagen: Imagen, posicion: tuple[int, int]):
        pass

class Cinta:
    paquetes: list[Paquete]
    def __init__(self, paquetes: list[Paquete]):
        self.paquetes = paquetes

class Partida:
    posiciones_mario: list[tuple[int, int]]
    posiciones_luigi: list[tuple[int, int]]
    mapa: Imagen
    mario: Jugador
    def __init__(self):
        self.posiciones_mario = [(173,103), (173, 68), (173, 28)]
        self.posiciones_luigi = [(55,96), (55,60), (55,22)]
        self.mapa = Imagen(1, (0, 0), (240, 136))
        self.mario = Jugador(self.posiciones_mario, MARIO_1_1, (pyxel.KEY_UP, pyxel.KEY_DOWN))

        pyxel.init(self.mapa.ancho, self.mapa.alto)
        pyxel.load('my_resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        self.mario.update()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(7)
        self.mapa.draw((0, 0))
        self.mario.draw()

if __name__ == '__main__':
    _ = Partida()
