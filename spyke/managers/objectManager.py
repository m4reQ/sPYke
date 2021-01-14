from ..utils import Static
from ..debug import Log, LogLevel

from OpenGL import GL
import gc

class ObjectManager(Static):
	__VertexArrays = []
	__Buffers = []
	__Textures = []
	__Shaders = []
	__Framebuffers = []
	__Renderbuffers = []

	def AddObject(obj):
		name = type(obj).__name__

		if name == "VertexArray":
			ObjectManager.__VertexArrays.append(obj.ID)
		elif name == "Framebuffer":
			ObjectManager.__Framebuffers.append(obj.ID)
			ObjectManager.__Textures.append(obj.ColorAttachment)
			if obj.Spec.HasDepthAttachment:
				ObjectManager.__Renderbuffers.append(obj.DepthRenderbuffer)
		elif "buffer" in name.lower() and name != "Framebuffer":
			ObjectManager.__Buffers.append(obj.ID)
		elif name == "Shader":
			ObjectManager.__Shaders.append(obj.ID)
		elif "texture" in name.lower():
			ObjectManager.__Textures.append(obj.ID)
		else:
			Log(f"Invalid object of type '{name}'.", LogLevel.Warning)
	
	def DeleteAll():
		for _ in ObjectManager.__Buffers:
			GL.glDeleteBuffers(len(ObjectManager.__Buffers), ObjectManager.__Buffers)
			
		Log(f"{len(ObjectManager.__Buffers)} buffers deleted succesfully.", LogLevel.Info)

		for _ in ObjectManager.__Framebuffers:
			GL.glDeleteFramebuffers(len(ObjectManager.__Framebuffers), ObjectManager.__Framebuffers)
			
		Log(f"{len(ObjectManager.__Framebuffers)} frame buffers deleted succesfully.", LogLevel.Info)
	
		for _ in ObjectManager.__Renderbuffers:
			GL.glDeleteRenderbuffers(len(ObjectManager.__Renderbuffers), ObjectManager.__Renderbuffers)
			
		Log(f"{len(ObjectManager.__Framebuffers)} render buffers deleted succesfully.", LogLevel.Info)
		
		for _ in ObjectManager.__Shaders:
			GL.glDeleteBuffers(len(ObjectManager.__Shaders), ObjectManager.__Shaders)
		
		Log(f"{len(ObjectManager.__Shaders)} shader programs deleted succesfully.", LogLevel.Info)

		for _ in ObjectManager.__Textures:
			GL.glDeleteTextures(len(ObjectManager.__Textures), ObjectManager.__Textures)
		
		Log(f"{len(ObjectManager.__Textures)} textures deleted succesfully.", LogLevel.Info)
		
		for _ in ObjectManager.__VertexArrays:
			GL.glDeleteVertexArrays(len(ObjectManager.__VertexArrays), ObjectManager.__VertexArrays)
		
		Log(f"{len(ObjectManager.__VertexArrays)} vertex arrays deleted succesfully.", LogLevel.Info)

		ObjectManager.__Buffers.clear()
		ObjectManager.__Framebuffers.clear()
		ObjectManager.__Renderbuffers.clear()
		ObjectManager.__Shaders.clear()
		ObjectManager.__Textures.clear()
		ObjectManager.__VertexArrays.clear()

		gc.collect()