import ctypes
from OpenGL import GL
import gc
import threading
import pickle

__GL_TYPE_SIZES = {
	GL.GL_DOUBLE: 8,
	GL.GL_FIXED: 4,
	GL.GL_FLOAT: 4,
	GL.GL_UNSIGNED_INT: 4,
	GL.GL_INT: 4,
	GL.GL_UNSIGNED_SHORT: 2,
	GL.GL_SHORT: 2,
	GL.GL_HALF_FLOAT: 2,
	GL.GL_UNSIGNED_BYTE: 1,
	GL.GL_BYTE: 1}

def __ThreadedGC():
	__GC_FLAG.wait()
	gc.collect()
	__GC_FLAG.clear()

__GC_FLAG = threading.Event()
__GC_THREAD = threading.Thread(target = __ThreadedGC, name = "spyke.gc")
__GC_THREAD.start()

def RequestGC():
	__GC_FLAG.set()

def GetGLTypeSize(_type: int) -> int:
	try:
		return __GL_TYPE_SIZES[_type]
	except KeyError:
		raise RuntimeError(f"Invalid enum: {_type}")

def GetPointer(value: int) -> ctypes.c_void_p:
	return ctypes.c_void_p(value)

class Serializable(object):
	ClassName = "Serializable"

	@classmethod
	def Deserialize(cls, data: str) -> object:
		pass

	@classmethod
	def DeserializeBin(cls, data: bytes) -> object:
		return pickle.loads(data)
	
	def Serialize(self) -> str:
		pass

	def SerializeBin(self) -> bytes:
		return pickle.dumps(self)