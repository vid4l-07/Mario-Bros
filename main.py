import pyxel

class Imagen:
    def __init__(self, imagen, posicion, tamano):
        self.x, self.y = posicion
        self.ancho, self.alto = tamano
        self.imagen = imagen

    def draw(self, posicion):
        x, y = posicion
        pyxel.blt(x, y, self.imagen, self.x, self.y, self.ancho, self.alto)

class Jugador:
    def __init__(self, posicion, imagen, escalones, teclas):
        self.x = posicion
        self.y = 0
        self.imagen = imagen
        self.escalones = escalones
        self.posicion = 0
        self.arriba, self.abajo = teclas

    def update(self):
        n = len(self.escalones)
        if pyxel.btnp(self.arriba):
            self.posicion = min(self.posicion + 1, n - 1)
        elif pyxel.btnp(self.abajo):
            self.posicion = max(self.posicion - 1, 0)

        self.y = self.escalones[self.posicion]

    def draw(self):
        self.imagen.draw((self.x, self.y))

MAPA = Imagen(1, (0, 12), (240, 136))
MARIO = Imagen(0, (0, 0), (16, 16))
LUIGI = Imagen(0, (0, 17), (16, 16))
PAQUETE = Imagen(2, (136, 36), (8, 3))

class Partida:
    def __init__(self, mapa: Imagen):
        self.mapa = mapa
        self.railes = [(224, 111)]

        pyxel.init(mapa.ancho, mapa.alto)
        pyxel.load('my_resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        

    def draw(self):
        pyxel.cls(0)
        self.mapa.draw((0, 0))
        PAQUETE.draw((self.railes[0][0] - PAQUETE.ancho, self.railes[0][1] - PAQUETE.alto))

if __name__ == '__main__':
    Partida(MAPA)
