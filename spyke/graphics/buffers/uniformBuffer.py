from ...utils import ObjectManager

from OpenGL import GL
import numpy

class UniformBuffer(object):
	def __init__(self, size: int, usage = GL.GL_STREAM_DRAW):
		self.__id = GL.glGenBuffers(1)
		
		GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, self.__id)
		GL.glBufferData(GL.GL_UNIFORM_BUFFER, size, None, usage)
		GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, 0)

		self.__size = size
		self.__usageFlag = usage

		ObjectManager.AddObject(self)

	def Delete(self):
		GL.glDeleteBuffers(1, [self.__id])

	def Bind(self):
		GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, self.__id)

	def Unbind(self):
		GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, 0)

	def BindToUniform(self, index: int):
		GL.glBindBufferBase(GL.GL_UNIFORM_BUFFER, index, self.__id)

	def AddData(self, data: list, size: int):
		GL.glBufferSubData(GL.GL_UNIFORM_BUFFER, 0, size, numpy.asarray(data, dtype=numpy.float32))

	def Clear(self):
		GL.glBufferData(GL.GL_UNIFORM_BUFFER, self.__size, None, self.__usageFlag)

	@property
	def Size(self):
		return self.__size
	
	@property
	def ID(self):
		return self.__id

	@staticmethod
	def UnbindAll() -> None:
		GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, 0)