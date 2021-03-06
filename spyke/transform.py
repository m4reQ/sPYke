#region Import
import glm
from glm import vec2 as Vector2, vec3 as Vector3, mat4 as Matrix4, vec4 as Vector4
from functools import lru_cache
#endregion

IdentityMatrix4 = glm.mat4(1.0)

QuadVertices = [
	glm.vec4(0.0, 0.0, 0.0, 1.0),
	glm.vec4(0.0, 1.0, 0.0, 1.0),
	glm.vec4(1.0, 1.0, 0.0, 1.0),
	glm.vec4(1.0, 0.0, 0.0, 1.0)]

QuadVerticesFloat = [
	0.0, 0.0, 0.0,
	0.0, 1.0, 0.0,
	1.0, 1.0, 0.0,
	1.0, 0.0, 0.0]

#region Transform
def CreateTranslation(pos: tuple) -> glm.mat4:
    return glm.translate(glm.mat4(1.0), glm.vec3(pos))

def CreateScale(size: tuple) -> glm.mat4:
    return glm.scale(glm.mat4(1.0), glm.vec3(size))

def CreateRotationX(angle: float) -> glm.mat4:
	return glm.rotate(glm.mat4(1.0), angle, glm.vec3(1.0, 0.0, 0.0))

def CreateRotationY(angle: float) -> glm.mat4:
	return glm.rotate(glm.mat4(1.0), angle, glm.vec3(0.0, 1.0, 0.0))

def CreateRotationZ(angle: float) -> glm.mat4:
    return glm.rotate(glm.mat4(1.0), angle, glm.vec3(0.0, 0.0, 1.0))

def CreateTransform3D(pos: glm.vec3, size: glm.vec3, rot: glm.vec3) -> glm.mat4:
	transform = glm.translate(glm.mat4(1.0), pos)
	transform = glm.scale(transform, size)

	transform = glm.rotate(transform, rot.x, glm.vec3(1.0, 0.0, 0.0))
	transform = glm.rotate(transform, rot.y, glm.vec3(0.0, 1.0, 0.0))
	return glm.rotate(transform, rot.z, glm.vec3(0.0, 0.0, 1.0))