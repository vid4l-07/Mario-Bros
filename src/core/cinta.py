from src.core.imagen import Imagen

# TODO: Imagen de caida
class Cinta:
    __imagen_paquete: Imagen
    __paquetes: list[int]
    __inicio: tuple[int, int]
    __velocidad: float
    __frame: int
    __direccion: int
    __pasos: int
    __lado: str | None
    __nivel: int | None

    @property
    def lado(self) -> str | None:
        return self.__lado

    @property
    def nivel(self) -> int | None:
        return self.__nivel

    def __init__(self, imagen_paquete: Imagen, inicio: tuple[int, int], pasos: int, direccion: int, lado: str | None = None, nivel: int | None = None):
        self.__imagen_paquete = imagen_paquete
        self.__paquetes = []
        self.__inicio = inicio
        self.__velocidad = 20
        self.__frame = 0
        self.__direccion = direccion
        self.__pasos = pasos
        self.__lado = lado
        self.__nivel = nivel

    def añadir_paquete(self):
        self.__paquetes.append(0)

    def eliminar_paquetes(self):
        self.__paquetes.clear()

    @property
    def velocidad(self) -> float:
        return self.__velocidad

    @velocidad.setter
    def velocidad(self, factor: float):
        self.__velocidad = 20 / factor

    def draw(self):
        x, y = self.__inicio
        for paquete in self.__paquetes:
            self.__imagen_paquete.draw((x + (paquete * 11 * self.__direccion), y))

    def caida(self) -> bool:
        return any(paso >= self.__pasos for paso in self.__paquetes)

    def avanzar(self) -> bool:
        self.__frame += 1
        if self.__frame < self.__velocidad:
            return False
        self.__frame = 0

        salida = False
        nuevos: list[int] = []

        for paquete in self.__paquetes:
            nuevo = paquete + 1
            if nuevo < self.__pasos:
                nuevos.append(nuevo)
            else:
                salida = True

        self.__paquetes = nuevos
        return salida
