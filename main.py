from tkinter import Tk, PhotoImage
from tkinterdnd2 import Tk

from menuBar import MenuBar
from loadingPage import LoadingPage
from mainPage import MainPage

from yoloModel import YoloModel
from assets import *


class App(Tk):
    def __init__(self):
        super().__init__()
        self.monitor = 'primary'
        # self.monitor = 'secondary'

        self.os = get_os()

        self.title("Mi Yolo")
        self.iconphoto(False, PhotoImage(file=resource_path('assets/icon.png')))

        x, y = get_monitor_center(self.monitor)
        self.geometry(f'300x430+{x-150}+{y-215}')
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.terminate)

        self.model = YoloModel()

        MenuBar(self)

        self.loadingPage = LoadingPage(self)
        self.start_loading_screen()
        ThreadedTask(MainPage, self)

    def start_loading_screen(self):
        self.loadingPage.interrupt = False
        self.loadingPage.pack(expand=1, fill="both")
        self.loadingPage.start()

    def stop_loading_screen(self):
        self.loadingPage.pack_forget()
        self.loadingPage.interrupt = True

    def start(self):
        self.mainloop()

    def terminate(self):
        sys.exit()


if __name__ == "__main__":
    App().start()
