from .textureHandle import TextureHandle
from ..transform import CreateTranslation, CreateScale
from ..utils import GetGLTypeSize, GLType

import glm

class ARenderable(object):
	def __init__(self):
		self.Transform = glm.mat4(1.0)

class Quad(ARenderable):
	VertexSize = (3 + 4 + 2 + 1 + 2) * GetGLTypeSize(GLType.Float)
	VertexLength = 3 + 4 + 2 + 1 + 2
	"""
	Vertex layout: pos - 3f, col - 4f, texPos - 2f, texId - 1f, tilingFactorXY - 2f
	"""

	def __init__(self, pos: list, size: list, color: list, texture: TextureHandle, tf: list):
		self.Position = pos
		self.Size = size
		self.Color = color
		self.TexCoord = (texture.U, texture.V)
		self.TexId = texture.Index
		self.TilingFactor = tf

		self.Transform = CreateTranslation(self.Position) * CreateScale((*self.Size, 0.0))

class Line(ARenderable):
	VertexSize = (3 + 4) * GetGLTypeSize(GLType.Float)
	VertexLength = 3 + 4
	"""
	Vertex layout: pos - 3f, col - 4f
	"""

	def __init__(self, startPos: list, endPos: list, color: list):
		self.StartPosition = startPos
		self.EndPosition = endPos
		self.Color = color

class PostRenderQuad(ARenderable):
	VertexSize = (3 + 4 + 2 + 2) * GetGLTypeSize(GLType.Float)
	VertexLength = 3 + 4 + 2 + 2
	"""
	Vertex layout: pos - 3f, col - 4f, texCoord - 2f, tilingFactorXY - 2f
	"""

	def __init__(self, pos: list, size: list, color: list, tilingFactor: list):
		self.Position = pos
		self.Size = size
		self.Color = color
		self.TilingFactor = tilingFactor

		self.Transform = CreateTranslation(self.Position) * CreateScale((*self.Size, 0.0))

class ATextQuad(ARenderable):
	VertexSize = (3 + 4 + 1 + 2) * GetGLTypeSize(GLType.Float)
	VertexLength = (3 + 4 + 1 + 2)
	"""
	Vertex layout: pos - 3f, col - 4f, texId - 1f, texCoord - 2f
	"""

NoTiling = [1.0, 1.0]