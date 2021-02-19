from votegain import update_population
import time


class Main():
    def main_loop(self):
        while True:
            start_time = time.time()
            update_population()
            time_elapsed = time.time() - start_time
            print(f"Population updated in {time_elapsed} seconds!")
            time.sleep(300-time_elapsed)
            print("Scraping in 5 minutes.")
            time.sleep(300)


program = Main()
program.main_loop()