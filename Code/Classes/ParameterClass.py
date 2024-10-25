import matlab
import os
from datetime import datetime

import tkinter as tk
import tkinter.messagebox as tkm
from tkinter import ttk

import Code.globals as glb

# CLASS TO ENTER PARAMETERS
# DEVELOPED BY GEORGIOS KOKALAS
class ParameterClass:
    def __init__(self):
        #### EDIT AS USER ####

        # exp - Experiment information
        #   - name: (NECESSARY) The name of the task
        #   - numBlocks: The number of Blocks
        self.exp = {'name': 'BinocularRivarly',
                    'numBlocks': 3
                    }
        
        # screen - Screen information
        #   - number: (NECESSARY) which screen to use (1st screen = 0, 2nd screen = 1...)
        #   - framerate: (NECESSARY) the framerate to use for the video
        #   - bgColor: (NECESSARY) The background color of the screen
        self.screen = {'number': 1,
                       'framerate': 60,
                       'bgColor': (5,5,5),
                       'pixCenter': [0,0]
                       }
        
        # text - Text Information
        #   - font: (NECESSARY) Information about the font
        #       - default: (NECESSARY) The font that will be used by default
        #   - size: (NECESSARY) Information about the letter size
        #       - default: (NECESSARY) The default size 
        #       - question: The size of the text for the questions asked
        #       - options: The size of the text when listing out all the options
        #   - color: (NECESSARY) Information abotu the letter Color
        #       - default: (NECESSARY) The default color
        #   - bgColor: (NECESSARY) Information abotu the textBox Color
        #       - default: (NECESSARY) The default color
        self.text = {'font':    {'default': 'Arial'},
                     'size':    {'default': 40,
                                 'question': 50,
                                 'options': 35,
                                 },
                     'color':   {'default': (255, 255, 255)},
                     'bgColor': {'default': None}
                     }

        # block - Information about each block
        #   - numTrials: The number of trials per block
        self.block = {'numTrials': 40}
        
        # trial - Inforation about each trial
        #   - pdDurS: The duration (in seconds) of the photodiode
        #   - promptDurS: The duration of the R/B prompt
        #   - imagineDurS: The duration of the imagination period
        #   - stimDurS: The duration for which the stimulus is shown.
        self.trial = {'pdDurS': 0.2,
                      'promptDurS': 0.75,
                      'imagineDurS':1,
                      'stimDurS':0.75
                      }

        #### STOP EDITING AS USER ####

        # Verify the framerate of the screen
        if self.screen['framerate'] <= 0:
            self.screen['framerate'] = -1

        # Create an ID For the participant
        self.ID = {}
        self.__launch_ID_UI()

        # Make a place to store all the events
        self.events = []
        
        # Make the savefile 
        # Generate the names for the savefile
        now:str = datetime.now().strftime("%Y%m%d_%H%M") 
        idName:str = self.ID['name']
        expName:str = self.exp['name']
        userPath:str = os.path.expanduser('~')
        
        # Create the directories for the savefiles if needed.
        outputDir = f'{userPath}/Documents/PatientData'
        if not os.path.exists(outputDir): os.mkdir(outputDir)

        outputDir += f'/{idName}'
        if not os.path.exists(outputDir): os.mkdir(outputDir)

        outputDir += f'/{expName}'
        if not os.path.exists(outputDir): os.mkdir(outputDir)
    
        self.outputDir = outputDir + f'/{expName}__{idName}_{now}/'
        if not os.path.exists(self.outputDir): os.mkdir(self.outputDir)

        print(self.outputDir)


    # Function that launches a UI for creating an ID for the user
    def __launch_ID_UI(self):
        idUI = tk.Tk() 
        idUI.title('ID specifications')
        rowNum = 0

        # Label text for Name
        nameLabel = ttk.Label(idUI, text = "Please enter the participant's name/refID:")
        nameLabel.grid(row =rowNum, column=1, padx=10, sticky='W')
        rowNum += 1

        # Text Box for the Name
        nameEntry = ttk.Entry(idUI, textvariable=tk.StringVar(), justify=tk.LEFT)
        nameEntry.insert(0, 'TEST')
        nameEntry.grid(row=rowNum, column=1, padx=10, sticky='W')
        rowNum += 1

        # Blank Space
        ttk.Label(idUI).grid(row =rowNum, column=1)
        rowNum += 1

        # Label for exp Env Option
        expEnvLabel = ttk.Label(idUI, text='Select Experimental Setup:')
        expEnvLabel.grid(row=rowNum, column=1, padx=10, sticky='W')
        rowNum += 1

        # Combobox creation 
        expEnvList = ttk.Combobox(idUI, width = 20, textvariable = tk.StringVar()) 
        expEnvList['values'] = ('None', 'BCM-EMU') 
        expEnvList.grid(row=rowNum, column=1, padx=10, sticky='W') 
        expEnvList.current() 
        rowNum += 1

        # Blank Space
        ttk.Label(idUI).grid(row =rowNum, column=1)
        rowNum += 1

        # Definition of save button functionality
        def save_button():
            self.ID.update({'name': nameEntry.get(),
                            'expEnv': expEnvList.get()})
            shouldDestroy = True
            for key in self.ID.keys():
                if self.ID[key] == '': shouldDestroy = False

            if self.ID['expEnv'] not in expEnvList['values']:
                shouldDestroy = False

            if shouldDestroy:
                idUI.destroy()
            else:
                tkm.showwarning(title='Incorrect values', message='Some of the values appear to be missing or incorrect')
        
        # Save button placement
        saveButton = ttk.Button(idUI, text='Save', command=save_button)
        saveButton.grid(row=rowNum, column = 1)
        idUI.mainloop() 

        # extra operations if we are operating in the EMU
        match self.ID['expEnv']:
            case 'BCM-EMU':
                logEntry = glb.MATENG.eval("getNextLogEntry();", nargout = 2)
                emuRunNum = int(logEntry[0])
                emuSaveName = f'EMU-{emuRunNum:04}_subj-{logEntry[1]}_BinocularRivarly'
                glb.MATENG.workspace['emuSaveName'] = glb.MATENG.cellstr(list(emuSaveName))
                glb.MATENG.eval("emuSaveName = [emuSaveName{:}];", nargout = 0)
                self.ID.update({'emuRunNum': emuRunNum})
    
    