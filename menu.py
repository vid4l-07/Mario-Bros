import pyxel

class Seleccion:
    def __init__(self, posiciones: list[tuple[int, int]]) -> None:
        self.posiciones = posiciones
        self.posicion = 0
        self.arriba, self.abajo = (pyxel.KEY_UP, pyxel.KEY_DOWN)

    def update(self) -> None:
        if pyxel.btnp(self.abajo):
            self.posicion = min(self.posicion + 1, len(self.posiciones) - 1)

        elif pyxel.btnp(self.arriba):
            self.posicion = max(self.posicion - 1, 0)

        elif pyxel.btnp(pyxel.KEY_RETURN):
            print(self.posicion)

    def draw(self) -> None:
        x, y = self.posiciones[self.posicion]
        pyxel.text(x,y, ">", 7)  # Blanco



class Menu:
    def __init__(self) -> None:
        self.posiciones = ([(5,10),(5,20),(5,30)])
        self.seleccion = Seleccion(self.posiciones)
        pyxel.init(100, 100)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.seleccion.update()

    def draw(self):
        pyxel.cls(0)                 # Limpiar pantalla con color negro
        pyxel.text(self.posiciones[0][0] + 5, self.posiciones[0][1], "Hola Pyxel!", 7)  # Blanco
        pyxel.text(self.posiciones[1][0] + 5, self.posiciones[1][1], "Una opcion", 3)
        pyxel.text(self.posiciones[2][0] + 5, self.posiciones[2][1], "Otra opcion", 3)
        self.seleccion.draw()




if __name__ == '__main__':
    _ = Menu()
