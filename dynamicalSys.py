# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 15:57:26 2022

@author: Alexandre
"""
import random
class dynamicalSys :
           
    def __init__(self,function5="",iteration=100,pointRound=10,sizeLimit=float("inf")):
        self.function = self.function(seed=str(random.randint(0,100)))
        self.iteration = iteration
        self.pointRound = pointRound
        self.sizeLimit = sizeLimit
    
    def getGeoList(self,t) :
        x = t
        y = t
        geoList = [[x,y]]
        for i in range(self.iteration) :
            x,y = self.function.getNewPoint(x,y,t)
            geoList.append([round(x,self.pointRound),round(y,self.pointRound)])
            if abs(x)+abs(y)>self.sizeLimit:
                break
        print(geoList[-10:-1])
        return geoList 
    
    class function :
        
        def __init__(self,geoVars="",timeVar="",seed="a") :
            self.geoVars = geoVars
            self.timeVar = timeVar
            self.seed = seed
            random.seed(self.seed)
            self.sx = [random.getrandbits(1) for i in range(20)]
            self.sy = [random.getrandbits(1) for i in range(20)]
            print(self.sx,"   ",self.sy)
        #(x**2)+(y**2)+(t**2)+x*y+t*x+t*y    
        def getNewPoint(self,x,y,t) :
            x2 = -(t**2)-x*y+t
            y2 = -x*y+x*t+y+t
            return x2,y2
        
        # def getNewPoint(self,x,y,t) :
        #     x2 = -(x**2)+x*t+y
        #     y2 = (x**2)-(y**2)-(t**2)-x*y+y*t-x+y
        #     return x2,y2
        
        # def getNewPoint(self,x,y,t) :
        #     x2 = (x**2)-(y**2)-(t**2)-x-t
        #     y2 = (y**2)+(t**2)-x*y-y-t
        #     return x2,y2
        
        # def getNewPoint(self,x,y,t) :
        #     x2 = -(x**2)+(y**2)+(t**2)-x*y-t*y-t
        #     y2 = (y**2)-x+t
        #     return x2,y2
        
        # def getNewPoint(self,x,y,t):
        #     return self.getNewPointSeries(x,y,t,self.sx,self.sy)
        
        # def getNewPointSeries(self,x,y,t,sx,sy):
        #     x2 = (-2)*(sx[0]-0.5)*(x**2)*sx[1]+(-2)*(sx[2]-0.5)*(y**2)*sx[3]+(-2)*(sx[4]-0.5)*(y**2)*sx[5]+(-2)*(sx[6]-0.5)*x*y*t*sx[7]+(-2)*(sx[8]-0.5)*x*y*sx[9]+(-2)*(sx[10]-0.5)*x*t*sx[11]+(-2)*(sx[12]-0.5)*y*t*sx[13]+(-2)*(sx[14]-0.5)*x*sx[15]+(-2)*(sx[16]-0.5)*y*sx[17]+(-2)*(sx[18]-0.5)*t*sx[19]
        #     y2 = (-2)*(sy[0]-0.5)*(x**2)*sy[1]+(-2)*(sy[2]-0.5)*(y**2)*sy[3]+(-2)*(sy[4]-0.5)*(y**2)*sy[5]+(-2)*(sy[6]-0.5)*x*y*t*sy[7]+(-2)*(sy[8]-0.5)*x*y*sy[9]+(-2)*(sy[10]-0.5)*x*t*sy[11]+(-2)*(sy[12]-0.5)*y*t*sy[13]+(-2)*(sy[14]-0.5)*x*sy[15]+(-2)*(sy[16]-0.5)*y*sy[17]+(-2)*(sy[18]-0.5)*t*sy[19]
        #     return x2,y2