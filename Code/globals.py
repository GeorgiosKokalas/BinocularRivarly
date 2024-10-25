import matlab.engine
from psychopy import core, visual, event

from enum import IntEnum

from PIL import Image
from Code.Classes.ParameterClass import ParameterClass

def create_globals():
    # initialize the MATLAB Engine in case it is needed
    global MATENG
    MATENG = matlab.engine.start_matlab()

    # Generate the parameters to be used
    global PARAMETERS
    PARAMETERS = ParameterClass()

    # Generate Clocks for use
    global REL_CLOCK, ABS_CLOCK
    REL_CLOCK = core.Clock()
    ABS_CLOCK = core.Clock()

    # Generate and ammend screen data
    global UI_WIN # Handler for the window
    UI_WIN = visual.Window(units='pix', checkTiming=True,  screen = PARAMETERS.screen['number']	,									
					fullscr=True, colorSpace='rgb255', color=PARAMETERS.screen['bgColor'])	
    PARAMETERS.screen.update({'pixDims': UI_WIN.size})	
    PARAMETERS.screen.update({'North': PARAMETERS.screen['pixDims'][0]/2,
                              'East' : PARAMETERS.screen['pixDims'][1]/2,
                              'South': -PARAMETERS.screen['pixDims'][0]/2,
                              'West' : -PARAMETERS.screen['pixDims'][1]/2,})
    
    # Generate all of the visual stimuli
    create_stimuli()


# Generate enums as constant variables representing specific actions
class ENUMS(IntEnum):
    Proceed = -13723
    Abort   = -29034
    

# Function that generates all the stimuli needed for the experiment
def create_stimuli():
    # Generate the photodiode
    global PHOTODIODE
    PHOTODIODE = visual.Rect(UI_WIN, pos=[PARAMETERS.screen['South']+75, PARAMETERS.screen['West']+75],
                             width=150, height=150, fillColor=[255,255,255], fillColorSpace='rgb255')
    
    # Create a generic text object
    global UI_TEXT
    UI_TEXT = visual.TextBox2(UI_WIN, text='', font=PARAMETERS.text['font']['default'], colorSpace='rgb255', fillColorSpace='rgb255',
							  pos = (0,0), alignment='center', letterHeight=PARAMETERS.text['size']['default'], padding=0, borderWidth=0,
                              color=PARAMETERS.text['color']['default'], fillColor=PARAMETERS.text['bgColor']['default'])
    
    # Generate shapes (Rectangle, Cycle and Line)
    global UI_RECT, UI_CYCLE, UI_LINE
    UI_RECT = visual.Rect(UI_WIN, colorSpace='rgb255', width=50, height=50, fillColor=(0,0,255), pos=(0,0), opacity = 1.0)
    UI_CYCLE = visual.Circle(UI_WIN, colorSpace='rgb255', radius=50, fillColor=(0,0,255), pos=(0,0))
    UI_LINE = visual.Line(UI_WIN, colorSpace='rgb255')

    # Generate a generic Image object
    global UI_IMG
    UI_IMG = visual.ImageStim(UI_WIN, image='Stimuli/Stimulus.png', opacity = 1)


    
    