#!/usr/bin/env python3

import sys, datetime, threading, time, shutil, hashlib
from Key import Key
from Display import Display
from Simulation import Simulation

class Main:
    def __init__(self):
        self.cuteloading = None
        self.asynckey = None
        try:
            sys.stdout.write(Display.screen(True) + Display.cursor(False))
            sys.stdout.flush()

            width, height = shutil.get_terminal_size((80, 20))

            self.key = Key()
            self.asynckey = threading.Thread(target=self.key.storechar, args=(), daemon=False)
            self.asynckey.start()
            self.time = time.time()

            self.cuteloading = threading.Thread(target=Display.startloading, args=(width,), daemon=False)
            self.cuteloading.start()
            Display.setdisplay(width - 1, height)

            self.now = datetime.datetime.now()

            Display.setstring("This is a test string!\nAnd this is as well!\n\nOk...")
            Display.stoploading(self.cuteloading)
            self.key.settrackkeys(True)
            self.main()
        finally:
            Display.stoploading(self.cuteloading)
            Key.close()
            self.asynckey.join()
            sys.stdout.write(Display.screen(False) + Display.cursor(True))
            sys.stdout.flush()

    def main(self):
        self.sim = Simulation.fromfile("test.sim")
        self.display()

        while True:
            new_time = time.time()
            time.sleep(max(0, 0.01 - new_time + self.time))
            self.time = new_time

            char = self.key.asyncgetchar()

            if not char:
                continue

            if char in ["\x1b", "\x03", "\t", "x"]:
                break

    def display(self):
        Display.clear()
        string = self.sim.getstring()
        # assert False, string
        Display.setstring(string)
        display = Display.outputdisplay()
        sys.stdout.write(display)
        sys.stdout.flush()

if __name__ == "__main__":
    Main() 
