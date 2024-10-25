import random, math
import pandas as pd

import Code.globals as glb
from Code.Support.markEvent import markEvent
from Code.RunScripts import Trial

# The main function of Experiment. Responsible for hosting all of the operations throughout the main experiment
def run(TaskVars:dict):
    # Pregenerate some of the data needed for storing the output
    outcome = ...
    allData = []

    # Loop going through the blocks
    for blockIdx in range(glb.PARAMETERS.exp['numBlocks']):
        # Generate needed data
        blockData=[]
        prompts = TaskVars['prompts']
        random.shuffle(prompts)
        # shuffledTrials = random.shuffle(list(range(glb.PARAMETERS.block['numTrials'])))
        # print(shuffledTrials)
        # mockAmount = math.floor(len(shuffledTrials)*0.0625)
        # mockBlue = shuffledTrials[0:mockAmount]
        # shuffledTrials = shuffledTrials[mockAmount:]
        # mockRed = shuffledTrials[0:mockAmount]

        # Mark the beginning of the block
        markEvent('blockStart', blockIdx+1)

        # Loop going through each trial in the block 
        for trialIdx in range(glb.PARAMETERS.block['numTrials']):
            mock = 0
            # if trialIdx in mockBlue:
            #     mock=1
            # elif trialIdx in mockRed:
            #     mock=2

            # Run the trial and store the outcome
            outcome = Trial.run(prompts[trialIdx], TaskVars['conditions'][blockIdx%2], trialIdx, blockIdx, mock)

            # Format the outcome of the trial to the specifications of the save data
            norm_outcome = (outcome['vividRating'], outcome['colorSeen'], prompts[trialIdx], TaskVars['conditions'][blockIdx%2])
            allData.append(norm_outcome)
            blockData.append(norm_outcome)

            # Stop looping through the trials if we need to abort
            if outcome['Abort']: break

        # Mark the end of the block
        markEvent('blockEnd', blockIdx+1)
        
        # Save the data for the block
        blockDataFrame = pd.DataFrame(blockData, columns=["Vividness Rating", "Color Seen", "Prompt", "Condition"])
        blockDataFrame.to_excel(glb.PARAMETERS.outputDir+f'Block_{blockIdx+1}.xlsx')
        
        # Stop looping through the blocks if we need to abort
        if outcome['Abort']: break
        
    # Save the data for all of the trials
    dataFrame = pd.DataFrame(allData, columns=["Vividness Rating", "Color Seen", "Prompt", "Condition"])
    dataFrame.to_excel(glb.PARAMETERS.outputDir+f'Behavioral Data.xlsx')

    # Mark the end of the experiment appropriately
    if outcome['Abort']: markEvent("taskAbort")
    else: markEvent("taskStop")

    # Save all of the events
    eventDataFrame = pd.DataFrame(glb.PARAMETERS.events, columns=["Event Name", "Event Time"])
    eventDataFrame.to_excel(glb.PARAMETERS.outputDir+f'Event Data.xlsx')
