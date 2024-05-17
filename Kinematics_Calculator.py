# Kinematics Calculator
# Created by: Khen Jomarie L. Alcantara
# Degree: BS Electronics And Communication Engineering
# Level: 1st Year
import fractions
# Import library
import os
import ctypes
from ctypes import wintypes
import sys
import sympy

# Initialize variable
columns = 0
topics = {
    1: "Displacement, Time Interval, and Average Velocity",
    2: "Instantaneous Velocity",
    3: "Average and Instantaneous Acceleration",
    4: "Constant Acceleration",
    5: "Free Fall",
    6: "Finding Velocity and Displacement from Acceleration"
}
p_i, p_f, v_i, v_f, a, t = sympy.symbols('p_i p_f v_i v_f a t')


class Kinematic:

    Given = {}

    Unknown = []

    Equation = {
        1: sympy.Eq(v_f, v_i + a * t),
        2: sympy.Eq(p_f - p_i, v_i * t + 0.5 * a * t**2),
        3: sympy.Eq(v_f**2, v_i**2 + 2 * a * (p_f - p_i)),
        4: sympy.Eq(p_f - p_i, 0.5 * (v_i + v_f) * t)
    }

    Answer = {}


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
        average_velocity = _displacement / _time_interval
        return average_velocity
    except ZeroDivisionError:
        return 0


def instantaneous_velocity(_equation, _time):
    derivative = sympy.diff(_equation, t)
    return round(float(derivative.subs(t, _time)), 2)


# Main Function
def main():
    # Title
    print("╔" + "═" * 78 + "╗")
    print(f"║{"KINEMATICS CALCULATOR":^78}║")
    print("╚" + "═" * 78 + "╝")

    # Option
    print("      TOPICS:")
    for key, topic in topics.items():
        print(f"         [{key}] {topic}")

    print("         [0] Exit\n")

    selection = False
    while not selection:
        select = int_input("      Select a topic: ")
        clear(10)
        for key, topic in topics.items():
            if key == select:
                print(topic.upper().center(columns))
                _topic = (topic.replace(" from ", "_from_").replace(", and ", "_").replace(", ", "_")
                          .replace(" ", "").replace("and", "_"))
                print("")
                globals()[_topic]()
                selection = True
                break
        else:
            clear(1)
            continue

    print("\n\n", end="")
    print(("-" * 68).center(columns))
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
    print("      Displacement:")
    x1 = float_input("         Initial position(m): ")
    x2 = float_input("         Final position(m)  : ")
    print(("-" * 68).center(columns))
    print("      Time Interval:")
    t1 = float_input("         Initial time(s)    : ")
    t2 = float_input("         Final time(s)      : ")

    print("")
    print(("-" * 68).center(columns))
    print("ANSWER\n".center(columns))
    print(f"         Displacement     : {displacement(x1, x2)}m")
    print(f"         Time Interval    : {time_interval(t1, t2)}s")
    print(f"         Average Velocity : {ave_velocity(displacement(x1, x2), time_interval(t1, t2))}m/s")


def InstantaneousVelocity():
    expression = 0
    while True:
        try:
            equation = input("      Enter the equation (20 + 5*t^2): ")
            equation = equation.replace("^", "**")
            expression = sympy.sympify(equation)
            break
        except TypeError:
            clear(1)
            continue
        except sympy.SympifyError:
            clear(1)
            continue

    time = float_input("      Enter the time(s)              : ")

    print("")
    print(("-" * 68).center(columns))
    print("ANSWER\n".center(columns))
    print(f"      Instantaneous Velocity: {instantaneous_velocity(expression, time)}m/s")


def Average_InstantaneousAcceleration():
    print("test")


def ConstantAcceleration():
    print("      Enter all the given (leave it blank if not given, or "'"?"'" if unknown): ")

    for var, symbol in zip(["Initial position(m)", "Final position(m)", "Initial velocity(m/s)", "Final velocity(m/s)",
                            "Acceleration(m/s²)", "Time(s)"], [p_i, p_f, v_i, v_f, a, t]):
        while True:
            user_input = input(f"         {var:<22}: ")
            try:
                if user_input:
                    if user_input == "?":
                        if p_i not in Kinematic.Unknown:
                            Kinematic.Unknown.append(symbol)
                            break
                        elif p_f not in Kinematic.Given:
                            if p_i not in Kinematic.Unknown:
                                Kinematic.Given[symbol] = user_input
                                break
                            else:
                                clear(1)
                                continue
                        else:
                            Kinematic.Unknown.append(symbol)
                            break
                    Kinematic.Given[symbol] = float(user_input)
                    break
                else:
                    if p_f not in Kinematic.Given and p_i not in Kinematic.Unknown:
                        break
                    else:
                        clear(1)
            except ValueError:
                clear(1)

    if p_i in Kinematic.Unknown:
        if v_i in Kinematic.Unknown:
            Kinematic.Answer[v_i] = sympy.solve(Kinematic.Equation[1].subs(Kinematic.Given), v_i)[0]
            Kinematic.Given[v_i] = Kinematic.Answer[v_i]

        Kinematic.Answer[p_i] = sympy.solve(Kinematic.Equation[2].subs(Kinematic.Given), p_i)[0]

    print(Kinematic.Unknown)
    print(Kinematic.Given)

    print("")
    print(("-" * 68).center(columns))
    print("ANSWER\n".center(columns))
    for var in Kinematic.Unknown:
        if var == p_i:
            print(f"      Initial position: {Kinematic.Answer[p_i]}")
        elif var == p_f:
            print(f"      Final position:")
        elif var == v_i:
            print(f"      Initial velocity: {Kinematic.Answer[v_i]}")
        elif var == v_f:
            print(f"      Final velocity:")
        elif var == a:
            print(f"      Acceleration:")
        elif var == t:
            print(f"      Time:")


