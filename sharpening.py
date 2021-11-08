import tkinter as tk
from PIL import Image
import numpy as np
import math as m

class sharpening_window(tk.Toplevel): 
    
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master=master)
        
        self.rotation_level = 0 
        
        self.true_image = self.master.adjusted_image 
        self.adjusted_image = self.master.adjusted_image
        
        self.sharpening_label = tk.Label(self, text ="Sharpen") 
        self.sharpening_scale = tk.Scale(self, from_=0, to_=3, length=250, resolution=0.01, orient=tk.HORIZONTAL)
        self.sharpening_scale.set(1)
        
        self.bluring_label = tk.Label(self, text="Blur") 
        self.bluring_scale = tk.Scale(self, from_=0, to_=1, length=250, resolution=0.01, orient=tk.HORIZONTAL)
        
        self.tilt_shift_variable = tk.StringVar(self)
        self.tilt_shift_variable.set("NONE")
        self.tilt_shift_label = tk.Label(self, text = "Tilt Shift")
        self.tilt_shift_optionmenu = tk.OptionMenu(self, self.tilt_shift_variable, "NONE", "LINEAR", "RADIAL")
        self.vignette_label = tk.Label(self, text="Vignette") 
        self.vignette_scale = tk.Scale(self, from_=0, to_=1, length=250, resolution=0.01, orient=tk.HORIZONTAL)
        
        self.apply_button = tk.Button(self, text = "Apply") 
        self.preview_button = tk.Button(self, text = "Preview")
        self.cancel_button = tk.Button(self, text = "Cancel")
        
        self.apply_button.bind("<ButtonRelease>", self.apply_changes)
        self.preview_button.bind("<ButtonRelease>", self.preview_changes)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_changes)
        
        self.sharpening_label.pack()
        self.sharpening_scale.pack()
        self.bluring_label.pack()
        self.bluring_scale.pack()
        self.tilt_shift_label.pack()
        self.tilt_shift_optionmenu.pack()
        self.vignette_label.pack()
        self.vignette_scale.pack()
        
        self.apply_button.pack(side = tk.LEFT)
        self.preview_button.pack(side = tk.LEFT)
        self.cancel_button.pack()
    
    def apply_changes(self, event):
        self.master.adjusted_image = self.adjusted_image
        self.close()
    
    def preview_changes(self, event):
        self.adjusted_image = self.master.adjusted_image
        self.adjusted_image = self.bluring(self.bluring_scale.get(), self.adjusted_image)
        self.adjusted_image = self.sharpening(self.sharpening_scale.get(), self.adjusted_image)
        self.adjusted_image = self.tilt_shift(self.tilt_shift_variable.get(), self.adjusted_image)
        self.adjusted_image = self.vignette(self.vignette_scale.get(), self.adjusted_image)
        self.image_show(self.adjusted_image)
    
    def cancel_changes(self, event):
        self.close()
    
    def image_show(self, image=None):
        self.master.canvas.image_show(image=image)
    
    def close(self):
        self.image_show(self.master.adjusted_image)
        self.destroy()
        
    
    def sharpening(self, alpha, image):
        
        if alpha == 1:
            return image
        image = np.array(image)
        image = np.int16(image)
        blur = self.blur(image)
        image = (1 - alpha)*blur + alpha*image

        image = np.where(image<255, image, 255)
        image = np.where(image<0, 0, image)
        image = np.uint8(image)
        return Image.fromarray(image)
        
    
    def gauss_kernel(self, shape, sigma):
       
        height = shape[0]
        width = shape[1]
        center_height = height // 2 #centar_visina
        center_width = width // 2
        kernel =np.zeros((height, width))
        for i in range(height):
            for j in range(width):            
                diff=((i-center_height)**2+(j-center_width)**2)
                kernel[i][j]=np.exp(-(diff)/(2*(sigma**2)))
                
        kernel = kernel/np.sum(kernel)
        
        return np.stack([kernel,kernel,kernel], axis = -1)
    
    
    def convolve2d(self, image, kernel):
       
        new_image = np.zeros_like(image)
        dimension = kernel.shape[0]
        if dimension%2==0:
            dimension-=1
        # Channel 1 
        image_padded = np.zeros((image.shape[0] + dimension-1, image.shape[1] + dimension-1,3))
        
        image_padded[int(np.floor((dimension-1)/2)):-int(np.floor((dimension-1)/2)), int(np.floor((dimension-1)/2)):-int(np.floor((dimension-1)/2))] = image[:,:]
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                image_padded[x: x+dimension, y: y+dimension] = np.where(image_padded[x: x+dimension, y: y+dimension]<=0, 
                                                          image_padded[x: x+dimension, y: y+dimension].mean(), image_padded[x: x+dimension, y: y+dimension])
                new_image[x, y]=(kernel * image_padded[x: x+dimension, y: y+dimension]).sum(axis=(0,1))
                
                         
        return new_image
    
    
    def blur(self, image):
       
        image = self.convolve2d(image, self.gauss_kernel((11,11),5))
        return image

    def bluring(self, alpha, image): #blur
        
        if alpha == 0:
            return image
        image = np.array(image)
        image = np.int16(image)
        white = np.ones_like(image)*255
        image = (1-alpha)*image + alpha*white
        image = np.where(image<255, image, 255)
        image = np.where(image<0, 0, image)
        image = np.uint8(image)
        return Image.fromarray(image)
    
    def tilt_shift(self, mode, image):
        
        if mode == "NONE":
            return image
        image = np.array(image)
        image = np.int16(image)
        uslov_idx = np.zeros((image.shape[0],image.shape[1]))
        kernel_vre = np.zeros((image.shape[0],image.shape[1]))
        if mode == "LINEAR":
            def uslov(x,y):
                if abs(x-image.shape[0]/2) > 2.0/6.0*image.shape[0]:
                    return 2
                elif abs(x-image.shape[0]/2) < 1.0/6.0*image.shape[0]:
                    return 0
                else:
                    return 1
            
            for x in range(image.shape[0]):
                for y in range(image.shape[1]):
                    uslov_idx[x,y] = uslov(x,y)
                    kernel_vre[x,y] = max(0.01, ((abs(x-image.shape[0]/2)-1.0/6.0*image.shape[0])/(1.0/6.0*image.shape[0])*9))
        
        if mode == "RADIAL":
            def uslov(x,y):
                if m.sqrt((x-image.shape[0]/2)**2 + (y-image.shape[1]/2)**2) > 2.0/6.0*min(image.shape[0], image.shape[1]):
                    return 2
                elif m.sqrt((x-image.shape[0]/2)**2 + (y-image.shape[1]/2)**2) < 1.0/6.0*min(image.shape[0], image.shape[1]):
                    return 0
                else:
                    return 1
                
            for x in range(image.shape[0]):
                for y in range(image.shape[1]):
                    uslov_idx[x][y] = uslov(x,y)
                    kernel_vre[x][y] = max(0.01, ((m.sqrt((x-image.shape[0]/2)**2 +
                                                          (y-image.shape[1]/2)**2)-1.0/6.0*image.shape[0])
                                                  /(1.0/6.0*min(image.shape[0], image.shape[1]))*9))
            
            
        kernel = self.gauss_kernel((21,21),9)
        kernel_norm = np.zeros((21,21,3))
        kernel_norm[10,10] = np.array([1,1,1])
        new_image = np.zeros_like(image)
        dimension = kernel.shape[0]
        if dimension%2==0:
            dimension-=1

        image_padded = np.zeros((image.shape[0] + dimension-1, image.shape[1] + dimension-1,3))
        
        image_padded[int(np.floor((dimension-1)/2)):-int(np.floor((dimension-1)/2)),
                     int(np.floor((dimension-1)/2)):-int(np.floor((dimension-1)/2))] = image[:,:]
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                print(x, uslov_idx[x,y])
                if uslov_idx[x,y] == 0:
                    kernel1 = kernel_norm
                elif uslov_idx[x,y] == 1:
                    kernel1 = self.gauss_kernel((21,21), kernel_vre[x,y])
                else:
                    kernel1 = kernel
                image_padded[x: x+dimension, y: y+dimension] = np.where(image_padded[x: x+dimension, y: y+dimension]<=0, 
                                                          image_padded[x: x+dimension, y: y+dimension].mean(),
                                                          image_padded[x: x+dimension, y: y+dimension])
                new_image[x, y]=(kernel1 * image_padded[x: x+dimension, y: y+dimension]).sum(axis=(0,1))
                
                         
        new_image = np.where(new_image<255, new_image, 255)
        new_image = np.where(new_image<0, 0, new_image)
        new_image = np.uint8(new_image)
        return Image.fromarray(new_image)
    
    
    def vignette(self, alpha, image):
        
        image = np.array(image)
        image = np.int16(image)
        kernel = self.gauss_kernel((image.shape[:2]), 1.0/3.0*min(image.shape[:2]))
        kernel *=2.0/float(kernel[kernel.shape[0]//2,kernel.shape[1]//2,0])
        kernel = np.where(kernel>1, 1, kernel)
        new_image = kernel * image
        image = (1-alpha)*image + alpha*new_image
        image = np.where(image<255,image,255)
        image = np.where(image<0,0,image)
        image = np.uint8(image)
        return Image.fromarray(image)
