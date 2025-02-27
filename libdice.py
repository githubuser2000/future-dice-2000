#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import math
import random
from PyQt5.QtCore import QObject, QTranslator, QLocale, QCoreApplication
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtQml import QQmlApplicationEngine
    #from collections import defaultdict
    # argv
    # 1 ist würfel bis zahl
    # 2 ist lin log root etc
    # zahl n, bei lin zB Schrittweite
    # zahl die definiert werden sein soll z.B. 5 Augen als kurz vor Maximum
    # sys.argv

#self.str_lin = QCoreApplication.translate('lin','lin')
#self.str_log = QCoreApplication.translate('log','log')
#self.str_root = QCoreApplication.translate('root','root')
#self.str_poly = QCoreApplication.translate('poly','poly')
#self.str_exp = QCoreApplication.translate('exp','exp')
#self.str_kombi = QCoreApplication.translate('kombi','kombi')
#self.str_logistic = QCoreApplication.translate('logistic','logistic')
#self.str_rand = QCoreApplication.translate('rand','rand')
#self.str_gewicht = QCoreApplication.translate('gewicht','gewicht')
#self.str_add = QCoreApplication.translate('add','add')
#self.str_mul = QCoreApplication.translate('mul','mul')
#self.str_wurf = QCoreApplication.translate("Wuerfelwurf: ","Würfelwurf: ")
#self.str_augen = QCoreApplication.translate(" (Wuerfelaugen "," (Würfelaugen ")

def getIndexByKey(key_, dictmap):
    for i,(key,value) in enumerate(dictmap.items()):
        if key_ == key:
            return i,value
    return None


class dice(QQmlApplicationEngine):

    def sigmoid(self,x,n,xe,e,xth=0):
        try:
            x-=int(self.inpp_[1])/2
            xe-=int(self.inpp_[1])/2
            return ( n / (n + math.exp(-x)) ) / ( n / (n + math.exp(-xe)) ) * e
        except:
            return 0

    def lin(self,x,n,xe,e,xth=0):
        try:
            return (x * e) / xe
        except:
            return 0
    def log(self,x,n,xe,e,xth=0):
        try:
            if math.log(xe,n) * e != 0:
                return math.log(x,n) / math.log(xe,n) * e
            else:
                return 0
        except:
            return 0
    def root(self,x,n,xe,e,xth=0):
        try:
            return pow(x,1/n) / pow(xe,1/n) * e
        except:
            return 0
    def poly(self,x,n,xe,e,xth=0):
        try:
            return pow(x,n) / pow(xe,n) * e
        except:
            return 0
    def expo(self,x,n,xe,e,xth=0):
        try:
            return pow(n,x) / pow(n,xe) * e
        except:
            return 0

    def randselect(self,includex):

            d = 1000

            #print("CC "+str((includex)))
            if not len(includex) == 4:
                flag1 = False
                for i,inc in enumerate(includex):
                    if self.randfkt[i+1].__name__ == dice.strlist[5]:
                        pass
                    elif self.randfkt[i+1].__name__ == dice.strlist[8]:
                        pass
                    elif self.randfkt[i+1].__name__ == dice.strlist[7]:
                        pass
                    elif inc:
                        flag1 = True
                if not flag1:
                    return 1
                self.randfktvarx = random.randrange(len(includex))+1

                while not includex[self.randfktvarx-1] or self.randfkt[self.randfktvarx].__name__ == dice.strlist[8]:
                    d-=1
                    if d <= 0:
                        return 1
                    self.randfktvarx = random.randrange(len(includex))+1
                return self.randfktvarx
            else:
                flag1 = False
                for i,inc in enumerate(includex):
                    if inc:
                        flag1 = True
                if flag1:
                    self.randfktvarx = random.randrange(len(includex))+1
                    while not includex[self.randfktvarx-1]:
                        d-=1
                        if d <= 0:
                            return 1
                        self.randfktvarx = random.randrange(len(includex))+1
                    #print("BB "+str(self.randfktvarx))
                    return self.randfktvarx
                else:
                    #print("AA 1")
                    return 1

    def kombi(self,x,n,xe,e,xth=0, reku = 50):
        try:
        #if True:
