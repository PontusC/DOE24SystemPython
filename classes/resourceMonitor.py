import psutil
from datetime import datetime
from classes.alarmMonitor import AlarmMonitor, AlarmType
# Import msvcrt on windows, getch on linux
try:
    import msvcrt as m
except ImportError:
    import getch as m # type: ignore
from psutil._common import bytes2human

class ResourceMonitor:
    
    # Singleton pattern
    _self_ = None
    def __new__(monitor):
        if monitor._self_ is None:
            monitor._self_ = super().__new__(monitor)
        return monitor._self_
    
    # Class variables
    monitoringStarted = False
    alarmMonitor = AlarmMonitor()
    cpuAlarm = None
    memAlarm = None
    dskAlarm = None
    
    # CPU stats
    cpuPercent : float = None
    cpuPercentMultiple : tuple = None
    # MEM stats
    memPercent : float = None
    memTotal : int = None
    memUsed : int = None
    # DSK stats
    dskPercent : float = None
    dskTotal : int = None
    dskUsed : int = None
    
    # constants
    DSKPATHWINDOWS = "C:\\" # windows
    DSKPATHWSL = "/mnt/c/" # WSL
    
    def __init__(self) -> None:
        pass
    
    # Switches monitoring to on
    def initMonitoring(self):
        if self.monitoringStarted:
            raise Exception("Already started")
        else:
            self.monitoringStarted = True
     
    # Returns formatted string containing all monitoring values       
    def returnMonitorValues(self) -> str:
        separationStr = "\n--------------------------------------------------------------------------"
        strByteSuffix = 'B' # Appended to say GB instead of just G
        if not self.monitoringStarted:
            raise Exception("Monitoring not started")
        else:
            self.updateValues()
            #CPU
            cpuStr = f"CPU\t-\t{self.cpuPercent}%\t-\tCores({len(self.cpuPercentMultiple)}) \t-\t{self.cpuPercentMultiple}{separationStr}"
            #MEM
            memStr = f"\nMEM\t-\t{self.memPercent}%\t-\tTotal: {bytes2human(self.memTotal)+strByteSuffix}\t-\tUsed: {bytes2human(self.memUsed)+strByteSuffix}{separationStr}"
            #DSK
            dskStr = f"\nDSK\t-\t{self.dskPercent}%\t-\tTotal: {bytes2human(self.dskTotal)+strByteSuffix}\t-\tUsed: {bytes2human(self.dskUsed)+strByteSuffix}{separationStr}"
            return "".join([cpuStr, memStr, dskStr])
        
    # Updates monitoring values
    def updateValues(self):
        # This function should be the one to raise exception if not initialized
        #CPU
        self.cpuPercent = psutil.cpu_percent(interval=0.1, percpu=False)
        self.cpuPercentMultiple = psutil.cpu_percent(interval=0.1, percpu=True)
        #MEM
        self.memPercent = psutil.virtual_memory().percent
        self.memTotal = psutil.virtual_memory().total
        self.memUsed = self.memTotal - psutil.virtual_memory().available
        #DSK
        try:
            self.dskPercent = psutil.disk_usage(self.DSKPATHWINDOWS).percent
            self.dskTotal = psutil.disk_usage(self.DSKPATHWINDOWS).total
            self.dskUsed = self.dskTotal - psutil.disk_usage(self.DSKPATHWINDOWS).free
        except OSError: # Throws error if running on WSL
            self.dskPercent = psutil.disk_usage(self.DSKPATHWSL).percent
            self.dskTotal = psutil.disk_usage(self.DSKPATHWSL).total
            self.dskUsed = self.dskTotal - psutil.disk_usage(self.DSKPATHWSL).free
            
    # Prints any alarms triggered and time
    def checkForAlarms(self):
        self.updateValues()
        currentTime = datetime.now()
        # Check CPU
        if not self.cpuAlarm == None and self.cpuPercent >= float(self.cpuAlarm.alarmThreshold):
            print(f"***** CPU-Alarm\tThreshold: {self.cpuAlarm.alarmThreshold}%\tCurrent %: {self.cpuPercent}\tTime: {currentTime} *****")
        # Check MEM
        if not self.memAlarm == None and self.memPercent >= float(self.memAlarm.alarmThreshold):
            print(f"***** MEM-Alarm\tThreshold: {self.memAlarm.alarmThreshold}%\tCurrent %: {self.memPercent}\tTime: {currentTime} *****")
        # Check DSK
        if not self.dskAlarm == None and self.dskPercent >= float(self.dskAlarm.alarmThreshold):
            print(f"***** DSK-Alarm\tThreshold: {self.dskAlarm.alarmThreshold}%\tCurrent %: {self.dskPercent}\tTime: {currentTime} *****")
       
    # Ran once before entering monitoring mode and checking for alarms to set the alarmvalues
    # Raises exception if no alarms created yet
    def setAlarms(self):
        self.cpuAlarm = self.alarmMonitor.getLowestCPUAlarm()
        self.memAlarm = self.alarmMonitor.getLowestMEMAlarm()
        self.dskAlarm = self.alarmMonitor.getLowestDSKAlarm()
        if self.cpuAlarm is None and self.memAlarm is None and self.dskAlarm is None:
            raise Exception("No alarms created")

    def returnCPUStr(self) -> str:
        pass
    
    def returnMEMStr(self) -> str:
        pass
    
    def returnDSKStr(self) -> str:
        pass