import pyxel

from src.core.imagen import Imagen
from src.constantes.configuracion import MAPA_DIMENSIONES
from src.constantes.jefe import *

class Jefe:
    __frame: int
    __mapa: Imagen
    __indice_anim: int
    __posiciones: tuple[tuple[int,int], tuple[int,int]]

    def __init__(self) -> None:
        self.__frame = 0
        self.__mapa = Imagen(1, (0, 0), MAPA_DIMENSIONES)
        self.__pause = False   # atributo para parar el juego
        self.__jugador = 1   # atrubuto para distinguir entre mario y luigi
        self.__posiciones = ((200,64), (1,101))

        # indice inicial
        self.__indice_anim = 0

    def toggle_animation(self):
        self.__indice_anim = not self.__indice_anim

    def animacion(self):
        # comprueba si el que ha fallado es mario o luigi
        posicion = self.__posiciones[self.jugador]
        jefe = ANIMACIONES_JEFE[self.jugador]

        pyxel.cls(7)
        self.__mapa.draw((0,0))

        jefe[self.__indice_anim].draw(posicion)   # pinta la animacion del jefe dependiendo de si es mario o luigi

        self.__frame += 1
        if self.__frame % 20 == 0:   # la animacion cambia cada 20 frames
            self.toggle_animation()

        if self.__frame >= 100:   # reanuda el juego
            self.pause = False
            self.__frame = 0

    @property
    def pause(self):
        return self.__pause

    @pause.setter
    def pause(self, value: bool):
        self.__pause = value

    @property
    def jugador(self):
        return self.__jugador

    @jugador.setter
    def jugador(self, value: int):
        if value == 0 or value == 1:
            self.__jugador = value
        else:
            raise ValueError("El atributo jefe.jugador tiene que ser 1 o 0")
