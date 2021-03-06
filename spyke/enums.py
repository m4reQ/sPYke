from OpenGL import GL
import openal
import glfw

#region Audio
class AudioState:
	Initial = 						openal.AL_INITIAL
	Paused = 						openal.AL_PAUSED
	Playing = 						openal.AL_PLAYING
	Stopped = 						openal.AL_STOPPED
#endregion

#region Graphics
class Vendor:
	Nvidia = 						"NVIDIA"
	Intel = 						"INTEL"
	Amd = 							"AMD"
	Unknown = 						"UNKNOWN"

class CameraType:
	Orthographic, Perspective = range(2)
#endregion

#region OpenGL
class TextureMagFilter:
	Linear = 						GL.GL_LINEAR
	Nearest = 						GL.GL_NEAREST
	
class TextureType:
	Rgb = 							GL.GL_RGB
	Rgba = 							GL.GL_RGBA
	
class HintMode:
	Fastest = 						GL.GL_FASTEST
	Nicest = 						GL.GL_NICEST
	DontCare = 						GL.GL_DONT_CARE

class Hint:
	FogHint = 						GL.GL_FOG_HINT
	FragmentShaderDerivativeHint = 	GL.GL_FRAGMENT_SHADER_DERIVATIVE_HINT
	GenerateMipmapHint = 			GL.GL_GENERATE_MIPMAP_HINT
	LineSmoothHint = 				GL.GL_LINE_SMOOTH_HINT
	PerspectiveCorrectionHint = 	GL.GL_PERSPECTIVE_CORRECTION_HINT
	PointSmoothHint = 				GL.GL_POINT_SMOOTH_HINT
	PolygonSmoothHint = 			GL.GL_POLYGON_SMOOTH_HINT
	TextureCompressionHint = 		GL.GL_TEXTURE_COMPRESSION_HINT
	MultisampleFilterNvHint = 		0x8534

class NvidiaIntegerName:
	GpuMemInfoTotalAvailable = 		0x9048
	GpuMemInfoCurrentAvailable = 	0x9049

class StringName:
	Vendor = 						GL.GL_VENDOR
	Renderer = 						GL.GL_RENDERER
	Version = 						GL.GL_VERSION
	ShadingLanguageVersion = 		GL.GL_SHADING_LANGUAGE_VERSION
	Extensions = 					GL.GL_EXTENSIONS

class ShaderType:
	VertexShader = 					GL.GL_VERTEX_SHADER
	FragmentShader = 				GL.GL_FRAGMENT_SHADER
	GeometryShader = 				GL.GL_GEOMETRY_SHADER
	ComputeShader = 				GL.GL_COMPUTE_SHADER
	TessEvaluationShader = 			GL.GL_TESS_EVALUATION_SHADER

class ErrorCode:
	NoError = 						GL.GL_NO_ERROR
	InvalidEnum = 					GL.GL_INVALID_ENUM
	InvalidValue = 					GL.GL_INVALID_VALUE
	InvalidOperation = 				GL.GL_INVALID_OPERATION
	InvalidFramebufferOperation = 	GL.GL_INVALID_FRAMEBUFFER_OPERATION
	OutOfMemory = 					GL.GL_OUT_OF_MEMORY

class PrimitiveMode:
	Triangles = 					GL.GL_TRIANGLES
	Points = 						GL.GL_POINTS
	LineStrip = 					GL.GL_LINE_STRIP
	LineLoop = 						GL.GL_LINE_LOOP
	Lines = 						GL.GL_LINES
	LineStripAdjacency = 			GL.GL_LINE_STRIP_ADJACENCY
	LinesAdjacency = 				GL.GL_LINES_ADJACENCY
	TriangleStrip = 				GL.GL_TRIANGLE_STRIP
	TriangleFan = 					GL.GL_TRIANGLE_FAN
	Triangles = 					GL.GL_TRIANGLES
	TriangleStripAdjacency = 		GL.GL_TRIANGLE_STRIP_ADJACENCY
	TrianglesAdjacency = 			GL.GL_TRIANGLES_ADJACENCY
	Patches = 						GL.GL_PATCHES

