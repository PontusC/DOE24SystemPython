import os, time
from classes.monitor import Monitor
# Import msvcrt on windows, getch on linux
try:
    import msvcrt as m
except ImportError:
    import getch as m # type: ignore

# Handles all menu interactions in terminal and forwarding commands to correct handler
class Menu:
    
    # Singleton pattern
    _self_ = None
    def __new__(menu):
        if menu._self_ is None:
            menu._self_ = super().__new__(menu)
        return menu._self_
    
    # Class variables/constants
    # Both below dicts should just be rewritten to be a list/array
    # All different menu commands excluding default menu
    MENUCHOICES = dict([(1, "Initiate monitoring"),
                        (2, "Show monitoring values"),
                        (3, "Create alarm"),
                        (4, "Remove alarm"),
                        (5, "Show alarms"),
                        (6, "Initiate monitoring mode"),
                        (7, "Exit")])
    # All different commands for alarm menues
    ALARMCHOICES = dict([(1, "CPU"),
                         (2, "MEM"),
                         (3, "DSK"),
                         (4, "Return")])
    
    # Used to remember if its the first time user has entered wrong input in validateInputChoice
    firstError = True
    
    # Reference to monitor
    monitor = Monitor()
    
    def __init__(self) -> None:
        pass
        
    def runMenu(self): # Initial program state, taking inputs and performing actions 
        # Main menu/program loop
        try: 
            while True:
                self.clearTerminal()
                self.listChoices(self.MENUCHOICES)
                clean_input = self.validateInputChoice(len(self.MENUCHOICES))
                match clean_input:
                    case 1:     # Initiate monitoring
                        self.initMonitoring()
                    case 2:     # Show monitoring values
                        self.showMonitoringValues()
                    case 3:     # Create alarm 
                        self.createAlarm()
                    case 4:     # Remove alarm
                        self.removeAlarm()
                    case 5:     # Show alarms
                        self.showAlarms()
                    case 6:     # Initiate monitoring mode
                        self.initMonitoringMode()
                    case 7:     # Exit
                        break
        except KeyboardInterrupt: # Control+C to exit
            pass
        
        
    # Starts monitor
    def initMonitoring(self):
        self.clearTerminal()
        try:
            self.monitor.initMonitoring()
            print("Monitoring initialized . . .")
        except Exception:
            print("Monitoring already initialized . . .")
        self.waitAnyKeypress()
        
    def showMonitoringValues(self):
        # checks for input and breaks
        def waitForInput() -> bool:
            # Cleans input so nothing remains in input buffer
            def flush_input():
                try:
                    m.getch()
                except: # Shouldnt happen but if it does this solves
                    import sys, termios    #for linux/unix
                    termios.tcflush(sys.stdin, termios.TCIOFLUSH)
                    
            for x in range(10):
                    time.sleep(0.1)
                    try: # Windows key detection
                        if m.kbhit():
                            flush_input() # Removes stored keystroke from kbhit
                            return True
                    except: # WSL key detection
                        pass
                
        self.clearTerminal()
        try:
            while True:
                print(self.monitor.returnMonitorValues())
                if not os.name == "nt":
                    self.waitAnyKeypress()
                    break
                print("Press any key to continue . . .")
                if waitForInput(): # Returns true if a button was pressed
                    break
                self.clearTerminal()
        except Exception: # Monitor throws exception if monitoring not initialized
            print("Monitoring not initialized . . .")
            self.waitAnyKeypress()
        
    def createAlarm(self):
        # Takes STR input to determine what type of alarm to generate
        # Returns the validated input to be used
        def setAlarmValue(self, alarmType: str) -> int:
            print(f"Enter an alarm value for {alarmType} between 1-100%")
            clean_input = self.validateInputChoice(100)
            print(f"Alarm created for {alarmType} at {clean_input}% usage")
            self.waitAnyKeypress()
            return clean_input
        
        # Takes input and generates correct alarm
        self.clearTerminal()
        self.listChoices(self.ALARMCHOICES)
        clean_input = self.validateInputChoice(len(self.ALARMCHOICES))
        self.clearTerminal()
        match clean_input:
            case 1: #CPU
                alarmValue : int = setAlarmValue(self,"CPU")
            case 2: #MEM
                alarmValue : int = setAlarmValue(self,"MEM")
            case 3: #DSK
                alarmValue : int = setAlarmValue(self,"DSK")
            case 4:
                pass
        
    def showAlarms(self):
        self.clearTerminal()
        print("Active alarms")
        self.waitAnyKeypress()
        
    def initMonitoringMode(self):
        self.clearTerminal()
        print("Monitoring mode")
        self.waitAnyKeypress()
        
    def removeAlarm(self):
        self.clearTerminal()
        print("remove alarms")
        self.waitAnyKeypress()
        
    # Given dict lists choices and actions
    def listChoices(self, dict: dict):
        print("Choices\t\tActions")
        self.printPrettyStates(dict)
        
    # Verifies and validates input, only allowed to be integers in range
    # Takes an endRange parameter, add +1 if using dict length.
    def validateInputChoice(self, endRange: int):
        try:
            clean_input = int(input("#: ")) # Throws ValueError if not int
            if not (0 < clean_input < endRange + 1):
                raise ValueError
            self.firstError = True # Reset firstError to default state
            return clean_input
        except ValueError:
            self.clearAboveLine()
            # If its not the first error input, has to clear two lines in terminal to keep it tidy
            if not self.firstError:
                self.clearAboveLine()
            else:
                self.firstError = False
            print("Invalid input, try again")
            return self.validateInputChoice(endRange)
    
    # Print and check for any keypress to proceed
    @staticmethod
    def waitAnyKeypress():
        print("Press any key to continue . . .")
        m.getch()
        
    # Prints the dict prettily with choices/actions
    def printPrettyStates(self, dict: dict, count=1):
        if count > len(dict):
            return
        action : str = dict[count]
        print(f"   {count}\t->\t{action}")
        self.printPrettyStates(dict, count + 1)
        
    # Run to clear one line above in terminal
    @staticmethod
    def clearAboveLine():
        LINE_UP = '\033[1A'     # ANSI-code that moves cursor up one line
        LINE_CLEAR = '\x1b[2K'  # ANSI-code that erases current line
        print(LINE_UP, end=LINE_CLEAR)
    
    # cls for windows, clear if linux
    @staticmethod
    def clearTerminal():
        os.system("cls" if os.name == "nt" else "clear")