def FreeFall():
    print("Free_Fall")


def convert_to_fraction(expression):
    expression = sympy.sympify(expression)
    coefficients = expression.as_coefficients_dict()
    fraction_coefficients = {var: fractions.Fraction(str(coe)).limit_denominator() for var, coe in
                             coefficients.items()}
    return sum(frac * var for var, frac in fraction_coefficients.items())


def FindingVelocity_Displacement_from_Acceleration():
    print("      Select an option you want to solve:")
    print("         [1] Velocity and Displacement")
    print("         [2] Time at Maximum Velocity and Maximum Displacement")
    print("")

    while True:
        select = input("      Select: ")
        print(("-" * 68).center(columns))
        if select == "1":
            print("Solve for Velocity and Displacement".center(columns))
            break
        elif select == "2":
            print("Solve for Time at Maximum Velocity and Maximum Displacement".center(columns))
            break
        else:
            clear(2)

    print("")
    while True:
        try:
            print("         Sample equation: (1.50 * t) - (0.120 * t^2)")
            equation = input("         Enter the acceleration equation: ")
            equation = equation.replace("^", "**")
            equation = sympy.sympify(equation)

            if equation.free_symbols == {t}:
                break
            else:
                clear(2)
        except TypeError:
            clear(2)
        except sympy.SympifyError:
            clear(2)

    x = sympy.Symbol("x")
    v = sympy.Symbol("v")
    c = sympy.Symbol("c")

    print("")
    given_velocity = None
    given_v_time = None
    at_v_time = None
    max_velocity = None
    given_position = None
    given_p_time = None
    at_p_time = None
    max_position = None
    while True:
        try:
            if given_velocity is None:
                given_velocity = float(input("         Enter the given velocity(m/s)          : "))

            if given_v_time is None:
                given_v_time = float(input("         Enter the given time(s) of velocity    : "))

            if select == "1":
                if at_v_time is None:
                    at_v_time = float(input("         Get the velocity at what time(s)?      : "))
                    print("")
            elif select == "2":
                if max_velocity is None:
                    max_velocity = float(input("         Enter the maximum velocity(m/s)        : "))
                    print("")

            if given_position is None:
                given_position = float(input("         Enter the given position(m)            : "))

            if given_p_time is None:
                given_p_time = float(input("         Enter the given time(s) of position    : "))

            if select == "1":
                if at_p_time is None:
                    at_p_time = float(input("         Get the displacement at what time(s)?  : "))
            elif select == "2":
                if max_position is None:
                    max_position = float(input("         Enter the maximum position(m)          : "))
            break
        except ValueError:
            clear(1)

    first_integration = sympy.integrate(equation, t)
    velocity_equation = sympy.Eq(v, first_integration + c)
    c_velocity = sympy.solve(velocity_equation.subs({v: given_velocity, t: given_v_time}), c)[0]
    velocity_function = sympy.Eq(v, first_integration + c_velocity)

    second_integration = sympy.integrate(velocity_function.rhs, t)
    displacement_function = sympy.Eq(x, second_integration + c)
    c_displacement = sympy.solve(displacement_function.subs({x: given_position, t: given_p_time}), c)[0]
    displacement_function = sympy.Eq(x, second_integration + c_displacement)

    formatted_velocity_function = f"v = {convert_to_fraction(velocity_function.rhs)}"
    formatted_displacement_function = f"x = {convert_to_fraction(displacement_function.rhs)}"

    print("")
    print(("-" * 68).center(columns))
    print("ANSWER\n".center(columns))
    print(f"         Velocity function      : {str(formatted_velocity_function).replace("**", "^")}")
    print(f"         Displacement function  : {str(formatted_displacement_function).replace("**", "^")}")

    if select == "1":
        _velocity = round(float(sympy.solve(velocity_function.subs({t: at_v_time}), v)[0]), 2)
        _displacement = round(float(sympy.solve(displacement_function.subs({t: at_p_time}), x)[0]), 2)

        print(f"         Velocity at {f"{at_v_time}"+"s":<11}: {_velocity}m/s")
        print(f"         displacement at {f"{at_p_time}"+"s":<7}: {_displacement}m")
    elif select == "2":
        v_time = sympy.solve(velocity_function.subs({v: max_velocity}), t)
        d_time = sympy.solve(displacement_function.subs({x: max_position}), t)

        v_total_time = ", ".join(f"{x}s" for x in [round(float(time), 2)
                                                   for time in v_time if time.is_real and time > 0])
        p_total_time = ", ".join(f"{x}s" for x in [round(float(time), 2)
                                                   for time in d_time if time.is_real and time > 0])
        if not p_total_time:
            p_total_time = ", ".join(f"{x}s" for x in [round(float(time.as_real_imag()[0]), 2) for time in d_time])

        print(f"         Time at max velocity is    : {v_total_time}")
        print(f"         Time at max displacement is: {p_total_time}")


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
