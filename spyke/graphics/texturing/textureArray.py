#region Import
from .textureData import TextureData
from .textureHandle import TextureHandle
from ... import USE_FAST_ARRAY_MIN_FILTER
from ...utils import ObjectManager, Timer
from ...enums import TextureType, TextureMagFilter
from ...debug import Log, LogLevel

import numpy
from OpenGL import GL
#endregion

class TexArraySpec(object):
	def __init__(self, width: int, height: int, layers: int):
		self.width = width
		self.height = height
		self.layers = layers
		self.mipLevels = 3
		self.minFilter = GL.GL_LINEAR_MIPMAP_LINEAR
		self.magFilter = GL.GL_NEAREST_MIPMAP_NEAREST

class TextureArray(object):
	__MaxLayersCount = 0

	def __init__(self, spec: TexArraySpec):
		Timer.Start()

		if not TextureArray.__MaxLayersCount:
			TextureArray.__MaxLayersCount = int(GL.glGetInteger(GL.GL_MAX_ARRAY_TEXTURE_LAYERS))
		
		if spec.layers > TextureArray.__MaxLayersCount:
			raise RuntimeError(f"Cannot create texture array with {spec.layers} layers (max layers count: {TextureArray.__MaxLayersCount}).")

		self.__spec = spec

		self.__currentLayer = 0

		self.__id = GL.glGenTextures(1)
		GL.glBindTexture(GL.GL_TEXTURE_2D_ARRAY, self.__id)
		GL.glTexStorage3D(GL.GL_TEXTURE_2D_ARRAY, self.__spec.mipLevels, GL.GL_RGBA, self.__spec.width, self.__spec.height, self.__spec.layers)
		GL.glTexParameter(GL.GL_TEXTURE_2D_ARRAY, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
		GL.glTexParameter(GL.GL_TEXTURE_2D_ARRAY, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
		GL.glTexParameter(GL.GL_TEXTURE_2D_ARRAY, GL.GL_TEXTURE_MIN_FILTER, self.__spec.minFilter)
		GL.glTexParameter(GL.GL_TEXTURE_2D_ARRAY, GL.GL_TEXTURE_MAG_FILTER, self.__spec.magFilter)

		GL.glBindTexture(GL.GL_TEXTURE_2D_ARRAY, 0)

		ObjectManager.AddObject(self)

		Log(f"Texture array of size ({self.__spec.width}x{self.__spec.height}x{self.__spec.layers}) initialized in {Timer.Stop()} seconds.", LogLevel.Info)
	
	def UploadTexture(self, texData: TextureData) -> TextureHandle:
		self.Bind()

		if self.__currentLayer + 1 > TextureArray.__MaxLayersCount:
			raise RuntimeError("Max texture array layers count exceeded.")
		if texData.width > self.__spec.width or texData.height > self.__spec.height:
			raise RuntimeError("Texture size is higher than maximum.")
		
		if texData.width != self.__spec.width or texData.height != self.__spec.height:
			GL.glTexSubImage3D(GL.GL_TEXTURE_2D_ARRAY, 0, 0, 0, self.__currentLayer, self.__spec.width, self.__spec.height, 1, texData.format, GL.GL_UNSIGNED_BYTE, numpy.empty(self.__spec.width * self.__spec.height * (3 if texData.format == GL.GL_RGB else 4), dtype = numpy.uint8))
		GL.glTexSubImage3D(GL.GL_TEXTURE_2D_ARRAY, 0, 0, 0, self.__currentLayer, texData.width, texData.height, 1, texData.format, GL.GL_UNSIGNED_BYTE, numpy.asarray(texData.data, dtype = numpy.uint8))
		GL.glGenerateMipmap(GL.GL_TEXTURE_2D_ARRAY)

		handle = TextureHandle()
		handle.u = (texData.width - 0.5) / self.__spec.width
		handle.v = (texData.height - 0.5) / self.__spec.height
		handle.layer = self.__currentLayer

		self.__currentLayer += 1

		return handle
	
	@staticmethod
	def UnbindAll():
		GL.glBindTexture(GL.GL_TEXTURE_2D_ARRAY, 0)
	
	def Bind(self):
		GL.glBindTexture(GL.GL_TEXTURE_2D_ARRAY, self.__id)
	
	def Delete(self):
		GL.glDeleteTextures(1, [self.__id])
	
	#region Getters
	@property
	def CurrentLayer(self):
		return self.__currentLayer
	
	@property
	def IsAccepting(self):
		return self.__currentLayer < self.__spec.layers
	
	@property
	def Width(self):
		return self.__spec.width
	
	@property
	def Height(self):
		return self.__spec.height
	
	@property
	def Layers(self):
		return self.__spec.layers
	#endregion