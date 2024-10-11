from psychopy import event

from Code.Support import GenericFunctions as gf, DrawFunctions as df

def run():
    df.draw_text("Binocular Rivarly")
    gf.winFlip()
    event.waitKeys(keyList=['space'])

    
    


    
    	