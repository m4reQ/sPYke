from ...utils import Static

from OpenGL import GL
import glm

class RendererSettings:
    """
    A class that stores set of rules about how renderer
    should work. To make them work any changes have to
    be made before renderer initialization. Be aware that
    in cetian cases renderer may not use settings provided
    here if it is necessary.
    """

    MaxQuadsCount = 300
    """
    Max quads count that can be renderer within one batch.
    """

    MaxTextures = 32
    """
    Max number of textures that can be used within one draw batch.
    """

    MaxFontTextures = 5
    """
    Max number of font textures that can be loaded.
    """

    MultisamplingEnabled = True
    """
    Indicates that renderer should use multisampling.
    This is only applied when using direct screen rendering.
    When using custom framebuffer multisampling should be set using appropriate
    framebuffer specifications.
    """

    ClearColor = glm.vec4(0.0)
    """
    Default color that will be used when clearing screen or framebuffer.
    """