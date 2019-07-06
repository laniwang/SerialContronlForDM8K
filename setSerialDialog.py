import tkinter as tk
from tkinter import ttk
# 弹窗
class setSerialDialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('串口信息配置')
        self.setup_UI()
    def setup_UI(self):
        self.com=tk.StringVar(self, 'COM4')
        self.baudrate=tk.StringVar(self,'38400')
        self.databit=tk.StringVar(self,'1')
        
        tk.Label(self, text='串口端口号：').grid()
        tk.Entry(self,textvariable=self.com).grid()
        
        tk.Label(self, text='波特率：').grid()
        ttk.Combobox(self,textvariable=self.baudrate, values=['4800','9600','11520','38400']).grid()
        
        tk.Label(self, text='数据位').grid()
        ttk.Combobox(self, textvariable=self.databit, value=['1','2']).grid()
        
        tk.Button(self,text='确定', command=self.ok).grid()
        tk.Button(self,text='取消' , command=self.cancel).grid()
    def ok():
        self.setserialInfor=[self.com.get(), self.baudrate.get(), self.databit.get()]
        self.destory()
    def cancel():
        self.setserialInfor = None # 空！
        self.destroy()
if __name__=='__main__':
    setSerdg=setSerialDialog()


