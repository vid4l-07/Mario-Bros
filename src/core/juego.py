import pyxel

from src.core.menu import Menu
from src.core.partida import Partida

from src.constantes.configuracion import MAPA_DIMENSIONES

class Juego:
    __menu: Menu
    __partida: None | Partida

    def __init__(self):
        self.__menu = Menu(['Facil', 'Medio', 'Extremo', 'Crazy'])
        self.__partida = Partida(0)

        MAPA_ANCHO, MAPA_ALTO = MAPA_DIMENSIONES
        pyxel.init(MAPA_ANCHO, MAPA_ALTO)
        pyxel.load('../../assets/my_resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        # Se puede cerrar el juego en cualquier momento
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Si se está usando el menú no se actualiza el estado del resto del juego
        seleccion = self.__menu.update()
        if seleccion != None:
            # Se crea una nueva partida con los valores de la nueva dificultad
            self.__partida = Partida(seleccion)
        if self.__menu.visible:
            return

        if self.__partida != None:
            self.__partida.update()

    def draw(self):
        pyxel.cls(7)
        if self.__partida != None:
            self.__partida.draw()
        self.__menu.draw()
