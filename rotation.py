import tkinter as tk
from PIL import Image
import numpy as np
import math as m

class rotation_window(tk.Toplevel):
    
    def __init__(self, master = None):
        tk.Toplevel.__init__(self, master = master)
        
        self.rotation_level = 0 
        
        self.true_image = self.master.adjusted_image 
        self.adjusted_image = self.master.adjusted_image
        
        self.rotation_label = tk.Label(self, text = "Degree [-25,25]") 
        self.rotation_scale = tk.Scale(self, from_ = -25, to_= 25, length = 250, resolution = 1, orient = tk.HORIZONTAL)
        self.zoom_label = tk.Label(self, text = "Zoom")
        self.zoom_scale = tk.Scale(self, from_=1.0, to_=10, length = 250, resolution = 0.01, orient = tk.HORIZONTAL)
        
        self.apply_button = tk.Button(self, text = "Apply") 
        self.preview_button = tk.Button(self, text = "Preview") 
        self.cancel_button = tk.Button(self, text = "Cancel") 
        
        self.apply_button.bind("<ButtonRelease>", self.apply_changes) 
        self.preview_button.bind("<ButtonRelease>", self.preview_changes) 
        self.cancel_button.bind("<ButtonRelease>", self.cancel_changes)
        
        self.rotation_label.pack()
        self.rotation_scale.pack()
        self.zoom_label.pack()
        self.zoom_scale.pack()
        
        self.apply_button.pack(side = tk.LEFT)
        self.preview_button.pack(side = tk.LEFT)
        self.cancel_button.pack()
    
    def apply_changes(self, event):
        self.master.adjusted_image = self.adjusted_image
        self.close()
    
    def preview_changes(self, event):
        self.adjusted_image = self.master.adjusted_image
        self.adjusted_image = self.zoom(self.zoom_scale.get(), self.adjusted_image)
        self.adjusted_image = self.rotation(self.rotation_scale.get(), self.adjusted_image) 
        self.show_image(self.adjusted_image) 
    
    def cancel_changes(self, event):
        self.close()
    
    def show_image(self, image = None):
        self.master.canvas.image_show(image=image) ###
    
    def close(self):
        self.show_image(self.master.adjusted_image)
        self.destroy()
        
        
        
        
    def zoom(self, alpha, image):
        
        if alpha == 1:
            return image
        
        image = np.int16(np.array(image))
        width = image.shape[1] - 1 
        height = image.shape[0] - 1 
        
        new_width = int(alpha*width) 
        new_height = int(alpha*height)
        
        width_ratio = float(width)/float(new_width) 
        height_ratio = float(height)/float(height)
        
        count = 0
        new_image = []
        
        for i in range(new_height):
            for j in range(new_width):
                x = int(width_ratio*j)
                y = int(height_ratio*i)
                x_diff = (width_ratio*j) - x
                y_diff = (height_ratio*i) - y
                
                if (x>=(new_width-1) or y>=(new_height-1)):
                    A_color = image[y][x]
                else:
                    A_color = image[y][x]
                if ((x+1)>=(new_width-1) or (y>=(new_height-1))):
                    B_color = image[y][x]
                else:
                    B_color = image[y+1][x]
                if (x>=(new_width-1) or ((y+1)>=(new_height-1))):
                    C_color = image[y][x]
                else:
                    C_color = image[y][x+1]
                if ((x+1)>=(new_width-1) or (y+1)>=(new_height-1)):
                    D_color = image[y][x]
                else:
                    D_color = image[y+1][x+1]
                
                color = np.int16( (A_color * (1 - x_diff) * (1 - y_diff)) + (B_color * (x_diff) * (1 - y_diff))
                                + (C_color * (y_diff)*(1 - x_diff)) + (D_color * (x_diff*y_diff)))
        
                
                new_row = int(count / new_width)
                new_col = count % new_width
                if(new_col==0):
                    new_image.append([])
                new_image[new_row].append(color)
                count +=1
                
        image = np.uint8(new_image)
        return Image.fromarray(image)
    
    def rotation(self, alpha, image):
        
        if alpha == 0:
            return image
        image = np.int16(np.array(image))
        alpha = m.radians(alpha)
        height = image.shape[0]
        width = image.shape[1]
        if height < width:
            tmp = height
            height = width
            sirina = tmp
            
        coef = (m.sqrt(height**2+width**2)*m.sin(m.atan(width/height)+abs(alpha)))/width
        
        old_height = height
        old_width = width
        new_image = self.zoom(coef, image)
        new_image = np.int16(new_image)
        
        height = new_image.shape[0]
        width = new_image.shape[1]
        center_height = round(((height+1)/2)-1)
        center_width = round(((width+1)/2)-1)
        new_height = round(abs(height*m.cos(alpha))+abs(width*m.cos(alpha)))+1
        new_width = round(abs(width*m.cos(alpha))+abs(height*m.cos(alpha)))+1
        new_center_height = round(((new_height+1)/2)-1)
        new_center_width = round(((new_width+1)/2)-1)
        
        slika = np.zeros((new_height, new_width, 3))
        
        for i in range(height):
            for j in range(sirina):
                
                x = height - 1 - i - center_height
                y = width - 1 - j - center_width
                
                x1 = round(x - y*m.tan(alpha/2))
                y1 = round(x1*m.sin(alpha) + y)
                x1 = round(x1 - y1*m.tan(alpha/2))
                
                x1 = new_center_height - x1
                y1 = new_center_width - y1
                slika[x1,y1, :] = new_image[i, j, :]
                
                
                

        image = image[round((new_height - height)/2):round((new_height - height)/2) + height+1,
                      round((new_width - width)/2):round((new_width - width)/2) + width+1]
        image = image[round((coef-1)/2*old_height):round((coef-1)/2*old_height)+old_height,
                      round((coef-1)/2*old_width):round((coef-1)/2*old_width)+old_width]
        image = np.uint8(image)
        return Image.fromarray(image)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    