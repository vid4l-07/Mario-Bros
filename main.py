import pyxel

class Imagen:
    def __init__(self, posición: tuple[int, int], tamaño: tuple[int, int]) -> None:
        self.x, self.y = posición
        self.ancho, self.alto = tamaño

    def renderizar(self, posición: tuple[int, int]) -> None:
        x, y = posición
        pyxel.blt(x, y, 0, self.x, self.y, self.ancho, self.alto)

class Jugador:
    def __init__(self, posición: int, imagen: Imagen, escalones: list[int], teclas) -> None:
        self.x = posición
        self.y = 0
        self.imagen = imagen
        self.escalones = escalones
        self.posición = 0
        self.arriba, self.abajo = teclas

    def actualizar(self) -> None:
        n = len(self.escalones)
        if pyxel.btnp(self.arriba):
            self.posición = min(self.posición + 1, n - 1)
        elif pyxel.btnp(self.abajo):
            self.posición = max(self.posición - 1, 0)

        self.y = self.escalones[self.posición]

    def renderizar(self) -> None:
        self.imagen.renderizar((self.x, self.y))

class Paquete:
    def __init__(self, posición: tuple[int, int], imagen: Imagen) -> None:
        self.x, self.y = posición
        self.imagen = imagen

    def actualizar(self) -> None:
        pass

    def renderizar(self) -> None:
        self.imagen.renderizar((self.x, self.y))

MARIO: Imagen = Imagen((0, 0), (16, 16))
LUIGI: Imagen = Imagen((0, 17), (16, 16))

class Partida:
    def __init__(self) -> None:
        self.mario = Jugador(900, MARIO, [400, 300, 200, 100], (pyxel.KEY_UP, pyxel.KEY_DOWN))
        self.luigi = Jugador(100, LUIGI, [400, 300, 200, 100], (pyxel.KEY_W, pyxel.KEY_S))
        pyxel.init(1000, 500)
        pyxel.load('my_resource.pyxres')
        pyxel.run(self.actualizar, self.dibujar)

    def actualizar(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.mario.actualizar()
        self.luigi.actualizar()

    def dibujar(self) -> None:
        pyxel.cls(0)
        self.mario.renderizar()
        self.luigi.renderizar()

if __name__ == '__main__':
    Partida()
