from classes.menu import Menu

TESTING = False

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
        pass