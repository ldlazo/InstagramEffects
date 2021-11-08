import tkinter as tk
from PIL import Image
import numpy as np
import converter as k



class color_adjust_window(tk.Toplevel): 
    
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master=master)

        
        self.true_image = self.master.adjusted_image 
        self.adjusted_image = self.master.adjusted_image
        
        self.brightness_label = tk.Label(self, text="Brightness") 
        self.brightness_scale = tk.Scale(self, from_=0, to_=3, length=250, resolution=0.01, orient=tk.HORIZONTAL)
        self.brightness_scale.set(1)
        
        self.contrast_label = tk.Label(self, text="Contrast") 
        self.contrast_scale = tk.Scale(self, from_=-50, to_=50, length=250, resolution=1, orient=tk.HORIZONTAL)
        self.contrast_scale.set(0)
        
        self.warmth_label = tk.Label(self, text="Warmth") 
        self.warmth_scale = tk.Scale(self, from_=-50, to_=50, length=250, resolution=1, orient=tk.HORIZONTAL)
        
        self.saturation_label = tk.Label(self, text = "Saturation") 
        self.saturation_scale = tk.Scale(self, from_=0, to_=3, length=250, resolution=0.01, orient=tk.HORIZONTAL)
        self.saturation_scale.set(1)
        
        self.highlight_label = tk.Label(self, text="Highlight") 
        self.highlight_scale = tk.Scale(self, from_=-50, to_=50, length=250, resolution=1, orient=tk.HORIZONTAL)
        
        self.shadow_label = tk.Label(self, text="Shadow") 
        self.shadow_scale = tk.Scale(self, from_=-50, to_=50, length=250, resolution=1, orient=tk.HORIZONTAL)
        
        self.apply_button = tk.Button(self, text = "Apply") 
        self.preview_button = tk.Button(self, text = "Preview") 
        self.cancel_button = tk.Button(self, text = "Cancel")
        
        self.apply_button.bind("<ButtonRelease>", self.apply_changes) 
        self.preview_button.bind("<ButtonRelease>", self.preview_changes)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_changes)
        
        self.brightness_label.pack()
        self.brightness_scale.pack()
        self.contrast_label.pack()
        self.contrast_scale.pack()
        self.warmth_label.pack()
        self.warmth_scale.pack()
        self.saturation_label.pack()
        self.saturation_scale.pack()
        self.highlight_label.pack()
        self.highlight_scale.pack()
        self.shadow_label.pack()
        self.shadow_scale.pack()
        self.apply_button.pack(side = tk.LEFT)
        self.preview_button.pack(side = tk.LEFT)
        self.cancel_button.pack()
    
    def apply_changes(self, event):
        self.preview_changes(event)
        self.master.adjusted_image = self.adjusted_image
        self.close()
    
    def preview_changes(self, event):
        self.adjusted_image = self.master.adjusted_image
        self.adjusted_image = self.brig_satu(self.brightness_scale.get(),self.saturation_scale.get(), self.adjusted_image)
        #self.adjusted_image = self.contrast(self.contrast_scale.get(), self.adjusted_image)
        self.adjusted_image = self.high_shad(self.contrast_scale.get(), -self.contrast_scale.get(), self.adjusted_image) 
        self.adjusted_image = self.warmth(self.warmth_scale.get(), self.adjusted_image)
        self.adjusted_image = self.high_shad(self.highlight_scale.get(),self.shadow_scale.get(), self.adjusted_image)
        self.image_show(self.adjusted_image)
    
    def cancel_changes(self, event):
        self.close()
    
    def image_show(self, image=None):
        self.master.canvas.image_show(image=image)
    
    def close(self):
        self.image_show(self.master.adjusted_image)
        self.destroy()
    
    def brig_satu(self, alpha, beta, image):
        
        image = np.float64(np.array(image))
        image = k.RGBtoHSV(image)
        image[:,:, 2] *= alpha
        image[:,:, 2] = np.where(image[:,:, 2]>1, 1, image[:,:,2])
        image[:,:, 2] = np.where(image[:,:, 2]<0, 0, image[:,:,2])
        image[:,:, 1] *= beta
        image[:,:, 1] = np.where(image[:,:, 1]>1, 1, image[:,:,1])
        image[:,:, 1] = np.where(image[:,:, 1]<0, 0, image[:,:,1])
        image = k.HSVtoRGB(image)
        image = np.uint8(image)
        return Image.fromarray(image)
    
    def warmth(self, value, image):
        
        if value == 0:
            return image
        image = np.int16(np.array(image))
        image[:,:,0] = image[:, :, 0] + value
        image[:,:,2] = image[:, :, 2] - value
        image = np.where(image<255, image, 255)
        image = np.where(image>0, image, 0)
        image = np.uint8(image)
        return Image.fromarray(image)
    
    
    def high_shad(self, alpha, beta, image):
        
        image = np.float64(np.array(image))
        image = k.RGBtoHSV(image)
        image[:,:, 2] = np.where(image[:,:,2]>0.3, image[:,:, 2]*(1+image[:,:, 2]*alpha/100.0), image[:,:,2])           
        image[:,:, 2] = np.where(image[:,:,2]<0.7,
                                 image[:,:, 2]*(1+(1-image[:,:, 2])*beta/100.0),
                                 image[:,:,2])
        image[:,:, 2] = np.where(image[:,:, 2]>1, 1, image[:,:,2])
        image[:,:, 2] = np.where(image[:,:, 2]<0, 0, image[:,:,2])
        image = k.HSVtoRGB(image)
        image = np.uint8(image)
        return Image.fromarray(image)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        