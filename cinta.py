from imagen import Imagen
from constantes import *

# TODO: Imagen de caida
class Cinta:
    imagen_paquete: Imagen
    paquetes: list[int]
    inicio: tuple[int, int]
    velocidad: int
    frame: int
    direccion: int
    pasos: int
    lado: str | None
    nivel: int | None

    def __init__(self, imagen_paquete: Imagen, inicio: tuple[int, int], pasos: int, direccion: int, lado: str | None = None, nivel: int | None = None):
        self.imagen_paquete = imagen_paquete
        self.paquetes = []
        self.inicio = inicio
        self.velocidad = 20
        self.frame = 0
        self.direccion = direccion
        self.pasos = pasos
        self.lado = lado
        self.nivel = nivel

    def añadir_paquete(self):
        self.paquetes.append(0)

    def eliminar_paquetes(self):
        self.paquetes.clear()

    def actualizar_velocidad(self, factor: float):
        self.velocidad = int(20 / factor)

    def draw(self):
        x, y = self.inicio
        for paquete in self.paquetes:
            self.imagen_paquete.draw((x + (paquete * 11 * self.direccion), y))

    def caida(self) -> bool:
        return any(paso >= self.pasos for paso in self.paquetes)

    def avanzar(self) -> bool:
        self.frame += 1
        if self.frame < self.velocidad:
            return False
        self.frame = 0

        salida = False
        nuevos: list[int] = []

        for paquete in self.paquetes:
            nuevo = paquete + 1
            if nuevo < self.pasos:
                nuevos.append(nuevo)
            else:
                salida = True

        self.paquetes = nuevos
        return salida

CINTA10 = Cinta(PAQUETE_6, (106, 28), 4, -1, 'IZQ', 2)
CINTA9 = Cinta(PAQUETE_5, (155, 28),  4, -1)
CINTA8 = Cinta(PAQUETE_5, (126, 47),  4, 1, 'DER', 2)
CINTA7 = Cinta(PAQUETE_4, (77,  46),  4, 1)
CINTA6 = Cinta(PAQUETE_4, (106, 65),  4, -1, 'IZQ', 1)
CINTA5 = Cinta(PAQUETE_3, (155, 67),  4, -1)
CINTA4 = Cinta(PAQUETE_3, (126, 86),  4, 1, 'DER', 1)
CINTA3 = Cinta(PAQUETE_2, (77,  86),  4, 1)
CINTA2 = Cinta(PAQUETE_2, (106, 105), 4, -1, 'IZQ', 0)
CINTA1 = Cinta(PAQUETE_1, (154, 108), 4, -1)
CINTA0 = Cinta(PAQUETE_1, (217, 108), 3, -1, 'DER', 0)

CINTAS = [CINTA0, CINTA1, CINTA2, CINTA3, CINTA4, CINTA5, CINTA6, CINTA7, CINTA8, CINTA9, CINTA10]

