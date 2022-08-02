# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:56:03 2022

@author: Alexandre
"""
class lsystem :
    def __init__(self,alphabet="",constants="",axiom="",rules=[""],readyString=""):
        self.alpha = list(alphabet)
        self.const = list(constants)
        self.axiom = axiom
        self.rules = rules
        self.beta = []
        self.constMaxRep = 30
        self.readyString = readyString
        for i in range(len(self.alpha)) :
            self.beta.append(i)
    
    def generate(self,n,maxSize=float("inf")) :
        seqStr = ""
        actualIte = 0
        if self.readyString=="":
            seqStr = self.axiom
            for i in range(n):
                seqStrNew = seqStr
                for j in range(len(self.alpha)) :
                    seqStrNew = seqStrNew.replace(self.alpha[j], self.toBeta(self.rules[j][0]))
                seqStrNew = self.toAlpha(seqStrNew)
                if len(seqStrNew)>maxSize:
                    actualIte = i+1
                    break
                seqStr = seqStrNew
                actualIte = i+1
        else :
            seqStr = self.readyString
        return_list = self.rawSequenceToFinalList(seqStr)
        return return_list,actualIte
    
    def rawSequenceToFinalList(self,rawString):
        return_str = self.stripAlpha(rawString)
        return_str = self.stripCanceling(return_str,["+−","−+"])
        maxRep = self.constMaxRep
        for constant in self.const :
            for i in range(maxRep) :
                return_str = self.replaceString(return_str,["+"*(maxRep-i-1)+constant,"−"*(maxRep-i-1)+constant],[str((maxRep-i-1)%8),str(-((-(-maxRep+i+1))%8))])
        return_str = self.stripCanceling(return_str,["+","−"])
        return_list = aggNegative(list(return_str))       
        return_list = self.listStrToInt(return_list)
        return return_list
    
    def toBeta(self,string):
        for i in range(len(self.alpha)) :
            string = string.replace(self.alpha[i],str(self.beta[i]))
        return string
    
    def toAlpha(self,string):
        for i in range(len(self.alpha)) :
            string = string.replace(str(self.beta[i]),self.alpha[i])
        return string
    
    def stripAlpha(self,string):
        for i in range(len(self.alpha)) :
            if self.alpha[i] not in self.const :
                string = string.replace(self.alpha[i],"")
        return string
    
    def stripCanceling(self,string,cancelList):
        for i in range(len(cancelList)):
            string = string.replace(cancelList[i],"")
        return string
    
    def replaceString(self,string,oldList,newList,batch=0):
        if batch==0:
            for i in range(len(oldList)) :
                string = string.replace(oldList[i],newList[i])
            return_string = string
        else :
            return_string = ""
            for i in range(int(len(string)/batch)) :
                tempStr = string[i*batch:(i+1)*batch]
                for j in range(len(oldList)) :
                    tempStr = tempStr.replace(oldList[j],newList[j])
                return_string = return_string+tempStr
        return return_string
    
    def replaceList(self,rootList,oldList,newList):
        for i in range(len(oldList)) :
            rootList = list(map(lambda x: x.replace(oldList[i], newList[i]), rootList))
        return rootList
    
    def listStrToInt(self,strList):
        return [int(x) for x in strList]

        

def difList(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))
    
def aggNegative(stringList):
    i = 0
    while i < len(stringList):
        if stringList[i]=="-":
            stringList[i] = "-"+stringList[i+1]
            stringList.pop(i+1)
        else :
            i = i+1
    return stringList 

            