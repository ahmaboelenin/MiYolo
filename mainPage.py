from tkinter import Canvas, Entry, Button, messagebox, filedialog
from tkinterdnd2 import DND_FILES

from assets import *


def browse_file():
    """This Function Open File Dialog to Read the New Image."""
    currdir = os.getcwd()
    filename = filedialog.askopenfilename(initialdir=currdir, title="Select a File",
                                          filetypes=(
                                              ("Media files", "*.jpeg *.jpg *.png *.svg *.webp"
                                                              " *.mp4 *.avi"),
                                              ("all files", "*.*")))
    return filename


class Media:
    def __init__(self, content, type_, height, width):
        self.content = content
        self.type = type_
        self.height = height
        self.width = width


class MiButton(Button):
    def __init__(self, parent, image, command, x, y, width, height, state="normal"):
        image = ImageTk.PhotoImage(Image.open(resource_path(image)))
        super().__init__(parent, image=image, command=command, state=state, borderwidth=0, highlightthickness=0,
                         relief="flat")
        self.img = image
        self.place(x=x, y=y, width=width, height=height)

    def change_state(self, state):
        self.config(state=state)


class MainPage(Canvas):
    def __init__(self, master):
        super().__init__(master=master, bg="#FFFFFF", highlightthickness=0)
        """____Model____"""
        self.model = self.master.model

        """____Vars____"""
        self.link = None
        self.media = None

        """____Controller____"""
        self.interrupt = False
        self.pause = False

        """____Interface_Elements____"""
        self.imagebox = None
        self.imageContainer = None
        self.linkEntry = None
        self.saveButton = None
        self.replayButton = None
        self.stopButton = None
        self.playButton = None
        self.pauseButton = None

        """____Initialize_Interface____"""
        x, y, width, height = get_monitor_info(self.master.monitor)

        self.initialize_image_box(width, height)
        self.initialize_tool_box(width, height)

        sleep(0.2)
        self.master.stop_loading_screen()
        self.config_geometry(x, y, width, height)
        self.pack(expand=1, fill='both')
        self.imageContainer = self.imagebox.create_image(self.imagebox.winfo_width() / 2,
                                                         self.imagebox.winfo_height() / 2, image="", anchor='center')

    def config_geometry(self, x, y, width, height):
        self.master.geometry(f'{width}x{height}+{x}+{y}')

        # self.master.resizable(True, True)
        # self.master.bind('<Configure>', self.resize)

    def resize(self, event):
        pass

    def initialize_image_box(self, width, height):
        self.imagebox = Canvas(self, bg="#F1F5F5", highlightthickness=0, cursor="arrow")
        self.imagebox.place(x=10, y=10, width=width-270, height=height-80)

        self.imagebox.drop_target_register(DND_FILES)
        self.imagebox.dnd_bind('<<Drop>>', self.drop)
        self.imagebox.bind('<Button-3>', self.reset_canvas)
        self.imagebox.bind('<Button-1>', lambda event: self.imagebox.scan_mark(event.x, event.y))
        self.imagebox.bind('<B1-Motion>', lambda event: self.imagebox.scan_dragto(event.x, event.y, gain=1))
        '''
        self.imScale, self.delta = 1.0, 0.75
        if self.os == 'win':
            self.imagebox.bind('<MouseWheel>', self.wheel)
        else:
            self.imagebox.bind("<Button-4>", self.wheel)
            self.imagebox.bind("<Button-5>", self.wheel)'''

    def initialize_tool_box(self, width, height):
        x1 = width-250
        height = height - 80

        """____Tool_Box____"""
        image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/image.png")))
        self.image = image
        self.create_image(width-250, 10, image=image, anchor='nw')

        image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/group.png")))
        self.image2 = image
        self.create_image(x1, height-305, image=image, anchor='nw')

        self.create_text(width-125, height - 34, text=" - ", tags='actual', anchor='nw')
        self.create_text(width - 125, height - 4, text=" - ", tags='view', anchor='nw')

        self.linkEntry = Entry(self, text="", font=("Inter", 15 * -1), bd=0, bg="#F1F5F5", highlightthickness=0)
        self.linkEntry.place(x=width - 245, y=height-280, width=230, height=32)
        self.linkEntry.bind("<Return>", self.get_button)

        """____Buttons____"""
        MiButton(self, r"assets/get_button.png", command=self.get_button, x=x1, y=height-234, width=240, height=40)
        MiButton(self, r"assets/browse_button.png", command=self.browse_button, x=x1, y=height-184, width=240, height=40)

        self.saveButton = MiButton(self, image=r"assets/save_button.png", command=self.save_button,
                                   x=x1, y=height-134, width=240, height=40, state='disabled')

        self.pauseButton = MiButton(self, image=r"assets/pause_button.png", command=self.pause_video_button,
                                    x=x1, y=height-84, width=55, height=40, state='disabled')
        self.playButton = MiButton(self, image=r"assets/play_button.png", command=self.play_video_button,
                                   x=width-190, y=height-84, width=55, height=40, state='disabled')
        self.stopButton = MiButton(self, image=r"assets/stop_button.png", command=self.stop_video_button,
                                   x=width-125, y=height-84, width=55, height=40, state='disabled')
        self.replayButton = MiButton(self, image=r"assets/replay_button.png", command=self.replay_video_button,
                                     x=width-65, y=height-84, width=55, height=40, state='disabled')

    """____Canvas_Functions____"""

    def reset_canvas(self, event=None):
        self.imScale, self.delta = 1.0, 0.75
        self.imagebox.scan_dragto(0, 0, gain=1)
        self.imagebox.configure(scrollregion=self.imagebox.bbox("all"))

    def wheel(self, event):
        """Zoom with mouse wheel"""
        x = self.imagebox.canvasx(event.x)
        y = self.imagebox.canvasy(event.y)

        scale = 1.0
        if event.num == 5 or event.delta == -120:  # scroll down, zoom out, smaller
            scale *= self.delta
            self.imScale *= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up, zoom in, bigger
            if self.imScale > 2:
                return
            scale /= self.delta
            self.imScale /= self.delta

        # Rescale all canvas objects
        self.imagebox.scale('all', x, y, scale, scale)
        self.imagebox.configure(scrollregion=self.imagebox.bbox("all"))

        image = self.imagebox.img
        print(image)
        height, width = image.height(), image.width()
        new_size = int(self.imScale * width), int(self.imScale * height)
        image = ImageTk.PhotoImage(image.resize(new_size))
        self.show(image)

    """____Drag_n_Drop_Functions____"""

    def drop(self, event):
        self.link = str(event.data)
        if self.link[0] == '{':
            self.link = self.link[1:]
        if self.link[-1] == '}':
            self.link = self.link[0:-1]
        ThreadedTask(self.prepare)

    """____Buttons_Functions____"""

    def get_button(self, event=None):
        link = self.linkEntry.get()
        if link == "":
            return
        self.link = link
        ThreadedTask(self.prepare)

    def browse_button(self):
        link = browse_file()
        if not link:
            return
        self.link = link
        self.prepare()

    def save_button(self):
        if self.media.type == 'image':
            path = filedialog.asksaveasfilename(initialfile='Untitled.jpg', defaultextension=".jpg",
                                                filetypes=[("jpg Image", "*.jpg"), ("jpeg Image", "*.jpeg"),
                                                           ("All Files", "*.*")])
        else:
            path = filedialog.asksaveasfilename(initialfile='Untitled.avi', defaultextension=".avi",
                                                filetypes=[("avi Video", "*.avi"), ("All Files", "*.*")])
        if not path:
            return
        self.save(path)

    def pause_video_button(self):
        self.pause = True
        self.pauseButton.change_state('disabled')
        self.playButton.change_state('normal')

    def play_video_button(self):
        self.pause = False
        self.playButton.change_state('disabled')
        self.pauseButton.change_state('normal')

    def stop_video_button(self):
        self.pauseButton.change_state('disabled')
        self.playButton.change_state('disabled')
        self.stopButton.change_state('disabled')
        self.replayButton.change_state('normal')
        self.interrupt = True

    def replay_video_button(self):
        self.pauseButton.change_state('normal')
        self.playButton.change_state('disabled')
        self.stopButton.change_state('disabled')
        self.replayButton.change_state('disabled')
        self.interrupt = False
        ThreadedTask(self.replay_video)

    """____Prepare_Functions____"""

    def enable_video_buttons(self):
        self.pauseButton.change_state('normal')
        self.playButton.change_state('disabled')
        self.stopButton.change_state('normal')
        self.replayButton.change_state('disabled')

    def disable_video_buttons(self):
        self.pauseButton.change_state('disabled')
        self.playButton.change_state('disabled')
        self.stopButton.change_state('disabled')
        self.replayButton.change_state('disabled')

    def end_video_buttons(self):
        self.saveButton.change_state('normal')
        self.pauseButton.change_state('disabled')
        self.stopButton.change_state('disabled')
        self.replayButton.change_state('normal')

    def prepare(self):
        try:
            media_type, media = get_media(self.link)
            if media_type == 'unsupported-url':
                messagebox.showwarning("Warning", "Unsupported URL.")
                return
            elif media_type == 'unsupported-file':
                messagebox.showwarning("Warning", "Unsupported File.")
                return
        except ValueError as error:
            messagebox.showwarning("Warning", f"{str(error)}")
            return
        except TypeError as error:
            messagebox.showwarning("Warning", f"{str(error)}.")
            return
        except RuntimeError as error:
            messagebox.showwarning("Warning", f"{str(error)}.")
            return

        self.pause = False
        self.interrupt = True
        while True:
            if len(enumerate()) <= 2:
                break
            sleep(0.1)

        if media_type == 'video':
            self.enable_video_buttons()
            ThreadedTask(self.run_on_video, media)
        else:
            self.disable_video_buttons()
            ThreadedTask(self.run_on_image, media)

    """____Media_Functions____"""

    def run_on_image(self, image):
        original_height, original_width = image.shape[:2]

        chk = check_frame_shape(original_height, original_width, self.master.monitor)
        if chk is not None:
            width, height = chk
            image = cv2.resize(image, (width, height))
        else:
            width, height = original_width, original_height

        image = self.detect(image)
        if image is None:
            messagebox.showwarning("Warning", "Error in Loading Image.")
            return

        self.edit_shape(f"{original_width} x {original_height}", f"{width} x {height}")
        self.show(image)

        self.media = Media(image, 'image', original_height, original_width)
        self.saveButton.change_state(state='normal')

    def run_on_video(self, media):
        try:
            assert media.isOpened()
        except:
            messagebox.showwarning("Warning", "Error in Loading Video.")
            return

        self.interrupt = False
        video = []

        original_height, original_width = int(media.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(media.get(cv2.CAP_PROP_FRAME_WIDTH))

        chk = check_frame_shape(original_height, original_width, self.master.monitor)
        if chk is not None:
            width, height = chk
        else:
            width, height = original_width, original_height

        self.edit_shape(f"{original_width} x {original_height}", f"{width} x {height}")

        while True:
            ret, frame = media.read()
            if not ret or self.interrupt:
                self.end_video_buttons()
                try:
                    self.media.release()
                except AttributeError:
                    media.release()
                self.media = Media(video, 'video', height, width)
                break

            if self.pause:
                sleep(1)
                continue

            if chk is not None:
                try:
                    frame = cv2.resize(frame, chk)
                except cv2.error:
                    continue

            frame = self.detect(frame)
            if frame is None:
                continue

            self.show(frame)
            video.append(frame)
            sleep(0.03)

    def replay_video(self):
        for frame in self.media.content:
            if self.interrupt:
                return
            while self.pause:
                if self.interrupt:
                    return
                sleep(0.3)
            self.show(frame)
            sleep(0.03)

        self.pauseButton.change_state(state='disabled')
        self.replayButton.change_state(state='normal')

    """____Final_Functions____"""

    def detect(self, frame):
        try:
            frame = self.model(frame)
        except AttributeError:
            return
        return frame

    def show(self, frame):
        frame = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.imagebox.itemconfig(self.imageContainer, image=frame)
        self.imagebox.img = frame
        self.imagebox.configure(scrollregion=self.imagebox.bbox("all"))

    def edit_shape(self, actual, view):
        self.itemconfig("actual", text=actual)
        self.itemconfig("view", text=view)

    def save(self, path):
        if self.media.type == 'image':
            cv2.imwrite(path, self.media.content)
        else:
            four_cc = cv2.VideoWriter_fourcc(*"MJPG")
            out = cv2.VideoWriter(path, four_cc, 20, (self.media.width, self.media.height))

            for i in range(len(self.media.content)):
                out.write(self.media.content[i])
            out.release()
