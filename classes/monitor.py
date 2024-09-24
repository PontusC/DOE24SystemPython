import psutil

class Monitor:
    
    # Singleton pattern
    _self_ = None
    def __new__(monitor):
        if monitor._self_ is None:
            monitor._self_ = super().__new__(monitor)
        return monitor._self_
    
    # Class variables
    monitoringStarted = False
    
    currentCPU : float = None
    currentMEM = None
    currentDSK = None
    
    def __init__(self) -> None:
        pass
    
    # Switches monitoring to on
    def initMonitoring(self):
        if self.monitoringStarted:
            raise Exception("Already started")
        else:
            self.monitoringStarted = True
     
    # Returns formatted string containing all monitoring values       
    def returnMonitoringValues(self) -> str:
        if not self.monitoringStarted:
            raise Exception("Monitoring not started")
        else:
            pass