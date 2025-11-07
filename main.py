import pyxel

class Imagen:
    def __init__(self, imagen: int, posicion: tuple[int, int], tamano: tuple[int, int]) -> None:
        self.x, self.y = posicion
        self.ancho, self.alto = tamano
        self.imagen = imagen

    def renderizar(self, posicion: tuple[int, int]) -> None:
        x, y = posicion
        pyxel.blt(x, y, self.imagen, self.x, self.y, self.ancho, self.alto)

class Jugador:
    def __init__(self, posicion: int, imagen: Imagen, escalones: list[int], teclas) -> None:
        self.x = posicion
        self.y = 0
        self.imagen = imagen
        self.escalones = escalones
        self.posicion = 0
        self.arriba, self.abajo = teclas

    def actualizar(self) -> None:
        n = len(self.escalones)
        if pyxel.btnp(self.arriba):
            self.posicion = min(self.posicion + 1, n - 1)
        elif pyxel.btnp(self.abajo):
            self.posicion = max(self.posicion - 1, 0)

        self.y = self.escalones[self.posicion]

    def renderizar(self) -> None:
        self.imagen.renderizar((self.x, self.y))

MAPA = Imagen(1, (0, 12), (240, 136))
MARIO: Imagen = Imagen(0, (0, 0), (16, 16))
LUIGI: Imagen = Imagen(0, (0, 16), (16, 16))

class Partida:
    def __init__(self, mapa: Imagen, mario: Imagen, luigi: Imagen) -> None:
        self.mapa = mapa
        self.mario = mario
        self.luigi = luigi
        self.posiciones_mario = [(173,113), (173, 78), (173, 38)]
        self.posiciones_luigi = [(55,96), (55,60), (55,22)]
        
        pyxel.init(mapa.ancho, mapa.alto)
        pyxel.load('my_resource.pyxres')
        pyxel.run(self.actualizar, self.dibujar)

    def actualizar(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def dibujar(self) -> None:
        pyxel.cls(0)
        self.mapa.renderizar((0, 0))
        self.mario.renderizar(self.posiciones_mario[0])
        self.luigi.renderizar(self.posiciones_luigi[0])

if __name__ == '__main__':
    Partida(MAPA, MARIO, LUIGI)
