from imagen import Imagen

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