#            okay1 = False
#            okay2 = False
#            for i,k in zip(self.include1,self.include2):
#                if i:
#                    okay1 = True
#                if k:
#                    okay2 = True
#
            #if not okay1 or not okay2:
            #    return None
            self.randfktvar1,self.randfktvar2,self.randfktvar3 = self.randselect(self.include1),self.randselect(self.include2),self.randselect(self.include3)
            #print("-- "+str(self.randfktvar1)+" "+str(self.randfktvar2)+" "+str(self.randfktvar3))

            if self.randfktvar3 == 1:
                print("Kombi Mulitply: "+str(self.randfkt2[self.randfktvar1])+" "+str(self.randfkt2[self.randfktvar2]))
                return self.randfkt[self.randfktvar1](x,n,xe,e) * self.randfkt[self.randfktvar2](x,n,xe,e)
            elif self.randfktvar3 == 2:
                print("Kombi Addition "+str(self.randfkt2[self.randfktvar1])+" "+str(self.randfkt2[self.randfktvar2]))
                return self.randfkt[self.randfktvar1](x,n,xe,e) + self.randfkt[self.randfktvar2](x,n,xe,e)
            elif self.randfktvar3 == 3:
                print("Kombi Logarithm "+str(self.randfkt2[self.randfktvar1])+" "+str(self.randfkt2[self.randfktvar2]))
                return math.log(self.randfkt[self.randfktvar1](x,n,xe,e)+1.1,self.randfkt[self.randfktvar2](x,n,xe,e)+1.1)
            elif self.randfktvar3 == 4:
                print("Kombi Root "+str(self.randfkt2[self.randfktvar1])+" "+str(self.randfkt2[self.randfktvar2]))
                return pow(self.randfkt[self.randfktvar1](x,n,xe,e), 1 / ( self.randfkt[self.randfktvar2](x,n,xe,e) + 1 ))
        except:
            if reku > 0:
                reku -= 1
                return self.kombi(x,n,xe,e,xth,reku)

    def gewicht(self,type1,x,n,xe,e,type2,n2,xe2,e2):
        return ( self.fkt[type1](x,n,xe,e),
                self.fkt[type2](x,n2,xe2,e2,1) )


    def rand(self,x,n,xe,e,xth=0):
        okay1 = False
        for i in self.include1:
            if i:
                okay1 = True
        if not okay1:
            return 1
        self.randfktvarA = self.randselect(self.include1 if xth == 0 else self.include2)
        result = self.randfkt[self.randfktvarA](x,n,xe,e,xth)
        return result



    def weightedrand(self,weights):
        #print("ww "+str(weights))
        self.summ = 0
        sum2 = []
        for weight in weights:
            self.summ += weight
            sum2.append(self.summ)

        rand1 = random.random() * self.summ

        for i,asum in enumerate(sum2):
            if rand1 < asum:
                return i # +1
        return None

    def wuerfelAugenSetNearEmpty(self):
        summe2 = 0
        for index in self.wuerfelAugenSet:
            summe2 += self.randos[index]
