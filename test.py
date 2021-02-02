if __debug__:
	import spyke
	spyke.DEBUG_ENABLE = True
	spyke.DEBUG_LOG_TIME = True
	spyke.DEBUG_COLOR = True

	from spyke.debugging import Log, LogLevel
	Log("Debugging enabled.", LogLevel.Info)

from spyke.ecs.components import *
from spyke.ecs.processors import *

from spyke.imgui import ImGui
from spyke.window import GlfwWindow, WindowSpecs
from spyke.graphics import *
from spyke.enums import *
from spyke.managers import *
from spyke.utils import *
from spyke.transform import *
from spyke.input import *
#from spyke.sceneLoader import SaveScene

class UserProcessor(Processor):
	def __init__(self):
		self.delayer = Delayer(2.0)
		self.system = None
	
	def LateInit(self):
		self.system = self.scene.ComponentForEntity(EntityManager.GetEntity("Particles"), ParticleSystemComponent)

	def Process(self, *args, **kwargs):
		if not self.delayer.IsWaiting():
			self.system.EmitParticle()

class Window(GlfwWindow):
	def __init__(self, windowSpec):
		super().__init__(windowSpec)
	
	def OnLoad(self):
		InputHandler.Initialize(self)
		# LoadScene("tests/newScene.scn")

		# self.ent4 = EntityManager.CreateEntity("Particles")
		# self.particleSystem1 = ParticleSystemComponent(Vector2(0.5, 0.5), 3.0, 50)
		# self.particleSystem1.colorBegin = Color(1.0, 0.0, 1.0, 1.0)
		# self.particleSystem1.colorEnd = Color(0.0, 1.0, 1.0, 1.0)
		# self.particleSystem1.sizeBegin = Vector2(0.25, 0.25)
		# self.particleSystem1.sizeEnd = Vector2(0.1, 0.1)
		# self.particleSystem1.velocity = Vector2(0.1, 0.3)
		# self.particleSystem1.rotationVelocity = 0.0
		# self.particleSystem1.randomizeMovement = True
		# self.particleSystem1.fadeOut = True
		# self.particleSystem1.texHandle = "tests/test1.jpg"
		# SceneManager.Current.AddComponent(self.ent4, self.particleSystem1)

		#ImGui.Initialize(self)
		#ImGui.UpdateScene()

		Renderer.Initialize(self.width, self.height)

		TextureManager.LoadTexture("tests/test1.jpg")
		TextureManager.LoadTexture("tests/test2.png")

		FontManager.CreateFont("tests/ArialNative.fnt", "tests/ArialNative.png", "Arial")

		SceneManager.CreateScene("TEST", True)
		InitializeDefaultProcessors(SceneManager.Current)

		ent1 = SceneManager.Current.CreateEntity() #VIOLET first
		SceneManager.Current.AddComponent(ent1, TransformComponent(Vector3(0.0, 0.5, 0.3), Vector3(0.5, 0.5, 0.0), Vector3(0.0, 0.0, 90.0)))
		SceneManager.Current.AddComponent(ent1, SpriteComponent("", Vector2(1.0, 1.0), Color(1.0, 0.0, 1.0, 0.8)))

		ent2 = SceneManager.Current.CreateEntity() #YELLOW first
		SceneManager.Current.AddComponent(ent2, TransformComponent(Vector3(0.0, 0.1, 0.2), Vector3(0.2, 0.3, 0.0), Vector3(0.0)))
		SceneManager.Current.AddComponent(ent2, SpriteComponent("", Vector2(1.0, 1.0), Color(1.0, 1.0, 0.0, 0.7)))

		ent3 = SceneManager.Current.CreateEntity() #TEXTURE last
		SceneManager.Current.AddComponent(ent3, TransformComponent(Vector3(0.0, 0.0, 0.4), Vector3(0.7, 0.6, 0.0), Vector3(0.0)))
		SceneManager.Current.AddComponent(ent3, SpriteComponent("tests/test2.png", Vector2(1.0, 1.0), Color(1.0, 1.0, 1.0, 1.0)))

		ent4 = SceneManager.Current.CreateEntity()
		SceneManager.Current.AddComponent(ent4, TransformComponent(Vector3(0.5, 0.5, 0.1), Vector3(1.0), Vector3(0.0)))
		SceneManager.Current.AddComponent(ent4, TextComponent("TEST", 40, "Arial", Color(0.0, 1.0, 1.0, 0.7)))

		# SceneManager.Current.AddProcessor(UserProcessor())

		fbSpec = FramebufferSpec(self.width, self.height)
		fbSpec.attachmentsSpecs = [
			FramebufferAttachmentSpec(FramebufferTextureFormat.Rgba8),
			FramebufferAttachmentSpec(FramebufferTextureFormat.Rgba8),
			FramebufferAttachmentSpec(FramebufferTextureFormat.Depth)]

		self.framebuffer = Framebuffer(fbSpec)

		self.camera = OrthographicCamera(0.0, 1.0, 0.0, 1.0, zNear = -1.0, zFar = 10.0)

		self.posTEST = glm.translate(glm.mat4(1.0), glm.vec3(-1.0, -1.0, 0.0))
		self.posTEST = glm.scale(self.posTEST, glm.vec3(2.0, 2.0, 0.0))

		#SaveScene("test.scn")

		ImGui.Initialize()

		RequestGC()

	def OnFrame(self):
		SceneManager.Current.Process(window = self)
		Renderer.RenderScene(SceneManager.Current, self.camera.viewProjectionMatrix, self.framebuffer)
		Renderer.ClearScreen()
		Renderer.RenderFramebuffer(Vector3(0.0, 0.0, 0.0), Vector3(1.0, 1.0, 0.0), Vector3(0.0), self.framebuffer, passIdx=0)

if __name__ == "__main__":
	specs = WindowSpecs(512, 512, "TestWindow", 4, 5)
	specs.Multisample = True
	specs.Samples = 4
	specs.Vsync = False
	
	win = Window(specs)
	win.Run()