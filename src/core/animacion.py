from src.core.imagen import Imagen

# Una clase para encapsular una imagen junto a una posición
class Frame:
    __imagen: Imagen
    __posicion: tuple[int, int]

    def __init__(self, imagen: Imagen, posicion: tuple[int, int]):
        self.__imagen = imagen
        self.__posicion = posicion

    def draw(self):
        self.__imagen.draw(self.__posicion)

# Estas animaciones son más largas y requieren parar el juego
class Animacion:
    __secuencia: list[list[Frame]]
    __contador_secuencia: int
    activo: bool
    __frame: int

    def __init__(self, secuencia: list[list[Frame]]):
        self.__secuencia = secuencia
        self.__contador_secuencia = 0
        self.activo = False
        self.__frame = 0

    def update(self):
        if not self.activo:
            return

        if self.__frame < 30:
            self.__frame += 1
            return
        self.__frame = 0 

        self.__contador_secuencia += 1

        if self.__contador_secuencia >= len(self.__secuencia):
            self.activo = False
            self.__contador_secuencia = 0
            return

    def draw(self):
        for frame in self.__secuencia[self.__contador_secuencia]:
            frame.draw()

