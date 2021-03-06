from .utils import Timer, StrToBool
from .debugging import Log, LogLevel
from .managers import TextureManager, FontManager, SceneManager, EntityManager
from .enums import TextureMagFilter
from .ecs.components import *
from .ecs import Scene
from .transform import Vector3, Vector2

from pydoc import locate
from copy import deepcopy

COMPONENTS_CLASSES_LOCATION = "spyke.ecs.components."

def SaveScene(filepath: str):
	f = open(filepath, "w+")
	
	f.write("#configuration\n")
	f.write(f"/c name {SceneManager.SceneName}\n")
	f.write(f"/c timed {SceneManager.Current.Timed}\n")

	f.write("#entities\n")
	for name in EntityManager.GetEntities():
		f.write(f"e {name}\n")

	f.write("#components\n")
	for ent in SceneManager.Current._entities:
		for comp in SceneManager.Current.ComponentsForEntity(ent):
			data = f"c {ent} {type(comp).ClassName} {comp.Serialize()}\n"
			f.write(data)

	f.close()

def __CreateComponent(_type, data):
	if _type == ColorComponent:
		return ColorComponent(float(data[0]), float(data[1]), float(data[2]), float(data[3]))
	elif _type == ScriptComponent:
		return ScriptComponent(data[0])
	elif _type == TransformComponent:
		convData = [float(x) for x in data]
		return TransformComponent(Vector3(convData[0], convData[1], convData[2]), Vector2(convData[3], convData[4]), convData[5])
	elif _type == LineComponent:
		convData = [float(x) for x in data]
		return LineComponent(Vector3(convData[0], convData[1], convData[2]), Vector3(convData[3], convData[4], convData[5]))
	elif _type == SpriteComponent:
		return SpriteComponent(data[0], (data[1], data[2]))
	elif _type == CameraComponent:
		if data[0] == "O":
			camType = CameraType.Orthographic
		elif data[0] == "P":
			camType = CameraType.Perspective

		return CameraComponent(camType, float(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]), float(data[6]))
	elif _type == TextComponent:
		return TextComponent(__RestoreSpaces(data[0]), int(float(data[1])), data[2])

def __DecodeLine(line: str, scene: Scene):
	if line.startswith("#"):
		return
	
	if line.startswith("r "):
		lineData = line.split(" ")
		_type = lineData[1]

		if _type == "arr":
			width = int(lineData[2])
			height = int(lineData[3])
			layers = int(lineData[4])
			levels = int(lineData[5])

			if lineData[6] == "L":
				magFilter = TextureMagFilter.Linear
			elif lineData[6] == "N":
				magFilter = TextureMagFilter.Nearest
			
			try:
				if lineData[7] == "BLANK":
					TextureManager.BlankArray = TextureManager.CreateTextureArray(width, height, layers, levels, magFilter, isBlank = True)
			except IndexError:
				TextureManager.CreateTextureArray(width, height, layers, levels, magFilter)

		elif _type == "tex":
			name = lineData[2]
			arrId = int(lineData[3])

			TextureManager.LoadTexture(name, arrId)
		elif _type == "fnt":
			fontFilepath = lineData[2]
			bitmapFilepath = lineData[3]
			name = lineData[4]

			FontManager.CreateFont(fontFilepath, bitmapFilepath, name)
	elif line.startswith("e "):
		name = line.split(" ")[1]
		EntityManager.CreateEntity(name)
	elif line.startswith("c "):
		lineData = line.split(" ")

		_type = locate("spyke.ecs.components." + lineData[1])
		ent = lineData[2]
		args = lineData[3:]

		scene.AddComponent(ent, __CreateComponent(_type, args))

def __LoadScene(filepath: str):
	Timer.Start()

	try:
		f = open(filepath, "r")
	except FileNotFoundError as e:
		raise RuntimeError(f"Cannot find scene file named '{e.filename}'.")

	timed = None
	name = None

	for line in f:
		line = line.replace("\n", "")
		if line.startswith("/c "):
			lineData = line.split(" ")
			if lineData[1] == "name":
				name = lineData[2]
			elif lineData[1] == "timed":
				timed = StrToBool(lineData[2])
		
		if timed != None and name != None:
			break
	
	if timed == None:
		timed = False

	SceneManager.CreateScene(str(name), timed)

	Log("Reloading managers...", LogLevel.Info)
	TextureManager.Reload()
	FontManager.Reload()
	EntityManager.Reload()

	for line in f:
		line = line.replace("\n", "")
		__DecodeLine(line, SceneManager.Current)
		
	f.close()
	Log(f"Scene from file '{filepath}' loaded in {Timer.Stop()} seconds.", LogLevel.Info)

def __SaveScene(scene: Scene, filepath: str):
	Timer.Start()

	timed = SceneManager.Current.Timed
	name = SceneManager.SceneName

	open(filepath, "w+").close()
	f = open(filepath, "a")

	f.write("#configuration\n")
	f.write(f"/c name {name}\n")
	f.write(f"/c timed {timed}\n")

	f.write("#resources\n")
	for array in TextureManager.GetTextureArrays():
		data = f"r arr {array.Width} {array.Height} {array.Layers} {array.Levels} {'L' if array.MagFilter == TextureMagFilter.Linear else 'N'}"
		if array.IsBlank:
			data += " BLANK"
		data += "\n"
		f.write(data)
	for (name, tex) in TextureManager.GetTextureNames().items():
		f.write(f"r tex {name} {tex.TexarrayID}\n")
	for (name, fnt) in FontManager.GetFonts().items():
		f.write(f"r fnt {fnt.FontFilepath} {fnt.BitmapFilepath} {name}\n")

	f.write("#entities\n")
	for name in EntityManager.GetEntities():
		f.write(f"e {name}\n")
	
	f.write("#components\n")
	for ent in SceneManager.Current._entities:
		for comp in SceneManager.Current.ComponentsForEntity(ent):
			_type = type(comp)
			strType = str(_type).replace("<class 'spyke.ecs.components.", "").replace("'>", "")
			line = f"c {strType} {ent} "
			
			if _type == ColorComponent:
				line += f"{comp.R} {comp.G} {comp.B} {comp.A}"
			elif _type == ScriptComponent:
				line += f"{comp.Filepath}"
			elif _type == TransformComponent:
				line += f"{comp.Position.x} {comp.Position.y} {comp.Position.z} {comp.Size.x} {comp.Size.y} {comp.Rotation}"
			elif _type == LineComponent:
				line += f"{comp.StartPos.x} {comp.StartPos.y} {comp.StartPos.z} {comp.EndPos.x} {comp.EndPos.y} {comp.EndPos.z}"
			elif _type == TextComponent:
				line += f"{__SecureSpaces(comp.Text)} {comp.Size} {comp.FontName}"
			elif _type == SpriteComponent:
				line += f"{comp.TextureName} {comp.TilingFactor[0]} {comp.TilingFactor[1]}"
			
			f.write(line + "\n")

	f.close()

	Log(f"Scene saved in {Timer.Stop()} seconds.", LogLevel.Info)