#        for rando in self.randos:
#            summe2 += rando
        print("w "+str(self.summ)+" "+str(summe2))
        diff = self.summ - summe2
        return True if abs(diff) <= 0.000001 else False

    def wuerfeln(self):
        self.wuerfelWuerfe2 = []
        print("- "+str(self.wuerfelAugenSet)+"-"+str(self.values))
        if len(self.wuerfelAugenSet) == len(self.values):
            self.wuerfelAugenSet = set()
        if self.wuerfelType == 0:
            while True:
                dice = random.randrange(len(self.values))
                if not dice in self.wuerfelAugenSet or not self.uniq:
                    self.wuerfelAugenSet.add(dice)
                    break
            self.wuerfelWuerfe2.append((dice,self.values[dice],self.bezeichners[dice]))
            self.wuerfelWuerfe.append((dice,self.values[dice],self.bezeichners[dice]))
            print(self.str_wurf+str(self.values[dice])+self.str_augen+str(dice+1)+")")
        elif self.wuerfelType == 1:
            while True:
                dice = self.weightedrand(self.randos)
                print("_ "+str(dice))
                print(str(self.wuerfelAugenSet))
                print(str(self.wuerfelAugenSetNearEmpty()))
                print(str(self.uniq))
                if (not dice in self.wuerfelAugenSet or self.wuerfelAugenSetNearEmpty()) \
                or not self.uniq:
                    self.wuerfelAugenSet.add(dice)
                    break
            #print("rand augenzahl ergebnis: "+str(dice))
            #dice = random.randrange(inp[1])+1
            #ergebnis = (self.randos[dice],self.values[dice])
            ergebnis = (self.values[dice],self.randos[dice])
            self.wuerfelWuerfe2.append((dice,ergebnis[0],ergebnis[1],self.bezeichners[dice]))
            self.wuerfelWuerfe.append((dice,ergebnis[0],ergebnis[1],self.bezeichners[dice]))
            print(self.str_wurf+str(self.randos[dice])+self.str_augen+str(dice)+")")
        return self.wuerfelWuerfe2

    def __init__(self,inp,werfen = 2, uniq_ = False, bezeichner : str = "", negativ = False, median = False):
        super(dice,self).__init__()
        #self.languages()
        #app = QtWidgets.QApplication(sys.argv)
        #translator = QTranslator()
        #translator.load(os.path.dirname(__file__)+os.sep+'dice.qm')
        #app.installTranslator(translator)
        print(str(inp))
        print(str(bezeichner))

        self.negativ = negativ
        self.median = median
        self.bezeichner = bezeichner
        self.wuerfeltype = None
        self.wuerfelAugenSet = set()
        self.fkt = { dice.strlist[0] : self.lin,
            dice.strlist[1] : self.log,
            dice.strlist[2] : self.root,
            dice.strlist[3] : self.poly,
            dice.strlist[4] : self.expo,
            dice.strlist[7] : self.rand,
            dice.strlist[5] : self.kombi,
            dice.strlist[8] : self.gewicht,
            '-'+dice.strlist[0] : self.lin,
            '-'+dice.strlist[1] : self.log,
            '-'+dice.strlist[2] : self.root,
            '-'+dice.strlist[3] : self.poly,
            '-'+dice.strlist[4] : self.expo,
            '-'+dice.strlist[5] : self.rand,
            '-'+dice.strlist[6] : self.kombi,
            dice.strlist[6] : self.sigmoid,
            '-'+dice.strlist[6] : self.sigmoid}



        self.randfkt = { 1 : self.lin,
            2 : self.log,
            3 : self.root,
            4 : self.poly,
            5 : self.expo,
            6 : self.kombi,
            7 : self.sigmoid,
            8 : self.rand,
            9 : self.gewicht}


        #self.randfkt2 = { 1 : self.str_lin,
        #    2 : self.str_log,
        #    3 : self.str_root,
        #    4 : self.str_poly,
        #    5 : self.str_exp,
        #    6 : self.str_kombi,
        #    7 : self.str_logistic,
        #    8 : self.str_rand,
        #    9 : self.str_gewicht}
