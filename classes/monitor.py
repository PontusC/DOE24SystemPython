import psutil
from psutil._common import bytes2human

class Monitor:
    
    # Singleton pattern
    _self_ = None
    def __new__(monitor):
        if monitor._self_ is None:
            monitor._self_ = super().__new__(monitor)
        return monitor._self_
    
    # Class variables
    monitoringStarted = False
    
    # CPU stats
    cpuPercent : float = None
    cpuPercentMultiple : tuple = None
    # MEM stats
    memPercent = None
    memTotal = None
    memUsed = None
    # DSK stats
    dskPercent = None
    dskTotal = None
    dskUsed = None
    
    # constants
    DSKPATHWINDOWS = "C:\\" # windows
    
    def __init__(self) -> None:
        pass
    
    # Switches monitoring to on
    def initMonitoring(self):
        if self.monitoringStarted:
            raise Exception("Already started")
        else:
            self.monitoringStarted = True
     
    # Returns formatted string containing all monitoring values       
    def printMonitorValues(self):
        def printSeparation():
            print("--------------------------------------------------------------------------")
        if not self.monitoringStarted:
            raise Exception("Monitoring not started")
        else:
            self.updateValues()
            #CPU
            print(f"CPU\t-\t{self.cpuPercent}%\t-\tCores({len(self.cpuPercentMultiple)}) \t-\t{self.cpuPercentMultiple}")
            printSeparation()
            #MEM
            print(f"MEM\t-\t{self.memPercent}%\t-\tTotal: {bytes2human(self.memTotal)+"B"}\t-\tUsed: {bytes2human(self.memUsed)+"B"}")
            #DSK
            printSeparation()
            print(f"DSK\t-\t{self.dskPercent}%\t-\tTotal: {bytes2human(self.dskTotal)+"B"}\t-\tUsed: {bytes2human(self.dskUsed)+"B"}")
            printSeparation()
        
    # Updates monitoring values
    def updateValues(self):
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
        except OSError:
            print("DSKPATH error")

    def returnCPUStr(self) -> str:
        pass
    
    def returnMEMStr(self) -> str:
        pass
    
    def returnDSKStr(self) -> str:
        pass