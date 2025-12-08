import pyxel
import sys

if len(sys.argv) != 2:
    print('a .pyxres file is required')
    exit(1)

class Selection:
    image: int
    x: int
    y: int
    w: int
    h: int

    def __init__(self, image:int, x: int, y: int, w: int, h: int):
        self.image = image
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def print(self):
        print(self.image, self.x, self.y, self.w, self.h)

class Edit:
    image: int
    vx: int
    vy: int
    mx: int
    my: int
    selecting: bool
    selection: Selection | None

    def __init__(self):
        self.image = 0
        self.vx = 0
        self.vy = 0
        self.mx = 0
        self.my = 0
        self.selecting = False
        self.selection = None

        pyxel.init(50, 50)
        pyxel.load(sys.argv[1])
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.selection = Selection(self.image, self.mx + self.vx, self.my + self.vy, pyxel.mouse_x - self.mx, pyxel.mouse_y - self.my)

        elif not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.selecting = False
            self.mx = pyxel.mouse_x
            self.my = pyxel.mouse_y
        else:
            self.selecting = True

        if pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            pyxel.images[self.image].pset(pyxel.mouse_x + self.vx, pyxel.mouse_y + self.vy, 7)

        if pyxel.btnp(pyxel.KEY_1):
            self.image = 0
        elif pyxel.btnp(pyxel.KEY_2):
            self.image = 1
        elif pyxel.btnp(pyxel.KEY_3):
            self.image = 2

        elif pyxel.btn(pyxel.KEY_DOWN):
            self.vy += 1
        elif pyxel.btn(pyxel.KEY_UP):
            self.vy -= 1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.vx += 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.vx -= 1

        elif pyxel.btnp(pyxel.KEY_V):
            if self.selection == None:
                return

            # paste selection in mouse position
            src = pyxel.images[self.selection.image]
            dst = pyxel.images[self.image]

            for dy in range(self.selection.h):
                for dx in range(self.selection.w):
                    color = src.pget(self.selection.x + dx, self.selection.y + dy)
                    dst.pset(pyxel.mouse_x + dx + self.vx, pyxel.mouse_y + dy + self.vy, color)

        elif pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        elif pyxel.btnp(pyxel.KEY_S):
            pyxel.save(sys.argv[1])

    def draw(self):
        pyxel.blt(0, 0, self.image, self.vx, self.vy, 256, 256)

        if self.selecting:
            pyxel.rectb(self.mx, self.my, pyxel.mouse_x - self.mx, pyxel.mouse_y - self.my, 3)
        else:
            pyxel.rectb(self.mx, self.my, 1, 1, 3)

_ = Edit()
