import pyxel
from imagen import Imagen
from animacion import Animacion

class Jugador:
    posiciones: list[tuple[int, int]]
    posicion: int
    teclas: tuple[int, int]
    animacion: bool
    animaciones: list[tuple[Imagen, Imagen]]
    imagen: Imagen
    frame: int
    animacion_jefe: Animacion

    def __init__(self, posiciones: list[tuple[int, int]], animaciones: list[tuple[Imagen, Imagen]], teclas: tuple[int, int], animacion_jefe: Animacion):
        self.posiciones = posiciones
        self.posicion = 0
        self.teclas = teclas

        self.animaciones = animaciones
        self.animacion = False
        self.imagen = self.animaciones[self.posicion][self.animacion]

        self.frame = 0

        self.animacion_jefe = animacion_jefe

    # Se llama cuando el personaje mueve un paquete. Esta función recive la
    # velocidad de la cinta desde la que el personaje coge el paquete. Esto
    # permite saber el tiempo justo que tiene que tardar el personaje en
    # desactivar la animación.
    def activar_animacion(self, tiempo: int):
        self.frame = tiempo
        self.animacion = True
        self.imagen = self.animaciones[self.posicion][self.animacion]

    def update(self) -> None:
        arriba, abajo = self.teclas
        if pyxel.btnp(arriba):
            self.frame = 0 # Se cancela la animación
            self.posicion = min(self.posicion + 1, len(self.posiciones) - 1)
        elif pyxel.btnp(abajo):
            self.frame = 0 # Se cancela la animación
            self.posicion = max(self.posicion - 1, 0)

        if self.frame > 0:
            self.frame -= 1
        elif self.frame == 0:
            self.animacion = False

        self.imagen = self.animaciones[self.posicion][self.animacion]

    def draw(self) -> None:
        x, y = self.posiciones[self.posicion]
        self.imagen.draw((x, y - self.imagen.alto))
        # Se calcula la coordenada del personaje desde la base. Esto es
        # necesario ya que hay animaciones con distinta altura.

