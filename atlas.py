import pyxel
pyxel.init(500, 500)
pyxel.load('my_resource.pyxres')
pyxel.images[1].load(0, 0, 'atlas1.png')
pyxel.images[2].load(0, 0, 'atlas2.png')
pyxel.save('my_resource.pyxres')
