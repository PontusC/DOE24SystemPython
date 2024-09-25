from enum import Enum
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
        
        alarmThreshold = None
        
        def __init__(self, threshold: int, type : AlarmType):
            self.alarmThreshold = threshold
            self.alarmType = type
        
        # Returns true if self object has lower threshold of alarm
        def __lt__(self, other) -> bool:
            return self.alarmThreshold <= other.alarmThreshold
    
    # Singleton pattern
    _self_ = None
    def __new__(alarm):
        if alarm._self_ is None:
            alarm._self_ = super().__new__(alarm)
        return alarm._self_
    
    # Class variables
    
    def __init__(self) -> None:
        self.alarmCPU = []
        self.alarmMEM = []
        self.alarmDSK = []
        
    # Creates alarm of given type and threshold
    def setAlarm(self, type : AlarmType, threshold : int):
        newAlarm = self.Alarm(threshold, type)
        match type:
            case 1: # Matches ENUM to it's value, CPU = 1 etc...
                bisect.insort(self.alarmCPU, newAlarm)
            case 2:
                bisect.insort(self.alarmMEM, newAlarm)
            case 3:
                bisect.insort(self.alarmDSK, newAlarm)
    
    # Attempts to remove given alarm, true if successful
    def removeAlarm(self) -> bool:
        pass