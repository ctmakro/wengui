import tkinter as tk

class Form(tk.Frame):
    def __init__(self, title='Form1'):
        master = tk.Tk() # make new window
        super().__init__(master)
        self.pack(expand=True,fill='both')

        # default settings for form
        master.title(title)
        master.minsize(320,240)
