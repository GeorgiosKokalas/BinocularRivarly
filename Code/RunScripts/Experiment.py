import random
import pandas as pd

import Code.globals as glb
from Code.Support.markEvent import markEvent
from Code.RunScripts import Trial


def run(TaskVars:dict):
    outcome = ...
    allData = []
    for blockIdx in range(glb.PARAMETERS.exp['numBlocks']):
        blockData=[]
        markEvent('blockStart', blockIdx+1)
        prompts = TaskVars['prompts']
        random.shuffle(prompts)
        
        for trialIdx in range(glb.PARAMETERS.block['numTrials']):
            outcome = Trial.run(prompts[trialIdx], TaskVars['conditions'][blockIdx%2], trialIdx, blockIdx)
            norm_outcome = (outcome['vividRating'], outcome['colorSeen'], prompts[trialIdx], TaskVars['conditions'][blockIdx%2])
            allData.append(norm_outcome)
            blockData.append(norm_outcome)
            if outcome['Abort']: break
            
        blockDataFrame = pd.DataFrame(blockData, columns=["Vividness Rating", "Color Seen", "Prompt", "Condition"])
        blockDataFrame.to_excel(glb.PARAMETERS.outputDir+f'Block_{blockIdx+1}.xlsx')
        
        if outcome['Abort']: break
        markEvent('blockEnd', blockIdx+1)
    
    dataFrame = pd.DataFrame(allData, columns=["Vividness Rating", "Color Seen", "Prompt", "Condition"])
    dataFrame.to_excel(glb.PARAMETERS.outputDir+f'Behavioral Data.xlsx')

    if outcome['Abort']: markEvent("taskAbort")
    else: markEvent("taskStop")

    eventDataFrame = pd.DataFrame(glb.PARAMETERS.events, columns=["Event Name", "Event Time"])
    eventDataFrame.to_excel(glb.PARAMETERS.outputDir+f'Event Data.xlsx')
