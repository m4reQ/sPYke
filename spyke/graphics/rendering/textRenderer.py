#region Import
from .renderStats import RenderStats
from .rendererComponent import RendererComponent
from .rendererSettings import RendererSettings
from ..shader import Shader
from ..buffers import VertexBuffer, IndexBuffer
from ..vertexArray import VertexArray
from ..text.font import Font
from ...managers import FontManager
from ...transform import CreateQuadIndices
from ...utils import GL_FLOAT_SIZE
from ...debug import Log, LogLevel

from OpenGL import GL
import glm
import time
#endregion

VERTEX_SIZE = (3 + 4 + 1 + 2) * GL_FLOAT_SIZE
VERTEX_DATA_VERTEX_SIZE = (3 + 2) * GL_FLOAT_SIZE
INSTANCE_DATA_VERTEX_SIZE = (4 + 1) * GL_FLOAT_SIZE

class TextRenderer(RendererComponent):
	def __init__(self):
		self.shader = Shader()
		self.shader.AddStage(GL.GL_VERTEX_SHADER, "spyke/graphics/shaderSources/text.vert")
		self.shader.AddStage(GL.GL_FRAGMENT_SHADER, "spyke/graphics/shaderSources/text.frag")
		self.shader.Compile()

		self.instanceDataVbo = VertexBuffer(INSTANCE_DATA_VERTEX_SIZE * RendererSettings.MaxQuadsCount)
		self.vertexDataVbo = VertexBuffer(VERTEX_DATA_VERTEX_SIZE * RendererSettings.MaxQuadsCount * 4)

		self.ibo = IndexBuffer(CreateQuadIndices(RendererSettings.MaxQuadsCount))

		self.vao = VertexArray()
		self.vao.Bind()

		self.vertexDataVbo.Bind()
		self.vao.SetVertexSize(VERTEX_DATA_VERTEX_SIZE)
		self.vao.ClearVertexOffset()
		self.vao.AddLayout(self.shader.GetAttribLocation("aPosition"), 3, GL.GL_FLOAT, False)
		self.vao.AddLayout(self.shader.GetAttribLocation("aTexCoord"), 2, GL.GL_FLOAT, False)

		self.instanceDataVbo.Bind()
		self.vao.SetVertexSize(INSTANCE_DATA_VERTEX_SIZE)
		self.vao.ClearVertexOffset()

		colLoc = self.shader.GetAttribLocation("aColor")
		tiLoc = self.shader.GetAttribLocation("aTexIdx")

		self.vao.AddLayout(colLoc, 4, GL.GL_FLOAT, False)
		self.vao.AddLayout(tiLoc, 1, GL.GL_FLOAT, False)

		self.vao.AddDivisor(colLoc, 1)
		self.vao.AddDivisor(tiLoc, 1)
		
		self.winSize = (1, 1)

		self.__vertexData = []
		self.__instanceData = []
		self.__indexCount = 0

		Log("Text renderer initialized", LogLevel.Info)

	def Resize(self, width: int, height: int):
		self.winSize = (width, height)
	
	def EndScene(self) -> None:
		if self.__indexCount != 0:
			self.__Flush()

	def __Flush(self) -> None:
		self.shader.Use()

		FontManager.Use()

		self.vao.Bind()
		self.ibo.Bind()

		self.instanceDataVbo.AddDataDirect(self.__instanceData, len(self.__instanceData) * GL_FLOAT_SIZE)
		self.vertexDataVbo.AddDataDirect(self.__vertexData, len(self.__vertexData) * GL_FLOAT_SIZE)

		GL.glDrawElementsInstanced(GL.GL_TRIANGLES, self.__indexCount, GL.GL_UNSIGNED_INT, None, self.__indexCount // 6)

		RenderStats.DrawsCount += 1

		self.__vertexData.clear()
		self.__instanceData.clear()
		self.__indexCount = 0

	def RenderText(self, pos: glm.vec3, color: glm.vec4, font: Font, size: int, text: str) -> None:
		advanceSum = 0

		glyphSize = size / font.baseSize

		for char in text:
			if self.__indexCount // 6 >= RendererSettings.MaxQuadsCount:
				self.__Flush()

			glyph = font.GetGlyph(ord(char))

			advance = advanceSum / self.winSize[0] * glyphSize

			width = glyph.width / self.winSize[0] * glyphSize
			height = glyph.height / self.winSize[1] * glyphSize

			xPos = pos.x + advance

			advanceSum += glyph.advance

			vertexData = [
				xPos, pos.y, 					pos.z, glyph.x, glyph.y + glyph.texHeight,
				xPos, pos.y + height, 			pos.z, glyph.x, glyph.y,
				xPos + width, pos.y + height, 	pos.z, glyph.x + glyph.texWidth, glyph.y,
				xPos + width, pos.y, 			pos.z, glyph.x + glyph.texWidth, glyph.y + glyph.texHeight]

			instanceData = [color.x, color.y, color.z, color.w, font.TextureIndex]

			self.__vertexData.extend(vertexData)
			self.__instanceData.extend(instanceData)
			
			self.__indexCount += 6
			RenderStats.QuadsCount += 1