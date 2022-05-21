from tkinter import Label
from PIL import Image, ImageTk
from assets import resource_path
from itertools import count, cycle


class LoadingPage(Label):
    def __init__(self, master):
        super().__init__(master=master, bg="#FFFFFF", highlightthickness=0)
        self.interrupt = False
        self.delay, self.frames = None, None
        self.image = Image.open(resource_path(r"assets/loading.gif"))

    def start(self):
        frames = []
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(self.image.copy()))
                self.image.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = self.image.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def next_frame(self):
        if self.interrupt:
            self.interrupt = False
            return

        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)
