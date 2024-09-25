import os, time
from classes.resourceMonitor import ResourceMonitor
from classes.alarmMonitor import AlarmMonitor, AlarmType
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
    
    # Reference to ResourceMonitor and AlarmMonitor
    resourceMonitor = ResourceMonitor()
    alarmMonitor = AlarmMonitor()
    
    # Constants for reused strings
    NOTINITIALIZED = "Monitoring not intialized . . ."
    
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
        
        
    # Starts monitoring
    def initMonitoring(self):
        self.clearTerminal()
        try:
            self.resourceMonitor.initMonitoring()
            print("Monitoring initialized . . .")
        except Exception:
            print("Monitoring already initialized . . .")
        self.waitAnyKeypress()
        
    # Contiually shows current resource usage (on windows)
    def showMonitoringValues(self):
        # checks for input and breaks a loop
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
                print(self.resourceMonitor.returnMonitorValues())
                if not os.name == "nt":
                    self.waitAnyKeypress()
                    break
                # It is reachable, needed for wsl/linux
                print("Press any key to continue . . .")
                if waitForInput(): # Returns true if a button was pressed
                    break
                self.clearTerminal()
        except Exception: # Monitor throws exception if monitoring not initialized
            print(self.NOTINITIALIZED)
            self.waitAnyKeypress()
        
    def createAlarm(self):
        # Takes input and generates correct alarm
        self.clearTerminal()
        self.listChoices(self.ALARMCHOICES)
        # Takes input and generates the correct ENUM associated with that AlarmType
        validatedInput = self.validateInputChoice(len(self.ALARMCHOICES))
        if validatedInput < 4: # Only 1-3 valid to generate alarms, 4 back to main menu
            alarmType = AlarmType(validatedInput)
            # Takes user input in range 1-100 and creates and stores that alarm
            self.clearTerminal()
            print(f"Enter an alarm value for {alarmType.name} between 1-100%")
            alarmThreshold = self.validateInputChoice(100)
            self.clearTerminal()
            self.alarmMonitor.createAlarm(alarmType, alarmThreshold)
            print(f"Alarm created for {alarmType.name} at {alarmThreshold}% usage")
            self.waitAnyKeypress()
        else:
            self.clearTerminal()
    
    # Prints all active alarms
    def showAlarms(self):
        self.clearTerminal()
        print(self.alarmMonitor.returnAlarms())
        self.waitAnyKeypress()
    
    # Continually (on windows) prints that it is monitoring and whenever an alarm occurs
    def initMonitoringMode(self):
        self.clearTerminal()
        if  not self.resourceMonitor.monitoringStarted:
            print(self.NOTINITIALIZED)
        else:
            # Set alarm values before entering
            self.resourceMonitor.setAlarms()
            # Loop here and check for changes and reprint, exit on input
            self.resourceMonitor.monitoringMode()
            print("Monitoring mode")
        self.waitAnyKeypress()
        
    def removeAlarm(self):
        self.clearTerminal()
        print("remove alarms")
        self.waitAnyKeypress()
        
    # Given dict lists choices and actions
    def listChoices(self, dict: dict):
        print("Choices\t\tActions")
        self.pprintDict(dict)
        
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
    def pprintDict(self, dict: dict, count=1):
        if count > len(dict):
            return
        action : str = dict[count]
        print(f"   {count}\t->\t{action}")
        self.pprintDict(dict, count + 1)
        
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