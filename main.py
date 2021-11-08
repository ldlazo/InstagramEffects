import tkinter as tk
from tkinter import filedialog
from PIL import Image
from adjusting import setting
from image_show import canvas


class Main(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
        
            self.filename = ""
            self.true_image = None
            self.adjusted_image = None
        
            self.title("Instagram")
            logo = tk.PhotoImage(file = 'insta.png')
            self.call('wm', 'iconphoto', self._w, logo)
            
            self.load = tk.Button(self, text = "Load new image", padx = 50, pady = 50)
            self.load.bind("<ButtonRelease>", self.image_loading)
            self.load.pack()
            
        def image_loading(self, event):
            global image
            if self.winfo_containing(event.x_root, event.y_root) == self.load:
                filename = filedialog.askopenfilename()
                load = Image.open(filename).convert("RGB")
                if load is not None:
                    self.filename = filename
                    self.true_image = load
                    self.adjusted_image = load
                    self.canvas = canvas(master = self)
                    self.canvas.image_show()
                    self.canvas.pack()
                    self.load.destroy()
                    self.setting = setting(master = self)
                    self.setting.grab_set()