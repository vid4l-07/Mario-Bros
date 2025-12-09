import pyxel

from src.core.imagen import Imagen
from src.constantes.configuracion import MAPA_DIMENSIONES
from src.constantes.jefe import *

class Jefe:
    __frame: int
    __mapa: Imagen
    __indice_anim: int
    __posicion: tuple[int, int]
    __jefe: tuple[Imagen, Imagen]

    def __init__(self) -> None:
        self.__frame = 0
        self.__mapa = Imagen(1, (0, 0), MAPA_DIMENSIONES)
        self.pause = False   # atributo para parar el juego
        self.jugador = 1   # atrubuto para distinguir entre mario y luigi

        # declarar atributos
        self.__indice_anim = 0
        self.__posicion = (200,64)
        self.__jefe = ANIMACIONES_JEFE[0]

    def toggle_animation(self):
        self.__indice_anim = not self.__indice_anim

    def animacion(self):
        # comprueba si el que ha fallado es mario o luigi
        if self.jugador == 0:
            self.__posicion = (200,64)
            self.__jefe = ANIMACIONES_JEFE[0]
        elif self.jugador == 1:
            self.__posicion = (1,101)
            self.__jefe = ANIMACIONES_JEFE[1]
        pyxel.cls(7)
        self.__mapa.draw((0,0))
        self.__jefe[self.__indice_anim].draw(self.__posicion)   # pinta la animacion del jefe dependiendo de di es mario o luigi  // el indice anim solo sirve para que empiece arriba
        if self.__frame % 20 == 0:   # la animacion cambia cada 20 frames
            self.toggle_animation()
        self.__frame += 1
        if self.__frame >= 100:
            self.pause = False
            self.__frame = 0

    @property
    def pause(self):
        return self.__pause
    @pause.setter
    def pause(self,value):
        if type(value) == bool:
            self.__pause = value
        else:
            raise TypeError("El atributo jefe.pause tiene que ser bool")

    @property
    def jugador(self):
        return self.__jugador
    @jugador.setter
    def jugador(self,value):
        if value == 0 or value == 1:
            self.__jugador = value
        else:
            raise ValueError("El atributo jefe.jugador tiene que ser 1 o 0")
