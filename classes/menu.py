import os


class Menu:
    def __init__(self) -> None:
        # All different menu states excluding default
        self.STATES = dict([(1, "Initiate monitoring"),
                            (2, "Show monitoring values"),
                            (3, "Create alarm"),
                            (4, "Remove alarm"),
                            (5, "Show alarms"),
                            (6, "Initiate monitoring mode")])

    def runMenu(self): # Initial program state, taking inputs and performing actions 
        # Verifies and validates input, only allowed to be integers in range
        # Default range is exclusive length of STATES
        def validateInputChoice(endRange = len(self.STATES) + 1):
            try:
                clean_input = int(input("#: ")) # Throws ValueError if not int
                if not (0 < clean_input < endRange):
                    raise ValueError
                return clean_input
            except ValueError:
                self.clear_above_line()
                # Removed, doesnt behave as intented fix later
                #print("Invalid input, try again")
                return validateInputChoice() 
        
        # Prints the STATES-dict prettily
        def printPrettyStates(STATES, count=1):
            if count > len(STATES):
                return
            action : str = STATES[count]
            print(f"   {count}\t->\t{action}")
            printPrettyStates(STATES, count + 1)
            
            
        
        # Main menu/program loop
        try: 
            while True:
                print("Choices\t\tActions")
                printPrettyStates(self.STATES)
                clean_input = validateInputChoice()
        except KeyboardInterrupt: # Control+C to exit
            pass
        
        
        
        
        
    def startMonitoring():
        print("Monitoring started")
        
    def listActiveMonitoring():
        print("active monitoring below")
        
    def createAlarms():
        print("Create alarms")
        
    def listActiveAlarms():
        print("Active alarms")
        
    def startMonitoringMode():
        print("Monitoring mode")
        
    def removeAlarms():
        print("remove alarms")
        
    # Run to clear one line above in terminal
    @staticmethod
    def clear_above_line():
        LINE_UP = '\033[1A'     # ANSI-code that moves cursor up one line
        LINE_CLEAR = '\x1b[2K'  # ANSI-code that erases current line
        print(LINE_UP, end=LINE_CLEAR)
        
    @staticmethod
    def clear_terminal():
        os.system("cls")