from tkinter import Menu, messagebox


class MenuBar(Menu):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.file_menu = Menu(self, tearoff=0)
        self.help_menu = Menu(self, tearoff=0)

        self.file_menu.add_command(label="Exit", command=self.terminate)

        self.help_menu.add_command(label="Credits",
                                   command=lambda: messagebox.showinfo("Credits", "This Simple App was Created By "
                                                                                     "Ahmed Aboelenin"))

        self.add_cascade(label="File", menu=self.file_menu)
        self.add_cascade(label="Help", menu=self.help_menu)

        self.master.configure(menu=self)

    def terminate(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.terminate()
