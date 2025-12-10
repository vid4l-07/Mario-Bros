import pyxel
import random

from src.core.imagen import Imagen
from src.core.jugador import Jugador
from src.core.cinta import Cinta
from src.core.camion import Camion
from src.core.jefe import Jefe

from src.constantes.mario import *
from src.constantes.luigi import *
from src.constantes.cintas import *

from src.constantes.configuracion import MAPA_DIMENSIONES

class Partida:
    __mapa: Imagen
    __mario: Jugador
    __luigi: Jugador
    __cintas: list[Cinta]
    __minimo_numero_paquetes: int
    __puntos_para_subir_numero_paquetes_minimos: int
    __repartos_para_quitar_fallo: int
    __paquetes: int
    __frame: int
    __puntos: int
    __fallos: int
    __repartos: int
    __camion: Camion
    __jefe: Jefe

    def __init__(self, dificultad: int):
        mario_arriba = pyxel.KEY_UP
        mario_abajo = pyxel.KEY_DOWN
        luigi_arriba = pyxel.KEY_W
        luigi_abajo = pyxel.KEY_S

        # TODO: no se si hacer un método para aplicar la dificultad
        if dificultad == 0:
            self.__cintas = CINTAS[:4] + CINTAS[8:]
            self.__puntos_para_subir_numero_paquetes_minimos = 50
            self.__repartos_para_quitar_fallo = 3

        elif dificultad == 1:
            self.__cintas = CINTAS
            self.__puntos_para_subir_numero_paquetes_minimos = 30
            self.__repartos_para_quitar_fallo = 5
            for cinta in self.__cintas[1::2]:
                cinta.velocidad = 1.5

        elif dificultad == 2:
            self.__cintas = CINTAS
            self.__puntos_para_subir_numero_paquetes_minimos = 30
            self.__repartos_para_quitar_fallo = 5
            for cinta in self.__cintas[1::2]:
                cinta.velocidad = 2
            for cinta in self.__cintas[2::2]:
                cinta.velocidad = 1.5

        elif dificultad == 3:
            self.__cintas = CINTAS[:4] + CINTAS[8:]
            self.__puntos_para_subir_numero_paquetes_minimos = 20
            self.__repartos_para_quitar_fallo = 0
            for cinta in self.__cintas:
                cinta.velocidad = random.uniform(1, 2)
            mario_arriba = pyxel.KEY_DOWN
            mario_abajo = pyxel.KEY_UP
            luigi_arriba = pyxel.KEY_S
            luigi_abajo = pyxel.KEY_W

        # Limpiar las cintas
        for cinta in self.__cintas:
            cinta.eliminar_paquetes()

        self.__minimo_numero_paquetes = 1
        self.__paquetes = 1
        self.__frame = 0
        self.__puntos = 0
        self.__fallos = 0
        self.__repartos = 0

        self.__mapa = Imagen(1, (0, 0), MAPA_DIMENSIONES)
        self.__mario = Jugador(MARIO_POSICIONES, ANIMACIONES_MARIO, (mario_arriba, mario_abajo))
        self.__luigi = Jugador(LUIGI_POSICIONES, ANIMACIONES_LUIGI, (luigi_arriba, luigi_abajo))
        self.__jefe = Jefe()
        self.__camion = Camion()

    # Esto comprueba si se cae un paquete
    def __fall_handler(self, cinta: Cinta) -> bool:
        jugador = None
        if cinta.lado == 'DER':
            jugador = self.__mario
            numero = 0
        elif cinta.lado == 'IZQ':
            jugador = self.__luigi
            numero = 1
        else:
            # No debería llegarse aquí pero si lo hace no pasaría nada
            return False

        if jugador.posicion != cinta.nivel:
            self.__paquetes += self.__minimo_numero_paquetes
            self.__fallos += 1
            self.__jefe.pause = True
            self.__jefe.jugador = numero

            if self.__fallos >= 3:
                pyxel.quit()
            return True

        else:
            self.__puntos += 1
            if self.__puntos >= self.__puntos_para_subir_numero_paquetes_minimos:
                self.__minimo_numero_paquetes += 1
            jugador.activar_animacion(cinta.velocidad)

        return False

    def __entregar_paquete(self):
        if self.__camion.añadir_paquete():
            self.__repartos += 1
            if self.__repartos == self.__repartos_para_quitar_fallo:
                self.__repartos_para_quitar_fallo = 0
                self.__fallos = max(0 , self.__fallos - 1)
            # Actualizar el mínimo de paquetes
            self.__puntos += 10
            if self.__puntos == self.__puntos_para_subir_numero_paquetes_minimos:
                self.__minimo_numero_paquetes += 1

    def update(self):
        if self.__jefe.pause:
            return

        # Generación de paquetes
        if self.__frame == 0:
            self.__frame = 60
            if self.__paquetes > 0:
                self.__paquetes -= 1
                self.__cintas[0].añadir_paquete()

        self.__frame -= 1

        # Actualizamos el estado de los jugadores
        self.__mario.update()
        self.__luigi.update()

        # Las cintas avanzan
        salidas: list[int] = []
        for numero_cinta, cinta in enumerate(self.__cintas):
            salida = cinta.avanzar()
            if salida and not self.__fall_handler(cinta):
                salidas.append(numero_cinta)

        # Se mueven los paquetes de una cinta a otra
        for numero_cinta in salidas:
            if numero_cinta + 1 < len(self.__cintas):
                self.__cintas[numero_cinta + 1].añadir_paquete()
            else:
                # Cada vez que un paquete llega al final
                self.__entregar_paquete()

                # Generar más paquetes
                self.__paquetes += self.__minimo_numero_paquetes

    def draw(self):
        # El orden es importante
        if self.__jefe.pause:
            self.__jefe.animacion()
        else:
            for cinta in self.__cintas:
                cinta.draw()

            self.__camion.draw()
            self.__mapa.draw((0, 0))
            self.__mario.draw()
            self.__luigi.draw()

            pyxel.text(50, 5, 'Puntos: ' + str(self.__puntos), 0)
            pyxel.text(150, 5, 'Fallos: ' + str(self.__fallos), 0)
