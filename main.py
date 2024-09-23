import psutil, time, os
from classes.menu import Menu

TESTING: bool = True

def run():
    print_data()
    try: 
        while True:
            print_data()
            time.sleep(1)
    except KeyboardInterrupt: # Control+C to exit
        pass
    
def print_data():
    
    # This block handles clearing the terminal to print the information on the same 3 lines
    if not hasattr(print_data, "first_loop"): # Sets up first_loop as a static variable, python version
        print_data.first_loop = True
    if not print_data.first_loop: # Doesn't need to clear first loop
        for x in range(3):
            clear_above_line()
    else:
        print_data.first_loop = False
        
    cpu:        float = psutil.cpu_percent(interval=None, percpu=False)
    mem:       float = psutil.virtual_memory().percent
    disk:       float = psutil.disk_usage("C:\\").percent

    print(f"CPU%:\t{cpu}\nMEM%:\t{mem}\nDSK%:\t{disk}")
        
# Run to clear one line above in terminal
def clear_above_line():
    LINE_UP = '\033[1A'     # ANSI-code that moves cursor up one line
    LINE_CLEAR = '\x1b[2K'  # ANSI-code that erases current line
    print(LINE_UP, end=LINE_CLEAR)


if __name__ == '__main__':
    print("Starting...")
    os.system("cls")
    if not TESTING:
        run()
    else: #Codeblock for testing code
        menu = Menu()
        menu.testprint()
        pass
    print("Terminating...")