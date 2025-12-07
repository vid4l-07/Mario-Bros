import pyxel
import random
from imagen import Imagen
from jugador import Jugador
from cinta import Cinta, CINTAS
from camion import Camion
from animacion import Animacion, Frame
from constantes import *

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

LUIGI_1_1 = Imagen(2, (88, 184), (19, 27))
LUIGI_1_2 = Imagen(2, (112, 184), (22, 27))
LUIGI_2_1 = Imagen(2, (158, 184), (17, 29))
LUIGI_2_2 = Imagen(2, (138, 184), (19, 29))
LUIGI_3_1 = Imagen(2, (203, 149), (43, 32))
LUIGI_3_2 = Imagen(2, (159, 149), (26, 32))

MARIO_POSICIONES = [(160, 129), (163, 94), (165, 54)]
LUIGI_POSICIONES = [(54, 112), (57, 76), (30, 38)]

ANIMACIONES_MARIO = [(MARIO_1_1, MARIO_1_2), (MARIO_2_1, MARIO_2_2), (MARIO_3_1, MARIO_3_2)]
ANIMACIONES_LUIGI = [(LUIGI_1_1, LUIGI_1_2), (LUIGI_2_1, LUIGI_2_2), (LUIGI_3_1, LUIGI_3_2)]

class Partida:
    mapa: Imagen
    mario: Jugador
    luigi: Jugador
    cintas: list[Cinta]
    minimo_numero_paquetes: int
    puntos_para_subir_numero_paquetes_minimos: int
    repartos_para_quitar_fallo: int
    paquetes: int
    frame: int
    puntos: int
    fallos: int
    repartos: int
    camion: Camion
    animacion: Animacion | None

    def __init__(self, dificultad: int):
        mario_arriba = pyxel.KEY_UP
        mario_abajo = pyxel.KEY_DOWN
        luigi_arriba = pyxel.KEY_W
        luigi_abajo = pyxel.KEY_S

        # TODO: no se si hacer un método para aplicar la dificultad
        if dificultad == 0:
            self.cintas = CINTAS[:4] + CINTAS[8:]
            self.puntos_para_subir_numero_paquetes_minimos = 50
            self.repartos_para_quitar_fallo = 3

        elif dificultad == 1:
            self.cintas = CINTAS
            self.puntos_para_subir_numero_paquetes_minimos = 30
            self.repartos_para_quitar_fallo = 5
            for cinta in self.cintas[1::2]:
                cinta.actualizar_velocidad(1.5)

        elif dificultad == 2:
            self.cintas = CINTAS
            self.puntos_para_subir_numero_paquetes_minimos = 30
            self.repartos_para_quitar_fallo = 5
            for cinta in self.cintas[1::2]:
                cinta.actualizar_velocidad(2)
            for cinta in self.cintas[2::2]:
                cinta.actualizar_velocidad(1.5)

        elif dificultad == 3:
            self.cintas = CINTAS[:4] + CINTAS[8:]
            self.puntos_para_subir_numero_paquetes_minimos = 20
            self.repartos_para_quitar_fallo = 0
            for cinta in self.cintas:
                cinta.actualizar_velocidad(random.uniform(1, 2))
            mario_arriba = pyxel.KEY_DOWN
            mario_abajo = pyxel.KEY_UP
            luigi_arriba = pyxel.KEY_S
            luigi_abajo = pyxel.KEY_W

        # Limpiar las cintas
        for cinta in self.cintas:
            cinta.eliminar_paquetes()

        self.minimo_numero_paquetes = 1
        self.paquetes = 1
        self.frame = 0
        self.puntos = 0
        self.fallos = 0
        self.repartos = 0
        self.animacion = None

        self.mapa = Imagen(1, (0, 0), MAPA_DIMENSIONES)
        self.mario = Jugador(MARIO_POSICIONES, ANIMACIONES_MARIO, (mario_arriba, mario_abajo), ANIMACION_JEFE_MARIO)
        self.luigi = Jugador(LUIGI_POSICIONES, ANIMACIONES_LUIGI, (luigi_arriba, luigi_abajo), ANIMACION_JEFE_MARIO)
        self.camion = Camion()

    # Esto comprueba si se cae un paquete
    def fall_handler(self, cinta: Cinta) -> bool:
        jugador = None
        if cinta.lado == 'DER':
            jugador = self.mario
        elif cinta.lado == 'IZQ':
            jugador = self.luigi
        else:
            # No debería llegarse aquí pero si lo hace no pasaría nada
            return False

        if jugador.posicion != cinta.nivel:
            jugador.animacion_jefe.activo = True
            self.animacion = jugador.animacion_jefe

            self.paquetes += self.minimo_numero_paquetes
            self.fallos += 1
            if self.fallos >= 3:
                pyxel.quit()
            return True

        else:
            self.puntos += 1
            if self.puntos >= self.puntos_para_subir_numero_paquetes_minimos:
                self.minimo_numero_paquetes += 1
            jugador.activar_animacion(cinta.velocidad)

        return False

    def update(self):
        if self.animacion and self.animacion.activo:
            self.animacion.update()
            return

        # Generación de paquetes
        if self.frame == 0:
            self.frame = 60
            if self.paquetes > 0:
                self.paquetes -= 1
                self.cintas[0].añadir_paquete()

        self.frame -= 1

        # Actualizamos el estado de los jugadores
        self.mario.update()
        self.luigi.update()

        # Las cintas avanzan
        salidas: list[int] = []
        for numero_cinta, cinta in enumerate(self.cintas):
            salida = cinta.avanzar()
            if salida and not self.fall_handler(cinta):
                salidas.append(numero_cinta)

        # Se mueven los paquetes de una cinta a otra
        for numero_cinta in salidas:
            if numero_cinta + 1 < len(self.cintas):
                self.cintas[numero_cinta + 1].añadir_paquete()
            else:
                # Cada vez que un paquete llega al final
                if self.camion.añadir_paquete():
                    self.repartos += 1
                    if self.repartos == self.repartos_para_quitar_fallo:
                        self.repartos_para_quitar_fallo = 0
                        self.fallos = max(0 , self.fallos - 1)
                    # Actualizar el mínimo de paquetes
                    self.puntos += 10
                    if self.puntos == self.puntos_para_subir_numero_paquetes_minimos:
                        self.minimo_numero_paquetes += 1

                # Generar más paquetes
                self.paquetes += self.minimo_numero_paquetes

    def draw(self):
        # El orden es importante

        if self.animacion == None or not self.animacion.activo:
            for cinta in self.cintas:
                cinta.draw()
            self.camion.draw()
            self.mapa.draw((0, 0))
            self.mario.draw()
            self.luigi.draw()
        elif self.animacion.activo:
            self.mapa.draw((0, 0))
            self.animacion.draw()

        pyxel.text(50, 5, 'Puntos: ' + str(self.puntos), 0)
        pyxel.text(150, 5, 'Fallos: ' + str(self.fallos), 0)

