from enum import Enum
from datetime import datetime
import bisect, json, logging

# Enums for the different alarmtypes
class AlarmType(int, Enum):
        CPU = 1
        MEM = 2
        DSK = 3

# Handles organizing and checking alarms
class AlarmHandler:
    # Inner hidden class used for serialization and managing type of alarm and thresholds
    # Sortable for easy management
    class Alarm:
        
        def __init__(self, threshold: int, type : AlarmType):
            self.alarmThreshold : int = threshold
            self.alarmType : AlarmType = type
        
        # Returns true if self object has lower threshold of alarm
        def __lt__(self, other) -> bool:
            return self.alarmThreshold <= other.alarmThreshold
        
        def __eq__(self, other) -> bool:
            return self.alarmThreshold == other.alarmThreshold and self.alarmType == other.alarmType
        
        def __str__(self) -> str:
            return f"{self.alarmType.name}-alarm at {self.alarmThreshold}%"
    
    # Singleton pattern
    _self_ = None
    def __new__(alarm):
        if alarm._self_ is None:
            alarm._self_ = super().__new__(alarm)
        return alarm._self_
    
    # Class variables
    # Constant for file name
    STOREDALARMS = "storedAlarms.json"
    
    # Arrays for containing alarms
    cpuAlarms = []
    memAlarms = []
    dskAlarms = []
    ALARMARRAYS = [cpuAlarms, memAlarms, dskAlarms]
    
    # Reference to logger
    log = logging.getLogger("AlarmHandler")
    
    def __init__(self) -> None:
        pass
        
    # Creates alarm of given type and threshold
    def createAlarm(self, type : AlarmType, threshold : int):
        newAlarm = self.Alarm(threshold, type)
        self.log.info(f"{newAlarm.alarmType.name}-Alarm at {newAlarm.alarmThreshold}% created")
        match type.value:
            case 1: # Matches ENUM to it's value, CPU = 1 etc...
                # Sorted insert
                bisect.insort(self.cpuAlarms, newAlarm)
            case 2:
                bisect.insort(self.memAlarms, newAlarm)
            case 3:
                bisect.insort(self.dskAlarms, newAlarm)
    
    # Returns a formatted str of all current alarms, listed in ascending order and grouped by type
    def getAlarmsString(self) -> str:
        allAlarms = [*self.cpuAlarms, *self.memAlarms, *self.dskAlarms] # Join all alarms into one array
        # Return None if empty alarms
        if len(allAlarms) == 0:
            return None
        return "".join(str(alarm)+"\n" for alarm in allAlarms).rstrip()
    
    # Returns a list of all alarm objects in ascending order grouped by type
    def getAlarms(self):
        return [*self.cpuAlarms, *self.memAlarms, *self.dskAlarms]
    
    # Checks if given threshold and alarm type triggers any alarms
    def checkIfAlarmTrigger(self, thresholdPercent: float, alarmType : AlarmType):
        alarms = self.ALARMARRAYS[alarmType.value - 1] # Gets correct array of alarms, based on AlarmType Enum
        # alarms are sorted lower->higher so iterate over list reversed to check highest alarms first
        for alarm in reversed(alarms):
            if alarm.alarmThreshold <= thresholdPercent:
                 print(f"***** {alarmType.name}-Alarm\tThreshold: {alarm.alarmThreshold}%\tCurrent: {thresholdPercent}%\tTime: {datetime.now().strftime(format="%H:%M:%S:%f03d")[:12]} *****")
                 self.log.info(f"Alarm: {alarmType.name}-Alarm\tThreshold: {alarm.alarmThreshold}%\tCurrent: {thresholdPercent}%")
                 break
        
    # Returns true if alarms exist
    def alarmsExist(self) -> bool:
        return len([*self.cpuAlarms, *self.memAlarms, *self.dskAlarms]) > 0
    
    # Attempts to remove given alarm, true if successful
    def removeAlarm(self, alarm : Alarm):
        alarms = self.ALARMARRAYS[alarm.alarmType.value - 1] # Gets correct array of alarms, based on AlarmType Enum
        alarms.remove(alarm)
        self.log.info(f"Removed {alarm}")
    
    # Converts all alarms to JSON and returns the string format [{"alarmThreshold": 3, "alarmType": 1}, ... ]
    def alarmsToJSON(self) -> str:
        return json.dumps([alarm.__dict__  for alarm in [*self.cpuAlarms, *self.memAlarms, *self.dskAlarms]])
        #return "".join(json.dumps(alarm.__dict__)+"\n" for alarm in [*self.cpuAlarms, *self.memAlarms, *self.dskAlarms]).rstrip()
          
    # Takes str from file input and generates an alarm per each stored alarm
    def JSONToAlarms(self, loadedAlarms : str):
        arrayOfStoredAlarms = json.loads(loadedAlarms)
        for storedAlarm in arrayOfStoredAlarms:
            # AlarmType and Threshold keys, Value is threshold 
            alarmType = AlarmType(storedAlarm["alarmType"])
            alarmThreshold = storedAlarm["alarmThreshold"]
            self.createAlarm(alarmType, alarmThreshold)
           
    def saveAlarmsToFile(self):
        file = open(self.STOREDALARMS, "w")
        file.write(self.alarmsToJSON())
        file.close()
        self.log.info(f"Alarms successfully saved to {self.STOREDALARMS}")
        
    # Loads and generates alarms from stored file if it exists
    def loadAlarmsFromFile(self):
        try:
            file = open(self.STOREDALARMS, "r")
            jsonAlarms = file.read()
            file.close()
            self.log.info(f"Loading alarms from {self.STOREDALARMS}")
            self.JSONToAlarms(jsonAlarms)
            self.log.info(f"Alarms successfully loaded from {self.STOREDALARMS}")
        except:
            self.log.info("No alarms found")
            pass