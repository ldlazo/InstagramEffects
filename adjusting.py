import tkinter as tk
from tkinter import filedialog
from rotation import rotation_window
from color_adjust import color_adjust_window
from sharpening import sharpening_window
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import numpy as np

class setting(tk.Toplevel):
    def __init__(self, master = None):
        tk.Toplevel.__init__(self, master = master)
        
        self.rotation = tk.Button(self, text="Rotation and other")
        self.color_adjust = tk.Button(self, text = "Brightness, contrast, warmth and saturation")
        self.sharpening = tk.Button(self, text = "Sharpening and vignette")
        self.save = tk.Button(self, text = "Save as:")
        self.histogram = tk.Button(self, text = "Histogram")
        self.original = tk.Button(self, text = "Original")
        
        self.rotation.bind("<ButtonRelease>", self.rotation_click)
        self.color_adjust.bind("<ButtonRelease>", self.color_adjust_click)
        self.sharpening.bind("<ButtonRelease>", self.sharpening_click)
        self.save.bind("<ButtonRelease>", self.save_click)
        self.histogram.bind("<ButtonRelease>", self.histogram_click)
        self.original.bind("<ButtonRelease>", self.original_click)
        
        self.rotation.grid(row = 0, column = 0)
        self.color_adjust.grid(row = 1, column = 0)
        self.sharpening.grid(row = 2, column = 0)
        self.save.grid(row = 3, column = 0)
        self.histogram.grid(row = 4, column = 0)
        self.original.grid(row = 5, column = 0)
        
        
    def rotation_click(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.rotation:
            self.master.rotation_window = rotation_window(master = self.master)
            self.master.rotation_window.grab_set()

    def color_adjust_click(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.color_adjust:
            self.master.color_adjust_window = color_adjust_window(master = self.master)
            self.master.color_adjust_window.grab_set()
    
    def sharpening_click(self,event):
        if self.winfo_containing(event.x_root, event.y_root) == self.sharpening:
            self.master.sharpening_window = sharpening_window(master = self.master)
            self.master.sharpening_window.grab_set()
            
    def save_click(self,event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save:
            original_type = self.master.filename.split('.')[-1]
            filename = filedialog.asksaveasfilename()
            filename = filename + "." + original_type
            
            saved_image = self.master.adjusted_image
            saved_image.save(filename)
            self.master.filename = filename
            
    def histogram_click(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.histogram:
            #plt.close("all")
            image = np.array(self.master.adjusted_image)
            print(image.shape)
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
            ax1.hist(image[:,:,0].ravel(), 256, [0,256], color = 'r')
            ax2.hist(image[:,:,1].ravel(), 256, [0,256], color = 'g')
            ax3.hist(image[:,:,2].ravel(), 256, [0,256], color = 'b')
            ax4.hist((image.sum(axis=-1)/3).ravel(), 256, [0,256], color = 'k')
            plt.show()
            
    def original_click(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.original:
            self.master.adjusted_image = self.master.true_image
            self.master.canvas.image_show()
            
            
            
            
            
            
            