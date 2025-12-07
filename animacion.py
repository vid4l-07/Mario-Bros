from imagen import Imagen

# Una clase para encapsular una imagen junto a una posición
class Frame:
    imagen: Imagen
    posicion: tuple[int, int]

    def __init__(self, imagen: Imagen, posicion: tuple[int, int]):
        self.imagen = imagen
        self.posicion = posicion

    def draw(self):
        self.imagen.draw(self.posicion)

# Estas animaciones son más largas y requieren parar el juego
class Animacion:
    secuencia: list[list[Frame]]
    contador_secuencia: int
    activo: bool
    frame: int

    def __init__(self, secuencia: list[list[Frame]]):
        self.secuencia = secuencia
        self.contador_secuencia = 0
        self.activo = False
        self.frame = 0

    def update(self):
        if not self.activo:
            return

        if self.frame < 30:
            self.frame += 1
            return
        self.frame = 0 

        self.contador_secuencia += 1

        if self.contador_secuencia >= len(self.secuencia):
            self.activo = False
            self.contador_secuencia = 0
            return

    def draw(self):
        for frame in self.secuencia[self.contador_secuencia]:
            frame.draw()

