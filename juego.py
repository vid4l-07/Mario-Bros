import pyxel

from menu import Menu
from partida import Partida

from configuracion import MAPA_DIMENSIONES

class Juego:
    menu: Menu
    partida: None | Partida

    def __init__(self):
        self.menu = Menu(['Facil', 'Medio', 'Extremo', 'Crazy'])
        self.partida = Partida(0)

        MAPA_ANCHO, MAPA_ALTO = MAPA_DIMENSIONES
        pyxel.init(MAPA_ANCHO, MAPA_ALTO)
        pyxel.load('assets/my_resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        # Se puede cerrar el juego en cualquier momento
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Si se está usando el menú no se actualiza el estado del resto del juego
        seleccion = self.menu.update()
        if seleccion != None:
            # Se crea una nueva partida con los valores de la nueva dificultad
            self.partida = Partida(seleccion)
        if self.menu.visible:
            return

        if self.partida != None:
            self.partida.update()

    def draw(self):
        pyxel.cls(7)
        if self.partida != None:
            self.partida.draw()
        self.menu.draw()
