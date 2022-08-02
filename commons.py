# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 22:19:07 2022

@author: Alexandre
"""

import tkinter as tk
from tkinter import *  
from PIL import ImageTk,Image  
import os
import io
import math

class commons :
    
    def __init__(self):
        return None
    
    #Window 
    def setRoot(self,width,height,offx=0,offy=0,top=True,fullscreen=False,resizable=True,zoom=True):
        root = tk.Tk()
        if type(width)!=type(None) :
            width_return = width
        else :
            width_return = root.winfo_screenwidth()
        if type(height)!=type(None) :
            height_return = height
        else :
            height_return = root.winfo_screenheight()
        root.geometry(str(width_return)+"x"+str(height_return)+"+"+str(offx)+"+"+str(offy))
        if top :
            root.attributes('-topmost',1)
        root.resizable(resizable, resizable)
        if zoom :
            root.state('zoomed')
        root.attributes("-fullscreen",fullscreen)
        root.attributes('-alpha', 1)
        return root,width_return,height_return
    
    #Canvas
    def getCanvasFullScreen(self,root,width,height,color,borderwidth=-2):
        canvas = Canvas(root, width = width, height = height, bg=color,borderwidth=borderwidth)
        return canvas
    
    def packCanvas(self,canvas,root=None):
        canvas.grid(column=0, row=1, sticky="nsew",padx=0,pady=0,ipadx=0,ipady=0)  
        #canvas.pack()
        if root!=None :
            root.update()
            
    def getCanvasSizePos(self,canvas):
        return Canvas.winfo_rootx(canvas),Canvas.winfo_rooty(canvas),Canvas.winfo_width(canvas),Canvas.winfo_height(canvas)
    
    def saveCanvas(self,canvas,path,filename,fileFormat):
        x,y,w,h=self.getCanvasSizePos(canvas)
        canvas.update()
        canvas.postscript(file=path+filename+".eps", colormode='color')
        img = Image.open(path+filename+".eps")
        img = img.convert('RGB')
        img.save(path+filename+"."+fileFormat)
        del img
        os.remove(path+filename+".eps")
        
    def saveCanvas2(self,canvas,path,filename,fileFormat,width,height,createFolder=False,folderName=""):
        dpi = 200
        canvas.update()
        if createFolder :
            try: 
                os.mkdir(path+folderName) 
            except OSError as error: 
                pass
        ps = canvas.postscript(colormode='color',width=width,height=height)
        im = open_eps(ps, dpi=dpi)
        im.save(path+filename+"."+fileFormat, dpi=(dpi, dpi))
        
    #Pos to pixel
    def getPixelFromPos(self,pos,ppu,width,height,roundDig):
        returnPos = [round((pos[0]*ppu)+int(width/2),roundDig),round((-pos[1]*ppu)+int(height/2),roundDig)]
        return returnPos
    
    def getPixelFromPosList(self,posList,ppu,width,height,roundDig):
        return [self.getPixelFromPos(pos,ppu,width,height,roundDig) for pos in posList]
    
    
    def drawPoint(self,canvas,pos,color,light,size,shape) :
        color = self.rgb_hack(color,light)
        figSize = max(size-1,1)
        if figSize==1:
            canvas.create_line(pos[0],pos[1],pos[0]+1,pos[1],fill=color)
        else :
            if shape=="square":
                canvas.create_rectangle(pos[0],pos[1],pos[0]+figSize,pos[1]+figSize,fill=color,outline="")
            elif shape=="round":
                canvas.create_oval(pos[0]-int(figSize/2),pos[1]-int(figSize/2),pos[0]+int(figSize/2),pos[1]+int(figSize/2),fill=color,outline="")
    
    def rgb_hack(self,rgb,light=1):
        rgb = (int(rgb[0]*255*light),int(rgb[1]*255*light),int(rgb[2]*255*light))
        return "#%02x%02x%02x" % rgb  
    
def open_eps(ps, dpi=300.0):
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    original = [float(d) for d in img.size]
    scale = dpi/72.0            
    if dpi != 0:
        img.load(scale = math.ceil(scale))
    if scale != 1:
        img.thumbnail([round(scale * d) for d in original], Image.ANTIALIAS)
    return img


commons()