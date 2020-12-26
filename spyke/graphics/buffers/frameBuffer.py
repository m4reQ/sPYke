from ...debug import Log, LogLevel
from ...utils import ObjectManager

from OpenGL import GL
import glm

class FramebufferSpecs(object):
	def __init__(self, width: int, height: int):
		self.Width = width
		self.Height = height
		self.Samples = 1
		self.HasDepthAttachment = False
		self.Color = glm.vec4(1.0, 1.0, 1.0, 1.0)
		self.Filtering = GL.GL_LINEAR

class Framebuffer(object):
	__InternalFormat = GL.GL_RGBA8
	__PixelFormat = GL.GL_RGBA
	__PixelType = GL.GL_UNSIGNED_BYTE

	def __init__(self, specification: FramebufferSpecs):
		self.Spec = specification

		self.__Invalidate(False)

		ObjectManager.AddObject(self)

	def __Invalidate(self, resizing: bool) -> None:
		if resizing:
			self.Delete()
		
		self.__colorAttachmentId = GL.glGenTextures(1)

		if self.Spec.Samples > 1:
			GL.glBindTexture(GL.GL_TEXTURE_2D_MULTISAMPLE, self.__colorAttachmentId)
			GL.glTexImage2DMultisample(GL.GL_TEXTURE_2D_MULTISAMPLE, self.Spec.Samples, Framebuffer.__InternalFormat, self.Spec.Width, self.Spec.Height, False)
		else:
			GL.glBindTexture(GL.GL_TEXTURE_2D, self.__colorAttachmentId)
			GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, Framebuffer.__InternalFormat, self.Spec.Width, self.Spec.Height, 0, Framebuffer.__PixelFormat, Framebuffer.__PixelType, None)
			GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, self.Spec.Filtering)
			GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
		
		self.__id = GL.glGenFramebuffers(1)
		GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.__id)
		GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D_MULTISAMPLE if self.Spec.Samples > 1 else GL.GL_TEXTURE_2D, self.__colorAttachmentId, 0)

		if self.Spec.HasDepthAttachment:
			self.__depthAttachmentId = GL.glGenTextures(1)
			GL.glBindTexture(GL.GL_TEXTURE_2D, self.__depthAttachmentId)
			GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_DEPTH24_STENCIL8, self.Spec.Width, self.Spec.Height, 0, GL.GL_DEPTH_STENCIL, GL.GL_UNSIGNED_INT_24_8, None)

			GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
			GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
			GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
			GL.glTexParameter(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)

			GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_TEXTURE_2D, self.__depthAttachmentId, 0)
		
		GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
		
		if not resizing:
			err = GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER)
			if err != GL.GL_FRAMEBUFFER_COMPLETE:
				raise RuntimeError(f"Framebuffer (id: {self.__id} incomplete: {err}.")
			else:
				Log(f"Framebuffer (id: {self.__id}) created succesfully", LogLevel.Info)
	
	def Resize(self, width: int, height: int) -> None:
		self.Spec.Width = width
		self.Spec.Height = height

		self.__Invalidate(True)

	def Bind(self) -> None:
		GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.__id)
	
	def Unbind(self) -> None:
		GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

	def Delete(self) -> None:
		GL.glDeleteFramebuffers(1, [self.__id])
		GL.glDeleteTextures([self.__colorAttachmentId])
		if self.Spec.HasDepthAttachment:
			GL.glDeleteTextures([self.__depthAttachmentId])
	
	@staticmethod
	def UnbindAll() -> None:
		GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)