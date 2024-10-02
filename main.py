import logging.config
from classes.menu import Menu
from classes.menu import AlarmHandler
import logging

if __name__ == '__main__':
    # Logging setup
    logFormat="%(asctime)s.%(msecs)03d:%(name)s:\"%(message)s\""
    logFilename = "logfile.log"
    logEncoding = "utf-8"
    logTimeformat = "%d/%m/%Y:%H:%M:%S"
    logLevel = logging.DEBUG
    logging.basicConfig(format=logFormat,filename=logFilename, encoding=logEncoding, level=logLevel, datefmt=logTimeformat)
    log = logging.getLogger("Main")
    log.info("Starting")
    
    TESTING = False
    
    if not TESTING:
        # Instantiating singletons
        menu = Menu()
        # Loading alarms
        AlarmHandler().loadAlarmsFromFile()
        menu.clearTerminal()
        # Starting menu
        menu.runMenu()
    else:
        pass
    log.info("Shutdown")
    logging.shutdown()