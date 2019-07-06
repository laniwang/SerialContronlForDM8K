# 默认串口 COM5 , 38400
import tkinter as tk
from allModuleDm8000 import *
from serialHelp import *
from time import *
import threading
import moduleclass

'''
主界面
'''
class serialMain(object):
    testMode=1
    def __init__(self,master):
        self.root=master
        self.msgstring='Start print command message.'
        self.isStoped=False
        self.mainUI()
    def mainUI(self):
        self.mdlInstance=moduleclass.module(moduletype='DM_Input_10_Channel',
                                            attribute='Input_Gain',
                                            InstanceTag='Input1')  #模块对象初始化
        
        self.moduleVar=tk.StringVar()
        self.attributeVar=tk.StringVar()
        self.attributevalueVar=tk.IntVar()
        self.channelVar=tk.IntVar()
        self.attributevalueVar.set(66)
        self.channelVar.set(1)

        self.moduleVar.set("Input1")
        self.attributeVar.set("Input_Gain")

        #第1行 
        tk.Label(self.root,text='请选择模块，InstanTag：').grid(row=1)
        self.moduleE=tk.Entry(self.root, textvariable=self.moduleVar).grid(row=1,column=1)
        tk.Label(self.root,text='请选择需要测试属性：').grid(row=1, column=2)
        self.attributeE=tk.Entry(self.root, textvariable=self.attributeVar).grid(row=1,column=3)
        tk.Label(self.root,text='通道ID：').grid(row=1, column=4)
        self.attributeE=tk.Entry(self.root, textvariable=self.channelVar).grid(row=1,column=5)
        tk.Label(self.root,text='数值：').grid(row=1, column=6)
        self.attributeE=tk.Entry(self.root, textvariable=self.attributevalueVar).grid(row=1,column=7)
        #第2行S
        '''
        模块列表
        '''
        self.modulelbx=tk.Listbox(self.root, height=10)
        #填充模块列表
        for mditem in allmodule.keys():
            self.modulelbx.insert(tk.END, mditem)
        self.modulelbx.select_set(0,0)
        # self.moduleVar.set(self.modulelbx.get(0)) #默认第一个模块显示在文本
        self.modulelbx.grid(row=2,column=0,sticky=tk.N+tk.S+tk.W)
