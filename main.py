import multiprocessing as mp

import pynput as pn

stop = False
stop_counter = 0

W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
o = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple


def stop_programm():
    print("Stop command send..")
    global stop
    stop = True


def f(x):
    while 1:
        # ---bonus: gradually use up RAM---
        x += 10000  # linear growth; use exponential for faster ending: x *= 1.01
        y = list(range(int(x)))
        # ---------------------------------
        pass  # infinite loop, use up CPU


def on_press(key):
    global stop_counter

    try:
        if key == pn.keyboard.Key.ctrl_l:
            stop_counter = 1

        if key == pn.keyboard.Key.ctrl_r:
            stop_counter = 2

    except Exception:
        pass

    if stop_counter >= 2:
        stop_programm()


def on_release(key):
    global stop_counter

    try:
        if key == pn.keyboard.Key.ctrl_l:
            stop_counter = 0

        if key == pn.keyboard.Key.ctrl_r:
            stop_counter = 1

    except Exception:
        pass


if __name__ == '__main__':  # name guard to avoid recursive fork on Windows
    print(R + "WARNING: \n" +
          W + " -> I am not responsible for the consequences of using this program. \n"
              " -> If you continue, you agree to it. \n"
              " -> This program can produce a lot of lags on this machine. \n"
              " -> To terminate the program press the" + o + " LEFT CONTROL" + W + " and" + o + " RIGHT CONTROL " + W + "together. \n"
          )
    continue_execution = input("Would you like to continue? (" + G + "y " + W + "/" + R + " N" + W + "): ")
    if continue_execution != "y":
        exit(-1)

    listener = pn.keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    n = mp.cpu_count() * 32  # multiply guard against counting only active cores
    pool = mp.Pool(processes=n)
    pool.apply_async(f)

    while not stop:
        pass

    print("Stopping..")

    listener.stop()
    pool.terminate()

    print("Finished")
    print("You can close now this window.")
    exit(-1)
