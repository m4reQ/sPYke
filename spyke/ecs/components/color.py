from glm import vec4

class ColorComponent(object):
	def __init__(self, *args):
		if isinstance(args[0], tuple):
			tup = args[0]
			self.R = tup[0]
			self.G = tup[1]
			self.B = tup[2]
			self.A = tup[3]
		elif isinstance(args[0], vec4):
			self.R = args[0].x
			self.G = args[0].y
			self.B = args[0].z
			self.A = args[0].w
		elif len(args) == 4:
			self.R = args[0]
			self.G = args[1]
			self.B = args[2]
			self.A = args[3]
		else:
			raise TypeError("Invalid color arguments.")
	
	def __iter__(self):
		yield self.R
		yield self.G
		yield self.B
		yield self.A