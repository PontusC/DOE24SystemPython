from classes.menu import Menu
from classes.menu import AlarmHandler, AlarmType
import json

TESTING = True

if __name__ == '__main__':
    print("Starting...")
    if not TESTING:
        # Instantiating singletons
        menu = Menu()
        menu.clearTerminal()
        # Starting menu
        menu.runMenu()
        print("Terminating . . .")
    else:
        alarmHandler = AlarmHandler()
        for i in range(1, 5):
            alarmHandler.createAlarm(AlarmType(1), i*3)
        firstAlarm : AlarmHandler.Alarm =  alarmHandler.getAlarms()[0]
        firstAlarmJSON = json.dumps(firstAlarm.__dict__)
        print(firstAlarmJSON)
        loadedAlarm = json.loads(firstAlarmJSON)
        print(loadedAlarm)
        allAlarmsJSON = alarmHandler.alarmsToJSON()
        print(allAlarmsJSON)
        for alarm in allAlarmsJSON.splitlines():
            print(alarm)
            print(json.loads(alarm)) # dict object