import pyxel
pyxel.init(500, 500)
pyxel.load('my_resource.pyxres')
pyxel.images[1].load(0, 0, 'mapa.png')
pyxel.images[2].load(0, 0, 'objetos.png')
pyxel.save('my_resource.pyxres')
