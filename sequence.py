# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 20:49:26 2022

@author: Alexandre
"""
import numpy as np
import math 
import lsystem as ls
import time

class sequence :
    
    def __init__(self,name="null",iteration=0,radChange=0,maxSize=float("inf"),display=True):
        self.name = name
        self.lsystem = False
        self.iteration = iteration
        self.radChange = radChange
        self.sequence_generated = []
        self.maxSize = maxSize
        self.sequenceConf = []
        self.actualItearion = 0
        self.timeToGenerate = self.getSquence()
        
        if display :
            print("Seq '"+name+"' gen (frame:"+str(len(self.sequence_generated))+",ite:"+str(self.iteration)+")")
            print("Generated in "+str(round(self.timeToGenerate,6))+"s")
    
    def getSquence(self):
        start = time.time()
        allConf = self.getAllCurveConf()
        for i in range(len(allConf)) :
            if allConf[i][0]==self.name :
                self.sequenceConf = allConf[i]
                self.lsystem = True
                if "fiboword" not in self.name :
                    sys = self.setLSystem(allConf[i][1])
                    self.sequence_generated,self.actualItearion = sys.generate(self.iteration,self.maxSize)
                else :
                    if "densefiboword" in self.name :
                        string = fiboWorldDense(self.iteration)
                    else :
                        string = fiboWorld(self.iteration)
                    string = ls.lsystem().replaceString(string,allConf[i][1][3][0], allConf[i][1][3][1],2)
                    sys = self.setLSystem(allConf[i][1],string)
                    self.sequence_generated,self.actualItearion = sys.generate(self.iteration,self.maxSize)
                if allConf[i][2] != None :
                    self.radChange = allConf[i][2]

        if self.name == "fibo" :
            self.sequence_generated = sequenceToBinary([int(x) for x in list(fibonacci(self.iteration))])
        elif self.name== "prime" :
            self.sequence_generated = sequenceToBinary([int(x) for x in list(prime(self.iteration))])
        end = time.time()
        return end-start
    
    def getSequenceEntry(self,index,angle):
        entry = self.sequence_generated[index]
        if not self.lsystem :
            if entry==0 :
                return -angle
            elif entry==1 :
                return angle
            else :
                return 0
        else :
            return entry*angle

                
    def newStartDirPos(self,center,direction,pos) :
        # if center :
        #     if self.name == "hilb" :
        #         pos = [pos[0]-hilbertSize(self.iteration)/2,pos[1]-hilbertSize(self.iteration)/2]
        #     if self.name == "moore" :
        #         pos = [pos[0]-hilbertSize(self.iteration),pos[1]]
        return direction,pos
    
    def setLSystem(self,conf,readyString="") :
        return ls.lsystem(conf[0],conf[1],conf[2],conf[3],readyString)

    def getAllCurveConf(self) :
        defaultAngle = [1,2]
        allConf = []
        allConf.append(["dragon",["AB","F","FA",[["A+BF+"],["−FA−B"]]],defaultAngle])
        allConf.append(["hilb",["AB","F","A",[["+BF−AFA−FB+"],["−AF+BFB+FA−"]]],defaultAngle])
        allConf.append(["hilb2",["XY","F","X",[["XFYFX+F+YFXFY−F−XFYFX"],["YFXFY−F−XFYFX+F+YFXFY"]]],defaultAngle])
        allConf.append(["twindragon",["AB","F","FA+FA",[["A+BF"],["FA−B"]]],defaultAngle])
        allConf.append(["terdragon",["F","F","F",[["F+F−F"]]],[2,3]])
        allConf.append(["moore",["LR","F","LFL+F+LFL",[["−RF+LFL+FR−"],["+LF−RFR−FL+"]]],defaultAngle])
        allConf.append(["mink",["F","F","F",[["F+F−F−F+F"]]],defaultAngle])
        allConf.append(["minkisland",["F","F","F+F+F+F",[["F−F+F+FF−F−F+F"]]],defaultAngle])
        allConf.append(["sierptri",["FG","FG","F−G−G",[["F−G+F+G−F"],["GG"]]],[2,3]])
        allConf.append(["sierptri2",["FX","F","X",[["FF"],["−−FXF++FXF++FXF−−"]]],[1,3]])
        allConf.append(["sierptri3",["F","F","F",[["F+F−F−F+F"]]],[2,3]])
        allConf.append(["sierptri4",["FG","F","F",[["−G+F+G−"],["+F−G−F+"]]],[1,3]])
        allConf.append(["sierparr",["AB","AB","A",[["+B−A−B+"],["−A+B+A−"]]],[1,3]])
        allConf.append(["siersqua",["X","F","F+XF+F+XF",[["XF−F+F−XF+F+XF−F+F−X"]]],defaultAngle])
        allConf.append(["siercurve",["X","FG","F−−XF−−F−−XF",[["XF+G+XF−−F−−XF+G+X"]]],[1,4]])
        allConf.append(["siercarpet",["FG","FG","F",[["F+F−F−F−G+F+F+F−F"],["GGG"]]],defaultAngle])
        allConf.append(["levy",["F","F","F",[["+F−−F+"]]],[1,4]])
        allConf.append(["gosper",["AB","AB","A",[["A−B−−B+A++AA+B−"],["+A−BB−−B−A++A+B"]]],[1,3]])
        # allConf.append(["fiboword",["F","F","F",[["01","10","00"], ["F−F","FF+","F−F+"]]],defaultAngle])
        # allConf.append(["densefiboword1",["F","F","F",[["1","2","0"],["+F","−F","+F−F"]]],defaultAngle])
        # allConf.append(["densefiboword2",["F","F","F",[["1","2","0"], ["+F","−F","F"]]],defaultAngle])
        # allConf.append(["densefiboword3",["F","F","F",[["1","2","0"], ["F−F","+FF","−F+F"]]],defaultAngle])
        # allConf.append(["densefiboword4",["F","F","F",[["1","2","0"], ["+F","−F",""]]],defaultAngle])
        allConf.append(["koshcurve",["F","F","F",[["F+F−−F+F"]]],[1,3]])
        allConf.append(["koshsnow",["F","F","F−−F−−F",[["F+F−−F+F"]]],[1,3]])
        allConf.append(["koshcurvehalf",["F","F","+F−−F+F",[["F+F−−F+F"]]],[1,3]])
        allConf.append(["koshisland",["F","F","F+F+F+F",[["F−F+F+FFF−F−F+F"]]],defaultAngle])
        allConf.append(["koshisland2",["F","F","F+F+F+F",[["F−FF+FF+F+F−F−FF+F+F−F−FF−FF+F"]]],defaultAngle])
        allConf.append(["koshisland3",["XY","F","X+X+X+X+X+X+X+X",[["X+YF++YF−FX−−FXFX−YF+X"],["−FX+YFYF++YF+FX−−FX−YF"]]],[1,4]])
        allConf.append(["peano",["F","F","F",[["F+F−F−F−F+F+F+F−F"]]],defaultAngle])
        allConf.append(["peano2",["XY","F","X",[["XFYFX+F+YFXFY−F−XFYFX"],["YFXFY−F−XFYFX+F+YFXFY"]]],defaultAngle])
        allConf.append(["box",["F","F","F+F+F+F",[["F+F−F−F+F"]]],defaultAngle])
        allConf.append(["box2",["F","F","F+F+F+F",[["FF+F−F+F+FF"]]],defaultAngle])
        allConf.append(["triangle",["F","F","F+F+F",[["F−F+F"]]],[2,3]])
        allConf.append(["quadgosper",["XY","F","−YF",[["XFX−YF−YF+FX+FX−YF−YFFX+YF+FXFXYF−FX+YF+FXFX+YF−FXYF−YF−FX+FX+YFYF−"],["+FXFX−YF−YF+FX+FXYF+FX−YFYF−FX−YF+FXYFYF−FX−YFFX+FX+YF−YF−FX+FX+YFY"]]],defaultAngle])
        allConf.append(["crystal",["F","F","F+F+F+F",[["FF+F++F+F"]]],defaultAngle])
        allConf.append(["board",["F","F","F+F+F+F",[["FF+F+F+F+FF"]]],defaultAngle])
        allConf.append(["cross",["F","F","F+F+F+F",[["F+FF++F+F"]]],defaultAngle])
        allConf.append(["cross2",["F","F","F+F+F+F",[["F+F−F+F+F"]]],defaultAngle])
        allConf.append(["cross3",["F","F","F+F+F+F",[["F+FF−F−FF+F"]]],defaultAngle])
        allConf.append(["penta",["F","F","F++F++F++F++F",[["F++F++F+++++F−F++F"]]],[1,5]])
        allConf.append(["pentadendrite",["F","F","F−F−F−F−F",[["F−F−F++F+F−F"]]],[2,5]])
        allConf.append(["ring",["F","F","F+F+F+F",[["FF+F+F+F+F+F−F"]]],defaultAngle])
        allConf.append(["krishna",["X","F","−X−−X",[["XFX−−XFX"]]],[1,4]])
        allConf.append(["chaosstar",["F","F","F++F++F++F",[["F+FF+++F++F−FF+++F++F−−F"]]],[1,4]])
        allConf.append(["koshcurvetri",["F","F","F++F++F",[["F+F−−F+F"]]],[1,3]])
        #allConf.append(["roundstar",["F","F","F−F−F−F",[["F++F"]]],[135,180]])
        #allConf.append(["roundstar2",["F","F","F−F−F−F−F−F−F−F",[["F++F"]]],[65,180]])
        allConf.append(["test",["F","F","F",[["F−F+F−F−F−F+F+F+F−F+F"]]],defaultAngle])
        allConf.append(["test2",["F","F","F+F+F+F",[["F+F−F−F−F+F+F+F−F"]]],defaultAngle])
        allConf.append(["crystal2",["F","F","F+F+F+F",[["FF+F++F+FF"]]],defaultAngle])
        allConf.append(["island",["FB","F","F−F−F−F",[["F−B+FF−F−FF−FB−FF+B−FF+F+FF+FB+FFF"],["BBBBBB"]]],defaultAngle])
        
        return allConf


def dragon(n,startSeq=[1],startSplit=[1]):
    seq = startSeq
    split = startSplit
    for i in range(0, n):
      newSeq = []
      newSeq.extend(seq)
      newSeq.extend(split)
      newSeq.extend(invertBinary(invertIndex(seq)))
      seq = newSeq
    return seq

def hilbert(n): 
    bridge = [[[1,0],[-1,-1],[0,1]],[[0,1],[0,0],[1,0]]]
    series = [1,1]
    for i in range(0,n) :
        series = multiplyList(series,-1)+bridge[i%2][0]+series+bridge[i%2][1]+series+bridge[i%2][2]+multiplyList(series,-1)
    return [0]+series

def fibonacci(n):
    fibonacciSeries = [0,1]
    if n>2:
	    for i in range(2, n):
		    nextElement = fibonacciSeries[i-1] + fibonacciSeries[i-2]
		    fibonacciSeries.append(nextElement)
    return fibonacciSeries

def prime(n):
    prime_list = []
    for i in range(0, n):
        if i == 0 or i == 1:
            continue
        else:
            for j in range(2, int(i/2)+1):
                if i % j == 0:
                    break
            else:
                prime_list.append(i)
    return prime_list

def fiboWorld(n):
    series = ["0","01"]
    for i in range(2,n+1) :
        series.append(series[i-1]+series[i-2])
    return series[n]

def fiboWorldDense(n):
    series = ["0","01"]
    for i in range(2,n+1) :
        series.append(series[i-1]+series[i-2])
    return_str = ls.lsystem().replaceString(series[n], ["01","10","00"], ["1","2","0"],2)
    return return_str

def fiboWorld2(n):
    series = ["0","01"]
    for i in range(2,n+1):
        if i%3==2 :
            series.append(series[i-1]+invertBinaryString(series[i-2]))
        else :
            series.append(series[i-1]+series[i-2])
    return series[n]

def sequenceToBinary(sequence) :
    seqMin = min(sequence)
    seqMax = max(sequence)
    binarySequence = []
    for i in range(seqMin,seqMax) :
        if i in sequence :
            #if i%2==0 :
            binarySequence.append(1)
            #else :
            #    binarySequence.append(0)
        else :
            binarySequence.append(-1)
    return binarySequence
    
def multiplyList(sequence,multiplier):
    return list(np.array(sequence)*multiplier)

def invertBinary(sequence):
    return_seq = []
    for i in range(len(sequence)) :
        if sequence[i]==1:
            return_seq.append(0)
        elif sequence[i]==0:
            return_seq.append(1)
    return return_seq

def invertBinaryString(string):
    return_str = ""
    for i in range(len(string)) :
        if string[i]=="1":
            return_str = return_str + "0"
        elif string[i]=="0":
            return_str = return_str + "1"
    return return_str


def invertIndex(sequence):
    return_seq = []
    for i in range(len(sequence)) :
        return_seq.append(sequence[-i-1])
    return return_seq

def hilbertSize(iteration):
    size = 0
    for i in range(0,iteration):
        size = size*2+1
    return size
