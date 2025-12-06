import random
import pyxel

class Imagen:
    x: int
    y: int
    ancho: int
    alto: int
    imagen: int

    def __init__(self, imagen: int, posicion: tuple[int, int], tamano: tuple[int, int]):
        self.x, self.y = posicion
        self.ancho, self.alto = tamano
        self.imagen = imagen

    def draw(self, posicion: tuple[int, int]):
        x, y = posicion
        pyxel.blt(x, y, self.imagen, self.x, self.y, self.ancho, self.alto, colkey=7)

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

class Jugador:
    posiciones: list[tuple[int, int]]
    posicion: int
    teclas: tuple[int, int]
    animacion: bool
    animaciones: list[tuple[Imagen, Imagen]]
    imagen: Imagen
    frame: int

    def __init__(self, posiciones: list[tuple[int, int]], animaciones: list[tuple[Imagen, Imagen]], teclas: tuple[int, int]) -> None:
        self.posiciones = posiciones
        self.posicion = 0
        self.teclas = teclas

        self.animaciones = animaciones
        self.animacion = False
        self.imagen = self.animaciones[self.posicion][self.animacion]

        self.frame = 0

    # Se llama cuando el personaje mueve un paquete. Esta función recive la
    # velocidad de la cinta desde la que el personaje coge el paquete. Esto
    # permite saber el tiempo justo que tiene que tardar el personaje en
    # desactivar la animación.
    def activar_animacion(self, tiempo: int):
        self.frame = tiempo
        self.animacion = True
        self.imagen = self.animaciones[self.posicion][self.animacion]

    def update(self) -> None:
        arriba, abajo = self.teclas
        if pyxel.btnp(arriba):
            self.frame = 0 # Se cancela la animación
            self.posicion = min(self.posicion + 1, len(self.posiciones) - 1)
        elif pyxel.btnp(abajo):
            self.frame = 0 # Se cancela la animación
            self.posicion = max(self.posicion - 1, 0)

        if self.frame > 0:
            self.frame -= 1
        elif self.frame == 0:
            self.animacion = False

        self.imagen = self.animaciones[self.posicion][self.animacion]

    def draw(self) -> None:
        x, y = self.posiciones[self.posicion]
        self.imagen.draw((x, y - self.imagen.alto))
        # Se calcula la coordenada del personaje desde la base. Esto es
        # necesario ya que hay animaciones con distinta altura.


# TODO: Imagen de caida
class Cinta:
    imagen_paquete: Imagen
    paquetes: list[int]
    inicio: tuple[int, int]
    velocidad: int
    frame: int
    direccion: int
    pasos: int

    def __init__(self, imagen_paquete: Imagen, inicio: tuple[int, int], pasos: int, direccion: int, factor_velocidad: float = 1):
        self.imagen_paquete = imagen_paquete
        self.paquetes = []
        self.inicio = inicio
        self.direccion = direccion
        self.pasos = pasos
        self.velocidad = int(20 / factor_velocidad)
        self.frame = 0

    def añadir_paquete(self):
        self.paquetes.append(0)

    def eliminar_paquetes(self):
        self.paquetes.clear()

    def actualizar_velocidad(self, factor: float):
        self.velocidad = int(20 / factor)

    def draw(self):
        x, y = self.inicio
        for paquete in self.paquetes:
            self.imagen_paquete.draw((x + (paquete * 11 * self.direccion), y))

    def caida(self) -> bool:
        return any(paso >= self.pasos for paso in self.paquetes)

    def avanzar(self) -> bool:
        self.frame += 1
        if self.frame < self.velocidad:
            return False
        self.frame = 0

        salida = False
        nuevos: list[int] = []

        for paquete in self.paquetes:
            nuevo = paquete + 1
            if nuevo < self.pasos:
                nuevos.append(nuevo)
            else:
                salida = True

        self.paquetes = nuevos
        return salida

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

PAQUETE_1 = Imagen(2, (135, 116), (9, 4))
PAQUETE_2 = Imagen(2, (109, 113), (9, 7))
PAQUETE_3 = Imagen(2, (151, 94), (9, 7))
PAQUETE_4 = Imagen(2, (109, 73), (9, 9))
PAQUETE_5 = Imagen(2, (136, 36), (9, 9))
PAQUETE_6 = Imagen(2, (109, 36), (9, 9))

# PAQUETE_1_CAIDA = Imagen(2, (9, 152), (9, 9))
# PAQUETE_2_CAIDA = Imagen(2, (75, 114), (10, 10))
# PAQUETE_3_CAIDA = Imagen(2, (162, 94), (10, 11))
# PAQUETE_4_CAIDA = Imagen(2, (0, 164), (11, 12))
# PAQUETE_5_CAIDA = Imagen(2, (0, 184), (12, 12))
# PAQUETE_6_CAIDA = Imagen(2, (16, 184), (13, 13))

