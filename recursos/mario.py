from animacion import Animacion, Frame
from imagen import Imagen

ANIMACION_JEFE_MARIO_FRAME_1_1 = Frame(Imagen(2, (226, 72), (16, 29)), (222, 64))
ANIMACION_JEFE_MARIO_FRAME_1_2 = Frame(Imagen(2, (207, 74), (18, 27)), (205, 66))

ANIMACION_JEFE_MARIO_FRAME_2_1 = Frame(Imagen(2, (52, 220), (16, 29)), (222, 64))
ANIMACION_JEFE_MARIO_FRAME_2_2 = Frame(Imagen(2, (32, 220), (14, 27)), (205, 66))

ANIMACION_JEFE_MARIO = Animacion([
    [ANIMACION_JEFE_MARIO_FRAME_1_1, ANIMACION_JEFE_MARIO_FRAME_1_2],
    [ANIMACION_JEFE_MARIO_FRAME_2_1, ANIMACION_JEFE_MARIO_FRAME_2_2],
])

MARIO_1_1 = Imagen(2, (32, 152), (39, 26))
MARIO_1_2 = Imagen(2, (77, 152), (27, 27))
MARIO_2_1 = Imagen(2, (62, 190), (20, 25))
MARIO_2_2 = Imagen(2, (34, 186), (22, 29))
MARIO_3_1 = Imagen(2, (111, 152), (21, 27))
MARIO_3_2 = Imagen(2, (133, 152), (21, 27))

MARIO_POSICIONES = [(160, 129), (163, 94), (165, 54)]
ANIMACIONES_MARIO = [(MARIO_1_1, MARIO_1_2), (MARIO_2_1, MARIO_2_2), (MARIO_3_1, MARIO_3_2)]