class BlendFactor:
	Zero = 							GL.GL_ZERO
	One = 							GL.GL_ONE
	SrcColor = 						GL.GL_SRC_COLOR
	OneMinusSrcColor = 				GL.GL_ONE_MINUS_SRC_COLOR
	DstColor = 						GL.GL_DST_COLOR
	OneMinusDstColor = 				GL.GL_ONE_MINUS_DST_COLOR
	SrcAlpha = 						GL.GL_SRC_ALPHA
	OneMinusSrcAlpha = 				GL.GL_ONE_MINUS_SRC_ALPHA
	DstAlpha = 						GL.GL_DST_ALPHA
	OneMinusDstAlpha = 				GL.GL_ONE_MINUS_DST_ALPHA
	ConstantColor = 				GL.GL_CONSTANT_COLOR
	OneMinusConstantColor = 		GL.GL_ONE_MINUS_CONSTANT_COLOR
	ConstantAlpha = 				GL.GL_CONSTANT_ALPHA
	OneMinusConstantAlpha = 		GL.GL_ONE_MINUS_CONSTANT_ALPHA
	SrcAlphaSaturate = 				GL.GL_SRC_ALPHA_SATURATE
	Src1Color = 					GL.GL_SRC1_COLOR
	OneMinusSrc1Color = 			GL.GL_ONE_MINUS_SRC1_COLOR
	Src1Alpha = 					GL.GL_SRC1_ALPHA
	OneMinusSrc1Alpha = 			GL.GL_ONE_MINUS_SRC1_ALPHA

class GLType:
	Float = 						GL.GL_FLOAT
	Double = 						GL.GL_DOUBLE
	Int = 							GL.GL_INT
	UnsignedInt = 					GL.GL_UNSIGNED_INT
	Byte = 							GL.GL_BYTE
	UnsignedByte = 					GL.GL_UNSIGNED_BYTE
	Short = 						GL.GL_SHORT
	UnsignedShort = 				GL.GL_UNSIGNED_SHORT

class VertexAttribType:
	Float = 						GL.GL_FLOAT
	Double = 						GL.GL_DOUBLE
	Int = 							GL.GL_INT
	Byte = 							GL.GL_BYTE
	Short = 						GL.GL_SHORT
	Fixed = 						GL.GL_FIXED
	HalfFloat = 					GL.GL_HALF_FLOAT

class ClearMask:
	ColorBufferBit = 				GL.GL_COLOR_BUFFER_BIT
	DepthBufferBit = 				GL.GL_DEPTH_BUFFER_BIT
	StencilBufferBit = 				GL.GL_STENCIL_BUFFER_BIT

class EnableCap:
	Blend = 						GL.GL_BLEND
	DepthTest = 					GL.GL_DEPTH_TEST
	CullFace = 						GL.GL_CULL_FACE
	MultiSample = 					GL.GL_MULTISAMPLE
	AlphaTest = 					GL.GL_ALPHA_TEST
	ScissorTest = 					GL.GL_SCISSOR_TEST

class AlphaOperator:
	Never = 						GL.GL_NEVER
	Always = 						GL.GL_ALWAYS
	Less = 							GL.GL_LESS
	Equal = 						GL.GL_EQUAL
	Greater = 						GL.GL_GREATER
	LessOrEqual = 					GL.GL_LEQUAL
	GreaterOrEqual = 				GL.GL_GEQUAL
	NotEqual = 						GL.GL_NOTEQUAL

class BufferUsageFlag:
	StaticDraw = 					GL.GL_STATIC_DRAW
	DynamicDraw = 					GL.GL_DYNAMIC_DRAW
	StreamDraw = 					GL.GL_STREAM_DRAW
#endregion

#region Input
class MouseButtons:
	Left = 							glfw.MOUSE_BUTTON_LEFT
	Middle = 						glfw.MOUSE_BUTTON_MIDDLE
	Right = 						glfw.MOUSE_BUTTON_RIGHT

class KeyMods:
	ModControl = 					glfw.MOD_CONTROL
	ModShift = 						glfw.MOD_SHIFT
	ModAlt = 						glfw.MOD_ALT
	ModSuper = 						glfw.MOD_SUPER
	ModCapsLock = 					glfw.MOD_CAPS_LOCK
	ModNumLock = 					glfw.MOD_NUM_LOCK

