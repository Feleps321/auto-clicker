import time
from datetime import datetime, timedelta
from pymouse import PyMouse, PyMouseEvent
import threading

__version__ = "0.0.1"

mouse = PyMouse()

clicks = []

new_click = False
capture = [0, 0, 1]

class mouse_event(PyMouseEvent):
    def move(self, x, y):
        pass
    
    def click(self, x, y, button, press):
        global new_click, capture

        if press:
            new_click = True
            capture = [x, y, button]


def main():
    global clicks, new_click

    e = mouse_event()
    e.capture = False
    e.daemon = False
    e.start()

    x = threading.Thread(target=thread_function, args=())
    x.start()

    print("auto-clicker", __version__)
    print("[1]: manual input")
    print("[2]: mouse capture")

    while True:
        try:
            print()

            click_time_str = input("Enter click time (YYYY-mm-dd HH:mm:SS): ")
            click_time = datetime.strptime(click_time_str, "%Y-%m-%d %H:%M:%S")
            
            input_mode = int(input("Enter input mode (1/2): "))

            click_data = [0, 0, 1]

            if input_mode == 1:
                click_data_str = input("Enter click (x, y, button): ").split(",")
                click_data[0] = int(click_data_str[0])
                click_data[1] = int(click_data_str[1])
                click_data[2] = int(click_data_str[2])
            
            elif input_mode == 2:
                print("Waiting for click")

                new_click = False

                while new_click == False:
                    time.sleep(0.1)

                click_data = capture.copy()
            
            else:
                raise Exception("Invalid input mode")
            
            add_click(click_time, click_data)

        except Exception as e:
            print("Error: ", e)

def add_click(click_time, click_data):
    clicks.append([click_time, click_data])
    clicks.sort(key=compare)


def compare(e):
    return e[0]

def thread_function():
    global clicks

    while True:
        now = datetime.now()

        if(len(clicks) > 0 and now >= clicks[0][0]):
            click_data = clicks[0][1]
            clicks.remove(clicks[0])

            mouse.click(*click_data)


if __name__ == '__main__':
    main()