class Menu:
    def __init__(self) -> None:
        self.STATES = dict([(1, "Start monitoring"),
                            (2, "List active monitoring"),
                            (3, "Create alarm"),
                            (4, "Show active alarms"),
                            (5, "Start monitoring mode"),
                            (6, "Remove alarms")])

    def startMenu(self): # Initial program state, taking inputs and performing actions
        # Fix input cleaning here
        raw_input = input("Select menu\n")
        clean_input = None
        try: 
            clean_input = int(raw_input)
        except ValueError:
            print("invalid number")
            
        print(self.STATES[clean_input])
        
        
        
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