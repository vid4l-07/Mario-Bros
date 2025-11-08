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
# personaje y una posición.
class Estado:
    def __init__(self, imagen, posicion, estado, condicion = None):
        self.imagen = imagen # imagen a dibujar
        self.posicion = posicion # posicion (x, y) del paquete
        # ejemplo de condicion
        # diccionario: { personaje: mario, posicion: 2 }
        self.condicion = condicion

    def draw(self):
        self.imagen.draw(self.posicion)

class Partida:
    def __init__(self):
        self.mapa = Imagen(1, (0, 12), (240, 136))

        pyxel.init(self.mapa.ancho, self.mapa.alto)
        pyxel.load('my_resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        self.mapa.draw((0, 0))

if __name__ == '__main__':
    Partida()