cinta10 = Cinta(PAQUETE_6, (106, 28), 4, -1)
cinta9 = Cinta(PAQUETE_5, (155, 28),  4, -1)
cinta8 = Cinta(PAQUETE_5, (126, 47),  4, 1)
cinta7 = Cinta(PAQUETE_4, (77,  46),  4, 1)
cinta6 = Cinta(PAQUETE_4, (106, 65),  4, -1)
cinta5 = Cinta(PAQUETE_3, (155, 67),  4, -1)
cinta4 = Cinta(PAQUETE_3, (126, 86),  4, 1)
cinta3 = Cinta(PAQUETE_2, (77,  86),  4, 1)
cinta2 = Cinta(PAQUETE_2, (106, 105), 4, -1)
cinta1 = Cinta(PAQUETE_1, (154, 108), 4, -1)
cinta0 = Cinta(PAQUETE_1, (217, 108), 3, -1)

cinta0.añadir_paquete()
cintas = [cinta0, cinta1, cinta2, cinta3, cinta4, cinta5, cinta6, cinta7, cinta8, cinta9, cinta10]

class Camion:
    paquetes: int
    imagen: Imagen

    def __init__(self):
        self.paquetes = 0
        self.imagen = Imagen(2, (180, 184), (36, 41))

    def añadir_paquete(self) -> bool:
        self.paquetes += 1
        if self.paquetes >= 2:
            self.paquetes = 0
            return True

        return False

    def draw(self):
        self.imagen.draw((4, 39))
        for paquete in range(self.paquetes):
            columna = paquete % 2
            fila = paquete // 2
            PAQUETE_6.draw((19 + (columna * 11), 58 - (fila * 10)))

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

    def __init__(self, dificultad: int):
        mario_arriba = pyxel.KEY_UP
        mario_abajo = pyxel.KEY_DOWN
        luigi_arriba = pyxel.KEY_W
        luigi_abajo = pyxel.KEY_S

        # TODO: no se si hacer un método para aplicar la dificultad
        if dificultad == 0:
            self.cintas = cintas[:7]
            self.puntos_para_subir_numero_paquetes_minimos = 50
            self.repartos_para_quitar_fallo = 3

        elif dificultad == 1:
            self.cintas = cintas
            self.puntos_para_subir_numero_paquetes_minimos = 30
            self.repartos_para_quitar_fallo = 5
            for cinta in self.cintas[1::2]:
                cinta.actualizar_velocidad(1.5)

        elif dificultad == 2:
            self.cintas = cintas
            self.puntos_para_subir_numero_paquetes_minimos = 30
            self.repartos_para_quitar_fallo = 5
            for cinta in self.cintas[1::2]:
                cinta.actualizar_velocidad(2)
            for cinta in self.cintas[2::2]:
                cinta.actualizar_velocidad(1.5)

        elif dificultad == 3:
            self.cintas = cintas[:7]
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

        # TODO: sacar como constantes
        MARIO_POSICIONES = [(160, 129), (163, 94), (165, 54)]
        LUIGI_POSICIONES = [(54, 112), (57, 76), (30, 38)]

        # TODO: sacar como constantes
        ANIMACIONES_MARIO = [(MARIO_1_1, MARIO_1_2), (MARIO_2_1, MARIO_2_2), (MARIO_3_1, MARIO_3_2)]
        ANIMACIONES_LUIGI = [(LUIGI_1_1, LUIGI_1_2), (LUIGI_2_1, LUIGI_2_2), (LUIGI_3_1, LUIGI_3_2)]

        self.mapa = Imagen(1, (0, 0), (240, 136))
        self.mario = Jugador(MARIO_POSICIONES, ANIMACIONES_MARIO, (mario_arriba, mario_abajo))
        self.luigi = Jugador(LUIGI_POSICIONES, ANIMACIONES_LUIGI, (luigi_arriba, luigi_abajo))
        self.camion = Camion()

    # Esto comprueba si se cae un paquete
    def fall_handler(self, numero_cinta: int) -> bool:
        resto = numero_cinta % 4
        posicion = None

        if resto == 0:
            # Por la derecha
            posicion = numero_cinta % 3
        elif resto == 2:
            # Por la izquierda
            posicion = (numero_cinta + 1) % 3

        if posicion is not None:
            jugador = self.mario if resto == 0 else self.luigi
            if jugador.posicion != posicion:
                self.paquetes += self.minimo_numero_paquetes
                self.fallos += 1
                if self.fallos >= 3:
                    pyxel.quit()
                return True
            else:
                self.puntos += 1
                if self.puntos >= self.puntos_para_subir_numero_paquetes_minimos:
                    self.minimo_numero_paquetes += 1
                jugador.activar_animacion(self.cintas[numero_cinta].velocidad)

        return False

    def update(self):
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
            if salida and not self.fall_handler(numero_cinta):
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
        for cinta in self.cintas:
            cinta.draw()
        self.camion.draw()
        self.mapa.draw((0, 0))
        self.mario.draw()
        self.luigi.draw()
        pyxel.text(50, 5, 'Puntos: ' + str(self.puntos), 0)
        pyxel.text(150, 5, 'Fallos: ' + str(self.fallos), 0)


# TODO: El tamaño del mapa debería ser una constante
class Juego:
    menu: Menu
    partida: None | Partida

    def __init__(self):
        self.menu = Menu(['Facil', 'Medio', 'Extremo', 'Crazy'])
        self.partida = Partida(0)

        pyxel.init(240, 136)
        pyxel.load('my_resource.pyxres')
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

if __name__ == '__main__':
    _ = Juego()
