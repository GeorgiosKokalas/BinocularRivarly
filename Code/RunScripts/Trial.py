from psychopy import core, event
import Code.globals as glb
from Code.Support.markEvent import markEvent
from Code.Support import GenericFunctions as gf, DrawFunctions as df

# GENERATE SCRIPT VARIABLES ONCE
# Radius for the selector ball
SEL_RADIUS = glb.PARAMETERS.screen['pixDims'][0]/64

# Position of the question
QUESTION_POS = (0,glb.PARAMETERS.text['size']['question']/2+SEL_RADIUS+10)

# Vividness question (VQ) variables
# Specify where the VQ line starts and ends
VIV_LINE_START = (-glb.PARAMETERS.screen['pixDims'][0]/4, 0)
VIV_LINE_END = (glb.PARAMETERS.screen['pixDims'][0]/4, 0)

# Specify where the selection notches for the VQ line will be
VIV_NOTCH_POS = [(-glb.PARAMETERS.screen['pixDims'][0]/4, 0),
                 (-glb.PARAMETERS.screen['pixDims'][0]/12, 0),
                 (glb.PARAMETERS.screen['pixDims'][0]/12, 0),
                 (glb.PARAMETERS.screen['pixDims'][0]/4, 0)
                ]

# Specify where the text for each notch in the VQ line will be
VIV_TEXT_POS = [(-glb.PARAMETERS.screen['pixDims'][0]/4, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10),
                (-glb.PARAMETERS.screen['pixDims'][0]/12, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10),
                (glb.PARAMETERS.screen['pixDims'][0]/12, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10),
                (glb.PARAMETERS.screen['pixDims'][0]/4, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10)
                ]

# Specify the VQ text options for selection
VIV_TEXT_CONT = ['Not at all', 'Very dimly', 'Mostly', 'Crystal Clear'] #'Somewhat', 'Mostly', 'Crystal Clear']


# Color reporting question (CRQ) variables
# Specify where the CRQ line starts and ends
COL_LINE_START = (-glb.PARAMETERS.screen['pixDims'][0]/8, 0)
COL_LINE_END = (glb.PARAMETERS.screen['pixDims'][0]/8, 0)

# Specify where the selection notches for the CRQ line will be
COL_NOTCH_POS = [(-glb.PARAMETERS.screen['pixDims'][0]/8, 0),
                  (0,0),
                  (glb.PARAMETERS.screen['pixDims'][0]/8, 0)
                  ]

# Specify where the text for each notch in the CRQ line will be
COL_TEXT_POS = [(-glb.PARAMETERS.screen['pixDims'][0]/8, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10),
                (0, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10),
                (glb.PARAMETERS.screen['pixDims'][0]/8, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10)
                ]

# Specify the CRQ text options for selection
COL_TEXT_CONT = ['Red', 'Mixed', 'Blue']

# The main script for each trial. Houses, and specifies the trial operations
def run(prompt:str, condition:str, trialIdx:int, blockIdx:int, Mock:int):
    # Generate the variable for holding the output
    output = {'vividRating': -1, 'colorSeen': -1, 'Abort': False}

    # Mark the start of the trial
    markEvent('trialBlockStart', trialIdx+1, blockIdx+1)

    glb.REL_CLOCK.reset() # DEBUG
    #Show the prompt
    markEvent('promptStart', trialIdx+1)
    df.draw_text(prompt)
    gf.winFlip()
    core.wait(glb.PARAMETERS.trial['promptDurS'])
    markEvent('promptEnd', trialIdx+1)
    print(f'PROMPT TIME {glb.REL_CLOCK.getTime()}')


    # Allow the user to imagine the cycle
    markEvent('imagineStart', trialIdx+1)
    match condition:
        case 'Dark': # Darkness condition
            df.draw_rect(FillColor=(0,0,0), Width=glb.PARAMETERS.screen['pixDims'][0],
                         Height=glb.PARAMETERS.screen['pixDims'][1], Pos=(0,0))
            gf.winFlip()
            core.wait(glb.PARAMETERS.trial['imagineDurS'])
        case 'Light': # Luminance condition
            for clr in range(15,256,10):
                df.draw_rect(FillColor=(clr,0, clr), Width=glb.PARAMETERS.screen['pixDims'][0],
                             Height=glb.PARAMETERS.screen['pixDims'][1], Pos=(0,0))
                gf.winFlip()
                core.wait(0.04)
            core.wait(glb.PARAMETERS.trial['imagineDurS']-2)
            for clr in range(255,10,-10):
                df.draw_rect(FillColor=(clr,0, clr), Width=glb.PARAMETERS.screen['pixDims'][0],
                             Height=glb.PARAMETERS.screen['pixDims'][1], Pos=(0,0))
                gf.winFlip()
                core.wait(0.04)
    markEvent('imagineEnd', trialIdx+1)


    # Ask the participant how vivid their imagined image was
    selPos = choice = 2
    markEvent('vividStart', trialIdx+1)
    while choice != glb.ENUMS.Proceed:
        choice = draw_vivid_Q(selPos)
        selPos = choice if choice>=0 else selPos
        if choice == glb.ENUMS.Abort:
            output['Abort']=True
            return output
    markEvent('vividEnd', trialIdx+1)
    output['vividRating'] = selPos          # Save the participant's choice
    
    
    # Show the stimulus to the participant
    glb.REL_CLOCK.reset() # DEBUG
    markEvent('stimulusStart', trialIdx+1)
    # df.draw_image('Stimuli/Stimulus.png', Opacity=0.6)
    if Mock == 0:
        df.draw_image('Stimuli/StimulusBLUE.png', Pos=(-glb.PARAMETERS.screen['pixDims'][0]/4, 0), Opacity=0.6)
        df.draw_image('Stimuli/StimulusRED.png', Pos=(glb.PARAMETERS.screen['pixDims'][0]/4, 0), Opacity=0.6)
    elif Mock == 1:
        df.draw_image('Stimuli/StimulusBLUEmock.png', Pos=(-glb.PARAMETERS.screen['pixDims'][0]/4, 0), Opacity=0.6)
    elif Mock == 2:
        df.draw_image('Stimuli/StimulusREDmock.png', Pos=(-glb.PARAMETERS.screen['pixDims'][0]/4, 0), Opacity=0.6)
        
    gf.winFlip()
    core.wait(glb.PARAMETERS.trial['stimDurS'])
    print(f'PROMPT TIME {glb.REL_CLOCK.getTime()}')
    markEvent('stimulusEnd', trialIdx+1)


    # Ask the user what color they saw
    selPos = choice = 1
    markEvent('colorStart', trialIdx+1)
    while choice != glb.ENUMS.Proceed:
        choice = draw_seen_Q(selPos)
        selPos = choice if choice>=0 else selPos
        if choice == glb.ENUMS.Abort:
            output['Abort']=True
            return output
    markEvent('colorEnd', trialIdx+1)
    output['colorSeen'] = COL_TEXT_CONT[selPos] # Save the participant's choice
    
    # Mark the end of the trial
    markEvent('trialBlockEnd', trialIdx+1, blockIdx+1)
    return output


