import tkinter as tk
from allModuleDm8000 import *
from mylib import *
from time import *
import threading
from setSerialDialog import setSerialDialog
import moduleclass
global ser

class serialMain(object):
    def __init__(self, master=None):
        #super().__init__()
        self.root=master
        self.msgString=''
        self.mainUI()
    def mainUI(self):
        #第一行 
        self.mdlVar=tk.StringVar()
        self.attVar=tk.StringVar()
        
        self.lb1=tk.Label(self.root,text='已选模块').grid(row=0)
        self.moduleE=tk.Entry(self.root,textvariable=self.mdlVar).grid(row=0,column=1,sticky=tk.W+tk.E)
        tk.Label(self.root,text='已选模块属性').grid(row=0, column=2)        
        self.attributeE=tk.Entry(self.root,textvariable=self.attVar).grid(row=0,column=3,sticky=tk.W+tk.E)
        
        self.getButton=tk.Button(self.root, text='读取参数值', command=self.getAttr).grid(row=0, column=4,sticky=tk.W+tk.E)
        self.setButton=tk.Button(self.root, text='设置值', command=self.setAttr).grid(row=0, column=5,sticky=tk.W+tk.E)
        self.conSerialButton=tk.Button(self.root, text='串口启动', command=self.startSerial).grid(row=1, column=2,sticky=tk.W+tk.E)
        self.start3rdButton=tk.Button(self.root, text='启动3rd', command=self.start3rd).grid(row=1,column=3,sticky=tk.W+tk.E)
        self.exit3rdButton=tk.Button(self.root, text='退出3rd', command=self.exit3rd).grid(row=1, column=4,sticky=tk.W+tk.E)
        self.disconSerialButton=tk.Button(self.root, text='串口停止', command=self.stopSerial).grid(row=1, column=5,sticky=tk.W+tk.E)       
        #第二行 
        tk.Label(self.root,text='请选择模块，模块列表：').grid(row=1)
        tk.Label(self.root,text='    请选择需要测试属性：').grid(row=1,column=1)
        #第三行
        self.mdlScrollbar=tk.Scrollbar(self.root)
        self.moduleLb=tk.Listbox(self.root, height=15,yscrollcommand=self.mdlScrollbar.set)
        for mditem in allmodule.keys():
            self.moduleLb.insert(tk.END, mditem)
        self.moduleLb.grid(row=2,column=0,sticky=tk.N+tk.S+tk.W)
        self.mdlScrollbar.grid(row=2,column=1,sticky=tk.N+tk.S+tk.W)
        self.mdlScrollbar.config(command=self.moduleLb.yview)
        self.moduleLb.bind('<Double-Button-1>',self.printModule)
         #循环信息窗口
        self.msgScrollbar=tk.Scrollbar(self.root)
        self.msgScrollbar.grid(row=2,column=6,sticky=tk.N+tk.S+tk.E)
        self.serialMsgText=tk.Text(self.root,yscrollcommand=self.msgScrollbar.set)
        self.serialMsgText.grid(row=2,column=4,columnspan=2,sticky=tk.N+tk.S+tk.W)
        self.msgScrollbar.config(command=self.serialMsgText.yview)
        self.attributeLb=tk.Listbox(self.root)
        self.attributeLb.grid(row=2,column=2,columnspan=2,sticky=tk.N+tk.S+tk.W+tk.E)
        self.attributeLb.bind('<ButtonRelease-1>', self.click_attlistbox)
        #第4行
        #self.comd_Attr=tk.Listbox(self,)
        
    def setSerial(self):
        inputDialog = setSerialDialog()        

    #模块列表显示
    def printModule(self, event):
        self.moduleType=self.moduleLb.get(self.moduleLb.curselection())
        self.mdlVar.set(self.moduleType)
        self.attributeLb.delete(0,tk.END) #清除上一个模块的属性
        for att in allmodule[self.moduleType].keys():
            self.attributeLb.insert(tk.END,att)
    
    #对应属性列表
    def click_attlistbox(self, event):
        self.attVar.set(self.attributeLb.get(self.attributeLb.curselection()))
   
    #循环打印串口信息
    def serialMsg(self, serInstance):
        while True:
            self.serialMsgText.insert(1.0,serInstance.readline())
            
    def serialMsg2(self):
        while True:
            self.serialMsgText.insert(1.0,self.msgString)

    def  startSerial(self):
        
        #ser,self.msgString=serialConn()
##        self.serialMsgText.insert(tk.START,self.msgString)
##        printThread=threading.Thread(target=self.serialMsg,args=( ser,))
        printThread=threading.Thread(target=self.serialMsg2)
        printThread.setDaemon(True)
        printThread.start()
        
    def start3rd(self):
        ser.write('3rdStart;'.encode('utf-8'))       
    def exit3rd(self):
        ser.write('exit;'.encode('utf-8'))      
    def stopSerial(self):
            ser.close()
    def getAttr(self):
        self.module=self.mdlVar.get()
        self.attribute=self.attVar.get()
##        if self.module=='Dynamic_AGC' and self.attribute!='':
##            self.cmdString='get AGC1 %s ;' % self.attribute
##        ser.write(self.cmdString.encode('utf-8'))
        try:
            moduleInstance=module('',self.module,self.attribute)
            self.msgString=moduleInstance.getCommand()
        except Exception as err:
            self.msgString=str(err)
            
    def setAttr(self):
        module=self.mdlVar.get()
        attribute=self.attVar.get()
        if module=='Dynamic_AGC' and attribute!='':
            cmdString='set AGC1 %s 1;' % attribute
        ser.write(cmdString.encode('utf-8'))

if __name__=='__main__':
    root=tk.Tk()
    root.title('自动化处理命令')
    app=serialMain(root)
