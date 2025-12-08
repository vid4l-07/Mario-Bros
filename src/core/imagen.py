import pyxel

class Imagen:
    __x: int
    __y: int
    __ancho: int
    __alto: int
    __imagen: int

    @property
    def alto(self) -> int:
        return self.__alto

    def __init__(self, imagen: int, posicion: tuple[int, int], tamano: tuple[int, int]):
        self.__x, self.__y = posicion
        self.__ancho, self.__alto = tamano
        self.__imagen = imagen

    def draw(self, posicion: tuple[int, int]):
        x, y = posicion
        pyxel.blt(x, y, self.__imagen, self.__x, self.__y, self.__ancho, self.__alto, colkey=7)
