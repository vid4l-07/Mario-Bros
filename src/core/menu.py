import pyxel

class Menu:
    opciones: list[str]
    seleccion: int
    visible: bool

    def __init__(self, opciones: list[str]):
        self.opciones = opciones
        self.seleccion = 0
        self.visible = True

    def update(self) -> int | None:
        if pyxel.btnp(pyxel.KEY_M):
            self.visible = not self.visible

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.seleccion = min(self.seleccion + 1, len(self.opciones) - 1)

        if pyxel.btnp(pyxel.KEY_UP):
            self.seleccion = max(self.seleccion - 1, 0)

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.visible = False
            return self.seleccion

        return None

    def draw(self):
        if not self.visible:
            return

        pyxel.cls(0)

        for i, opcion in enumerate(self.opciones):
            pyxel.text(10, 10 + (10 * i), opcion, 1 if i == self.seleccion else 7)

        pyxel.text(50, 10 + (10 * self.seleccion), '<', 1)

