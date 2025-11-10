import pyxel

class Imagen:
    def __init__(self, imagen, posicion, tamano):
        self.x, self.y = posicion
        self.ancho, self.alto = tamano
        self.imagen = imagen

    def draw(self, posicion):
        x, y = posicion
        pyxel.blt(x, y, self.imagen, self.x, self.y, self.ancho, self.alto, colkey=7)

class Jugador:
    posicion:int
    posiciones:list
    def __init__(self, posiciones: list, imagen: Imagen, num_escalones: int, teclas) -> None:
        self.num_escalones = num_escalones
        try:
            self.posiciones.remove(posiciones[num_escalones])
        except:
            pass

        self.posiciones = posiciones 
        self.posicion = 0 # ahora esta variable posicion se podria usar para la condicion de los paquetes que decias
        self.imagen = imagen
        self.arriba, self.abajo = teclas

    def update(self) -> None:
        if pyxel.btnp(self.arriba):
            self.posicion = min(self.posicion + 1, self.num_escalones - 1)

        elif pyxel.btnp(self.abajo):
            self.posicion = max(self.posicion - 1, 0)

    def draw(self) -> None:
        self.x, self.y = self.posiciones[self.posicion]
        self.imagen.draw((self.x, self.y))

    # def __init__(self, posicion, imagen, escalones, teclas):
    #     self.x = posicion
    #     self.y = 0
    #     self.imagen = imagen
    #     self.escalones = escalones
    #     self.posicion = 0
    #     self.arriba, self.abajo = teclas
    #
    # def update(self):
    #     n = len(self.escalones)
    #     if pyxel.btnp(self.arriba):
    #         self.posicion = min(self.posicion + 1, n - 1)
    #     elif pyxel.btnp(self.abajo):
    #         self.posicion = max(self.posicion - 1, 0)
    #
    #     self.y = self.escalones[self.posicion]
    #
    # def draw(self):
    #     self.imagen.draw((self.x, self.y))
    #
# Los paquetes no se mueven con fluidez. Van dando saltos. Hay un número limitado
# de posición en las que puede estár un paquete. La clase 'Estado' representa
# una imagen en un lugar. Sólo hay que determinar si se debe dibujar o no.
# De este modo los paquetes pueden ser representados como una posición en una lista
# de estados.

# Entonces, el juego puede representarse como un camino a seguir. El problema es
# que el camino depende del jugador. Si un paquete se cae porque el jugador no está
# en su sitio el camino de estados cambia.

# Eso significa que hay algunos estados con ramas. Hay algunos estados que únicamente
# tienen un posible paso siguiente. Pero hay otros estados que pueden tener más pasos.
# Si un estado representa un paquete al borde de caer, hay dos posibilidades: una es que
# el jugador esté bien posicionado y el paquete continue su camino con normalidad. Y la
# otra es que el jugador no esté en el sitio adecuado y el paquete caiga. Dos caminos.

# Un paquete empieza siendo el número 0. Y va avanzando: 1, 2, 3. Cada número corresponde
# a un estado. Hay algunos estados que necesitan una condición. La condición es un
# personaje y una posición. El camino sigue únicamente si el personaje está en la posición.
class Estado:
    def __init__(self, imagen, posicion, condicion = None):
        self.imagen = imagen # imagen a dibujar
        self.posicion = posicion # posicion (x, y) del paquete
        # ejemplo de condicion
        # diccionario: (mario, 2)
        self.condicion = condicion

    def draw(self):
        # Falta implementar la condición
        self.imagen.draw(self.posicion)

PAQUETE_1_1 = Imagen(2, (0, 152), (9, 4))
PAQUETE_1_2 = Imagen(2, (0, 152), (3, 4))
PAQUETE_1_3 = Imagen(2, (9, 152), (9, 9))

MARIO_1_1 = Imagen(2, (18, 152), (27, 26))
MARIO_1_2 = Imagen(2, (45, 152), (27, 26))

class Partida:
    def __init__(self):
        self.frame = 0
        self.posiciones_mario = [(173,103), (173, 68), (173, 28)]
        self.posiciones_luigi = [(55,96), (55,60), (55,22)]
        self.mapa = Imagen(1, (0, 0), (240, 136))
        self.mario = Jugador(self.posiciones_mario, MARIO_1_1, 3, (pyxel.KEY_UP, pyxel.KEY_DOWN))
        self.CAMINO = [
            Estado(PAQUETE_1_1, (217, 108)),
            Estado(PAQUETE_1_1, (206, 108)),
            Estado(PAQUETE_1_3, (195, 108), (self.mario, 0)),
            Estado(PAQUETE_1_1, (154, 108)),
            Estado(PAQUETE_1_1, (143, 108)),
            Estado(PAQUETE_1_1, (132, 108)),
            Estado(PAQUETE_1_2, (127, 108)),
        ] # camino de ejemplo
        self.paquete = 0 # paquete de ejemplo

        pyxel.init(self.mapa.ancho, self.mapa.alto)
        pyxel.load('my_resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        self.mario.update()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.frame += 1
        if self.frame % 10 == 0:
            self.frame = 0
            self.paquete += 1
            if self.paquete >= len(self.CAMINO):
                self.paquete = 0

    def draw(self):
        pyxel.cls(7)
        self.mapa.draw((0, 0))
        self.mario.draw()
        # MARIO_1_1.draw((173, 103))

        self.CAMINO[self.paquete].draw()

        # for estado in self.CAMINO:
        #     estado.draw()

if __name__ == '__main__':
    Partida()
