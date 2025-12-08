from src.core.imagen import Imagen

from src.constantes.paquetes import PAQUETE_6
from src.constantes.camion import CAMION

class Camion:
    __paquetes: int
    __imagen: Imagen

    def __init__(self):
        self.__paquetes = 0
        self.__imagen = CAMION

    def añadir_paquete(self) -> bool:
        self.__paquetes += 1
        if self.__paquetes >= 8:
            self.__paquetes = 0
            return True

        return False

    def draw(self):
        self.__imagen.draw((4, 39))
        for paquete in range(self.__paquetes):
            columna = paquete % 2
            fila = paquete // 2
            PAQUETE_6.draw((19 + (columna * 11), 58 - (fila * 10)))

