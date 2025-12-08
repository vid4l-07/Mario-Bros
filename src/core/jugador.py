import pyxel
from src.core.imagen import Imagen

class Jugador:
    __posiciones: list[tuple[int, int]]
    __posicion: int
    __teclas: tuple[int, int]
    __animacion: bool
    __animaciones: list[tuple[Imagen, Imagen]]
    __imagen: Imagen
    __frame: int

    @property
    def posicion(self) -> int:
        return self.__posicion

    def __init__(self, posiciones: list[tuple[int, int]], animaciones: list[tuple[Imagen, Imagen]], teclas: tuple[int, int]):
        self.__posiciones = posiciones
        self.__posicion = 0
        self.__teclas = teclas

        self.__animaciones = animaciones
        self.__animacion = False
        self.__imagen = self.__animaciones[self.__posicion][self.__animacion]

        self.__frame = 0

    # Se llama cuando el personaje mueve un paquete. Esta función recive la
    # velocidad de la cinta desde la que el personaje coge el paquete. Esto
    # permite saber el tiempo justo que tiene que tardar el personaje en
    # desactivar la animación.
    def activar_animacion(self, tiempo: float):
        self.__frame = int(tiempo)
        self.__animacion = True
        self.__imagen = self.__animaciones[self.__posicion][self.__animacion]

    def update(self) -> None:
        arriba, abajo = self.__teclas
        if pyxel.btnp(arriba):
            self.__frame = 0 # Se cancela la animación
            self.__posicion = min(self.__posicion + 1, len(self.__posiciones) - 1)
        elif pyxel.btnp(abajo):
            self.__frame = 0 # Se cancela la animación
            self.__posicion = max(self.__posicion - 1, 0)

        if self.__frame > 0:
            self.__frame -= 1
        elif self.__frame == 0:
            self.__animacion = False

        self.__imagen = self.__animaciones[self.__posicion][self.__animacion]

    def draw(self) -> None:
        x, y = self.__posiciones[self.__posicion]
        self.__imagen.draw((x, y - self.__imagen.alto))
        # Se calcula la coordenada del personaje desde la base. Esto es
        # necesario ya que hay animaciones con distinta altura.

