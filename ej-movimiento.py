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
    def __init__(self, posiciones: list, imagen: Imagen, num_escalones: int, teclas) -> None:
        self.num_escalones = num_escalones
        try:
            self.posiciones = posiciones.remove(posiciones[num_escalones])
            print('eliminado')
        except:
            print('nada mas que eliminar')

        self.posiciones = posiciones # esta es la lista de posiciones de cada uno que se pone en la clase partida
        self.posicion = self.posiciones[0] # esto solo declara la posicion inicial
        self.imagen = imagen
        self.arriba, self.abajo = teclas

    def actualizar(self) -> None:
        if pyxel.btnp(self.arriba):
            self.posicion = self.posiciones[min(self.posiciones.index(self.posicion) + 1, self.num_escalones -1)]

        elif pyxel.btnp(self.abajo):
            self.posicion = self.posiciones[max(self.posiciones.index(self.posicion) - 1, 0)]

    def renderizar(self) -> None:
        self.x, self.y = self.posicion
        self.imagen.renderizar((self.x, self.y))

MAPA = Imagen(1, (0, 12), (240, 136))
MARIO: Imagen = Imagen(0, (0, 0), (16, 16))
LUIGI: Imagen = Imagen(0, (0, 16), (16, 16))

class Partida:
    def __init__(self, mapa: Imagen) -> None:
        self.posiciones_mario = [(173,113), (173, 78), (173, 38)]
        self.posiciones_luigi = [(55,96), (55,60), (55,22)]
        self.mapa = mapa
        self.num_escalones = 3
        self.mario = Jugador(self.posiciones_mario, MARIO, self.num_escalones, (pyxel.KEY_UP, pyxel.KEY_DOWN))
        self.luigi = Jugador(self.posiciones_luigi, LUIGI, self.num_escalones, (pyxel.KEY_W, pyxel.KEY_S))
        
        pyxel.init(mapa.ancho, mapa.alto)
        pyxel.load('my_resource.pyxres')
        pyxel.run(self.actualizar, self.dibujar)

    def actualizar(self) -> None:
        self.mario.actualizar()
        self.luigi.actualizar()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def dibujar(self) -> None:
        pyxel.cls(0)
        self.mapa.renderizar((0, 0))
        self.mario.renderizar()
        self.luigi.renderizar()

if __name__ == '__main__':
    Partida(MAPA)
