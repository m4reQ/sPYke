from OpenGL import GL
import openal

#region Window
class WindowAPI:
	GLFW = "API::GLFW"
	Pygame = "API::Pygame"
	NoAPI = "API::None"

class WindowEvent:
	CloseEvent = 0
	ResizeEvent = 1
	MouseMoveEvent = 2
	MouseClickEvent = 3
	MouseScrollEvent = 4
	KeyEvent = 5
	IconifiedEvent = 6
	FileDropEvent = 7
	TextDropEvent = 8
#endregion

#region Audio
class AudioState:
	Initial = openal.AL_INITIAL
	Paused = openal.AL_PAUSED
	Playing = openal.AL_PLAYING
	Stopped = openal.AL_STOPPED
#endregion

#region Graphics
class CameraType:
	Orthographic = "Orthographic"
	Perspective = "Perspective"

class UniformTarget:
	ViewProjectionMatrix = "VIEW_PROJECTION_MATRIX"
	DeltaTime = "DELTA_TIME"
#endregion

#region OpenGL
class TextureType:
	Rgb = GL.GL_RGB
	Rgba = GL.GL_RGBA
	
class HintMode:
	Fastest = GL.GL_FASTEST
	Nicest = GL.GL_NICEST
	DontCare = GL.GL_DONT_CARE

class Hint:
	FogHint = GL.GL_FOG_HINT
	FragmentShaderDerivativeHint = GL.GL_FRAGMENT_SHADER_DERIVATIVE_HINT
	GenerateMipmapHint = GL.GL_GENERATE_MIPMAP_HINT
	LineSmoothHint = GL.GL_LINE_SMOOTH_HINT
	PerspectiveCorrectionHint = GL.GL_PERSPECTIVE_CORRECTION_HINT
	PointSmoothHint = GL.GL_POINT_SMOOTH_HINT
	PolygonSmoothHint = GL.GL_POLYGON_SMOOTH_HINT
	TextureCompressionHint = GL.GL_TEXTURE_COMPRESSION_HINT
	MultisampleFilterNvHint = 0x8534

class NvidiaIntegerName:
	GpuMemInfoTotalAvailable = 0x9048
	GpuMemInfoCurrentAvailable = 0x9049

class StringName:
	Vendor = GL.GL_VENDOR
	Renderer = GL.GL_RENDERER
	Version = GL.GL_VERSION
	ShadingLanguageVersion = GL.GL_SHADING_LANGUAGE_VERSION
	Extensions = GL.GL_EXTENSIONS

class ShaderType:
	VertexShader = GL.GL_VERTEX_SHADER
	FragmentShader = GL.GL_FRAGMENT_SHADER
	GeometryShader = GL.GL_GEOMETRY_SHADER
	ComputeShader = GL.GL_COMPUTE_SHADER
	TessEvaluationShader = GL.GL_TESS_EVALUATION_SHADER

class ErrorCode:
	NoError = GL.GL_NO_ERROR
	InvalidEnum = GL.GL_INVALID_ENUM
	InvalidValue = GL.GL_INVALID_VALUE
	InvalidOperation = GL.GL_INVALID_OPERATION
	InvalidFramebufferOperation = GL.GL_INVALID_FRAMEBUFFER_OPERATION
	OutOfMemory = GL.GL_OUT_OF_MEMORY

class PrimitiveMode:
	Triangles = GL.GL_TRIANGLES
	Points = GL.GL_POINTS
	LineStrip = GL.GL_LINE_STRIP
	LineLoop = GL.GL_LINE_LOOP
	Lines = GL.GL_LINES
	LineStripAdjacency = GL.GL_LINE_STRIP_ADJACENCY
	LinesAdjacency = GL.GL_LINES_ADJACENCY
	TriangleStrip = GL.GL_TRIANGLE_STRIP
	TriangleFan = GL.GL_TRIANGLE_FAN
	Triangles = GL.GL_TRIANGLES
	TriangleStripAdjacency = GL.GL_TRIANGLE_STRIP_ADJACENCY
	TrianglesAdjacency = GL.GL_TRIANGLES_ADJACENCY
	Patches = GL.GL_PATCHES

class BlendFactor:
	Zero = GL.GL_ZERO
	One = GL.GL_ONE
	SrcColor = GL.GL_SRC_COLOR
	OneMinusSrcColor = GL.GL_ONE_MINUS_SRC_COLOR
	DstColor = GL.GL_DST_COLOR
	OneMinusDstColor = GL.GL_ONE_MINUS_DST_COLOR
	SrcAlpha = GL.GL_SRC_ALPHA
	OneMinusSrcAlpha = GL.GL_ONE_MINUS_SRC_ALPHA
	DstAlpha = GL.GL_DST_ALPHA
	OneMinusDstAlpha = GL.GL_ONE_MINUS_DST_ALPHA
	ConstantColor = GL.GL_CONSTANT_COLOR
	OneMinusConstantColor = GL.GL_ONE_MINUS_CONSTANT_COLOR
	ConstantAlpha = GL.GL_CONSTANT_ALPHA
	OneMinusConstantAlpha = GL.GL_ONE_MINUS_CONSTANT_ALPHA
	SrcAlphaSaturate = GL.GL_SRC_ALPHA_SATURATE
	Src1Color = GL.GL_SRC1_COLOR
	OneMinusSrc1Color = GL.GL_ONE_MINUS_SRC1_COLOR
	Src1Alpha = GL.GL_SRC1_ALPHA
	OneMinusSrc1Alpha = GL.GL_ONE_MINUS_SRC1_ALPHA

class GLType:
	Float = GL.GL_FLOAT
	Double = GL.GL_DOUBLE
	Int = GL.GL_INT
	UnsignedInt = GL.GL_UNSIGNED_INT
	Byte = GL.GL_BYTE
	UnsignedByte = GL.GL_UNSIGNED_BYTE
	Short = GL.GL_SHORT
	UnsignedShort = GL.GL_UNSIGNED_SHORT

class VertexAttribType:
	Float = GL.GL_FLOAT
	Double = GL.GL_DOUBLE
	Int = GL.GL_INT
	Byte = GL.GL_BYTE
	Short = GL.GL_SHORT
	Fixed = GL.GL_FIXED
	HalfFloat = GL.GL_HALF_FLOAT

class ClearMask:
	ColorBufferBit = GL.GL_COLOR_BUFFER_BIT
	DepthBufferBit = GL.GL_DEPTH_BUFFER_BIT
	StencilBufferBit = GL.GL_STENCIL_BUFFER_BIT

class EnableCap:
	Blend = GL.GL_BLEND
	DepthTest = GL.GL_DEPTH_TEST
	CullFace = GL.GL_CULL_FACE
	MultiSample = GL.GL_MULTISAMPLE
	AlphaTest = GL.GL_ALPHA_TEST
	ScissorTest = GL.GL_SCISSOR_TEST

class AlphaOperator:
	Never = GL.GL_NEVER
	Always = GL.GL_ALWAYS
	Less = GL.GL_LESS
	Equal = GL.GL_EQUAL
	Greater = GL.GL_GREATER
	LessOrEqual = GL.GL_LEQUAL
	GreaterOrEqual = GL.GL_GEQUAL
	NotEqual = GL.GL_NOTEQUAL

class BufferUsageFlag:
	StaticDraw = GL.GL_STATIC_DRAW
	DynamicDraw = GL.GL_DYNAMIC_DRAW
	StreamDraw = GL.GL_STREAM_DRAW

#endregion