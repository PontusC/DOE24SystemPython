import os, time, logging, time
from classes.resourceMonitor import ResourceMonitor
from classes.alarmHandler import AlarmHandler, AlarmType
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
    # All menu commands 
    MENUCHOICES = dict([(1, "Initiate monitoring"),
                        (2, "Show monitoring values"),
                        (3, "Create alarm"),
                        (4, "Remove alarm"),
                        (5, "Show alarms"),
                        (6, "Initiate monitoring mode"),
                        (7, "Exit")])
    # All commands for alarm creation menu
    ALARMCHOICES = dict([(1, "CPU"),
                         (2, "MEM"),
                         (3, "DSK"),
                         (4, "Return")])
    # Defines how often to check for alarms in seconds
    alarmIntervalCheck = 5
    
    # Used to remember if its the first time user has entered wrong input in validateInputChoice
    firstUserInputError = True
    
    # References to ResourceMonitor and AlarmMonitor
    resourceMonitor = ResourceMonitor()
    alarmHandler = AlarmHandler()
    
    # Reference to logger
    log = logging.getLogger("Menu")
    
    # Constants for reused strings
    NOTINITIALIZED = "Monitoring not intialized . . ."
    INITIALIZED = "Monitoring initialized . . ."
    ALREADYINITIALIZED = "Monitoring already initialized . . ."
    ANYKEYCONTINUE = "Press any key to continue . . ."
    NOALARMS = "No alarms created . . ."
    
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
                        self.initMonitoringMenuChoice()
                    case 2:     # Show monitoring values
                        self.showMonitoringMenuChoice()
                    case 3:     # Create alarm 
                        self.createAlarmMenuChoice()
                    case 4:     # Remove alarm
                        self.removeAlarmMenuChoice()
                    case 5:     # Show alarms
                        self.showAlarmsMenuChoice()
                    case 6:     # Initiate alarm monitoring mode
                        self.initAlarmMonitoringMenuChoice()
                    case 7:     # Exit
                        self.alarmHandler.saveAlarmsToFile()
                        break
        except KeyboardInterrupt: # Control+C to exit
            pass
        
    # Enables monitoring in the ResourceMonitor
    def initMonitoringMenuChoice(self):
        self.clearTerminal()
        try:
            self.resourceMonitor.initMonitoring()
            print(self.INITIALIZED)
        except Exception:
            print(self.ALREADYINITIALIZED)
        self.waitAnyKeypress()
        
    # Continually prints and reprints current resource usage (on windows)
    def showMonitoringMenuChoice(self):
        printedLogFile = False
        self.clearTerminal()
        try:
            while True:
                print(self.resourceMonitor.returnMonitorValues())
                # Used to only log once, needed because of my try/except structure
                if not printedLogFile:
                    self.log.info("Resource monitoring: started")
                    printedLogFile = True
                if not os.name == "nt": 
                    # It is reachable, needed for wsl/linux
                    self.waitAnyKeypress()
                    break
                print(self.ANYKEYCONTINUE)
                if self.waitForInput(): # Returns true if a button was pressed, also pauses program
                    break
                
                self.clearTerminal()
            self.log.info("Resource monitoring: exited")
        except Exception: # resourceMonitor throws exception if monitoring not initialized
            print(self.NOTINITIALIZED)
            self.waitAnyKeypress()
        
    # Takes input and generates alarm of specified type and threshold
    def createAlarmMenuChoice(self):
        self.clearTerminal()
        self.listChoices(self.ALARMCHOICES)
        validatedInput = self.validateInputChoice(len(self.ALARMCHOICES))
        if validatedInput < 4: # Only 1-3 valid to generate alarms, 4 back to main menu
            # Takes input and generates corresponding AlarmType Enum
            alarmType = AlarmType(validatedInput)
            # Takes user input in range 1-100 and creates and stores that alarm
            self.clearTerminal()
            print(f"Enter an alarm threshold for {alarmType.name} between 1-100%")
            alarmThreshold = self.validateInputChoice(100)
            self.clearTerminal()
            self.alarmHandler.createAlarm(alarmType, alarmThreshold)
            print(f"Alarm created for {alarmType.name} at {alarmThreshold}% usage")
            self.waitAnyKeypress()
        else:
            self.clearTerminal()
    
    # Prints all active alarms
    def showAlarmsMenuChoice(self):
        self.clearTerminal()
        alarmStr = self.alarmHandler.getAlarmsString()
        if alarmStr is None:
            print(self.NOALARMS)
        else:
            print(alarmStr)
        self.waitAnyKeypress()
    
    # Continually (on windows) prints whenever an alarm occurs
    def initAlarmMonitoringMenuChoice(self):
        self.clearTerminal()
        if not self.resourceMonitor.monitoringStarted:
            print(self.NOTINITIALIZED)
            self.waitAnyKeypress()
        else:
            # checks if alarms exist
            if self.alarmHandler.alarmsExist():
                print("\t\t\t***** MONITORING ON *****\n")
                self.log.info("Alarm monitoring: started")
                # Loop here and check for changes and reprint, exit on input
                # Checks every 5 seconds for alarms
                while True:
                    self.clearAboveLineTerminal()
                    self.resourceMonitor.checkForAlarms()
                    print(self.ANYKEYCONTINUE)
                    if not os.name == "nt":
                        self.waitAnyKeypress()
                        break
                        # It is reachable, needed for wsl/linux
                    if self.waitForInput(self.alarmIntervalCheck):
                        break
                self.log.info("Alarm monitoring: exited")
            else:
                print(self.NOALARMS)
                self.waitAnyKeypress()
        
    # Removevs a specified alarm
    def removeAlarmMenuChoice(self):
        self.clearTerminal()
        if self.alarmHandler.alarmsExist():
            alarms = self.alarmHandler.getAlarms()
            # Generates a dict that follows format for pprintDict()
            removeAlarmChoices = {index + 1: alarm for index, alarm in enumerate(alarms)}
            print("Choices\t\tAlarm to remove")
            self.pprintDict(removeAlarmChoices)
            validated_input = self.validateInputChoice(len(removeAlarmChoices))
            self.alarmHandler.removeAlarm(removeAlarmChoices[validated_input])
            print(f"Removed {removeAlarmChoices[validated_input]}")
            self.waitAnyKeypress()
        else:
            print(self.NOALARMS)
            self.waitAnyKeypress()
        
    # Given dict lists choices and actions
    def listChoices(self, dict: dict):
        print("Choices\t\tActions")
        self.pprintDict(dict)
        
    # Verifies and validates input, only allowed to be integers in given range
    def validateInputChoice(self, endRange: int):
        try:
            clean_input = int(input("#: ")) # Throws ValueError if not int
            if not (0 < clean_input < endRange + 1):
                raise ValueError
            self.firstUserInputError = True # Reset firstError to default state
            return clean_input
        except ValueError:
            self.clearAboveLineTerminal()
            # If its not the first error input, has to clear two lines in terminal to keep it tidy
            if not self.firstUserInputError:
                self.clearAboveLineTerminal()
            else:
                self.firstUserInputError = False
            print("Invalid input, try again")
            return self.validateInputChoice(endRange)
    
    # Print and check for any keypress to proceed
    def waitAnyKeypress(self):
        print(self.ANYKEYCONTINUE)
        m.getch()
        
    # checks for ANY input and returns true if it happens, clears input-buffer
    # Also can take a delay parameter which specifies seconds to sleep
    # Used to break out of loops when repeatedly printing and clearing terminal to update values
    def waitForInput(self, delay=1) -> bool:
        # Cleans input so nothing remains in input buffer
        def flush_input():
            try:
                m.getch()
            except: # Shouldnt happen but if it does this solves
                import sys, termios    #for linux/unix
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        # Default is to sleep for 1s
        for x in range(delay*10):
                time.sleep(0.1)
                try: # Windows key detection
                    if m.kbhit():
                        flush_input() # Removes stored keystroke from kbhit
                        return True
                except: # WSL key detection
                    pass
        
    # Prints given dict prettily with choices/actions
    def pprintDict(self, dict: dict, count=1):
        if count > len(dict):
            return
        action : str = dict[count]
        print(f"   {count}\t->\t{action}")
        self.pprintDict(dict, count + 1)
        
    # Run to clear one line above in terminal
    @staticmethod
    def clearAboveLineTerminal():
        LINE_UP = '\033[1A'     # ANSI-code that moves cursor up one line
        LINE_CLEAR = '\x1b[2K'  # ANSI-code that erases current line
        print(LINE_UP, end=LINE_CLEAR)
    
    # cls for windows, clear if linux
    @staticmethod
    def clearTerminal():
        os.system("cls" if os.name == "nt" else "clear")