# Function for drawing the Vividness Question (Separated to make code more readable)
def draw_vivid_Q(SelPos):
    # Draw the question and the selection line
    df.draw_text('How vividly did you imagine the picture?', Pos=QUESTION_POS, HozLength=1000)
    df.draw_line(Start=VIV_LINE_START, End=VIV_LINE_END)

    # Draw each selection notch and text option
    for notchIdx in range(len(VIV_NOTCH_POS)):
        df.draw_cycle(Pos=VIV_NOTCH_POS[notchIdx], Radius=5)
        df.draw_text(VIV_TEXT_CONT[notchIdx], Pos=VIV_TEXT_POS[notchIdx], Size=glb.PARAMETERS.text['size']['options'])

    # Draw the selection ball
    df.draw_cycle(Pos=VIV_NOTCH_POS[SelPos], Radius=SEL_RADIUS, FillColor=(255,0,0))

    # Present the image
    gf.winFlip()
    

    # Process the participant's choices
    pressedKey = event.waitKeys(keyList=['left', 'right', 'return', 'escape'])
    choice = ...
    match pressedKey[0]:
        case 'left':      # Move your selection to the left
            choice = max(0, SelPos-1)
        case 'right':     # Move your selection to the right
            choice = min(len(VIV_NOTCH_POS)-1, SelPos+1)
        case 'return':    # Store this option as your choice and move on
            choice = glb.ENUMS.Proceed
        case 'escape':    # Abort the experiment
            choice = glb.ENUMS.Abort
    return choice


# Function for drawing the Color Reporting Question (Separated to make code more readable)
def draw_seen_Q(SelPos):
    # Draw the question and the selection line
    df.draw_text('What colour was the cycle?', Pos=QUESTION_POS, HozLength=1000)
    df.draw_line(Start=COL_LINE_START, End=COL_LINE_END)

    # Draw each selection notch and text option
    for notchIdx in range(len(COL_NOTCH_POS)):
        df.draw_cycle(Pos=COL_NOTCH_POS[notchIdx], Radius=5)
        df.draw_text(COL_TEXT_CONT[notchIdx], Pos=COL_TEXT_POS[notchIdx], Size=glb.PARAMETERS.text['size']['options'])

    # Draw the selection ball
    df.draw_cycle(Pos=COL_NOTCH_POS[SelPos], Radius=SEL_RADIUS, FillColor=(255,0,0))

    # Present the image
    gf.winFlip()
    

    # Process the participant's choices
    pressedKey = event.waitKeys(keyList=['left', 'right', 'return', 'escape'])
    choice = ...
    match pressedKey[0]:
        case 'left':        # Move your selection to the left
            choice = max(0, SelPos-1)
        case 'right':       # Move your selection to the right
            choice = min(len(COL_NOTCH_POS)-1, SelPos+1)
        case 'return':      # Store this option as your choice and move on
            choice = glb.ENUMS.Proceed
        case 'escape':      # Abort the experiment
            choice = glb.ENUMS.Abort
    return choice
    
    
