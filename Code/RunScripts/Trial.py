from psychopy import core, event
import Code.globals as glb
from Code.Support.markEvent import markEvent
from Code.Support import GenericFunctions as gf, DrawFunctions as df


SEL_RADIUS = glb.PARAMETERS.screen['pixDims'][0]/64

QUESTION_POS = (0,glb.PARAMETERS.text['size']['question']/2+SEL_RADIUS+10)

VIV_LINE_START = (-glb.PARAMETERS.screen['pixDims'][0]/4, 0)
VIV_LINE_END = (glb.PARAMETERS.screen['pixDims'][0]/4, 0)

VIV_NOTCH_POS = [(-glb.PARAMETERS.screen['pixDims'][0]/4, 0),
                 (-glb.PARAMETERS.screen['pixDims'][0]/12, 0),
                 #(0,0),
                 (glb.PARAMETERS.screen['pixDims'][0]/12, 0),
                 (glb.PARAMETERS.screen['pixDims'][0]/4, 0)
                 ]

VIV_TEXT_POS = [(-glb.PARAMETERS.screen['pixDims'][0]/4, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10),
                (-glb.PARAMETERS.screen['pixDims'][0]/12, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10),
                #(0, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10),
                (glb.PARAMETERS.screen['pixDims'][0]/12, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10),
                (glb.PARAMETERS.screen['pixDims'][0]/4, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10)
                ]

VIV_TEXT_CONT = ['Not at all', 'Very dimly', 'Mostly', 'Crystal Clear'] #'Somewhat', 'Mostly', 'Crystal Clear']

COL_LINE_START = (-glb.PARAMETERS.screen['pixDims'][0]/8, 0)
COL_LINE_END = (glb.PARAMETERS.screen['pixDims'][0]/8, 0)

COL_NOTCH_POS = [(-glb.PARAMETERS.screen['pixDims'][0]/8, 0),
                  (0,0),
                  (glb.PARAMETERS.screen['pixDims'][0]/8, 0)
                  ]

COL_TEXT_POS = [(-glb.PARAMETERS.screen['pixDims'][0]/8, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10),
                (0, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10),
                (glb.PARAMETERS.screen['pixDims'][0]/8, -SEL_RADIUS-glb.PARAMETERS.text['size']['options']/2-10)
                ]

COL_TEXT_CONT = ['Red', 'Mixed', 'Blue']


def run(prompt:str, condition:str, trialIdx:int, blockIdx:int):
    output = {'vividRating': -1, 'colorSeen': -1, 'Abort': False}
    markEvent('trialBlockStart', trialIdx+1, blockIdx+1)
    markEvent('promptStart', trialIdx+1)
    df.draw_text(prompt)
    gf.winFlip()
    core.wait(glb.PARAMETERS.trial['promptDurS'])
    markEvent('promptEnd', trialIdx+1)

    markEvent('imagineStart', trialIdx+1)
    match condition:
        case 'Dark':
            df.draw_rect(FillColor=(0,0,0), Width=glb.PARAMETERS.screen['pixDims'][0],
                         Height=glb.PARAMETERS.screen['pixDims'][1], Pos=(0,0))
            gf.winFlip()
            core.wait(glb.PARAMETERS.trial['imagineDurS'])
        case 'Light':
            for clr in range(15,256,10):
                df.draw_rect(FillColor=(clr,clr,0), Width=glb.PARAMETERS.screen['pixDims'][0],
                             Height=glb.PARAMETERS.screen['pixDims'][1], Pos=(0,0))
                gf.winFlip()
                core.wait(0.04)
            core.wait(glb.PARAMETERS.trial['imagineDurS']-2)
            for clr in range(255,10,-10):
                df.draw_rect(FillColor=(clr,clr,0), Width=glb.PARAMETERS.screen['pixDims'][0],
                             Height=glb.PARAMETERS.screen['pixDims'][1], Pos=(0,0))
                gf.winFlip()
                core.wait(0.04)
    markEvent('imagineEnd', trialIdx+1)

    selPos = choice = 2
    markEvent('vividStart', trialIdx+1)
    while choice != glb.ENUMS.Proceed:
        choice = draw_vivid_Q(selPos)
        selPos = choice if choice>=0 else selPos
        if choice == glb.ENUMS.Abort:
            output['Abort']=True
            return output
    markEvent('vividEnd', trialIdx+1)
    output['vividRating'] = selPos
    
    

    markEvent('stimulusStart', trialIdx+1)
    glb.UI_STIM.draw()
    gf.winFlip()
    core.wait(glb.PARAMETERS.trial['stimDurS'])
    markEvent('stimulusEnd', trialIdx+1)

    selPos = choice = 1
    markEvent('colorStart', trialIdx+1)
    while choice != glb.ENUMS.Proceed:
        choice = draw_seen_Q(selPos)
        selPos = choice if choice>=0 else selPos
        if choice == glb.ENUMS.Abort:
            output['Abort']=True
            return output
    markEvent('colorEnd', trialIdx+1)

    output['colorSeen'] = COL_TEXT_CONT[selPos]
    
    markEvent('trialBlockEnd', trialIdx+1, blockIdx+1)
    return output


def draw_vivid_Q(SelPos):
    df.draw_text('How vividly did you imagine the picture?', Pos=QUESTION_POS, HozLength=1000)
    df.draw_line(Start=VIV_LINE_START, End=VIV_LINE_END)

    for notchIdx in range(len(VIV_NOTCH_POS)):
        df.draw_cycle(Pos=VIV_NOTCH_POS[notchIdx], Radius=5)
        df.draw_text(VIV_TEXT_CONT[notchIdx], Pos=VIV_TEXT_POS[notchIdx], Size=glb.PARAMETERS.text['size']['options'])

    df.draw_cycle(Pos=VIV_NOTCH_POS[SelPos], Radius=SEL_RADIUS, FillColor=(255,0,0))

    gf.winFlip()
    
    pressedKey = event.waitKeys(keyList=['left', 'right', 'return', 'escape'])
    choice = ...
    match pressedKey[0]:
        case 'left':
            choice = max(0, SelPos-1)
        case 'right':
            choice = min(len(VIV_NOTCH_POS)-1, SelPos+1)
        case 'return':
            choice = glb.ENUMS.Proceed
        case 'escape':
            choice = glb.ENUMS.Abort
    return choice


def draw_seen_Q(SelPos):
    df.draw_text('What colour was the cycle?', Pos=QUESTION_POS, HozLength=1000)
    df.draw_line(Start=COL_LINE_START, End=COL_LINE_END)

    for notchIdx in range(len(COL_NOTCH_POS)):
        df.draw_cycle(Pos=COL_NOTCH_POS[notchIdx], Radius=5)
        df.draw_text(COL_TEXT_CONT[notchIdx], Pos=COL_TEXT_POS[notchIdx], Size=glb.PARAMETERS.text['size']['options'])

    df.draw_cycle(Pos=COL_NOTCH_POS[SelPos], Radius=SEL_RADIUS, FillColor=(255,0,0))

    gf.winFlip()
    
    pressedKey = event.waitKeys(keyList=['left', 'right', 'return', 'escape'])
    choice = ...
    match pressedKey[0]:
        case 'left':
            choice = max(0, SelPos-1)
        case 'right':
            choice = min(len(COL_NOTCH_POS)-1, SelPos+1)
        case 'return':
            choice = glb.ENUMS.Proceed
        case 'escape':
            choice = glb.ENUMS.Abort
    return choice
    
    
