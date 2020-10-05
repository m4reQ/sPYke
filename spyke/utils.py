from .enums import GLType, VertexAttribType
from .debug import Log, LogLevel

import ctypes
from OpenGL import GL
import gc
import glm

FLOAT_SIZE = ctypes.sizeof(ctypes.c_float)
INT_SIZE = ctypes.sizeof(ctypes.c_int)

GL_FLOAT_SIZE = 4
GL_INT_SIZE = 4

def GetGLTypeSize(type: GLType or VertexAttribType):
	if type == GL.GL_FLOAT:
		return 4
	elif type == GL.GL_UNSIGNED_BYTE or type == GL.GL_BYTE:
		return 1
	elif type == GL.GL_UNSIGNED_SHORT or type == GL.GL_SHORT:
		return 2
	elif type == GL.GL_UNSIGNED_INT or type == GL.GL_INT:
		return 4
	elif type == GL.GL_DOUBLE:
		return 8
	elif type == GL.GL_HALF_FLOAT:
		return 2
	elif type == GL.GL_FIXED:
		return 4
	else:
		raise RuntimeError(f"Invalid enum: {type}")

def GetPointer(value):
	return ctypes.c_void_p(value)

def GetQuadIndexData(count):
	data = []

	offset = 0
	i = 0
	while i < count:
		data.extend([
			0 + offset,
			1 + offset,
			2 + offset,
			2 + offset,
			3 + offset,
			0 + offset])
		
		offset += 4
		i += 6
	
	return data

def CollectGarbage():
	objCount = gc.get_count()[0]
	gc.collect()
	Log(f"Garbage collection freed {objCount - gc.get_count()[0]} objects.", LogLevel.Info)

def Mat4ToList(matrix: glm.mat4):
	matList = matrix.to_list()
	arr = []

	arr.extend(matList[0])
	arr.extend(matList[1])
	arr.extend(matList[2])
	arr.extend(matList[3])

	return arr

def KwargParse(kwargs: dict, list: list, usage: str, copy = True) -> dict:
	if not usage in ["n", "r", "l"]:
		raise RuntimeError(f"Invalid usage mode: {usage}")
	
	if copy:
		args = kwargs.copy()
	else:
		args = kwargs

	if usage == "r":
		for name in list:
			try:
				del args[name]
			except KeyError:
				pass
		return args
	elif usage == "l":
		_args = args.copy()
		for key in args.keys():
			if key not in list:
				del _args[key]
		return _args
	else:
		return args

def noexcept(func):
	def __wrapper(*args, **kwargs):
		r = None
		try:
			r = func(*args, **kwargs)
		except Exception:
			pass
		return r
	return __wrapper

class Abstract:
	def __new__(self):
		raise RuntimeError("Cannot instantiate abstract class.")

class Static:
	def __decorator(_cls):
		def inner(cls):
			for attr in cls.__dict__:
				_attr = getattr(cls, attr)
				if callable(_attr):
					setattr(cls, attr, staticmethod(_attr))
			return cls
		return inner 

	def __init_subclass__(cls, *args, **kwargs):
		return Static.__decorator(_cls = cls)
	
	def __new__(self, *args, **kwargs):
		raise RuntimeError("Cannot instantiate static class.")

class Enum:
	def __new__(self):
		raise RuntimeError("Cannot instantiate an enum.")

class ObjectManager(Static):
	Objects = []

	def AddObject(obj):
		ObjectManager.Objects.append(obj)

	def DeleteObject(obj):
		if obj not in ObjectManager.Objects:
			Log(f"Cannot delete object of type {type(obj).__name__}, object not present.", LogLevel.Error)
			return
		
		try:
			obj.Delete()
		except Exception as e:
			raise RuntimeError(f"Cannot delete object of type '{type(obj).__name__}', {e}")

		ObjectManager.Objects.remove(obj)

		Log(f"Object of type {type(obj).__name__} deleted.", LogLevel.Info)

	def DeleteAll():
		for obj in ObjectManager.Objects:
			try:
				obj.Delete()
			except Exception as e:
				raise RuntimeError(f"Cannot delete object of type '{type(obj).__name__}', {e}")

			Log(f"Object of type {type(obj).__name__} deleted.", LogLevel.Info)
		
		ObjectManager.Objects.clear()
		
		Log("All objects deleted succesfully.", LogLevel.Info)
