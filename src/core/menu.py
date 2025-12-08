import pyxel

class Menu:
    __opciones: list[str]
    __seleccion: int
    __visible: bool

    @property
    def visible(self) -> bool:
        return self.__visible

    def __init__(self, opciones: list[str]):
        self.__opciones = opciones
        self.__seleccion = 0
        self.__visible = True

    def update(self) -> int | None:
        if pyxel.btnp(pyxel.KEY_M):
            self.__visible = not self.__visible

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.__seleccion = min(self.__seleccion + 1, len(self.__opciones) - 1)

        if pyxel.btnp(pyxel.KEY_UP):
            self.__seleccion = max(self.__seleccion - 1, 0)

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.__visible = False
            return self.__seleccion

        return None

    def draw(self):
        if not self.__visible:
            return

        pyxel.cls(0)

        for i, opcion in enumerate(self.__opciones):
            pyxel.text(10, 10 + (10 * i), opcion, 1 if i == self.__seleccion else 7)

        pyxel.text(50, 10 + (10 * self.__seleccion), '<', 1)

