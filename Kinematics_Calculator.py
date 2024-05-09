# Kinematics Calculator
# Created by: Khen Jomarie L. Alcantara
# Degree: BS Electronics And Communication Engineering
# Level: 1st Year

# Import library
import os
import ctypes
from ctypes import wintypes
import sys

# Initialize variable
columns = 0


# Function for requesting administration
def run_as_administrator():
    # Checking current console if not running as administrator
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, os.path.basename(__file__), None, 1)
        sys.exit()


# Function for single instance console application
def is_single_instance(_title):
    # Define necessary Windows types
    lpctstr = ctypes.c_wchar_p

    # Create a mutex
    mutex_handle = ctypes.windll.kernel32.CreateMutexW(None, True, lpctstr(_title))

    # Check if the mutex already exists
    if ctypes.windll.kernel32.GetLastError() == 183 or mutex_handle is None:  # ERROR_ALREADY_EXISTS = 183

        # Find the window by title
        hwnd = ctypes.windll.user32.FindWindowW(None, lpctstr(_title))

        # Bring the window to the foreground
        if hwnd != 0:
            ctypes.windll.user32.ShowWindow(hwnd, 1)  # If console is in minimize it will show
            ctypes.windll.user32.SetForegroundWindow(hwnd)

        return False

    return True


# Function for assigning console title
def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)


# Function for resizing console
def set_console_size(width: int, height: int):
    os.system(f"mode con cols={width} lines={height}")


# Function for aligning console to center windows
def center_console_window():
    # Define necessary constants
    gwl_style = -16
    ws_size_box = 0x00040000
    ws_maximize_box = 0x00010000

    # Get handle to the console window
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()

    # Get current style
    style = ctypes.windll.user32.GetWindowLongW(hwnd, gwl_style)

    # Restore console style
    original_style = style | ws_size_box | ws_maximize_box
    ctypes.windll.user32.SetWindowLongW(hwnd, gwl_style, original_style)

    # Get screen dimensions
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    # Get dimensions of the console window
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    console_width = rect.right - rect.left
    console_height = rect.bottom - rect.top

    # Calculate new position
    x = (screen_width - console_width) // 2
    y = (screen_height - console_height) // 2

    # Set console window position
    ctypes.windll.user32.MoveWindow(hwnd, x, y, console_width, console_height, True)

    # Update console style to disable resizing of console
    new_style = style & ~ws_size_box & ~ws_maximize_box
    ctypes.windll.user32.SetWindowLongW(hwnd, gwl_style, new_style)


# Function for clearing/deleting a line
def clear(line):
    for _ in range(line):
        print("\x1b[1A\x1b[2K", end="\r")


def int_input(_prompt: str):
    while True:
        try:
            input_int = int(input(_prompt))
            return input_int
        except ValueError:
            clear(1)
            continue


def float_input(_prompt: str):
    while True:
        try:
            input_int = float(input(_prompt))
            return input_int
        except ValueError:
            clear(1)
            continue


def displacement(x1, x2):
    return x2 - x1


def time_interval(t1, t2):
    return t2 - t1


def ave_velocity(_displacement, _time_interval):
    try:
        average_velocity = displacement(_displacement, _time_interval)
        return average_velocity
    except ZeroDivisionError:
        return 0


# Main Function
def main():
    # Title
    print("╔" + "═" * 78 + "╗")
    print(f"║{"KINEMATICS CALCULATOR":^78}║")
    print("╚" + "═" * 78 + "╝")

    # Option
    print("      TOPICS:")
    print("         [1] Displacement, Time Interval, and Average Velocity")
    print("         [2] Instantaneous Velocity")
    print("         [3] Average and Instantaneous Acceleration")
    print("         [4] Constant Acceleration")
    print("         [5] Free Fall")
    print("         [6] Finding Velocity and Displacement from Acceleration")
    print("         [0] Exit\n")

    while True:
        choice = int_input("      Select a topic: ")
        if choice in range(0, 7):
            clear(10)
            if choice == 1:
                Displacement_TimeInterval_AverageVelocity()
            break
        else:
            clear(1)
            continue

    print("\n", end="")
    while True:
        choice = input("      Select [Y] to exit or [N] to continue: ").upper()
        if choice == "y".upper():
            exit()
        elif choice == "n".upper():
            clear(100)
            return main()
        else:
            clear(1)
            continue


def Displacement_TimeInterval_AverageVelocity():
    print("Displacement, Time Interval, and Average Velocity".upper().center(columns))
    print("      Displacement:")
    x1 = float_input("         Initial position(m): ")
    x2 = float_input("         Final position(m)  : ")
    print(("-" * 68).center(columns))
    print("      Time Interval:")
    t1 = float_input("         Initial time(s)    : ")
    t2 = float_input("         Final time(s)      : ")
    print(("-" * 68).center(columns))

    print("ANSWER".center(columns))
    print(f"         Displacement     : {displacement(x1, x2)}m")
    print(f"         Time Interval    : {time_interval(t1, t2)}s")
    print(f"         Average Velocity : {ave_velocity(displacement(x1, x2), time_interval(t1, t2))}m/s")


if __name__ == "__main__":
    # Title of console
    console_title = "Kinematics Calculator"

    run_as_administrator()  # Request for administration privilege

    # Check for single instances
    if not is_single_instance(console_title):
        exit()

    set_console_title(console_title)  # Set the title of console
    set_console_size(80, 40)  # Resizing of console
    columns = os.get_terminal_size().columns  # Save the new column size
    center_console_window()  # Align the console to center
    main()
