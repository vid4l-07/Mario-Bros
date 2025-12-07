from src.core.imagen import Imagen
from src.constantes.paquetes import PAQUETE_6

class Camion:
    paquetes: int
    imagen: Imagen

    def __init__(self):
        self.paquetes = 0
        self.imagen = Imagen(2, (180, 184), (36, 41))

    def añadir_paquete(self) -> bool:
        self.paquetes += 1
        if self.paquetes >= 8:
            self.paquetes = 0
            return True

        return False

    def draw(self):
        self.imagen.draw((4, 39))
        for paquete in range(self.paquetes):
            columna = paquete % 2
            fila = paquete // 2
            PAQUETE_6.draw((19 + (columna * 11), 58 - (fila * 10)))

