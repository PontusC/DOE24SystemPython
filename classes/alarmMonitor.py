from enum import Enum
from datetime import datetime
import bisect

 # Enumtypes for the different alarmtypes
class AlarmType(Enum):
        CPU = 1
        MEM = 2
        DSK = 3

class AlarmMonitor:
    # Inner hidden class used for serialization and managing type of alarm and thresholds
    # Sortable for easy management
    class Alarm:
        
        def __init__(self, threshold: int, type : AlarmType):
            self.alarmThreshold = threshold
            self.alarmType = type
        
        # Returns true if self object has lower threshold of alarm
        def __lt__(self, other) -> bool:
            return self.alarmThreshold <= other.alarmThreshold
        
        def __str__(self) -> str:
            return f"{self.alarmType.name}-alarm at {self.alarmThreshold}%"
    
    # Singleton pattern
    _self_ = None
    def __new__(alarm):
        if alarm._self_ is None:
            alarm._self_ = super().__new__(alarm)
        return alarm._self_
    
    # Class variables
    
    def __init__(self) -> None:
        self.cpuAlarms = []
        self.memAlarms = []
        self.dskAlarms = []
        self.ALARMARRAYS = [self.cpuAlarms, self.memAlarms, self.dskAlarms]
        
    # Creates alarm of given type and threshold
    def createAlarm(self, type : AlarmType, threshold : int):
        newAlarm = self.Alarm(threshold, type)
        match type.value:
            case 1: # Matches ENUM to it's value, CPU = 1 etc...
                bisect.insort(self.cpuAlarms, newAlarm)
            case 2:
                bisect.insort(self.memAlarms, newAlarm)
            case 3:
                bisect.insort(self.dskAlarms, newAlarm)
    
    # Returns a formatted str of all current alarms, listed in rising order and by type
    def returnAlarms(self) -> str:
        allAlarms = [*self.cpuAlarms, *self.memAlarms, *self.dskAlarms] # Join all alarms into one array
        # Return None if empty alarms
        if len(allAlarms) == 0:
            return None
        return "".join(str(alarm)+"\n" for alarm in allAlarms).rstrip()
    
    # Below function checks if given threshold and alarm type triggers any alarms
    # Prints any found alarms
    def checkIfAlarmTrigger(self, thresholdPercent: float, alarmType : AlarmType):
        alarms = self.ALARMARRAYS[alarmType.value - 1] # Gets correct array of alarms, based on AlarmType Enum
        # alarms are sorted lower->higher so iterate over list reversed to check highest alarms first
        for alarm in reversed(alarms):
            if alarm.alarmThreshold <= thresholdPercent:
                 print(f"***** {alarmType.name}-Alarm\tThreshold: {alarm.alarmThreshold}%\tCurrent %: {thresholdPercent}\tTime: {datetime.now()} *****")
                 break
        
    # Returns true if alarms exist
    def alarmsExist(self) -> bool:
        return len([*self.cpuAlarms, *self.memAlarms, *self.dskAlarms]) > 0
    
    # Below functions return the lowest threshold active alarms, return None if doesnt exist
    def getLowestCPUAlarm(self) -> Alarm:
        if len(self.cpuAlarms) > 0:
            return self.cpuAlarms[0]
        return None
    
    def getLowestMEMAlarm(self) -> Alarm:
        if len(self.memAlarms) > 0:
            return self.memAlarms[0]
        return None
    
    def getLowestDSKAlarm(self) -> Alarm:
        if len(self.dskAlarms) > 0:
            return self.dskAlarms[0]
        return None
    
    # Attempts to remove given alarm, true if successful
    def removeAlarm(self) -> bool:
        pass