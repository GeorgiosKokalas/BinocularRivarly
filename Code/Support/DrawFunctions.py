import Code.globals as glb
from psychopy import visual


# FILE CONTAINING FUNCTIONS WRAPPING IN THE DRAWING OF SHAPES

# Wrapper for drawign text
def draw_text(text:str, BgColor=glb.PARAMETERS.text['bgColor']['default'], Pos=(0,0),
              Color=glb.PARAMETERS.text['color']['default'], HozLength=None,
              Size=glb.PARAMETERS.text['size']['default'],
              Font=glb.PARAMETERS.text['font']['default']):
    glb.UI_TEXT.setText(text)

    textStim = visual.TextStim(glb.UI_WIN, text=glb.UI_TEXT.text, height=glb.UI_TEXT.letterHeight)
    hozSize = textStim.boundingBox[0]*1.2 if HozLength==None else HozLength
    glb.UI_TEXT.setSize((hozSize, textStim.boundingBox[1]*1.1))

    glb.UI_TEXT.setFillColor(BgColor)
    glb.UI_TEXT.setColor(Color)
    glb.UI_TEXT.setLetterHeight(Size)
    glb.UI_TEXT.setFont(Font)
    glb.UI_TEXT.setPos(Pos)
    glb.UI_TEXT.draw()


def draw_rect(FillColor=(255,255,255), Width=10, Height=10, Pos=(0,0), Opacity=1):
    glb.UI_RECT.setFillColor(FillColor)
    glb.UI_RECT.setWidth(Width)
    glb.UI_RECT.setHeight(Height)
    glb.UI_RECT.setPos(Pos)
    glb.UI_RECT.setOpacity(Opacity)

    glb.UI_RECT.draw()


def draw_cycle(FillColor=(255,255,255), Radius=50,Pos=(0,0), Opacity=1):
    glb.UI_CYCLE.setFillColor(FillColor)
    glb.UI_CYCLE.setRadius(Radius)
    glb.UI_CYCLE.setPos(Pos)
    glb.UI_CYCLE.setOpacity(Opacity)

    glb.UI_CYCLE.draw()

def draw_line(Start=(-0.5, -0.5), End=(0.5, 0.5), Size=1, Opacity=1, Color=(255,255,255)):
    glb.UI_LINE.setStart(Start)
    glb.UI_LINE.setEnd(End)
    glb.UI_LINE.setSize(Size)
    glb.UI_LINE.setOpacity(Opacity)
    glb.UI_LINE.setColor(Color)

    glb.UI_LINE.draw()
    
