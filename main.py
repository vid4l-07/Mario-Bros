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

class Estado:
    imagen: Imagen
    posicion: tuple[int, int]
    def __init__(self, imagen: Imagen, posicion: tuple[int, int]):
        self.imagen = imagen
        self.posicion = posicion

    def draw(self):
        self.imagen.draw(self.posicion)

# TODO: hay que cambiar la manera en la que se especifica la velocidad, es decir, seleccionar una velocidad base por defecto y poder
# especificar la velocidad con un factor: 1, 1.5, 2
# Solo hay que multiplicar por un float la constante de velocidad.
class Cinta:
    paquetes: list[int]
    estados: list[Estado]
    velocidad: int
    frame: int
    def __init__(self, paquete: Imagen, paquete_caida: Imagen | None, referencia: tuple[int, int], numero: int, direccion: bool, velocidad: int = 20):
        self.paquetes = []
        self.velocidad = velocidad
        self.estados = [Estado(paquete, referencia)]
        self.frame = 0

        if paquete_caida != None:
            numero -= 1

        desplazamiento = 11 if direccion else -11
        for _ in range(numero - 1):
            x, y = self.estados[-1].posicion
            self.estados.append(Estado(paquete, (x + desplazamiento, y)))

        if paquete_caida != None:
            x, y = self.estados[-1].posicion
            self.estados.append(Estado(paquete_caida, (x + desplazamiento, y)))

    def añadir_paquete(self):
        self.paquetes.append(0)

    def draw(self):
        for paquete in self.paquetes:
            if paquete < len(self.estados):
                self.estados[paquete].draw()

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
MARIO_1_2 = Imagen(2, (45, 152), (27, 26))

PAQUETE_1 = Imagen(2, (135, 116), (9, 4))
PAQUETE_1_CAIDA = Imagen(2, (9, 152), (9, 9))

PAQUETE_2 = Imagen(2, (109, 113), (9, 7))
PAQUETE_2_CAIDA = Imagen(2, (75, 114), (10, 10))

cinta2 = Cinta(paquete=PAQUETE_2, paquete_caida=PAQUETE_2_CAIDA, referencia=(106, 105), numero=4, direccion=False)
cinta1 = Cinta(paquete=PAQUETE_1, paquete_caida=None,            referencia=(154, 108), numero=4, direccion=False, velocidad=10)
cinta0 = Cinta(paquete=PAQUETE_1, paquete_caida=PAQUETE_1_CAIDA, referencia=(217, 108), numero=3, direccion=False)

cinta0.añadir_paquete()
cinta1.añadir_paquete()

cintas = [cinta0, cinta1, cinta2]

class Partida:
    posiciones_mario: list[tuple[int, int]]
    posiciones_luigi: list[tuple[int, int]]
    mapa: Imagen
    mario: Jugador
    dificultad: int
    def __init__(self, dificultad: int):
        self.posiciones_mario = [(173,103), (173, 68), (173, 28)]
        self.posiciones_luigi = [(55,96), (55,60), (55,22)]
        self.mapa = Imagen(1, (0, 0), (240, 136))
        self.mario = Jugador(self.posiciones_mario, MARIO_1_1, (pyxel.KEY_UP, pyxel.KEY_DOWN))
        self.dificultad = dificultad
        # self.velocidad = 10

        pyxel.init(self.mapa.ancho, self.mapa.alto)
        pyxel.load('my_resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        self.mario.update()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        salidas: list[int] = []
        for i, cinta in enumerate(cintas):
            salida = cinta.avanzar()
            if salida:
                salidas.append(i)

        for i in salidas:
            if i + 1 < len(cintas):
                cintas[i + 1].añadir_paquete()
 
        # self.frame += 1
        # cinta: Cinta | None = cinta0
        #
        # velocidades = [[self.velocidad] * 3, 
        #              [self.velocidad, self.velocidad * 1.5, self.velocidad * 1.5],
        #              [self.velocidad, self.velocidad * 1.5, self.velocidad * 2],
        #              [self.velocidad, self.velocidad * random.randrange(1,2), self.velocidad * random.randrange(1,2)]]
        # velocidad = velocidades[self.dificultad]
        #
        # num_cinta = 0
        # while cinta != None:
        #     if self.frame % velocidad[num_cinta % 2] == 0:
        #         cinta.paso()
        #     cinta = cinta.siguiente
        #     num_cinta += 1

    def draw(self):
        pyxel.cls(7)
        for cinta in cintas:
            cinta.draw()
        self.mapa.draw((0, 0))
        self.mario.draw()

if __name__ == '__main__':
    _ = Partida(0)