##        self.mdlScrollbar.grid(row=2,column=1,sticky=tk.N+tk.S+tk.W)  #滚动条
##        self.mdlScrollbar.config(command=self.moduleLb.yview)
        self.modulelbx.bind('<Double-Button-1>',self.printAttributelist)  #挷定模块列表双击事件
        '''
        命令列表
        '''
        self.cmdlbx=tk.Listbox(self.root, height=10)
        self.cmdlbx.grid(row=2,column=2)
        '''
        属性列表
        '''
        self.attributelbx=tk.Listbox(self.root,height=10)
        for att in allmodule['DM_Input_10_Channel'].keys():  #填充第一个模块的属性到 属性列表
            self.attributelbx.insert(tk.END,att)
        # self.attributeVar.set(self.attributelbx.get(0)) #默认第一个模块的第一个属性
        self.attributelbx.grid(row=2,column=1)
        
        self.attributelbx.bind('<ButtonRelease-1>', self.click_attlistbox) #绑定属性列表单击事件
        self.getbtn=tk.Button(self.root,text='get参数值',command=self.getValue)
        self.getbtn.grid(row=2,column=4)
        self.getbtn=tk.Button(self.root,text='set参数值',command=self.setValue)
        self.getbtn.grid(row=2,column=3)
        
        self.lbfrm=tk.LabelFrame(self.root, text='循环Channel范围',width=120,heigh=100)
        self.lbfrm.grid(row=2, column=5)
        self.minChannelVar=tk.IntVar() #最小值
        self.maxChannelVar=tk.IntVar()
        self.minChannelVar.set(1)
        self.maxChannelVar.set(10)
        self.minChannelE=tk.Entry(self.lbfrm, textvariable=self.minChannelVar)
        self.maxChannelE =tk.Entry(self.lbfrm, textvariable=self.maxChannelVar)
        self.minChannelE.place(x=0 ,y=0)
        tk.Label(self.lbfrm,text=' To ').place(x=0,y=25)
        self.maxChannelE.place(x=0,y=50)
        '''
        循环多个参数值，
        多个通道数
        '''
        self.valueframe=tk.LabelFrame(self.root,text=' Value range', width=120, height=100)
        self.valueframe.grid(row=2,column=6)
        self.minValueVar=tk.IntVar() #最小值
        self.maxValueVar=tk.IntVar()
        self.minValueVar.set(-100)
        self.maxValueVar.set(12)
        self.minValueE=tk.Entry(self.valueframe, textvariable=self.minValueVar)
        self.maxValueE=tk.Entry(self.valueframe, textvariable=self.maxValueVar)
        self.minValueE.place(x=0,y=0)
        tk.Label(self.valueframe,text=' To ').place(x=0,y=25)
        self.maxValueE.place(x=0,y=50)
        '''
        循环步值设置
        '''
        self.stepValueframe=tk.LabelFrame(self.root, text='Step Value', width=120, height=100)
        self.stepValueframe.grid(row=2, column=7)
        self.stepValue=tk.IntVar()
        self.stepValue.set(0.5)
        self.stepValueE=tk.Entry(self.stepValueframe,textvariable=self.stepValue)
        self.stepValueE.place(x=0, y=25)
        
        # 第3行
        '''
        串口信息容器
        '''
        self.msgtext=tk.Text(self.root,width=40, height=30)
        self.msgtext.tag_configure('big',foreground='#476042', font=('Arial',14,'bold'))
        self.msgtext.grid(row=3,column=0,columnspan=2, sticky=tk.N+tk.S+tk.W)
        self.comframe=tk.LabelFrame(self.root,width=120, height=150,text='1.启动串口')
        self.comframe.grid(row=3,column=2)
        self.comidVar=tk.StringVar()
        self.combaudrateVar=tk.IntVar()
        self.comidVar.set('COM5')
        self.combaudrateVar.set(38400)
        self.comid=tk.Entry(self.comframe,textvariable=self.comidVar)
        self.comid.place(x=0,y=0)
        self.combaudrate=tk.Entry(self.comframe,textvariable=self.combaudrateVar)
        self.combaudrate.place(x=0,y=25)
        self.startcombtn=tk.Button(self.comframe, text='启动串口/3rd', command=self.startCom)
        self.startcombtn.place(x=0,y=50)
        '''
        停止打印信息
        '''
        self.serverframe=tk.LabelFrame(self.root, width=120, height=150,text='2.信息服务')
        self.serverframe.grid(row=3,column=3)
        self.startbtn=tk.Button(self.serverframe, text='启动打印信息', command=self.startPrint)
        self.startbtn.place(x=0,y=0)
        self.stopbtn=tk.Button(self.serverframe, text='停止打印信息', command=self.stopPrint)
        self.stopbtn.place(x=0,y=50)
        self.mlpvalueSet=tk.Button(self.root, text='循环所有数值(set)', command=self.setAllValue)
        self.mlpvalueSet.grid(row=3, column=4)
        self.mlpvalueSet=tk.Button(self.root, text='循环所有数值(get)', command=self.getAllValue)
        self.mlpvalueSet.grid(row=3, column=5)