#
#        self.randfkt3 = { 1 : 'mul',
#            2 : 'add',
#            3 : self.str_log,
#            4 : self.str_root}
        self.inpp_ = inp
        self.wuerfelWuerfe = werfen
        self.uniq =uniq_
        self.wuerfelWuerfe = []
        self.wuerfelWuerfeMoeglichkeiten = {}

        #if len(self.bezeichners) > 0:
        #    if self.bezeichners[-1] == "?":
        #        self.bezeichner = " ".join(self.bezeichners)

        if len(inp) > 3:
            if type(inp[-3]) is list and type(inp[-2]) is list and type(inp[-1]) is list:
                self.include1,self.include2,self.include3 = inp[-3],inp[-2],inp[-1]
                #print('_'+str(self.include3))
                inp=inp[:-3]
            else:
                i1,i2,i3 = [],[],[True,True,True,True]
                for i in range(len(self.randfkt2)):
                    i1.append(True)
                    i2.append(True)
                self.include1,self.include2,self.include3 = i1,i2,i3
        print(inp[2]+" "+dice.strlist[8])

        bezeichnerlist = bezeichner.split()
        flag = True
        flag2 = True
        flag3 = False
        flag4 = False
        flag5 = False
        self.randos = []
        self.values = []
        bezeichnerNeuList = []
        for i,bezeichnung in enumerate(bezeichnerlist):
            if i % 2 == 0 and not bezeichnung.isdigit():
                bezeichnerNeuList.append(bezeichnung)
            elif i % 2 == 1 and bezeichnung.isdigit():
                self.values.append(int(bezeichnung))
            else:
                flag = False
        if not flag:
            self.randos = []
            self.values = []
            bezeichnerNeuList = []
            for i,bezeichnung in enumerate(bezeichnerlist):
                if i % 3 == 0 and not bezeichnung.isdigit():
                    bezeichnerNeuList.append(bezeichnung)
                elif i % 3 == 1 and bezeichnung.isdigit():
                    self.values.append(int(bezeichnung))
                elif i % 3 == 2 and bezeichnung.isdigit():
                    self.randos.append(int(bezeichnung))
                else:
                    flag2 = False

        if len(bezeichnerlist) % 2 == 0 and flag:
            bezeichner = " ".join(bezeichnerNeuList)
            self.bezeichner = bezeichner.strip()
            self.bezeichners = bezeichnerNeuList
            flag4 = True
        elif len(bezeichnerlist) % 3 == 0 and flag2 and len(inp) == 11 and inp[2] == dice.strlist[8]:
            #inp[1] = int(inp[1]) / 3
            bezeichner = " ".join(bezeichnerNeuList)
            self.bezeichner = bezeichner.strip()
            self.bezeichners = bezeichnerNeuList
            flag5 = True
        else:
            self.values = []
            self.randos = []

        self.bezeichners = str(bezeichner).split()
        if not self.bezeichner == "":
            while len(self.bezeichners) < int(inp[1]):
                self.bezeichners.append("?")
        else:
            while len(self.bezeichners) < int(inp[1]):
                self.bezeichners.append("")

        if len(inp) == 6:
            until = int(inp[1])
            inp[4] = int(inp[4])
            inp[5] = float(inp[5])
            inp[3] = float(inp[3])
            inp[1] = int(inp[1])
            #print("UU-"+str(inp[1])+" "+str(inp[4])+" ")
            print(str(inp[2]))
            if inp[4] <= inp[1] and inp[4] > 0 and inp[2] != dice.strlist[8]:
                if not flag4 or len(self.values) < 2:
                    self.values = []
                    for a in range(1,until+1):
                        self.values.append(self.fkt[inp[2]](a,inp[3],inp[4],inp[5]))
                if inp[2][0]=='-':
                    self.values.reverse()
                for i,(value, bezeich) in enumerate(zip(self.values,self.bezeichners)):
                    self.wuerfelWuerfeMoeglichkeiten[i] = [value, bezeich]
                    print(str(i+1)+": "+str(value))
                self.wuerfelType = 0
        elif len(inp) == 11 and inp[2] == dice.strlist[8]:
            #print("d")
            until = int(inp[1])
            inp[4] = int(inp[4])
            inp[5] = int(inp[5])
            inp[6] = float(inp[6])
            inp[1] = int(inp[1])
            inp[8] = float(inp[8])
            inp[9] = int(inp[9])
            inp[10] = float(inp[10])
            if inp[5] <= inp[1] and inp[5] > 0 and inp[9] <= inp[1] and inp[9] > 0:
                if not flag5 or len(self.values) < 2:
                    self.values = []
                    self.randos = []
                    for a in range(1,until+1):
                        thing = self.fkt[inp[2]](inp[3],a,inp[4],inp[5],inp[6],inp[7],inp[8],inp[9],inp[10])
                        self.values.append(thing[0])
                        self.randos.append(thing[1])
                if inp[3][0]=='-':
                    self.values.reverse()
                if inp[7][0]=='-':
                    self.randos.reverse()
                for i,(rando,value,bezeich) in enumerate(zip(self.values,self.randos,self.bezeichners)):
                    self.wuerfelWuerfeMoeglichkeiten[i] = [rando,value,bezeich]
                    #print(str(i+1)+": "+str(value))
                    print(str(i+1)+": "+str(rando)+", "+str(value))
                self.wuerfelType = 1
        else:
            return None
        if self.negativ:
            #avg = 0
            #for key,wert in self.wuerfelWuerfeMoeglichkeiten.items():
            #    avg += float(wert[len(self.wuerfelWuerfeMoeglichkeiten)- 2])
            #avg = avg / len(self.wuerfelWuerfeMoeglichkeiten)
            self.values = []
            middle = self.wuerfelWuerfeMoeglichkeiten[int(len(self.wuerfelWuerfeMoeglichkeiten)/2)][0]
            for key,wert in self.wuerfelWuerfeMoeglichkeiten.items():
                #print("p "+str(self.wuerfelWuerfeMoeglichkeiten[int(len(self.wuerfelWuerfeMoeglichkeiten)/2)][0]))
                #print("p "+str((self.wuerfelWuerfeMoeglichkeiten[key])))
                #print(self.wuerfelWuerfeMoeglichkeiten[int(len(self.wuerfelWuerfeMoeglichkeiten)/2)][len(self.wuerfelWuerfeMoeglichkeiten[0])- 2])
                #print(str(self.wuerfelWuerfeMoeglichkeiten[int(len(self.wuerfelWuerfeMoeglichkeiten)/2)][len(self.wuerfelWuerfeMoeglichkeiten)- 2]))
                wert[0] -= middle
                self.values.append(wert[0])
        for i in range(werfen):
            self.wuerfelWuerfe.append(self.wuerfeln())
        self.result = (self.wuerfelWuerfeMoeglichkeiten,self.wuerfelWuerfe)
        print(str(self.result))

    def out(self):
        return self.result

    translator = None

    @staticmethod
    def __langs__(QUrl):
        #return {QLocale.German : (os.path.dirname(__file__)+os.sep+'dice-de.qm',QUrl('qrc:/deutschland.png')),QLocale.English : (os.path.dirname(__file__)+os.sep+'dice-en.qm',QUrl('qrc:/usa.png')),QLocale.Korean : (os.path.dirname(__file__)+os.sep+'dice-kr.qm',QUrl('qrc:/korea.png'))}
        return {QLocale.German : (os.path.dirname(__file__)+os.sep+'dice-de.qm',QUrl('qrc:/deutschland.png')),QLocale.Korean : (os.path.dirname(__file__)+os.sep+'dice-kr.qm',QUrl('qrc:/korea.png')),QLocale.English : (os.path.dirname(__file__)+os.sep+'dice-en.qm',QUrl('qrc:/usa.png')),QLocale.Chinese : (os.path.dirname(__file__)+os.sep+'dice-cn.qm',QUrl('qrc:/china.png')),QLocale.Polish : (os.path.dirname(__file__)+os.sep+'dice-pl.qm',QUrl('qrc:/polen.png')),QLocale.Japanese : (os.path.dirname(__file__)+os.sep+'dice-jp.qm',QUrl('qrc:/japan.png')),QLocale.Portuguese : (os.path.dirname(__file__)+os.sep+'dice-pt.qm',QUrl('qrc:/portugal.png')),QLocale.Russian : (os.path.dirname(__file__)+os.sep+'dice-ru.qm',QUrl('qrc:/russland.png')),QLocale.Spanish : (os.path.dirname(__file__)+os.sep+'dice-es.qm',QUrl('qrc:/spanien.png')),QLocale.Italian : (os.path.dirname(__file__)+os.sep+'dice-it.qm',QUrl('qrc:/italien.png')),QLocale.Czech : (os.path.dirname(__file__)+os.sep+'dice-cz.qm',QUrl('qrc:/tschechien.png')),QLocale.Hindi : (os.path.dirname(__file__)+os.sep+'dice-in.qm',QUrl('qrc:/indien.png')),QLocale.Dutch : (os.path.dirname(__file__)+os.sep+'dice-nl.qm',QUrl('qrc:/niederlande.png')),QLocale.Hebrew : (os.path.dirname(__file__)+os.sep+'dice-il.qm',QUrl('qrc:/israel.png')),QLocale.French : (os.path.dirname(__file__)+os.sep+'dice-fr.qm',QUrl('qrc:/frankreich.png'))}
    @staticmethod
    def __langu1__(key, QUrl):
        langs = dice.__langs__(QUrl)
        print(str(dice.langNum))
        return list(langs.values())[(dice.langNum + 1) % len(langs)] + ((dice.langNum + 1) % len(langs),)

    @staticmethod
    def __langu__(key, QUrl):
        langs = dice.__langs__(QUrl)
        return langs.get(key,(os.path.dirname(__file__)+os.sep+'dice-en.qm',QUrl('qrc:/usa.png'))) + getIndexByKey(key, langs)

    @staticmethod
    def languages1(app, engine, QUrl):
        dice.translator = QTranslator(app)
        selection = dice.__langu__(QLocale().language(),QUrl)
        dice.translator.load(selection[0])
        app.installTranslator(dice.translator)
        dice.langNum = selection[2]
        return selection

    @staticmethod
    def languages1b(app, engine, QUrl):
        translator = QTranslator(app)
        app.removeTranslator(dice.translator)
        selection = dice.__langu1__(QLocale().language(),QUrl)
        translator.load(selection[0])
        #translator.load(dice.langu(QLocale().language()))
        app.installTranslator(translator)
        dice.langNum = selection[2]
        langimg = engine.rootObjects()[0].findChild(QObject, "langimg")
        langimg.setProperty("source",selection[1])
        return selection

    @staticmethod
    def languages2(strlist):
        dice.strlist = strlist
        dice.randfkt2 = { 1 : strlist[0],
            2 : strlist[1],
            3 : strlist[2],
            4 : strlist[3],
            5 : strlist[4],
            6 : strlist[5],
            7 : strlist[6],
            8 : strlist[7],
            9 : strlist[8]}

        dice.randfkt3 = { 1 : strlist[10],
            2 : strlist[9],
            3 : strlist[1],
            4 : strlist[2]}
        dice.str_augen = strlist[12]
        dice.str_wurf =  strlist[11]
