import Code.globals as glb
import matlab

def markEvent(EventType:str, *args):
    eventName = ''
    eventTime = glb.ABS_CLOCK.getTime()
    match EventType:
        # Task generic events (NECESSARY)
        case "taskStart":
            eventName = "Task Started"
        case "taskStop":
            eventName = "Task Ended Successfully"
        case "taskAbort":
            eventName = "Task Aborted"

        # Intro Events
        case "introStart":
            eventName = f'Intro Started'
        case "introEnd":
            eventName = f'Intro Ended'

        # Block and Trial generic events
        case "blockStart":
            eventName = f'Block {args[0]} Started'
        case "blockEnd":
            eventName = f'Block {args[0]} Ended'
        case "trialStart":
            eventName = f'Trial {args[0]} Started'
        case "trialEnd":
            eventName = f'Trial {args[0]} Ended'
        case "trialBlockStart":
            eventName = f'Trial {args[0]} in Block {args[1]} Started'
        case "trialBlockEnd":
            eventName = f'Trial {args[0]} in Block {args[1]} Ended'
        
        # Task specific events
        case "promptStart":
            eventName = f'Prompt Start. Trial {args[0]}'
        case "promptEnd":
            eventName = f'Prompt End. Trial {args[0]}'
        case "imagineStart":
            eventName = f'Imagination Start. Trial {args[0]}'
        case "imagineEnd":
            eventName = f'Imagination End. Trial {args[0]}'
        case "vividStart":
            eventName = f'Vividness Rating Start. Trial {args[0]}'
        case "vividEnd":
            eventName = f'Vividness Rating End. Trial {args[0]}'
        case "stimulusStart":
            eventName = f'Stimulus Start. Trial {args[0]}'
        case "stimulusEnd":
            eventName = f'Stimulus End. Trial {args[0]}'
        case "colorStart":
            eventName = f'Color Reporting Start. Trial {args[0]}'
        case "colorEnd":
            eventName = f'Color Reporting End. Trial {args[0]}'

        case _:
            eventName = f'UNKNOWN EVENT'
        
    glb.PARAMETERS.events.append((eventName, eventTime))

        
    match glb.PARAMETERS.ID['expEnv']:
        case "BCM-EMU":
            match EventType:
                case "taskStart":
                    onlineNSP = glb.MATENG.eval("TaskComment('start', emuSaveName);", nargout = 1)
                    glb.MATENG.workspace['onlineNSP'] = matlab.double(onlineNSP)
                case "taskStop":
                    glb.MATENG.eval("TaskComment('stop', emuSaveName);", nargout = 0)
                case "taskAbort":
                    glb.MATENG.eval("TaskComment('kill', emuSaveName);", nargout = 0)
                case _:
                    blackRockComment = glb.MATENG.cellstr(list(eventName))
                    glb.MATENG.workspace['blackRockComment'] = blackRockComment
                    glb.MATENG.eval("blackRockComment = [blackRockComment{:}];", nargout = 0)
                    glb.MATENG.eval("for i=1:numel(onlineNSP); cbmex('comment', 255, 0, blackRockComment,'instance',onlineNSP(i)-1); end", nargout = 0)