##        #第5行
        '''
        定制命令发送行
        '''
        self.scmVar=tk.StringVar()
        self.scmVar.set('3rdStart;')
        self.singlecmdE=tk.Entry(self.root,width=40, textvariable=self.scmVar)
        self.singlecmdE.grid(row=5, column=0, columnspan=2)
        self.sendSingleBt=tk.Button(self.root, text='Send', width=10)
        self.sendSingleBt.grid(row=5, column=2)
        self.sendSingleBt.configure(command=self.sendCmd)
        tk.Label
                    
    #  模块列表双击事件： 属性列表填充...
    def printAttributelist(self, event):
        self.mdlInstance.moduleType=self.modulelbx.get(self.modulelbx.curselection())
        self.moduleVar.set('')
        self.cmdlbx.delete(0,tk.END) #清除上一个模块的命令集
        self.attributelbx.delete(0,tk.END) #清除上一个模块的属性
        self.attributeVar.set('')
        for att in allmodule[self.mdlInstance.moduleType].keys():
            self.attributelbx.insert(tk.END,att)

    #点击模块列表事件
    def click_modulelbx(self, event):
        self.moduleVar.set(self.modulelbx.get(self.modulelbx.curselection()))

    #点击对应属性列表
    def click_attlistbox(self, event):
        self.attributeVar.set(self.attributelbx.get(self.attributelbx.curselection()))

        #填充命令集列表
        if self.cmdlbx.size()>0:
            self.cmdlbx.delete(0,tk.END)
        for cl in allmodule[self.mdlInstance.get_moduletype()][self.attributeVar.get()].items():
            self.cmdlbx.insert(tk.END,str(cl))
    #发送定制命令    
    def sendCmd(self):
        if self.scmVar:
            self.ser.write( self.scmVar.get().encode())

    #创建串口连接
    def startCom(self):
        #先建立串口连接对象，再启动3rd
        try:

            self.serInstance=SerialClass(self.comidVar.get(),self.combaudrateVar.get()) #连接DM8000 serial串口
            self.ser= self.serInstance.ser
            cmdMsg= self.serInstance.start3rd()
            self.msgtext.insert(tk.END,cmdMsg)
        except Exception as e:
            self.msgtext.insert(tk.END, e)
            self.msgtext.insert(tk.END, '\r\n'+'设备连接故障,检查串口ID')


    '''
    打印线程启动
    '''      
    def startPrint(self):
        if self.testMode: #测试模式
            self.isStoped=False
            printthread=threading.Thread(target=self.serialMsg) #获取串口信息并显示在窗口
            printthread.setDaemon(True)
            printthread.start()
            return
        #启动打印线程
        self.isStoped=False
        printthread=threading.Thread(target=self.serialMsg) #获取串口信息并显示在窗口
        printthread.setDaemon(True)
        printthread.start()

    def stopPrint(self):
        if self.testMode==1:
            self.isStoped=True
            return
        try:
            if self.serInstance:
                self.serInstance.exit3rd()
                self.isStoped=True
            else:
                print('Pls start 3rd first. ')
                return
        except Exception as e:
            print(e)
            self.msgtext.insert(tk.END,e, 'big')

    def serialMsg(self):
        self.msgtext.insert(1.0,'>>START PRINT MESSAGE.','big')
        if self.testMode:  #测试模式
            n=1
            while True:
                if self.isStoped:
                    break
                data='test mode' + str(n)
                n+=1
                self.msgtext.insert(tk.END, data+'\r\n')
                self.msgtext.see(tk.END)            
                sleep(0.9)
        '''
        循环打印线程主体
        '''
        try:          
            while True:
                if self.isStoped==1:
                    if self.ser.isOpen==True:
                        self.ser.close()
                        self.serInstance.ser.close()
                    break
                data=''
                data=data.encode('utf-8')
                m = self.ser.inWaiting()
                data=data+self.ser.read(m)
                if data:
                    print(data)
                    self.msgtext.insert(tk.END, data.decode())
                    self.msgtext.see(tk.END)            
                    sleep(0.2)
                else:continue
        except Exception as e:
            print(e)
            

    #添加信息到打印信息窗口     
    def printMsg(self, msgInfor):
        self.msgtext.insert(END,msgInfor)
        self.msgtext.insert(END,'\n')

    #获取当前参数值
    def getValue(self):
        print('get the value')

        #self.mdlInstance.InstanceTag='Input1'   #self.moduleVar.get()
        self.mdlInstance.atrribute=self.attributeVar.get()
        self.mdlInstance.minChannel=self.channelVar.get()
        
        self.cmdString=self.mdlInstance.getCommand()
        print(self.cmdString)
        try:
            self.ser.write(self.cmdString.encode('utf-8'))
        except Exception as e:
            print(e)
        print('Get value over.')
        
    def setValue(self):
        self.mdlInstance.atrribute=self.attributeVar.get()
        self.mdlInstance.minValue= self.attributevalueVar.get()
        self.mdlInstance.minChannel=self.channelVar.get()
        self.cmdString=self.mdlInstance.setCommand()
        print(self.cmdString)    
        #发送set命令。
        self.ser.write(self.cmdString.encode('utf-8'))
        
    #遍历所有的值 set
    def setAllValue(self):
        self.mdlInstance.set_atrribute(self.attributeVar.get())
        self.mdlInstance.set_InstanceTag(self.moduleVar.get())
        for chl in range(self.minChannelVar.get(), self.maxChannelVar.get()+1):
            self.mdlInstance.set_minChannel(chl)
            for i in range(self.minValueVar.get(),self.maxValueVar.get()+1):
                self.mdlInstance.set_minValue(i)
                self.msgtext.insert(tk.END, self.mdlInstance.setCommand())
                self.msgtext.insert(tk.END, '\r\n')
        self.msgtext.see(tk.END)
    #遍历所有的值 get
    def getAllValue(self):
        self.mdlInstance.set_atrribute(self.attributeVar.get())
        self.mdlInstance.set_InstanceTag(self.moduleVar.get())
        for chl in range(self.minChannelVar.get(), self.maxChannelVar.get()+1):
            self.mdlInstance.set_minChannel(chl)
            self.msgtext.insert(tk.END, self.mdlInstance.getCommand())
            self.msgtext.insert(tk.END, '\r\n')
        self.msgtext.see(tk.END)
        
    #遍历所有的值
    def setAllChannel(self):
        pass  
            
if __name__=='__main__':
    root=tk.Tk()
    root.title('3rd 命令')
    app=serialMain(root)
    root.mainloop()
