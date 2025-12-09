import pyxel

from src.core.imagen import Imagen
from src.constantes.configuracion import MAPA_DIMENSIONES
from src.constantes.jefe import *

class Jefe:
    pause: bool
    frame: int
    mapa: Imagen
    indice_anim: int
    jugador: int
    posicion: tuple[int, int]
    jefe: tuple[Imagen, Imagen]

    def __init__(self) -> None:
        self.pause = False
        self.frame = 0
        self.mapa = Imagen(1, (0, 0), MAPA_DIMENSIONES)
        self.indice_anim = 0
        self.jugador = 1

        self.posicion = (200,64)
        self.jefe = ANIMACIONES_JEFE[0]

    def toggle_animation(self):
        self.indice_anim = not self.indice_anim

    def animacion(self):
        if self.jugador == 0:
            self.posicion = (200,64)
            self.jefe = ANIMACIONES_JEFE[0]
        elif self.jugador == 1:
            self.posicion = (1,101)
            self.jefe = ANIMACIONES_JEFE[1]
        pyxel.cls(7)
        self.mapa.draw((0,0))
        self.jefe[self.indice_anim].draw(self.posicion)
        if self.frame % 20 == 0:
            self.toggle_animation()
        self.frame += 1
        if self.frame >= 100:
            self.pause = False
            self.frame = 0

