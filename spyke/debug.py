from .enums import StringName, ErrorCode, NvidiaStringName

from OpenGL.GL import glGetError, glGetString, glGetIntegerv, glGetStringi, GL_NUM_EXTENSIONS
import time

ENABLED = False
LOG_TIME = False
IS_NVIDIA = False

START_TIME = time.perf_counter()

class LogLevel:
	Info = "INFO"
	Warning = "WARNING"
	Error = "ERROR"

def Log(msg, logLevel: LogLevel):
    global ENABLED
    if ENABLED:
        if LOG_TIME:
            print(f"[{logLevel}][{(time.perf_counter() - START_TIME):.3F}s] {msg}")
        else:
            print(f"[{logLevel}] {msg}")

def GetGLError():
    err = glGetError()
    if err != ErrorCode.NoError:
        Log(err, LogLevel.Error)

def GetGLInfo():
    print("-----INFO-----")
    print(f"Renderer: {glGetString(StringName.Renderer).decode()}")
    print(f"Vendor: {glGetString(StringName.Vendor).decode()}")
    print(f"Version: {glGetString(StringName.Version).decode()}")
    print(f"Shading language version: {glGetString(StringName.ShadingLanguageVersion).decode()}")

    n = glGetIntegerv(GL_NUM_EXTENSIONS);

    exts = []
    for i in range(n):
        exts.append(glGetStringi(StringName.Extensions, i).decode())
    
    print(f"Extensions: {', '.join(exts)}")

    if IS_NVIDIA:
        print(f"Total memory available: {glGetString(NvidiaStringName.GpuMemInfoTotalAvailable)}kB")

class Timer:
    __Start = 0.0
    
    @staticmethod
    def Start():
        Timer.__Start = time.perf_counter()
    
    @staticmethod
    def Stop():
        return time.perf_counter() - Timer.__Start
    
    @staticmethod
    def GetCurrent():
        return time.perf_counter()