from machine import reset
class Menu(object):
	"""
	Clase Menu, simplifica la creacion de menus para realizar pruebas
	ejemplo de uso:
		>>> menu = Menu("Bienvenido al menu")
		>>> menu.add("Probar sensor", fun_sensor) #donde fun_sensor es un metodo o funcion que prueba el sensor
		>>> menu.add("Bienvenido al submenu", Menu()) #se puede añadir un submenu de la misma forma
		>>> menu.start()	
	"""
	nOpenedMenus = 0
	def __init__(self, title):
		super(Menu, self).__init__()
		self.registeredoptions = []
		self.optioncounter = 0
		self.title = title
		self.__name__='Menu'
	
	"""
	Permite añadir un item al menu, de igual forma se pueden añadir submenus.
	Cada item tiene un título y un callback
	"""
	def add(self, title, callback, menu=None):
		if title is None or callback is None:
			print("title o callback no pueden ser nulos")

		elif menu is None and callback is not None and callback.__name__ is not 'Menu':
			self.registeredoptions.append((self.optioncounter+1, title, callback))
			self.optioncounter+=1
		
		elif menu is None and callback is not None and callback.__name__ is 'Menu':
			self.registeredoptions.append((self.optioncounter+1, title, callback.start))
			self.optioncounter+=1

		elif menu is not None and menu.__name__ is "Menu" and callback is None:
			self.registeredoptions.append((self.optioncounter+1, title, menu.start))
			self.optioncounter+=1
		else:
			print("Ingresa bien los argumentos")
		return self

	"""
	Inicia el menú y espera la entrada de teclado correcta.
	Basta con llamar una vez para iniciar el menú principal.
	Se llama luego de configurar el menú con add()
	"""
	def start(self):
		keyboardinput = None
		Menu.nOpenedMenus += 1
		try:
			while True:
				for i in self.registeredoptions:
					print("({0}) {1} \t \t[llama a: {2}]".format(i[0], i[1], i[2]))
				print("({}) Atras".format(self.optioncounter+1))
				print("Para salir y reiniciar la placa usa [CTRL+C]")
				keyboardinput = int(input())
				if keyboardinput is not None and keyboardinput > 0 and keyboardinput < self.optioncounter + 1:
					self.registeredoptions[keyboardinput-1][2]()
				elif keyboardinput is self.optioncounter + 1 and Menu.nOpenedMenus > 1:
					Menu.nOpenedMenus-=1
					break
				elif keyboardinput is self.optioncounter + 1 and Menu.nOpenedMenus == 1:
					print("Este es el menú principal, no puedes volver\n")
				else:
					print("Ingresa una opción dentro del rango\n")
		except KeyboardInterrupt:
			reset()