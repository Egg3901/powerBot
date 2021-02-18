from votegain import update_population
import time


class Main():
    def main_loop(self):
        while True:
            update_population()
            print("Population updated!")
            time.sleep(600)


program = Main()
program.main_loop()