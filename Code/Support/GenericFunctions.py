import Code.globals as glb
from psychopy import core


LAST_FLIP = core.Clock()
REFRESH_TIME = 1/glb.PARAMETERS.screen['framerate']
FIRST_FLIP = core.Clock()

def winFlip(Buffer = True):
    if REFRESH_TIME > 0:
        core.wait(max(0, REFRESH_TIME - LAST_FLIP.getTime()))
    glb.UI_WIN.flip(Buffer) 
    LAST_FLIP.reset()

