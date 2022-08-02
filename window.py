# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 20:27:32 2022

@author: Alexandre
"""
import tkinter as tk
from tkinter import *  
from PIL import ImageTk,Image  
import time
import math 
import colorsys
import sys
import sequence as sq
import dynamicalSys as ds
from PIL import ImageGrab
import os
import numpy as np
import commons as com
sys.setrecursionlimit(100000000)

class window :
    
    
    
    def getParameters(self):
        self.parameters = [self.curveNameMenu.get()]
        for i in range(len(self.textInputList)) :
            self.parameters.append(self.textInputList[i].get())
        self.parameters.append(self.colorMenu.get())
        self.parameters.append(self.colorBgMenu.get())
        #print(self.parameters)
        self.reset = True
       
        #time.sleep(1)
        self.sequenceName = self.parameters[0]
        self.iteration = int(self.parameters[1])
        self.pixelPerUnits = int(self.parameters[2])
        self.lineWidth = int(self.parameters[3])
        self.sleepTime = int(self.parameters[4])/1000
        self.batchSize = int(self.parameters[5])
        self.maxSize = int(self.parameters[6])
        self.curveSteps = int(self.parameters[7])
        self.hueStretch = -1/int(self.parameters[8])
        self.defaultColor = self.parameters[9]
        self.backgroundColor = self.parameters[10]
        self.changeHue = self.checkListVar[0].get()
        self.center = self.checkListVar[1].get()
        self.optimalSize = self.checkListVar[2].get()
        self.saveEnd = self.checkListVar[3].get()
        self.printStats = self.checkListVar[4].get()
 
        # getting screen's width in pixels
        self.resetCruve(self.dirStart)
        self.generationLoopCurve(1)
    
    #def exitWindow(self) :
        
    
    def __init__(self):
        #Selection vars
        self.type = "curve"
        #self.type = "dynamical"
        
        #Dynamical vars
        self.pointSize = 10
        self.pointColor = [1]*3
        self.pointShape = "round"
        #self.timeStart = 0.107
        #self.timeStart = -0.27
        self.timeStart = 0
        self.timeIncrement = 0.001
        self.frameIteration = 50
        self.timeIteration = 10
        self.refresh = True
        self.pixelPointMat = []
        self.dotShadow = 1
        self.diffColors = False
        self.hueStretchDyn = 2
        self.sizeLimit = float("inf")
        
        #Window 
        #Add your window size here : 
        width = 1366
        height = 768
        offset = 0
        fullscreen = False
        windowTapeSize = 23
        smallWindow = True
        menuHeight = 20
        if not fullscreen :
            height = height - windowTapeSize
        height = height - menuHeight
        self.root,self.width,self.height = c.setRoot(width,height,offset,0,False,fullscreen,True,True)       
        
        self.pixelPerUnits = 16
        self.generationNumber = 1
        self.sleepTime = 0.000
        self.startPos = [0,0]
        self.frameCount = 0
        self.backgroundColor = "black"
        self.canvas = c.getCanvasFullScreen(self.root,self.width,self.height,self.backgroundColor)
        self.seqList,self.sequenceNumber = self.getCurveNameList()
        self.menuTest(self.seqList)
        c.packCanvas(self.canvas)
        
        #Curve display var
        self.lineWidth = 3
        self.batchSize = 20
        self.pointList = []
        self.posCurve = self.startPos
        self.leftDownCorner = self.startPos
        self.rightUpCorn = self.startPos
        self.dash = (0,0)
        self.curveSteps = 1
        self.print = True
        self.borderSize = 40
        
        #Save vars
        self.saveEnd = False
        self.saveAll = False
        self.saveFormat = "png"
        self.saveFolder = "C:/Users/Alexandre/Desktop/curve/images/"
        
        #Curve draw vars
        self.dirStart = 0
        self.radChangeStart = [1,2]
        self.radChange = self.radChangeStart#math.pi*(2/3)
        self.modMultiDir = math.pow(2, 6)
        self.modMultiLen = math.pow(2, 8)
        self.multiDir = 1
        self.multiLen = 1
        self.roundDigitCurve = 10
        self.roundDigitPixel = 5
        self.defaultColor = c.rgb_hack((1, 1, 1))
        self.changeHue = True
        self.hueStretch = math.pow(2, -3)
        self.hueOffset = 0
        self.center = True
        self.optimalSize = True
        self.maxSize = 5000
        self.printStats = False
        self.reset=True
        self.iteration = 100
        self.sequenceName = "dragon"
        
        #Used to generate all curves configured 
        # self.seqList,self.sequenceNumber = self.getCurveNameList()
        # self.generationNumber = self.sequenceNumber+1
        
        #Series generation vars
        if self.type == "curve" and self.generationNumber==1: 
            # self.iteration = 6
            # self.sequenceName = "hilb"
            # self.sequence = sq.sequence(self.sequenceName,self.iteration,self.radChange,self.maxSize)
            # self.series = self.sequence.sequence_generated
            # self.radChange = self.sequence.radChange
            # self.dir, self.posCurve = self.sequence.newStartDirPos(self.center,self.dirStart,self.startPos)#
            self.resetCruve(self.dirStart,False)
            self.getParameters()
        elif self.type == "curve" and self.generationNumber>1: 
            self.resetCruve(self.dirStart,False)
            self.generationLoopCurve(self.generationNumber)

        
        if self.type == "dynamical" :
            self.generationLoopDynamical(self.timeIteration)
        self.root.mainloop() 
    
    def fractionToRad(self,fractList):
        return math.pi*(fractList[0]/fractList[1])
    
    def menuTest(self,curveList):
        menuColor = "black"
        textColor = "white"
        dropColor = "gray"
        buttonColor = "gray"
        
        self.menu = c.getCanvasFullScreen(self.root,self.width,100,menuColor)
        self.menu.config(highlightcolor=menuColor,bd=-2)
        
        curveNameList = curveList
        curveColorList = ["white","black","blue","green","red","cyan","magenta","yellow"]
        curveColorBgList = ["black","white","blue","green","red","cyan","magenta","yellow"]
        labelListStr = ["Iteration:","Pixel p u:","Line wid:","Sleep ms:","Draw step:","Max line:","Curve ite:","Hue mod:"]
        labelListCheck = ["Change hue","Center", "Auto size","Save","Disp stats"]
        labelListDropStr = ["Curve :","Color :","Bg color :"]
        inputSetList = [10,10,1,0,100,100000,1,4]
        inputSizeList = [2,3,1,3,3,5,1,2]
        checkSet = [1,1,1,0,1]
        sepFont=("Courier",10,"bold")
        fontSize = 7
        labFont=("Small Fonts",fontSize)
        checkFont=("Small Fonts",fontSize)
        dropFont=("Small Fonts",fontSize)
        
        self.checkListVar = []
        for i in range(len(labelListCheck)) :
            but = tk.IntVar()
            but.set(checkSet[i])
            self.checkListVar.append(but)
           
        paddingMenu = {'padx': 0, 'pady': 0}
        paddingsButton = {'padx': 0, 'pady': 0}
        paddingsDrop = {'padx': 0, 'pady': 0}
        paddingsLabel = {'padx': 0, 'pady': 0}
        paddingsInput = {'padx': 0, 'pady': 0}
        paddingsSep = {'padx': 0, 'pady': 0}
        paddingsCheck = {'padx': 0, 'pady': 0}
        textWidth = 1
        self.textInputList = []
        self.checkboxList = []
        labelList = []
        col = 0
        for i in range(len(labelListStr)) :
            labelList.append(tk.Label(self.menu, text = labelListStr[i]))
            ent = tk.Entry(self.menu,width=inputSizeList[i],bd=0,justify="right")
            ent.config({"background": "gray"})
            self.textInputList.append(ent)
                   
        col = self.addLabel(self.menu,labelListDropStr[0],col,menuColor,textColor,paddingsLabel,labFont)
        col,self.curveNameMenu = self.addDropMenu(self.menu,curveNameList,col,dropColor,textColor,paddingsDrop,dropFont)
        col = self.addSeparator(self.menu,col,menuColor,textColor,paddingsSep,sepFont)
        col = self.addLabel(self.menu,labelListDropStr[1],col,menuColor,textColor,paddingsLabel,labFont)
        col,self.colorMenu = self.addDropMenu(self.menu,curveColorList,col,dropColor,textColor,paddingsDrop,dropFont)
        col = self.addSeparator(self.menu,col,menuColor,textColor,paddingsSep,sepFont)
        col = self.addLabel(self.menu,labelListDropStr[2],col,menuColor,textColor,paddingsLabel,labFont)
        col,self.colorBgMenu = self.addDropMenu(self.menu,curveColorBgList,col,dropColor,textColor,paddingsDrop,dropFont)
        col = self.addSeparator(self.menu,col,menuColor,textColor,paddingsSep,sepFont)
        
        for i in range(len(labelListStr)):
            col = self.addLabel(self.menu,labelListStr[i],col,menuColor,textColor,paddingsLabel,labFont)
            self.textInputList[i].grid(column=col, row=0, sticky=tk.W, **paddingsInput)
            col = col +1
            self.textInputList[i].insert(0,inputSetList[i])
            col = self.addSeparator(self.menu,col,menuColor,textColor,paddingsSep,sepFont)
            
        for i in range(len(labelListCheck)):
            button = tk.Checkbutton(self.menu, text=labelListCheck[i],variable=self.checkListVar[i], onvalue=1, offvalue=0,bg=menuColor,bd=0,fg=textColor,selectcolor=menuColor,width=0,height=0)
            self.checkboxList.append(button)
            self.checkboxList[i].config(font=checkFont,pady=0,padx=0,borderwidth=0)
            self.checkboxList[i].grid(column=col, row=0, sticky=tk.W, **paddingsCheck)
            col = col +1
            col = self.addSeparator(self.menu,col,menuColor,textColor,paddingsSep,sepFont)
        
        genButton = Button( self.menu , text = "Generate Curve" , command = self.getParameters,height=0)
        genButton.config(bg=buttonColor,fg=textColor,pady=0,padx=0,borderwidth=0)
        genButton.grid(column=col, row=0, sticky=tk.W, **paddingsButton)
        col = col + 1
        exitButton = Button( self.menu , text = "X" , command = self.root.destroy ,width=5,height=0)
        exitButton.config(bg="red",fg=textColor,pady=0,padx=0,borderwidth=0)
        exitButton.grid(column=col, row=0, sticky=tk.W, **paddingsButton)
        
        self.menu.grid(column=0, row=0, sticky="nsew", **paddingMenu)
    
    def addLabel(self,menu,string,column,bgColor,textColor,padding,font=None) :
        label = tk.Label(menu, text = string,fg=textColor,bg=bgColor,width=0,height=0)
        if font!=None :
            label.config(font=font,pady=0,padx=0,borderwidth=0)
        label.grid(column=column, row=0, sticky=tk.W, **padding)
        return column+1
        #return menu
    
    def addDropMenu(self,menu,strList,column,bgColor,textColor,padding,font=None):
        borderwidth = 0
        width = 5
        height = 1
        if len(strList)>15 :
            width = 15
        highlightbackground=bgColor
        menuBg = "lightgray"
        dropMenu = StringVar(menu)
        dropMenu.set(strList[0])
        drop = OptionMenu(menu , dropMenu , *strList)
        drop.config(bg=bgColor,fg=textColor,borderwidth=borderwidth,highlightbackground=highlightbackground,activebackground=highlightbackground,width=width,height=height,font=font,pady=0,padx=0)
        if font!=None :
            drop.config(font=font)
        drop["menu"].config(bg=menuBg)
        drop.grid(column=column, row=0, sticky=tk.W, **padding)
        return column+1,dropMenu
    
    def addSeparator(self,menu,column,bgColor,textColor,padding,font=None) :
        return self.addLabel(menu,"|",column,bgColor,textColor,padding,font)
    
    def getCurveNameList(self) :
        seqList = []
        for seq in sq.sequence(display=False).getAllCurveConf() :
            seqList.append(seq[0])
        return seqList,len(seqList)
    
    # def generationLoopDynamical(self,timeIte):
    #     pixelPointList = []
    #     t = self.timeStart
    #     sys = ds.dynamicalSys("",self.frameIteration,10,self.sizeLimit)
    #     iteList = []
    #     start = time.time()
    #     for i in range(0,timeIte) :
    #         if self.refresh :
    #             self.canvas.delete("all")
    #         pointList = sys.getGeoList(t)
    #         pixelPointList = self.cleanPointList(c.getPixelFromPosList(pointList,self.pixelPerUnits,self.width,self.height,self.roundDigitPixel))
    #         self.pixelPointMat.append(pixelPointList)          
    #         t = t + self.timeIncrement
    #         for j in range(len(self.pixelPointMat)) :
    #             self.getNewCanvasDynamical(self.canvas,self.pixelPointMat[j],(j+1)/len(self.pixelPointMat))
    #         time.sleep(self.sleepTime)
    #         c.packCanvas(self.canvas,self.root)
    #         if len(self.pixelPointMat)>=self.dotShadow:
    #             self.pixelPointMat.pop(0)
    #         if self.print :
    #             print("Frame #"+str(i+1)," (t="+str(round(t,8))+", ite="+str(len(pointList))+", iteclean="+str(len(pointList)-len(pixelPointList))+")")
    #     end = time.time()
    #     if self.print :
    #         val = (end-start)/timeIte
    #         print("Finished in "+str(round(end-start,6))+"s ("+f"{val:.7f}"+"s/frame)")
    #     return 0
    
    def getNewCanvasDynamical(self,canvas,pointList,light=1): 
        color = self.pointColor
        for i in range(len(pointList)):
            if self.diffColors :
                color = colorsys.hsv_to_rgb((self.hueStretchDyn*i/len(pointList))%1,1,1)
            c.drawPoint(canvas,pointList[i],color,light,self.pointSize,self.pointShape)
    
    def cleanPointList(self,pointList):
        return self.dropPointDuplicates(self.dropPointOutside(pointList))
    
    def dropPointDuplicates(self,pointList):
        return [x for n, x in enumerate(pointList) if x not in pointList[:n]]
    
    def dropPointOutside(self,pointList):
        returnPointList = []
        for entry in pointList :
            if entry[0]>0 and entry[0]<self.width and entry[1]>0 and entry[1]<self.height :
                returnPointList.append(entry)
        return returnPointList
    
    #Curve def
    def generationLoopCurve(self,iteration):
        start = time.time()
        #self.resetCruve(self.dirStart)

        for i in range(0,iteration) :
            self.canvas.delete("all")
            self.canvas = self.drawBackground(self.canvas,self.width,self.height,self.backgroundColor)
            if self.print :
                print("Generation #"+str(i)+" of curve drawing")
            self.pointList = [self.posCurve]
            self.getPixelListCurve()
            #if len(self.pointList)<50000:
            self.drawCurve()
            
            if self.saveEnd :
                filename = "e#"+str(i+1)+"_"+self.sequenceName
                c.saveCanvas2(self.canvas,self.saveFolder,filename,self.saveFormat,self.width,self.height)
            if i!=iteration-1:
                self.sequenceName = self.seqList[i]
                #self.iteration = self.iteration + 1
                #self.radChange = math.pi*(1/(2+0.005*(i+1)))
                self.resetCruve(self.dirStart)
        end = time.time()
        if self.print :
            print("Generated in "+str(round(end-start,6))+"s")
            
    def resetCruve(self,direction,deleteSequence=True):
        if deleteSequence :
            del self.sequence
        printSequence = False
        if self.print and deleteSequence==True :
            printSequence = True
        self.sequence = sq.sequence(self.sequenceName,self.iteration,self.radChangeStart,self.maxSize,printSequence)
        self.series = self.sequence.sequence_generated
        self.radChange = self.sequence.radChange
        self.canvas.delete("all")
        self.canvas.configure(bg=self.backgroundColor)
        self.canvas = c.getCanvasFullScreen(self.root,self.width,self.height,self.backgroundColor)
        self.dir, self.posCurve = self.sequence.newStartDirPos(self.center,self.dirStart,self.startPos)
        self.frameCount = 0
        self.root.update()
        
    
    def getPixelListCurve(self):
        radChange = self.fractionToRad(self.radChange)
        pixelGenFrame = 0
        lineWidth = self.lineWidth
        while pixelGenFrame < len(self.series):
            for i in range(0,self.batchSize) :
                if pixelGenFrame >= len(self.series):
                    break
                self.genNewPointCurve(pixelGenFrame,radChange)
                pixelGenFrame += 1
        if self.center :
            offset = [-self.getCenter()[0]+self.startPos[0],-self.getCenter()[1]+self.startPos[1]]
        else :
            offset=[0,0]
        self.pointList = self.offsetListByPoint(self.pointList,offset)
        if self.optimalSize :
            self.pixelPerUnits = self.getOptimalSize()
    
    def genNewPointCurve(self,iteNum,radChange):
        mulTurn = 1
        mulLen = 1
        if self.frameCount%self.modMultiDir==0:
            mulTurn=self.multiDir
        if self.frameCount%self.modMultiLen==0:
            mulLen=self.multiLen
        turnRad = self.sequence.getSequenceEntry(iteNum,radChange)*mulTurn
        if self.curveSteps == 1 :
            self.turn(turnRad,mulLen)
            self.pointList.append(self.posCurve)
        else :
            mulLen = mulLen/(self.curveSteps+1)
            self.turn(0,mulLen)
            self.pointList.append(self.posCurve)
            for steps in range(0,self.curveSteps) :
                self.turn(turnRad/self.curveSteps,mulLen)
                self.pointList.append(self.posCurve)
    
    def drawCurve(self) :
        if self.printStats :
            self.drawStats()
        frame = 0
        start = time.time()
        lineWidth = self.lineWidth
        hueStretch = self.hueStretch*len(self.pointList)
        drawCount = 0
        while frame < len(self.pointList)-1:
            for i in range(0,self.batchSize) :
                if frame >= len(self.pointList)-1:
                    break
                if self.changeHue :
                    color = c.rgb_hack(colorsys.hsv_to_rgb(((frame/hueStretch)+self.hueOffset)%1, 1, 1))
                else :
                    color = self.defaultColor
                pos1 = c.getPixelFromPos(self.pointList[frame],self.pixelPerUnits,self.width,self.height,self.roundDigitPixel)
                pos2 = c.getPixelFromPos(self.pointList[frame+1],self.pixelPerUnits,self.width,self.height,self.roundDigitPixel)
                self.canvas.create_line(pos1[0],pos1[1],pos2[0],pos2[1],fill=color, width=lineWidth,tags="line")
                frame += 1
                # if math.log2(frame)%1==0 and self.print :
                #     print("Frame:"+str(frame)+" log2:"+str(int(math.log2(frame))))
            c.packCanvas(self.canvas,self.root)
            if self.saveAll :
                #filename = "#"+str(drawCount)+"_"+self.sequenceName
                filename = self.sequenceName+"/"+"#"+str(drawCount)
                #c.saveCanvas2(self.canvas,self.saveFolder,filename,self.saveFormat,self.width,self.height)
                c.saveCanvas2(self.canvas,self.saveFolder,filename,self.saveFormat,self.width,self.height,True,self.sequenceName)
            drawCount = drawCount + 1
            time.sleep(self.sleepTime)

        end = time.time()
        if self.print :
            val = (end-start)/max(frame,1)
            print("Curve drawn in "+str(round(end-start,6))+"s ("+f"{val:.7f}"+"s/frame)")
            
    def drawStats(self):
        textSize = 10
        textx = 5
        texty = 10
        textyAdd = textSize+4
        textfont=("Times",textSize,"normal")
        textColor = "white"
        ruleStr = ""
        for i in range(len(self.sequence.sequenceConf[1][3])) :
            ruleStr = ruleStr + "(" + list(self.sequence.sequenceConf[1][0])[i] + "→" + self.sequence.sequenceConf[1][3][i][0] + ")"
            if i+1!=len(self.sequence.sequenceConf[1][3]):
                ruleStr = ruleStr + " , "
        statListName = ["Number of segments :","Iteration :","Dimention :","L-system :","   Variables :","   Constants :","   Start :","   Angle :","   Rules :"]
        statListVal = [str(len(self.pointList)),str(self.sequence.actualItearion),"0","",str(self.sequence.sequenceConf[1][0]),"+−",str(self.sequence.sequenceConf[1][2]),"π×("+str(self.sequence.sequenceConf[2][0])+"/"+str(self.sequence.sequenceConf[2][1])+")",ruleStr]
        for i in range(len(statListName)) :
            self.canvas.create_text(textx, texty, anchor=W, font=textfont,text=statListName[i]+" "+statListVal[i],fill=textColor)
            texty = texty + textyAdd
    def turn(self,angle,step) :
        self.dir = self.dir + angle
        self.posCurve = [round(self.posCurve[0]+math.cos(self.dir)*step,self.roundDigitCurve),round(self.posCurve[1]+math.sin(self.dir)*step,self.roundDigitCurve)]
      
    def recenter(self) :
        self.posCurve = [(self.rightUpCorn[0]-self.leftDownCorner[0])/2,(self.rightUpCorn[1]-self.leftDownCorner[1])/2]
    
    def getCenter(self) :
        minx,maxx,miny,maxy=self.getPixelCorner()
        newCenter = [float((maxx+minx)/2),float((maxy+miny)/2)]
        return newCenter
    
    def getOptimalSize(self) :
        minx,maxx,miny,maxy=self.getPixelCorner()
        widthPixel = self.width
        heightPixel = self.height
        borderPixel = self.borderSize
        dx = max(1,maxx-minx)
        dy = max(1,maxy-miny)
        optSize=float(min((widthPixel-2*borderPixel)/dx,(heightPixel-2*borderPixel)/dy))
        optSize = min(optSize,100)
        return optSize
        
    def offsetListByPoint(self,pointList,point):
        newPointList = []
        for i in range(len(pointList)) :
            newPointList.append([pointList[i][0]+point[0],pointList[i][1]+point[1]])
        return newPointList
            
    def getPixelCorner(self) :
        xlist, ylist = map(list, zip(*self.pointList))
        return min(xlist),max(xlist),min(ylist),max(ylist)
    
    def drawBackground(self,canvas,width,height,color):
        canvas.create_rectangle(-10, -10, width+10, height+10, fill=color)
        return canvas
    
c = com.commons()
win = window()