class Keys:
	KeyInvalid = 					glfw.KEY_UNKNOWN

	#special
	KeySpace = 						glfw.KEY_SPACE
	KeyApostrophe = 				glfw.KEY_APOSTROPHE
	KeyComma = 						glfw.KEY_COMMA
	KeyMinus = 						glfw.KEY_MINUS
	KeyPeriod = 					glfw.KEY_PERIOD
	KeySlash = 						glfw.KEY_SLASH
	KeySemicolon = 					glfw.KEY_SEMICOLON
	KeyLeftBracket = 				glfw.KEY_LEFT_BRACKET
	KeyRightBracket = 				glfw.KEY_RIGHT_BRACKET
	KeyBackslash = 					glfw.KEY_BACKSLASH
	KeyGrave = 						glfw.KEY_GRAVE_ACCENT
	KeyEscape = 					glfw.KEY_ESCAPE
	KeyEnter = 						glfw.KEY_ENTER
	KeyTab = 						glfw.KEY_TAB
	KeyBackspace = 					glfw.KEY_BACKSPACE
	KeyInsert = 					glfw.KEY_INSERT
	KeyDelete = 					glfw.KEY_DELETE
	KeyPageUp = 					glfw.KEY_PAGE_UP
	KeyPageDown = 					glfw.KEY_PAGE_DOWN
	KeyHome = 						glfw.KEY_HOME
	KeyEnd = 						glfw.KEY_END
	KeyCapsLock = 					glfw.KEY_CAPS_LOCK
	KeyScrollLock = 				glfw.KEY_SCROLL_LOCK
	KeyNumLock = 					glfw.KEY_NUM_LOCK
	KeyPrintScreen = 				glfw.KEY_PRINT_SCREEN
	KeyPause = 						glfw.KEY_PAUSE
	KeyMenu = 						glfw.KEY_MENU

	#functional
	KeyF1 = 						glfw.KEY_F1
	KeyF2 = 						glfw.KEY_F2
	KeyF3 = 						glfw.KEY_F3
	KeyF4 = 						glfw.KEY_F4
	KeyF5 = 						glfw.KEY_F5
	KeyF6 = 						glfw.KEY_F6
	KeyF7 = 						glfw.KEY_F7
	KeyF8 = 						glfw.KEY_F8
	KeyF9 = 						glfw.KEY_F9
	KeyF10 = 						glfw.KEY_F10
	KeyF11 = 						glfw.KEY_F11
	KeyF12 = 						glfw.KEY_F12

	#modifiers
	KeyLeftShift = 					glfw.KEY_LEFT_SHIFT
	KeyRightShift = 				glfw.KEY_RIGHT_SHIFT
	KeyLeftControl = 				glfw.KEY_LEFT_CONTROL
	KeyRightControl = 				glfw.KEY_RIGHT_CONTROL
	KeyLeftAlt = 					glfw.KEY_LEFT_ALT
	KeyRightAlt = 					glfw.KEY_RIGHT_ALT
	KeyLeftSuper = 					glfw.KEY_LEFT_SUPER
	KeyRightSuper = 				glfw.KEY_RIGHT_SUPER

	#arrows
	KeyRight = 						glfw.KEY_RIGHT
	KeyLeft = 						glfw.KEY_LEFT
	KeyUp = 						glfw.KEY_UP
	KeyDown = 						glfw.KEY_DOWN
	
	#numerical
	Key0 = 							glfw.KEY_0
	Key1 = 							glfw.KEY_1
	Key2 = 							glfw.KEY_2
	Key3 = 							glfw.KEY_3
	Key4 = 							glfw.KEY_4
	Key5 = 							glfw.KEY_5
	Key6 = 							glfw.KEY_6
	Key7 = 							glfw.KEY_7
	Key8 = 							glfw.KEY_8
	Key9 = 							glfw.KEY_9
	
	#alphabetical
	KeyA = 							glfw.KEY_A
	KeyB = 							glfw.KEY_B
	KeyC = 							glfw.KEY_C
	KeyD = 							glfw.KEY_D
	KeyE = 							glfw.KEY_E
	KeyF = 							glfw.KEY_F
	KeyG = 							glfw.KEY_G
	KeyH = 							glfw.KEY_H
	KeyI = 							glfw.KEY_I
	KeyJ = 							glfw.KEY_J
	KeyK = 							glfw.KEY_K
	KeyL = 							glfw.KEY_L
	KeyM = 							glfw.KEY_M
	KeyN = 							glfw.KEY_N
	KeyO = 							glfw.KEY_O
	KeyP = 							glfw.KEY_P
	KeyQ = 							glfw.KEY_Q
	KeyR = 							glfw.KEY_R
	KeyS = 							glfw.KEY_S
	KeyT = 							glfw.KEY_T
	KeyU = 							glfw.KEY_U
	KeyV = 							glfw.KEY_V
	KeyW = 							glfw.KEY_W
	KeyX = 							glfw.KEY_X
	KeyY = 							glfw.KEY_Y
	KeyZ = 							glfw.KEY_Z
#endregion