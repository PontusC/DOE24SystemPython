import psutil, time, os
from classes.menu import Menu
from classes.resourceMonitor import ResourceMonitor

if __name__ == '__main__':
    print("Starting...")
    # Instantiating singletons
    menu = Menu()
    menu.clearTerminal()
    # Starting menu
    menu.runMenu()
    print("Terminating . . .")