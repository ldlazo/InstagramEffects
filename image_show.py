import tkinter as tk
from PIL import  ImageTk

class canvas(tk.Canvas):
    def __init__(self, master=None):
        tk.Canvas.__init__(self, master=master, bg="gray", width=400, height=600)
        
        self.shown_image = None 


    def image_show(self, image=None):

        self.clear_canvas() 
        if image is None:
            image = self.master.adjusted_image.copy()
        else:
            image = image
            
        width, height = image.size
        self.shown_image = ImageTk.PhotoImage(image)

        
        self.config(width=width, height=height)
        self.create_image(width / 2, height / 2, anchor=tk.CENTER, image=self.shown_image)
        self.image = self.shown_image
        
        
    def clear_canvas(self):
        self.delete("all")