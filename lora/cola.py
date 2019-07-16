class cola:
	def __init__(self):#creación de la lista para utilizar como cola
		self.frames=[]
	
	def agregar(self,frame):#se agrega un elemento al final de la cola
		self.frames.append(frame)
    
	def extraer(self):#se extrae el elemento al inicio de la cola
		return self.frames.pop()
	
	def vacia(self):
		return self.frames == []
		
	def len(self):
		return len(self.frames)