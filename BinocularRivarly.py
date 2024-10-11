## THE MAIN SCRIPT TO CALL THE CODE FROM
## CREATED: 27 SEPT. 2024
## AUTHOR:  GEORGIOS KOKALAS
#----------------------------------------
## CHANGELOG
#----------------------------------------

# IMPORT LIBRARIES AND CODE
# Gain access to the OS and add the code to the Python Path
import os, sys
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("./Code/")

def makeTaskVars() -> dict:
    import Code.globals as glb
    import math

    prompts = ['R', 'C']
    conditions = ['Dark', 'Light']
    
    prompts *= math.ceil(glb.PARAMETERS.block['numTrials']/2)
    if len(prompts) > glb.PARAMETERS.block['numTrials']:
        prompts = prompts[0:glb.PARAMETERS.block['numTrials']-1]

    taskVars = {'prompts': prompts,
                'conditions': conditions}
    
    return taskVars

    


# MAIN CALL
if __name__ == "__main__":
    import Code.globals as glb
    glb.create_globals()
    taskVars:dict = makeTaskVars()

    from Code.Support.markEvent import markEvent
    from Code.RunScripts import Intro, Experiment

    markEvent('taskStart')
    Intro.run()
    Experiment.run(taskVars)


    glb.MATENG.quit()
    glb.UI_WIN.close()